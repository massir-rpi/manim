from manim import *


class DefaultTemplate(Scene):
    def construct(self):
        circle = Circle()  # create a circle
        circle.set_fill(PINK, opacity=0.5)  # set color and transparency

        square = Square()  # create a square
        square.flip(RIGHT)  # flip horizontally
        square.rotate(-3 * TAU / 8)  # rotate a certain amount

        self.play(Create(square))  # animate the creation of the square
        self.play(Transform(square, circle))  # interpolate the square into the circle
        self.play(FadeOut(square))  # fade out animation

class TransformParts(AnimationGroup):
    """Transform one MathTex into another, part by part.

    Parts with the same tex string move onto each other, paired up left to
    right when a string repeats. ``matches`` pairs up parts whose tex changes,
    by index: ``(5, 6)`` turns source part 5 into target part 6, and a list of
    indices merges or splits parts, e.g. ``([8, 11], 9)``. Leftover source
    parts fade out where they are; leftover target parts come in afterwards,
    with ``introducer``.

    TransformMatchingTex works the same way, but it slides leftover parts
    toward each other (toward the screen center when there's nothing to slide
    toward), and its key_map can't merge parts.
    """

    def __init__(self, source, target, matches=(), introducer=FadeIn, **kwargs):
        source_keys = [part.tex_string for part in source]
        target_keys = [part.tex_string for part in target]
        for n, (src, tgt) in enumerate(matches):
            for i in np.atleast_1d(src):
                source_keys[i] = n
            for i in np.atleast_1d(tgt):
                target_keys[i] = n

        moving_source, moving_target = VGroup(), VGroup()
        for key in dict.fromkeys(target_keys):
            if key in source_keys:
                moving_source.add(VGroup(*[p for p, k in zip(source, source_keys) if k == key]))
                moving_target.add(VGroup(*[p for p, k in zip(target, target_keys) if k == key]))
        # empty parts (like a lone "}") have nothing to draw
        leaving = VGroup(*[
            p for p, k in zip(source, source_keys)
            if k not in target_keys and p.family_members_with_points()
        ])
        arriving = VGroup(*[
            p for p, k in zip(target, target_keys)
            if k not in source_keys and p.family_members_with_points()
        ]).copy()

        moves = [Transform(moving_source, moving_target, **kwargs)]
        if leaving:
            moves.append(FadeOut(leaving, **kwargs))
        anims = [AnimationGroup(*moves)]
        if arriving:
            anims.append(introducer(arriving, **kwargs))
        # new parts come in once everything else has moved, so they aren't
        # drawn on top of terms still sliding past
        super().__init__(*anims, lag_ratio=1)
        self.source, self.target, self.arriving = source, target, arriving

    def clean_up_from_scene(self, scene):
        # Not calling super(): FadeOut's clean up removes the leaving parts on
        # their own, which makes the scene split up the source, so removing the
        # source below would miss its remaining parts. Same as manim's own
        # TransformMatchingTex. Instead, put the source back the way it was and
        # swap in the real target.
        for anim in self.animations:
            anim.interpolate(0)
        scene.remove(self.mobject, self.source, self.arriving)
        scene.add(self.target)


def equals(eq):
    """The = sign of eq."""
    return eq.get_part_by_tex("=", substring=False)


def place_below(eq, above, buff=0.4):
    """Put eq under `above`, with their = signs lined up."""
    eq.next_to(above, DOWN, buff=buff)
    eq.shift((equals(above).get_x() - equals(eq).get_x()) * RIGHT)
    return eq


def hl(eq, *indices):
    """Color the given parts of eq yellow, to show what's being worked on."""
    for i in indices:
        eq[i].set_color(YELLOW)
    return eq


def align_equals(eq, ref):
    """Shift eq so its = sign sits exactly where ref's does."""
    eq.shift(equals(ref).get_center() - equals(eq).get_center())
    return eq

class QuadraticFormula(Scene):
    def construct(self):
        def unhighlight(*mobs):
            """Fade highlighted mobjects back to white."""
            self.play(*[m.animate.set_color(WHITE) for m in mobs], run_time=0.75)
            self.wait(0.5)

        formula = MathTex("a", "x^2", "+", "b", "x", "+c", "=", "0")
        subC = hl(MathTex("a", "x^2", "+", "b", "x", "=", "-c"), 6)
        divA = hl(MathTex("x^2", "+", "{b", "\\over", "a}", "x", "=", "-{c", "\\over", "a}"), 3, 4, 8, 9)

        subC.move_to(formula)
        divA.move_to(subC, UP + LEFT)

        self.play(Write(formula))  # animate the writing of the formula

        self.wait(1)  # wait for a moment to let the formula appear

        # move c across, flipping its sign; the 0 fades away
        self.play(TransformParts(formula, subC, matches=[(5, 6)], run_time=2))

        self.wait(1)  # wait for a moment to let the transformation complete
        unhighlight(subC)

        # divide by a: the a splits under both b and c
        self.play(TransformParts(
            subC, divA,
            matches=[(0, [4, 9]), (3, 2), (6, 7)],
            introducer=Write,
            run_time=2,
        ))

        self.wait(1)  # wait for a moment to let the transformation complete
        unhighlight(divA)

        square = Square(side_length=1, stroke_width=2)
        linear = Rectangle(height=1, width=0.5, stroke_width=2)
        const = Rectangle(height=1.5, width=1, stroke_width=2)
        plus = Tex("+")
        equal = Tex("=")
        geoEq = VGroup(square, plus, linear, equal, const).arrange(RIGHT, buff=0.25)
        geoEq.move_to(ORIGIN)  # center the group

        # Move equation up and shrink it
        self.play(
            divA.animate.shift(3*UP),
            run_time=2
        )

        geoEq.move_to(ORIGIN)

        # Draw the geometric representation of the equation
        self.play(Create(geoEq))

        self.wait(1)  # wait for a moment to let the geometric representation appear

        # new shape positions for labeled equation
        square_labeled = Square(side_length=1, stroke_width=2)
        linear_labeled = Rectangle(height=1, width=0.5, stroke_width=2)
        const_labeled = Rectangle(height=1.5, width=1, stroke_width=2)
        plus_labeled = Tex("+")
        equal_labeled = Tex("=")

        # Label the square's sides with 'x'
        square_label1 = MathTex("x")
        square_label2 = MathTex("x")
        #square_label1.next_to(square_labeled, LEFT, buff=0.05)

        # Label the left rectangle's sides with 'x' and 'b/a'
        linear_label1 = MathTex("x")
        linear_label2 = MathTex("\\frac{b}{a}").scale(0.8)
        #linear_label1.next_to(linear_labeled, LEFT, buff=0.05)

        #Label const rectangle with 'c/a'
        const_label = MathTex("-\\frac{c}{a}").scale(0.8)

        # Put vertical labels in-line
        geoEqLabeled = VGroup(square_label1, square_labeled, plus_labeled, linear_label1, linear_labeled, equal_labeled, const_labeled).arrange(RIGHT, buff=0.25)
        geoEqLabeled.move_to(geoEq)
        const_label.move_to(const_labeled.get_center())

        # Position the horizontal labels
        square_label2.next_to(square_labeled, DOWN, buff=0.05)
        linear_label2.next_to(linear_labeled, DOWN, buff=0.05)

        # Animate the labels
        self.play(*[
                ReplacementTransform(
                    old,
                    new,
                    run_time = 2
                ) for old, new in [
                    (square, square_labeled),
                    (linear, linear_labeled),
                    (const, const_labeled),
                    (plus, plus_labeled),
                    (equal, equal_labeled)
                ]
            ]
        )

        self.play(
            Write(square_label1),
            Write(square_label2),
            Write(linear_label1),
            Write(linear_label2),
            Write(const_label)
        )

        # --- Animation: Replace b/a with 2b/2a in TeX equation ---
        divA2 = hl(MathTex("x^2", "+", "2", "{b", "\\over", "2", "a}", "x", "=", "-{c", "\\over", "a}"), 2, 5)
        divA2.move_to(divA)
        self.play(TransformParts(divA, divA2, introducer=Write, run_time=2))
        self.wait(1)

        # --- Animation: Split linear rectangle and replace b/a label ---
        # Create two half-rectangles
        linear_half = Line(linear_labeled.get_top(), linear_labeled.get_bottom(), stroke_width=2, color=YELLOW)

        # New labels
        linear_label_left = MathTex("\\frac{b}{2a}", color=YELLOW).scale(0.6)
        linear_label_right = MathTex("\\frac{b}{2a}", color=YELLOW).scale(0.6)
        linear_label_left.next_to(linear_half, DOWN + LEFT, buff=0.05)
        linear_label_right.next_to(linear_half, DOWN + RIGHT, buff=0.05)

        # Animate: fade out old label, show new rectangles and labels
        self.play(
            FadeOut(linear_label2),
            Write(linear_half),
            Write(linear_label_left),
            Write(linear_label_right),
        )

        #Two rectangles to cover old rectangle
        linear_left = Rectangle(height=1, width=0.25, stroke_width=2, color=YELLOW)
        linear_right = Rectangle(height=1, width=0.25, stroke_width=2, color=YELLOW)
        linear_left.move_to(linear_half, aligned_edge=RIGHT)
        linear_right.move_to(linear_half, aligned_edge=LEFT)
        self.play(
            Write(linear_left),
            Write(linear_right),
            FadeOut(linear_labeled),
            FadeOut(linear_half),
        )
        self.wait(1)

        # --- Animation: Attach linear halves to square ---
        '''square_group = VGroup(square_labeled, square_label1, square_label2,
                              linear_left, linear_right,
                              linear_label_left, linear_label_right)
        geEqArr = VGroup(square_group, equal_labeled, const_labeled)

        self.play(
            geEqArr.animate.arrange(RIGHT, buff=0.25),
            linear_left.animate.rotate(PI/2).move_to(square_labeled.get_top(), aligned_edge=DOWN),
            linear_right.animate.move_to(square_labeled.get_right(), aligned_edge=LEFT),
            linear_label_left.animate.next_to(linear_left, LEFT, buff=0.05),
            linear_label_right.animate.next_to(linear_right, DOWN, buff=0.05),
            const_label.animate.move_to(const_labeled.get_center()),
            FadeOut(plus_labeled),
            FadeOut(linear_label1),
            run_time = 2
        )'''

        square_att = square_labeled.copy()
        equal_att = equal_labeled.copy()
        square_label1_att = square_label1.copy()
        square_label2_att = square_label2.copy()
        const_att = const_labeled.copy()
        const_att_label = const_label.copy()

        linear_top_att = Rectangle(height=1, width=0.25, stroke_width=2, color=YELLOW).rotate(PI/2)
        linear_top_att.move_to(square_att.get_top(), aligned_edge=DOWN)
        linear_right_att = Rectangle(height=1, width=0.25, stroke_width=2, color=YELLOW)
        linear_right_att.move_to(square_att.get_right(), aligned_edge=LEFT)

        linear_top_att_label = MathTex("\\frac{b}{2a}", color=YELLOW).scale(0.6)
        linear_top_att_label.next_to(linear_top_att, LEFT, buff=0.05)
        linear_right_att_label = MathTex("\\frac{b}{2a}", color=YELLOW).scale(0.6)
        linear_right_att_label.next_to(linear_right_att, DOWN, buff=0.05)

        square_group_att = VGroup(
            square_att, square_label1_att, square_label2_att,
            linear_top_att, linear_right_att,
            linear_top_att_label, linear_right_att_label)

        geo_eq_att = VGroup(
            square_group_att, equal_att, const_att
        ).arrange(RIGHT, buff=0.25)
        const_att_label.move_to(const_att.get_center())

        self.play(
            ReplacementTransform(
                square_labeled, square_att,
                run_time = 2
            ),
            ReplacementTransform(
                equal_labeled, equal_att,
                run_time = 2
            ),
            ReplacementTransform(
                square_label1, square_label1_att,
                run_time = 2
            ),
            ReplacementTransform(
                square_label2, square_label2_att,
                run_time = 2
            ),
            ReplacementTransform(
                linear_left, linear_top_att,
                run_time = 2
            ),
            ReplacementTransform(
                linear_right, linear_right_att,
                run_time = 2
            ),
            ReplacementTransform(
                linear_label_left, linear_top_att_label,
                run_time = 2
            ),
            ReplacementTransform(
                linear_label_right, linear_right_att_label,
                run_time = 2
            ),
            ReplacementTransform(
                VGroup(const_labeled, const_label), VGroup(const_att, const_att_label),
                run_time = 2
            ),
            FadeOut(plus_labeled),
            FadeOut(linear_label1),
        )
        
        self.wait(2)
        unhighlight(divA2, linear_top_att, linear_right_att, linear_top_att_label, linear_right_att_label)

        square_comp1 = Square(side_length=0.25, stroke_width=2, color=YELLOW)
        square_comp2 = Square(side_length=0.25, stroke_width=2, color=YELLOW)
        plus.move_to(const_att.get_right()+0.25*RIGHT, aligned_edge=LEFT)
        square_comp2.move_to(plus.get_right()+0.25*RIGHT, aligned_edge=LEFT)
        square_comp1.move_to(linear_right_att.get_top(), aligned_edge=DOWN)

        self.play(
            Write(plus),
            Write(square_comp1),
            Write(square_comp2),
        )

        # The corner square's sides are the bars' thicknesses, so borrow their
        # labels. The copies start invisible, so there are never two full
        # copies stacked.
        corner_top_label = linear_top_att_label.copy().set_color(YELLOW).next_to(square_comp1, UP, buff=0.05)
        corner_right_label = linear_right_att_label.copy().set_color(YELLOW).next_to(square_comp1, RIGHT, buff=0.05)
        self.play(*[
            ReplacementTransform(label.copy().set_opacity(0), target)
            for label, target in [
                (linear_top_att_label, corner_top_label),
                (linear_right_att_label, corner_right_label),
            ]
        ], run_time=1.5)

        self.wait(1)

        eq_comp_sq = hl(MathTex(
            "x^2", "+", "2", "{b", "\\over", "2", "a}", "x", "+{b^2 \\over 4a^2}",
            "=", "-{c", "\\over", "a}", "+{b^2 \\over 4a^2}",
        ), 8, 13)
        eq_comp_sq.move_to(divA2.get_top(), aligned_edge=UP)

        self.play(TransformParts(divA2, eq_comp_sq, introducer=Write, run_time=2))

        self.wait(2)
        unhighlight(eq_comp_sq, square_comp1, square_comp2, corner_top_label, corner_right_label)

        # --- Animation: Display completed square equation under geo eq ---
        eq_sq = hl(MathTex(
            "\\left(", "x", "+{b", "\\over", "2a}", "\\right)^2",
            "=", "-{c", "\\over", "a}", "+{b^2", "\\over", "4a^2}",
        ), 0, 1, 2, 3, 4, 5)

        geo_eq_comp = VGroup(
            square_group_att, equal_att, const_att, const_att_label, plus,
            square_comp1, square_comp2, corner_top_label, corner_right_label,
        )
        self.play(
            eq_comp_sq.animate.to_corner(UL, buff=0.5),
            # arc right, then up, so the shapes don't sweep through the equation
            geo_eq_comp.animate(path_arc=-PI / 3).to_corner(UR, buff=0.5),
        )

        place_below(eq_sq, eq_comp_sq)
        self.play(Write(eq_sq))

        self.wait(2)
        unhighlight(eq_sq)

        # --- Animation: Drop the geometry and solve for x ---
        # Two columns of steps. Each step leaves a copy of the last line where
        # it is, slides the line into the next slot, and rewrites it there in
        # small sub-steps, with the terms being worked on in yellow. Lines are
        # scaled down so two columns of them fit side by side.
        left_x, right_x, top, scale = -4.0, 3.15, 3.4, 0.85

        def to_column_top(eq, column_x):
            """Shift eq so its = sign is at column_x and its top at the top."""
            eq.shift((column_x - equals(eq).get_x()) * RIGHT)
            eq.shift((top - eq.get_top()[1]) * UP)
            return eq

        def slide(line, column_x=None):
            """Leave a copy of line behind and move line to the next slot:
            below itself, or to the top of the column at column_x."""
            stay = line.copy()
            if column_x is None:
                target = place_below(line.copy(), line, buff=0.5)
                path_arc = 0
            else:
                target = to_column_top(line.copy(), column_x)
                # swing down and around, under the column it's leaving
                path_arc = PI / 2
            # The copy is just there, since the line never really left. Start
            # fast so the moving line clears it within a frame or two (while
            # they overlap, the line looks bold).
            self.add(stay)
            self.bring_to_front(line)
            self.play(
                line.animate(path_arc=path_arc, rate_func=rate_functions.ease_out_cubic).move_to(target),
                run_time=1.5,
            )
            return stay

        def rewrite(eq, new, matches=(), **kwargs):
            """Transform eq in place into new, keeping the = sign fixed."""
            align_equals(new.scale(scale), eq)
            self.play(TransformParts(eq, new, matches=matches, introducer=Write, run_time=1.5, **kwargs))
            self.wait(0.5)
            return new

        def emphasize(eq, yellow=(), white=()):
            self.play(
                *[eq[i].animate.set_color(YELLOW) for i in yellow],
                *[eq[i].animate.set_color(WHITE) for i in white],
                run_time=0.75,
            )

        # (x + b/2a)^2, split up so its pieces can move on their own
        sq = ["\\left(", "x", "+{b", "\\over", "2a}", "\\right)^2"]

        self.play(FadeOut(geo_eq_comp), FadeOut(eq_comp_sq))
        eq_sq.generate_target()
        to_column_top(eq_sq.target.scale(scale), left_x)
        self.play(MoveToTarget(eq_sq), run_time=1.5)
        self.wait(0.5)
        kept = []

        # 1. Put -c/a over the common denominator: multiply top and bottom by 4a
        kept.append(slide(eq_sq))
        eq = rewrite(eq_sq, hl(MathTex(
            *sq, "=", "-{c", "\\cdot 4a", "\\over", "a", "\\cdot 4a}", "+{b^2", "\\over", "4a^2}",
        ), 8, 11), matches=[(9, 10)])
        eq = rewrite(eq, hl(MathTex(
            *sq, "=", "-{4ac", "\\over", "4a^2}", "+{b^2", "\\over", "4a^2}",
        ), 7, 9), matches=[([7, 8], 7), ([10, 11], 9)])
        unhighlight(eq)

        # 2. Swap the fractions, then put them over one bar
        kept.append(slide(eq))
        eq = rewrite(eq, MathTex(
            *sq, "=", "{b^2", "\\over", "4a^2}", "-{4ac", "\\over", "4a^2}",
        ), matches=[(10, 7), (11, 8), (12, 9), (7, 10), (8, 11), (9, 12)], path_arc=PI / 2)
        eq = rewrite(eq, hl(MathTex(
            *sq, "=", "{b^2", "-4ac", "\\over", "4a^2}",
        ), 9, 10), matches=[(7, 7), (10, 8), ([8, 11], 9), ([9, 12], 10)])
        unhighlight(eq)

        # 3. Square root of both sides; on the left it undoes the square, and
        #    on the right it could be either sign
        kept.append(slide(eq))
        eq = rewrite(eq, hl(MathTex(
            "\\sqrt{", *sq, "}", "=", "\\sqrt{", "{b^2", "-4ac", "\\over", "4a^2}", "}",
        ), 0, 9))
        emphasize(eq, yellow=(1, 6), white=(9,))
        eq = rewrite(eq, hl(MathTex(
            "x", "+{b", "\\over", "2a}", "=", "\\pm", "\\sqrt{", "{b^2", "-4ac", "\\over", "4a^2}", "}",
        ), 5), matches=[(9, 6)])
        unhighlight(eq)

        # 4. Split the root over the top and bottom; the root of 4a^2 is 2a
        kept.append(slide(eq, column_x=right_x))
        eq = rewrite(eq, hl(MathTex(
            "x", "+{b", "\\over", "2a}", "=", "\\pm",
            "{", "\\sqrt{", "b^2", "-4ac", "}", "\\over", "\\sqrt{", "4a^2", "}}",
        ), 7, 12), matches=[(6, [7, 12]), (7, 8), (10, 13)])
        eq = rewrite(eq, hl(MathTex(
            "x", "+{b", "\\over", "2a}", "=", "\\pm",
            "{", "\\sqrt{", "b^2", "-4ac", "}", "\\over", "2a}",
        ), 12), matches=[([12, 13], 12)])
        unhighlight(eq)

        # 5. Subtract b/2a from both sides; it cancels on the left
        kept.append(slide(eq))
        eq = rewrite(eq, hl(MathTex(
            "x", "+{b", "\\over", "2a}", "-{b", "\\over", "2a}",
            "=", "-{b", "\\over", "2a}", "\\pm", "{", "\\sqrt{", "b^2", "-4ac", "}", "\\over", "2a}",
        ), 4, 5, 6, 8, 9, 10), matches=[(2, 2), (3, 3), (11, 17), (12, 18)])
        emphasize(eq, yellow=(1, 2, 3), white=(8, 9, 10))
        eq = rewrite(eq, MathTex(
            "x", "=", "-{b", "\\over", "2a}", "\\pm", "{", "\\sqrt{", "b^2", "-4ac", "}", "\\over", "2a}",
        ), matches=[(8, 2), (9, 3), (10, 4), (17, 11), (18, 12)])
        self.wait(0.5)

        # 6. Both fractions are over 2a, so combine them
        kept.append(slide(eq))
        eq = rewrite(eq, hl(MathTex(
            "x", "=", "{-b", "\\pm", "\\sqrt{", "b^2", "-4ac", "}", "\\over", "2a}",
        ), 8, 9), matches=[(2, 2), ([3, 11], 8), ([4, 12], 9)])
        unhighlight(eq)

        # --- Animation: Box the quadratic formula ---
        quad_formula = eq
        self.play(*[FadeOut(line) for line in kept])
        self.play(quad_formula.animate.scale(1.5 / scale).move_to(ORIGIN), run_time=1.5)
        box = SurroundingRectangle(quad_formula, buff=0.3)
        title = Tex("The Quadratic Formula").next_to(box, UP, buff=0.4)
        self.play(Create(box), Write(title))

        self.wait(2)


class Move(Scene):
    def construct(self):
        # f_tex = self.graph_label_tex
        equation = Tex(
            "dA", "\\approx", "dx", "x^2",
            arg_separator=" ",
            tex_environment="align*"
        )
        #equation.to_edge(RIGHT).shift(3*UP)
        deriv_equation = Tex(
            "{dA", "\\over \\,", "dx}", "\\approx", "x^2",
            arg_separator=" ",
            tex_environment="align*"
        )

        deriv_equation.move_to(equation, UP+LEFT)

        self.play(*[
            ReplacementTransform(
                equation.get_part_by_tex(tex),
                deriv_equation.get_part_by_tex(tex),
                run_time = 2,
            )
            for tex in ("dA", "approx", "x^2", "dx")
        ] + [
            Write(deriv_equation.get_part_by_tex("over"))
        ])
