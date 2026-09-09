# class Solution:
#     def climbStairs(self, n: int):
#         memo = [-1] * (n + 1)
#         return self.climbStairsRecur(n, memo)

#     def climbStairsRecur(self, i, memo):
#         if i == 0 or i == 1:
#             return 1

#         if memo[i] != -1:
#             return memo[i]

#         memo[i] = self.climbStairsRecur(i - 1, memo) + self.climbStairsRecur(i - 2, memo)

#         return memo[i]
        

class Solution:
    def climbStairs(self, n: int) -> int:
        if n <= 2:
            return n
        
        first = 1
        second = 2

        for i in range(3, n + 1):
            first, second = second, first+ second

        return second

if __name__ == "__main__":
    sol = Solution()
    print(sol.climbStairs(44))

