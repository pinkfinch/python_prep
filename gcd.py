# Given 2 numbers, find their GCD.
# Euclid's algorithm:
# 1. Save B as a temp variable.
# 2. Set B equal to A % B.
# 3. Set A equal to the temp.
# 4. Repeat steps 1-3 until B equals 0.
# 5. Return A.

def gcd(a,b):
    if b>a:
        a,b = b,a
    while(b != 0):
        tmp = b
        b = a%b
        a = tmp
    return a


print( gcd(78,52))
print( gcd(12, 5))
print( gcd(24, 12))
