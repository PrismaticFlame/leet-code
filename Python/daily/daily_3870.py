import resource
import tracemalloc

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
    tracemalloc.start()
    print(Solution().countCommas(1002))
    current, peak = tracemalloc.get_traced_memory()
    print(f"current={current}, peak={peak} bytes")
    tracemalloc.stop()
    print(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss, "KB")

    # was getting annoyed with leetcode saying my solution, Solution, was using more memory
    # than another persons solution, Solution2, and wanted to see how much memory was being used.
    # mine overall uses less memory, but leetcode seems to think otherwise
    # AI says small problems have variable memory usages due to Python overhead, initialization, and 
    # leet code judge harness have some noise going on