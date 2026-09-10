class Solution:

    letters      = {"I": 1,
                    "V": 5,
                    "X": 10,
                    "L": 50,
                    "C": 100,
                    "D": 500,
                    "M": 1000}
    subtractions = {"IV": 4,
                    "IX": 9,
                    "XL": 40,
                    "XC": 90,
                    "CD": 400,
                    "CM": 900}

    def romanToInt(self, s: str) -> int:
        """
        My solution to the problem. Got 0ms but pretty high memory usage. Although I think
        that is nearly entirely due to the class variables and the while loops.
        """
        value = 0
        for key in self.subtractions:
            # print(self.subtractions[key])
            while key in s:
                value += self.subtractions[key]
                s = s.replace(key, "", 1)
        for key in self.letters:
            while key in s:
                value += self.letters[key]
                s = s.replace(key, "", 1)
        return value

    def romanToIntLowMem(self, s: str) -> int:
        """
        This is supposedly a low memory version of my solution. Leetcode disagrees.
        Found it on LeetCode, did not create it myself.
        """
        value = 0
        for i in range(len(s)):
            if i + 1 < len(s) and (self.letters[s[i]] < self.letters[s[i + 1]]):
                value -= self.letters[s[i]]
            else:
                value += self.letters[s[i]]
        return value

if __name__ == "__main__":
    print(Solution().romanToInt("III"))
    print(Solution().romanToInt("LII"))
    print(Solution().romanToInt("MCMXCIV"))

    print(Solution().romanToIntLowMem("III"))
    print(Solution().romanToIntLowMem("LII"))
    print(Solution().romanToIntLowMem("MCMXCIV"))
