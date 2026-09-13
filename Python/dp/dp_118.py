from typing import List

class Solution:
    def generate(self, numRows: int) -> List[List[int]]:
        if numRows == 1:
            return [[1]]

        triangle = [[]] * numRows
        for i in range(0, numRows + 1):
            triangle[i - 1] = [1] * i

        for i in range(2, numRows):
            for j in range(1, i):
                triangle[i][j] = triangle[i-1][j-1] + triangle[i-1][j]
        
        return triangle

if __name__ == "__main__":
    sol = Solution()
    print(sol.generate(5))