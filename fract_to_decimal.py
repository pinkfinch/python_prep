'''
Fraction to Recurring Decimal

Given two integers representing the numerator and denominator of a fraction, return the fraction in string format.
If the fractional part is repeating, enclose the repeating part in parentheses.
If multiple answers are possible, return any of them.
It is guaranteed that the length of the answer string is less than 104 for all the given inputs.
Note that if the fraction can be represented as a finite length string, you must return it.

Example 1:
Input: numerator = 1, denominator = 2
Output: "0.5"

Example 2:
Input: numerator = 2, denominator = 1
Output: "2"

Example 3:
Input: numerator = 4, denominator = 333
Output: "0.(012)"

Constraints:
-2^31 <= numerator, denominator <= 2^31 - 1
denominator != 0

Divide: Divide the first part of the dividend by the divisor and write the answer (quotient) on top.
If the first digit is too small, use the first two digits.
Multiply: Multiply the quotient you just wrote by the divisor.
Subtract: Subtract the result from the dividend or the partial dividend you were working with.
Bring down: Bring down the next digit from the dividend to the right of the subtraction result.
Repeat: Repeat the process with the new number formed until there are no more digits to bring down.

if negative - append "-" to string

dividend = numerator

quotient = dividend//denomiator
remainder = %

append(quotient)
next_dividend = dividend - (quotient*denominator)


'''
import re
from typing import Union, Any


def fractionToDecimalOrig(numerator: int, denominator: int) -> str:
    if numerator == 0:
        return "0"
    res = ""
    dict = {}
    # Determine the sign
    if numerator < 0 or denominator < 0:
        if not (numerator < 0 and denominator < 0):
            res += "-"
    dividend = numerator
    while dividend != 0 and denominator != 0:
        quotient = dividend // denominator
        remainder = abs(dividend % denominator)
        res += str(abs(quotient))
        if remainder == 0:
            return "".join(res)

        dividend = remainder
        if dividend < denominator:
            if res.find(".") == -1:
                res += "."
            dividend = dividend * 10

        if res.find(".") != -1:
            decimal_idx = res.find('.')
            match = re.search(r"(.+)\1{2,}", res[decimal_idx+1:])
            if match:
                repeating = match.group(1)
                repeating_idx = res.find(repeating, decimal_idx + 1)
                res = res[:repeating_idx] +  "(" + repeating + ")"
                print(res)
                return res

def fractionToDecimal(numerator: int, denominator: int) -> str:
    if numerator == 0:
        return "0"
    res = ""
    map = {}
    # Determine the sign
    if numerator < 0 or denominator < 0:
        if not (numerator < 0 and denominator < 0):
            res += "-"
    numerator = abs(numerator)
    denominator = abs(denominator)
    remainder = numerator % denominator
    res += str(numerator // denominator)
    if remainder == 0: return res
    res += "."

    while remainder != 0 and remainder not in map:
        map[remainder] = len(res)
        remainder *= 10
        res += str(remainder//denominator)
        remainder %= denominator
    if remainder in map:
        res = res[:map[remainder]] + "(" + res[map[remainder]:] + ")"
    if res.startswith(".") or res.startswith("-."):
        res = "0" + res
    return res




print(fractionToDecimal(23,6))
print(fractionToDecimal(4,333))
print(fractionToDecimal(1, 333))
print(fractionToDecimal(233, 6))
print(fractionToDecimal(1, 17))
print(fractionToDecimal(-50, 8))