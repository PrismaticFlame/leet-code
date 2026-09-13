from typing import List
from bisect import bisect_left

class Solution:
    def maximumWeight(self, intervals: List[List[int]]) -> List[int]:
        # complicated way of sorting the given list based on the right index
        sorted_intervals = sorted([interval + [i] for i, interval in enumerate(intervals)], key=lambda l:l[1])
        # the right indexes of each interval from the sorted list
        rights = [sorted_intervals[i][1] for i in range(len(intervals))]
        # for each position, how many intervals finish before it starts, OR how many intervals' right index ARE LESS than the current positions left index
        # i.e., at index 3 in the counts list, this represents the interval at index 3 in sorted_intervals. given that, how many intervals before this one 
        # have a right index that is less (ends before) the current indexes left index
        counts = [bisect_left(rights, sorted_intervals[i][0]) for i in range(len(sorted_intervals))]
        # memo: for each position, the best total weight achieveable
        # this is a 2D list of pairs. this is 1 behind sorted_intervals unlike counts.
        # memo[i][k]: using only the FIRST i intervals of sorted_intervals
        #   (positions 0..i-1 — note the offset, row 0 means none of them),
        #   picking AT MOST k of them in total,
        #   what's the best score and which original indices achieve it?
        # so memo[3][2] is saying "given up to sorted_intervals[3], and that we can only choose 1 OTHER PREVIOUS intervals, what is the maximum score and the intervals that make that maximum score?"
        memo = [[[0, []], [0 ,[]], [0, []], [0, []], [0, []]] for _ in range(len(sorted_intervals) + 1)]

        # print("memo: ", memo)
        # print("len of memo: ", len(memo))
        # print("len of inner memo: ", len(memo[0]))
        # print("len of inner-inner memo: ", len(memo[0][0]))

        # print("sorted_intervals: ", sorted_intervals)
        # print("rights:            ", rights)
        # print("counts:            ", counts)

        for i in range(len(sorted_intervals)):
            curr_weight = sorted_intervals[i][2]
            curr_idx = sorted_intervals[i][3]
            for k in range(1, 5):
                base_score, base_list = memo[counts[i]][k-1]
                prev = memo[i][k]
                skip = prev
                take = [curr_weight + base_score, sorted(base_list + [curr_idx])]
                if take[0] > skip[0]:
                    memo[i + 1][k] = take
                elif (take[0] == skip[0]) and take[1] < skip[1]:
                    memo[i + 1][k] = take
                else:
                    memo[i + 1][k] = skip
            
        # print("memo:              ", memo)

        return memo[len(memo) - 1][4][1]


if __name__ == "__main__":
    intervals = [[1,3,2],[4,5,2],[1,5,5],[6,9,3],[6,7,1],[8,9,1]]
    # [2,3]
    intervals_2 = [[5,8,1],[6,7,7],[4,7,3],[9,10,6],[7,8,2],[11,14,3],[3,5,5]]
    # [1,3,5,6]

    # 6:21PM, September 12, 2026: this is a very hard problem for me conceptually, and I am have to use 
    # AI considerably to help me understand this problem. Not having it give me any code, just help me conceptually.
    # 7:46PM, September 12, 2026: i cannot believe that i've spent ~2.5 hours on this. it is making slightly more sense 
    # but, i would assume, at like 70% understanding. lots of AI help in concept, adamantly refusing coding assistance
    # 7:55PM, September 12, 2026: taking a damn break, eating dinner
    # 8:20PM, September 12, 2026: back
    # 9:42PM, September 12, 2026: i've got the right answer, no thanks to myself, and i am still having a ridiculous time understanding 
    # this problem. i'm getting seriously confused, minorly pissed off, and majorly depressed
    # 10:09PM, September 12, 2026: submitted to leet code and passed. Claude made a manim animation to explain the process and i think i have it understood. 
    # going to take a break and come back and see if it makes more sense
    # 12:17AM September 13, 2026: doesn't make such more sense, so it will come to me in my dreams

    print("PROBLEM: ", intervals)
    print("ANSWER:  ", Solution().maximumWeight(intervals))
    print("PROBLEM: ", intervals_2)
    print("ANSWER:  ", Solution().maximumWeight(intervals_2))