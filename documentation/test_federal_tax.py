import pytest
from typing import List


class TaxBracket:
    """
    Defines the tax brackets based on the current income tax rates
    """

    def __init__(self, min_income: float, tax_percentage: float):
        """
        Args
            min_income: the minimum income for which this bracket is activated
            tax_percentage: the percentage of tax to apply for this bracket, as a decimal - so 12% is .12
        Returns
            An object with the above values initialized
        Raises
            ValueError if the type of fields do not match expected values
        """
        if min_income is None or tax_percentage is None:
            raise ValueError(f"Invalid inputs: min_income passed is {min_income} and tax is {tax_percentage}")
        
        if not isinstance(min_income, (int, float)):
            raise TypeError("min_income needs to be an int or float")
        
        if not isinstance(tax_percentage, float):
            raise TypeError(f"tax_percentage must be a float (decimal), got {type(tax_percentage).__name__}")
        
        if not (0 <= tax_percentage <= 1):
            raise ValueError(
                f"tax_percentage: rate must be between 0 and 1 (as decimal). "
                f"Received: {tax_percentage}. Did you mean {tax_percentage / 100}?"
            )
        
        self.min_income = min_income
        self.tax_percentage = tax_percentage


class FederalTax:
    """
    Returns the total tax based on the taxable income and the tax brackets passed in
    """

    def __init__(self, tax_brackets: List[TaxBracket]):
        """
        Args
            tax_brackets: the tax brackets to calculate the taxes from.
            Must be a list of TaxBrackets

        Returns
            a FederalTax object to be used to calculate the federal tax for an income

        Raises
            TypeError, ValueError from TaxBrackets
        """
        if not tax_brackets:
            raise ValueError("Tax brackets cannot be null or empty")

        for obj in tax_brackets:
            if not isinstance(obj, TaxBracket):
                raise TypeError(f"Objects in tax_brackets must be of Type TaxBracket")
        
        # Sort by min_income
        tax_brackets.sort(key=lambda x: x.min_income)
        
        # Validate brackets are in ascending order
        for index, obj in enumerate(tax_brackets):
            if index > 0:
                if tax_brackets[index].min_income <= tax_brackets[index-1].min_income:
                    raise ValueError(
                        f"The minimum income at index {index} ({tax_brackets[index].min_income}) "
                        f"is less than or equal to the minimum income at index {index-1} "
                        f"({tax_brackets[index-1].min_income})"
                    )

        self.tax_brackets = tax_brackets

    def calculate_tax_on_income(self, taxable_income):
        """
        args
            taxable_income - the taxable income for which we are trying to calculate the federal marginal taxes
        return
            the amount of federal tax to be paid
        raise
            ValueError - the data is < 0
            TypeError - the data is not numeric
        example
            if the taxable_income is 12,400 the tax would be - 1488
        """
        if not isinstance(taxable_income, (int, float)):
            raise TypeError(f"Income must be numeric, got {type(taxable_income)}")

        if taxable_income < 0:
            raise ValueError(f"Taxable income cannot be negative, got {taxable_income}")

        if taxable_income == 0:
            return 0.0

        tax_amt = taxable_income
        prev_bracket = 0
        tax = 0
        
        for bracket in self.tax_brackets:
            current_bracket = bracket.min_income - prev_bracket
            tax += min(current_bracket, tax_amt) * bracket.tax_percentage
            
            if tax_amt > current_bracket:
                tax_amt = tax_amt - current_bracket
                prev_bracket = bracket.min_income
            else:
                break
        
        return tax


# ==================== TAXBRACKET TESTS ====================

class TestTaxBracketInit:
    """Test TaxBracket initialization and validation"""

    def test_valid_bracket_creation(self):
        """Test creating a valid TaxBracket"""
        bracket = TaxBracket(12400, 0.12)
        assert bracket.min_income == 12400
        assert bracket.tax_percentage == 0.12

    def test_valid_bracket_with_int_income(self):
        """Test creating bracket with integer income"""
        bracket = TaxBracket(50000, 0.22)
        assert bracket.min_income == 50000
        assert isinstance(bracket.min_income, int)

    def test_valid_bracket_with_float_income(self):
        """Test creating bracket with float income"""
        bracket = TaxBracket(12400.50, 0.12)
        assert bracket.min_income == 12400.50
        assert isinstance(bracket.min_income, float)

    def test_zero_income_valid(self):
        """Test that zero income is valid"""
        bracket = TaxBracket(0, 0.0)
        assert bracket.min_income == 0
        assert bracket.tax_percentage == 0.0

    def test_max_rate(self):
        """Test maximum valid tax rate (1.0 = 100%)"""
        bracket = TaxBracket(100000, 1.0)
        assert bracket.tax_percentage == 1.0

    def test_none_min_income_raises_error(self):
        """Test that None min_income raises ValueError"""
        with pytest.raises(ValueError):
            TaxBracket(None, 0.12)

    def test_none_tax_percentage_raises_error(self):
        """Test that None tax_percentage raises ValueError"""
        with pytest.raises(ValueError):
            TaxBracket(12400, None)

    def test_min_income_not_numeric_raises_error(self):
        """Test that non-numeric min_income raises TypeError"""
        with pytest.raises(TypeError):
            TaxBracket("12400", 0.12)

    def test_min_income_list_raises_error(self):
        """Test that list as min_income raises TypeError"""
        with pytest.raises(TypeError):
            TaxBracket([12400], 0.12)

    def test_tax_percentage_not_float_raises_error(self):
        """Test that non-float tax_percentage raises TypeError"""
        with pytest.raises(TypeError):
            TaxBracket(12400, 12)  # Integer instead of 0.12

    def test_tax_percentage_as_integer_raises_error(self):
        """Test that integer tax percentage raises TypeError"""
        with pytest.raises(TypeError):
            TaxBracket(50000, 22)

    def test_tax_percentage_as_string_raises_error(self):
        """Test that string tax percentage raises TypeError"""
        with pytest.raises(TypeError):
            TaxBracket(12400, "0.12")

    def test_tax_percentage_negative_raises_error(self):
        """Test that negative tax percentage raises ValueError"""
        with pytest.raises(ValueError):
            TaxBracket(12400, -0.12)

    def test_tax_percentage_greater_than_one_raises_error(self):
        """Test that tax percentage > 1 raises ValueError"""
        with pytest.raises(ValueError):
            TaxBracket(12400, 1.5)

    def test_tax_percentage_percentage_format_error_message(self):
        """Test helpful error message for percentage format"""
        with pytest.raises(ValueError) as exc_info:
            TaxBracket(12400, 22)
        assert "Did you mean" in str(exc_info.value)

    def test_negative_income_valid(self):
        """Test that negative income is technically allowed (though unusual)"""
        # The class doesn't explicitly forbid negative income
        bracket = TaxBracket(-1000, 0.12)
        assert bracket.min_income == -1000


# ==================== FEDERALTAX TESTS ====================

class TestFederalTaxInit:
    """Test FederalTax initialization and bracket validation"""

    def test_valid_brackets_creation(self):
        """Test creating FederalTax with valid brackets"""
        brackets = [
            TaxBracket(12400, 0.12),
            TaxBracket(50400, 0.22),
            TaxBracket(105700, 0.24),
        ]
        fed_tax = FederalTax(brackets)
        assert len(fed_tax.tax_brackets) == 3

    def test_2026_tax_brackets(self):
        """Test with actual 2026 tax brackets for single filers"""
        brackets = [
            TaxBracket(12400, 0.12),
            TaxBracket(50400, 0.22),
            TaxBracket(105700, 0.24),
            TaxBracket(201775, 0.32),
            TaxBracket(256225, 0.35),
            TaxBracket(640600, 0.37),
        ]
        fed_tax = FederalTax(brackets)
        assert len(fed_tax.tax_brackets) == 6

    def test_brackets_auto_sorted(self):
        """Test that brackets are automatically sorted by min_income"""
        brackets = [
            TaxBracket(105700, 0.24),
            TaxBracket(12400, 0.12),
            TaxBracket(50400, 0.22),
        ]
        fed_tax = FederalTax(brackets)
        # Should be sorted in ascending order
        assert fed_tax.tax_brackets[0].min_income == 12400
        assert fed_tax.tax_brackets[1].min_income == 50400
        assert fed_tax.tax_brackets[2].min_income == 105700

    def test_empty_brackets_raises_error(self):
        """Test that empty bracket list raises ValueError"""
        with pytest.raises(ValueError):
            FederalTax([])

    def test_none_brackets_raises_error(self):
        """Test that None brackets raises ValueError"""
        with pytest.raises(ValueError):
            FederalTax(None)

    def test_non_taxbracket_object_raises_error(self):
        """Test that non-TaxBracket object in list raises TypeError"""
        brackets = [
            TaxBracket(12400, 0.12),
            (50400, 0.22),  # Tuple instead of TaxBracket
        ]
        with pytest.raises(TypeError):
            FederalTax(brackets)

    def test_duplicate_min_income_raises_error(self):
        """Test that duplicate min_income values raise ValueError"""
        brackets = [
            TaxBracket(12400, 0.12),
            TaxBracket(12400, 0.22),  # Same min_income
        ]
        with pytest.raises(ValueError):
            FederalTax(brackets)

    def test_non_ascending_brackets_raises_error(self):
        """Test that non-ascending bracket thresholds raise ValueError"""
        brackets = [
            TaxBracket(12400, 0.12),
            TaxBracket(125000, 0.24),
            TaxBracket(70000, 0.32),  # Out of order
        ]
        with pytest.raises(ValueError):
            FederalTax(brackets)

    def test_single_bracket(self):
        """Test that a single bracket is valid"""
        brackets = [TaxBracket(0, 0.20)]
        fed_tax = FederalTax(brackets)
        assert len(fed_tax.tax_brackets) == 1


# ==================== TAX CALCULATION TESTS ====================

class TestCalculateTaxOnIncome:
    """Test tax calculation with various income levels"""

    @pytest.fixture
    def standard_brackets(self):
        """Standard 2026 tax brackets for testing"""
        return FederalTax([
            TaxBracket(12400, 0.12),
            TaxBracket(50400, 0.22),
            TaxBracket(105700, 0.24),
            TaxBracket(201775, 0.32),
            TaxBracket(256225, 0.35),
            TaxBracket(640600, 0.37),
        ])

    def test_zero_income(self, standard_brackets):
        """Test that zero income results in zero tax"""
        assert standard_brackets.calculate_tax_on_income(0) == 0.0

    def test_income_in_first_bracket(self, standard_brackets):
        """Test income that falls entirely in the first bracket"""
        # $10,000 at 12% = $1,200
        result = standard_brackets.calculate_tax_on_income(10000)
        assert result == 10000 * 0.12

    def test_income_at_bracket_threshold(self, standard_brackets):
        """Test income exactly at a bracket threshold"""
        # $12,400 at 12% = $1,488
        result = standard_brackets.calculate_tax_on_income(12400)
        expected = 12400 * 0.12
        assert result == expected

    def test_income_spanning_two_brackets(self, standard_brackets):
        """Test income that spans two brackets"""
        # Income: $60,000
        # First bracket: $12,400 at 12% = $1,488
        # Second bracket: $60,000 - $12,400 = $47,600 at 22% = $10,472
        # Total: $11,960
        result = standard_brackets.calculate_tax_on_income(60000)
        expected = (12400 * 0.12) + (47600 * 0.22)
        assert result == expected

    def test_income_spanning_multiple_brackets(self, standard_brackets):
        """Test income that spans multiple brackets"""
        # Income: $200,000
        income = 200000
        expected = (
            (50400 - 12400) * 0.22 +    # $38,000 at 22%
            (105700 - 50400) * 0.24 +   # $55,300 at 24%
            (200000 - 105700) * 0.32    # $94,300 at 32%
        )
        expected += 12400 * 0.12  # First bracket
        
        result = standard_brackets.calculate_tax_on_income(income)
        assert result == expected

    def test_high_income_all_brackets(self, standard_brackets):
        """Test very high income using all brackets"""
        result = standard_brackets.calculate_tax_on_income(700000)
        # Should apply all 6 brackets
        assert result > 0

    def test_income_at_top_bracket_threshold(self, standard_brackets):
        """Test income at the top bracket threshold"""
        result = standard_brackets.calculate_tax_on_income(640600)
        assert result > 0

    def test_income_above_top_bracket(self, standard_brackets):
        """Test income well above the top bracket"""
        result1 = standard_brackets.calculate_tax_on_income(640600)
        result2 = standard_brackets.calculate_tax_on_income(640601)
        # Adding $1 should add $0.37 in taxes (37% rate)
        assert abs((result2 - result1) - 0.37) < 0.01

    def test_negative_income_raises_error(self, standard_brackets):
        """Test that negative income raises ValueError"""
        with pytest.raises(ValueError):
            standard_brackets.calculate_tax_on_income(-1000)

    def test_non_numeric_income_raises_error(self, standard_brackets):
        """Test that non-numeric income raises TypeError"""
        with pytest.raises(TypeError):
            standard_brackets.calculate_tax_on_income("50000")

    def test_none_income_raises_error(self, standard_brackets):
        """Test that None income raises TypeError"""
        with pytest.raises(TypeError):
            standard_brackets.calculate_tax_on_income(None)

    def test_float_income(self, standard_brackets):
        """Test with float income"""
        result = standard_brackets.calculate_tax_on_income(50000.50)
        assert result > 0

    def test_income_with_cents(self, standard_brackets):
        """Test income with cents precision"""
        income = 75000.99
        result = standard_brackets.calculate_tax_on_income(income)
        assert result > 0

    def test_single_bracket_calculator(self):
        """Test tax calculation with single bracket"""
        brackets = FederalTax([TaxBracket(0, 0.25)])
        result = brackets.calculate_tax_on_income(10000)
        assert result == 2500.0  # $10,000 * 0.25

    def test_flat_tax_multiple_brackets(self):
        """Test with multiple brackets but same rate (edge case)"""
        brackets = FederalTax([
            TaxBracket(0, 0.20),
            TaxBracket(50000, 0.20),
            TaxBracket(100000, 0.20),
        ])
        result = brackets.calculate_tax_on_income(150000)
        expected = 150000 * 0.20
        assert result == expected

    def test_very_small_income(self, standard_brackets):
        """Test with very small income amounts"""
        result = standard_brackets.calculate_tax_on_income(0.01)
        expected = 0.01 * 0.12
        assert abs(result - expected) < 0.0001


# ==================== INTEGRATION TESTS ====================

class TestIntegration:
    """Integration tests combining multiple components"""

    def test_example_from_docstring(self):
        """Test the example from the docstring"""
        brackets = FederalTax([
            TaxBracket(12400, 0.12),
            TaxBracket(50400, 0.22),
            TaxBracket(105700, 0.24),
            TaxBracket(201775, 0.32),
            TaxBracket(256225, 0.35),
            TaxBracket(640600, 0.37),
        ])
        
        result = brackets.calculate_tax_on_income(12400)
        expected = 12400 * 0.12
        assert result == expected

    def test_multiple_calculations_same_calculator(self):
        """Test that calculator can be reused for multiple calculations"""
        brackets = FederalTax([
            TaxBracket(12400, 0.12),
            TaxBracket(50400, 0.22),
            TaxBracket(105700, 0.24),
        ])
        
        result1 = brackets.calculate_tax_on_income(30000)
        result2 = brackets.calculate_tax_on_income(100000)
        
        assert result1 < result2

    def test_progressive_taxation_increases(self):
        """Test that tax increases progressively with income"""
        brackets = FederalTax([
            TaxBracket(12400, 0.12),
            TaxBracket(50400, 0.22),
            TaxBracket(105700, 0.24),
        ])
        
        tax_10k = brackets.calculate_tax_on_income(10000)
        tax_30k = brackets.calculate_tax_on_income(30000)
        tax_100k = brackets.calculate_tax_on_income(100000)
        
        assert tax_10k < tax_30k < tax_100k

    def test_effective_tax_rate_increases_with_income(self):
        """Test that effective tax rate increases with income (progressive)"""
        brackets = FederalTax([
            TaxBracket(12400, 0.12),
            TaxBracket(50400, 0.22),
            TaxBracket(105700, 0.24),
        ])
        
        tax_30k = brackets.calculate_tax_on_income(30000)
        rate_30k = tax_30k / 30000
        
        tax_100k = brackets.calculate_tax_on_income(100000)
        rate_100k = tax_100k / 100000
        
        assert rate_30k < rate_100k


# ==================== EDGE CASES ====================

class TestEdgeCases:
    """Test edge cases and boundary conditions"""

    def test_zero_tax_rate(self):
        """Test bracket with 0% tax rate"""
        brackets = FederalTax([
            TaxBracket(0, 0.0),
            TaxBracket(50000, 0.10),
        ])
        # First $50k at 0%, then rest at 10%
        result = brackets.calculate_tax_on_income(100000)
        expected = 50000 * 0.10  # Only income above $50k is taxed
        assert result == expected

    def test_very_large_income(self):
        """Test with very large income"""
        brackets = FederalTax([
            TaxBracket(0, 0.10),
            TaxBracket(1000000, 0.37),
        ])
        result = brackets.calculate_tax_on_income(1000000000)
        assert result > 0

    def test_income_just_above_bracket_threshold(self):
        """Test income just barely above a bracket threshold"""
        brackets = FederalTax([
            TaxBracket(50000, 0.10),
            TaxBracket(50000.01, 0.20),
        ])
        # Just crossing the threshold
        result = brackets.calculate_tax_on_income(50000.01)
        assert result > 0

    def test_fractional_cents(self):
        """Test with very precise decimal values"""
        brackets = FederalTax([
            TaxBracket(0, 0.123456),
        ])
        income = 1000000.999999
        result = brackets.calculate_tax_on_income(income)
        expected = income * 0.123456
        assert abs(result - expected) < 0.01


if __name__ == "__main__":
    # Run tests with: pytest test_federal_tax.py -v
    pytest.main([__file__, "-v"])
