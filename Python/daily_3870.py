import resource

class Solution:
    def countCommas(self, n: int) -> int:
        if n - 1000 < 0:
            return 0
        return n - 1000 + 1


class Solution2:
    def countCommas(self, n: int) -> int:
        if n < 1000 :
            return 0
        
        if len(str(n)) % 3 == 0  :
            return (len(str(n)) // 3 -1) + (n - 1000)
        return len(str(n)) // 3 + n - 1000

if __name__ == "__main__":
    print(Solution().countCommas(1002))
    print(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss, "KB")