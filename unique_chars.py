"""
Given a string str, your task is to find the smallest window length that contains all the characters of the given string at least one time.

Examples:

Input: str = "aabcbcdbca"
Output: 4
Explanation: Sub-string -> "dbca"

Input: str = "aaab"
Output: 2
Explanation: Sub-string -> "ab"
"""
def get_hash_length(hash):
    keys = hash.keys()
    count = 0
    for key in keys:
        if hash[key] > 0: count += 1
    return count


def find_length(s):
    s_set = set(s)
    hash = {}
    i, j = 0, 0
    min_length = float('inf')
    for j in range(len(s)):
        hash[s[j]] = hash.get(s[j], 0) + 1
        while get_hash_length(hash) == len(s_set):
            min_length = min(min_length, j-i+1)
            hash[s[i]] -= 1
            i += 1
    return min_length



print(find_length("aabcbcdbca"))
print(find_length("aaab"))





