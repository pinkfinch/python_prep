'''
 Longest Substring Without Repeating Characters

 Given a string s, find the length of the longest substring without duplicate characters.

Example 1:
Input: s = "abcabcbb"
Output: 3
Explanation: The answer is "abc", with the length of 3. Note that "bca" and "cab" are also correct answers.

Example 2:
Input: s = "bbbbb"
Output: 1
Explanation: The answer is "b", with the length of 1.

Example 3:
Input: s = "pwwkew"
Output: 3
Explanation: The answer is "wke", with the length of 3.
Notice that the answer must be a substring, "pwke" is a subsequence and not a substring.


Constraints:

0 <= s.length <= 5 * 104
s consists of English letters, digits, symbols and spaces.
'''


def lengthOfLongestSubstring(s: str) -> int:
    if s == "": return 0
    max_len = 1
    length = len(s)
    h = {}
    prev_index = 0
    for i in range(0,length):
        if s[i] in h:
            max_len = max(max_len, i-prev_index)
            prev_index = i
        else:
            # print(s[prev_index:i+1])
            max_len = max(max_len, i-prev_index+1)
        h[s[i]] = i

    return max_len

# print(lengthOfLongestSubstring("abcabcbb"))
print(lengthOfLongestSubstring("aabaab!bb"))
# print(lengthOfLongestSubstring("pwwkew"))
# print(lengthOfLongestSubstring("au"))