import re

pattern = r"(.+)\1+"
string = "833"

# Using re.search to find any match within the string
match = re.search(pattern, string)

if match:
    print(f"Match found! The matched substring is: {match.group(0)}")
    print(f"The captured group (\\1) is: {match.group(1)}")
else:
    print("No match found.")
res = "3.8333"
decimal_idx = res.find('.')
print(decimal_idx)
match = re.search(r"(.+)\1+", res[decimal_idx + 1:])
if match:
    repeating = match.group(1)
    repeating_idx = res.find(repeating, decimal_idx + 1)
    res = res[:repeating_idx] + "(" + repeating + ")"
    print(res)

dividend = 50
denominator = 8
quotient = dividend // denominator
print(quotient)