from manim import *
from bisect import bisect_left

EX2 = [[5, 8, 1], [6, 7, 7], [4, 7, 3], [9, 10, 6], [7, 8, 2], [11, 14, 3], [3, 5, 5]]

C_TAKE = TEAL_C
C_SKIP = YELLOW_C
C_WRITE = PURPLE_B
C_ROW = BLUE_C


def build_trace(intervals):
    si = sorted([iv + [i] for i, iv in enumerate(intervals)], key=lambda l: l[1])
    rights = [x[1] for x in si]
    counts = [bisect_left(rights, x[0]) for x in si]
    n = len(si)
    memo = [[[0, []] for _ in range(5)] for _ in range(n + 1)]
    steps = []
    for i in range(n):
        w, oidx = si[i][2], si[i][3]
        for k in range(1, 5):
            base_score, base_list = memo[counts[i]][k - 1]
            skip = [memo[i][k][0], list(memo[i][k][1])]
            take = [w + base_score, sorted(base_list + [oidx])]
            if take[0] > skip[0]:
                win, why = take, "take wins on score"
            elif take[0] == skip[0] and take[1] < skip[1]:
                win, why = take, "tie, take is lex smaller"
            else:
                win, why = skip, "skip wins"
            memo[i + 1][k] = [win[0], list(win[1])]
            steps.append(dict(i=i, k=k, cnt=counts[i], w=w, oidx=oidx,
                              take_src=(counts[i], k - 1), skip_src=(i, k),
                              dst=(i + 1, k), take=take, skip=skip,
                              win=[win[0], list(win[1])], why=why))
    return si, rights, counts, steps, memo


def fmt(pair):
    lst = ",".join(str(x) for x in pair[1])
    return str(pair[0]), "[" + lst + "]"


class DPWalkthrough(Scene):
    def construct(self):
        si, rights, counts, steps, memo = build_trace(EX2)
        n = len(si)

        title = Text("Interval DP — example 2", font_size=30, weight=BOLD)
        title.to_edge(UP, buff=0.25)
        self.play(Write(title), run_time=1.2)

        # ---------- left table ----------
        hdr = ["pos", "span", "w", "idx", "cnt"]
        colx = [-6.55, -5.75, -4.95, -4.45, -3.85]
        tbl = VGroup()
        hdr_row = VGroup(*[Text(h, font_size=15, color=GREY_B).move_to([colx[j], 2.55, 0])
                           for j, h in enumerate(hdr)])
        tbl.add(hdr_row)
        row_bgs = {}
        rowtexts = []
        for r in range(n):
            y = 2.15 - r * 0.46
            bg = Rectangle(width=3.4, height=0.42, stroke_width=0,
                           fill_color=C_ROW, fill_opacity=0).move_to([-5.2, y, 0])
            row_bgs[r] = bg
            vals = [str(r), f"{si[r][0]}-{si[r][1]}", str(si[r][2]),
                    str(si[r][3]), str(counts[r])]
            g = VGroup(*[Text(v, font_size=15).move_to([colx[j], y, 0])
                         for j, v in enumerate(vals)])
            rowtexts.append(g)
            tbl.add(bg, g)
        cap = Text("sorted by right endpoint", font_size=13, color=GREY_B)
        cap.move_to([-5.2, 2.9, 0])
        self.play(FadeIn(tbl), FadeIn(cap), run_time=1.4)

        # ---------- memo grid ----------
        CW, CH = 1.32, 0.52
        gx0, gy0 = -1.05, 2.35
        cells, ctexts = {}, {}
        grid = VGroup()
        for c in range(5):
            lab = Text(f"k={c}", font_size=15, color=GREY_B)
            lab.move_to([gx0 + c * CW + CW / 2, gy0 + 0.38, 0])
            grid.add(lab)
        for r in range(n + 1):
            lab = Text(f"row {r}", font_size=13, color=GREY_B)
            lab.move_to([gx0 - 0.52, gy0 - r * CH - CH / 2, 0])
            grid.add(lab)
            for c in range(5):
                rect = Rectangle(width=CW, height=CH, stroke_width=1.2,
                                 stroke_color=GREY_D, fill_opacity=0)
                rect.move_to([gx0 + c * CW + CW / 2, gy0 - r * CH - CH / 2, 0])
                s = Text("0", font_size=14).move_to(rect.get_center() + UP * 0.10)
                l = Text("[]", font_size=11, color=GREY_B).move_to(rect.get_center() + DOWN * 0.12)
                cells[(r, c)] = rect
                ctexts[(r, c)] = VGroup(s, l)
                grid.add(rect, s, l)
        self.play(Create(grid), run_time=2.0)

        note = Text("row r = the first r intervals;  column k = at most k picks",
                    font_size=15, color=GREY_B)
        note.next_to(grid, DOWN, buff=0.22)
        self.play(FadeIn(note), run_time=1.0)
        self.wait(1.2)
        self.play(FadeOut(note), run_time=0.5)

        info = Text("", font_size=17).move_to([0.6, -3.35, 0])
        sub = Text("", font_size=15, color=GREY_B).move_to([0.6, -3.72, 0])
        self.add(info, sub)

        def set_info(a, b, col=WHITE):
            ni = Text(a, font_size=17, color=col).move_to([0.6, -3.35, 0])
            ns = Text(b, font_size=15, color=GREY_B).move_to([0.6, -3.72, 0])
            return Transform(info, ni), Transform(sub, ns)

        cur_i = -1
        arrow = None
        for st in steps:
            i, k = st["i"], st["k"]
            if i != cur_i:
                if cur_i >= 0:
                    self.play(row_bgs[cur_i].animate.set_fill(opacity=0), run_time=0.3)
                cur_i = i
                a1, a2 = set_info(
                    f"position {i}:  span {si[i][0]}-{si[i][1]},  weight {si[i][2]},  original index {si[i][3]}",
                    f"counts = {st['cnt']}  ->  read row {st['cnt']}")
                self.play(row_bgs[i].animate.set_fill(opacity=0.28), a1, a2, run_time=0.9)
                if arrow is not None:
                    self.play(FadeOut(arrow), run_time=0.2)
                arrow = Arrow(rowtexts[i][4].get_right() + RIGHT * 0.05,
                              cells[(st["cnt"], 0)].get_left() + LEFT * 0.05,
                              buff=0.05, stroke_width=2.5, color=C_TAKE,
                              max_tip_length_to_length_ratio=0.09)
                self.play(GrowArrow(arrow), run_time=0.7)
                self.wait(0.5)

            tr, tc = st["take_src"]
            sr, sc = st["skip_src"]
            dr, dc = st["dst"]

            a1, a2 = set_info(f"k = {k}   budget of {k} pick(s)", "")
            self.play(a1, a2, run_time=0.5)

            self.play(cells[(sr, sc)].animate.set_stroke(C_SKIP, width=3.5)
                      .set_fill(C_SKIP, opacity=0.16), run_time=0.5)
            ss, sl = fmt(st["skip"])
            a1, a2 = set_info(f"skip  = {ss}  {sl}",
                              "same column, one row up — no pick spent")
            self.play(a1, a2, run_time=0.8)
            self.wait(0.7)

            self.play(cells[(tr, tc)].animate.set_stroke(C_TAKE, width=3.5)
                      .set_fill(C_TAKE, opacity=0.16), run_time=0.5)
            ts, tl = fmt(st["take"])
            bs, bl = fmt([st["take"][0] - st["w"], sorted(set(st["take"][1]) - {st["oidx"]})])
            a1, a2 = set_info(f"take  = {st['w']} + {bs} = {ts}   {tl}",
                              f"row {tr} (overlap), column {tc} (budget spent)")
            self.play(a1, a2, run_time=0.8)
            self.wait(0.9)

            ws, wl = fmt(st["win"])
            a1, a2 = set_info(st["why"] + f"   ->   {ws}  {wl}",
                              f"write into row {dr}, column {dc}",
                              col=C_WRITE)
            self.play(a1, a2, run_time=0.7)

            new_s = Text(ws, font_size=14).move_to(cells[(dr, dc)].get_center() + UP * 0.10)
            new_l = Text(wl, font_size=11, color=GREY_B).move_to(cells[(dr, dc)].get_center() + DOWN * 0.12)
            self.play(cells[(dr, dc)].animate.set_stroke(C_WRITE, width=3.5)
                      .set_fill(C_WRITE, opacity=0.22),
                      Transform(ctexts[(dr, dc)][0], new_s),
                      Transform(ctexts[(dr, dc)][1], new_l), run_time=0.7)
            self.wait(0.6)

            self.play(cells[(sr, sc)].animate.set_stroke(GREY_D, width=1.2).set_fill(opacity=0),
                      cells[(tr, tc)].animate.set_stroke(GREY_D, width=1.2).set_fill(opacity=0),
                      cells[(dr, dc)].animate.set_stroke(GREY_D, width=1.2).set_fill(opacity=0),
                      run_time=0.4)

        self.play(row_bgs[cur_i].animate.set_fill(opacity=0), FadeOut(arrow), run_time=0.4)

        fs, fl = fmt(memo[n][4])
        a1, a2 = set_info(f"answer = memo[{n}][4] = {fl}   score {fs}", "", col=C_TAKE)
        self.play(cells[(n, 4)].animate.set_stroke(C_TAKE, width=4.5)
                  .set_fill(C_TAKE, opacity=0.3), a1, a2, run_time=1.2)
        self.wait(3.0)