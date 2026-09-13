from typing import List

class Solution:
    def getRow(self, rowIndex: int) -> List[int]:
        if rowIndex == 0:
            return [1]

        triangle = [[]] * (rowIndex + 1)
        print(triangle)
        for i in range(0, rowIndex + 2):
            triangle[i - 1] = [1] * i
        print(triangle)

        for i in range(2, rowIndex + 1):
            for j in range(1, i):
                triangle[i][j] = triangle[i-1][j-1] + triangle[i-1][j]
        
        return triangle[rowIndex]


if __name__ == "__main__":
    sol = Solution()
    print(sol.getRow(3))