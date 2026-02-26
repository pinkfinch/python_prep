"""
Federal income tax calculator using progressive tax brackets.

This module provides a flexible, extensible tax calculation library that can be
used by multiple firms to calculate federal income tax liabilities.
"""

from typing import Union, List
from dataclasses import dataclass


@dataclass
class TaxBracket:
    """
    Represents a single tax bracket.

    A bracket is defined by an upper threshold (where it ends) and a tax rate.
    The bracket starts where the previous bracket ended.

    Example:
        If we have brackets:
        - TaxBracket(12400, 0.12)  -> 0 to 12,400 taxed at 12%
        - TaxBracket(50400, 0.22)  -> 12,400 to 50,400 taxed at 22%
    """
    threshold: float  # Income level at which this bracket ENDS
    rate: float  # Tax rate for this bracket (0.0 to 1.0)

    def __post_init__(self):
        """Validate bracket data."""
        if self.threshold < 0:
            raise ValueError(f"Threshold must be non-negative, got {self.threshold}")
        if not 0 <= self.rate <= 1:
            raise ValueError(f"Tax rate must be between 0 and 1, got {self.rate}")


class FederalTaxCalculator:
    """
    Calculate federal income tax based on progressive tax brackets.

    This calculator implements the progressive tax system where income is taxed
    at increasing rates as it moves into higher brackets.

    The brackets list should be sorted by threshold (ascending).
    Each bracket's threshold represents the upper limit of that bracket's income range.

    Example:
        >>> brackets = [
        ...     TaxBracket(12400, 0.12),    # 0-12,400 at 12%
        ...     TaxBracket(50400, 0.22),    # 12,400-50,400 at 22%
        ...     TaxBracket(105700, 0.24),   # 50,400-105,700 at 24%
        ... ]
        >>> calc = FederalTaxCalculator(brackets)
        >>> tax = calc.calculate(75000)
    """

    def __init__(self, brackets: List[TaxBracket]):
        """
        Initialize the calculator with tax brackets.

        Args:
            brackets: List of TaxBracket objects representing tax brackets.
                     Must have at least one bracket.

        Raises:
            ValueError: If brackets are invalid or not properly sorted.
        """
        if not brackets:
            raise ValueError("At least one tax bracket must be provided")

        self._validate_brackets(brackets)
        # Sort by threshold to ensure correct order
        self.brackets = sorted(brackets, key=lambda b: b.threshold)

    @staticmethod
    def _validate_brackets(brackets: List[TaxBracket]) -> None:
        """Validate bracket structure and ordering."""
        if not brackets:
            raise ValueError("At least one tax bracket must be provided")

        # Check that brackets are in ascending order
        for i in range(len(brackets) - 1):
            if brackets[i].threshold >= brackets[i + 1].threshold:
                raise ValueError(
                    f"Brackets must be in ascending order by threshold. "
                    f"Got {brackets[i].threshold} followed by {brackets[i + 1].threshold}"
                )

    def calculate(self, taxable_income: Union[int, float]) -> float:
        """
        Calculate federal income tax on taxable income.

        Uses progressive taxation: income is taxed at increasing rates as it
        moves into higher brackets.

        Args:
            taxable_income: Total taxable income for the year.

        Returns:
            Total federal income tax owed (rounded to nearest cent).

        Raises:
            ValueError: If income is negative.
            TypeError: If income is not numeric.

        Example:
            >>> calc.calculate(75000)
            8688.0
        """
        if not isinstance(taxable_income, (int, float)):
            raise TypeError(f"Income must be numeric, got {type(taxable_income)}")

        if taxable_income < 0:
            raise ValueError(f"Taxable income cannot be negative, got {taxable_income}")

        if taxable_income == 0:
            return 0.0

        tax = 0.0
        previous_threshold = 0.0

        for bracket in self.brackets:
            # Stop if we've already taxed all income
            if taxable_income <= previous_threshold:
                break

            # Calculate how much income is in this bracket
            income_in_bracket = min(taxable_income, bracket.threshold) - previous_threshold

            # Add tax for this bracket
            tax += income_in_bracket * bracket.rate

            # Move to next bracket
            previous_threshold = bracket.threshold

        return round(tax, 2)  # Round to nearest cent



# 2026 Tax brackets for reference (from IRS)
# https://www.irs.gov/newsroom/irs-releases-tax-inflation-adjustments-for-tax-year-2026-including-amendments-from-the-one-big-beautiful-bill
BRACKETS_2026_SINGLE = [
    TaxBracket(12400, 0.12),
    TaxBracket(50400, 0.22),
    TaxBracket(105700, 0.24),
    TaxBracket(201775, 0.32),
    TaxBracket(256225, 0.35),
    TaxBracket(640600, 0.37),
]

BRACKETS_2026_MARRIED_FILING_JOINTLY = [
    TaxBracket(24800, 0.12),
    TaxBracket(100800, 0.22),
    TaxBracket(211400, 0.24),
    TaxBracket(403550, 0.32),
    TaxBracket(512450, 0.35),
    TaxBracket(768700, 0.37),
]