class Solution:
    def countCommas(self, n: int) -> int:
        if n > 1_000_000_000_000:
            print((n - 999_999_999_999))
            return ((n - 999_999_999) + (n - 999_999) + (n - 999))
        if n > 1_000_000_000:
            return ((n - 999_999_999) + (n - 999_999) + (n - 999))
        if n > 1_000_000:
            return ((n - 999_999) + (n - 999)) 
        if n > 1_000:
            return (n - 999)
        return 0

    def countCommas2(self, n: int) -> int:

        ans = 0
        i = 1000
        print("Before loop: ", n % i)
        times = 1
        while i < n:
            ans += (n - i) 
            print(f"Round {times}: ", n % i)
            print(f"       : ", ans)
            i *= 1000
            times += 1
        return ans

    # was so close on this one! i worked out the intuition, but just couldn't reason the math quite well enough
    # tough 

    def countCommas3(self, n: int) -> int:
        p = 1000
        res = 0
        while p <= n:
            res += n - p + 1
            p *= 1000
        return res


if __name__ == "__main__":
    # print(Solution().countCommas(3_367_615_771_392))  
    # correct answer for 1004590: 1008182
    # correct answer for 3_367_615_771_392: 3_490_488_028_856
    # incorrect attempt                    12_469_462_084_572
    # incorrect attempt                    10_101_846_313_179
    # print(Solution().countCommas2(1004590))
    print(Solution().countCommas3(1004590))
    print(Solution().countCommas3(3_367_615_771_392))