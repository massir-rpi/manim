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

class QuadraticFormula(Scene):
    def construct(self):
        formula = Tex(
            "a", "x^2", "+", "b", "x", "+c", "=", "0",
            arg_separator=" ",
            tex_environment="align*"
        )
        subC = Tex(
            "a", "x^2", "+", "b", "x", "=", "-c",
            arg_separator=" ",
            tex_environment="align*"
        )
        divA = Tex(
            "x^2", "+", "{b", "\\over \\,", "a}", "x", "=", "-{c", "\\over \\,", "a}",
            arg_separator=" ",
            tex_environment="align*"
        )

        subC.move_to(formula)
        divA.move_to(subC, UP + LEFT)

        #print("formula ", [formula.get_part_by_tex(tex) for tex in ("a", "x^2", "b", "x", "=", "c")], "\n", 
        #      "subC ", [subC.get_part_by_tex(tex) for tex in ("a", "x^2", "b", "x", "=", "c")])

        self.play(Write(formula))  # animate the writing of the formula

        self.wait(1)  # wait for a moment to let the formula appear

        self.play(*[
            ReplacementTransform(
                formula.get_part_by_tex(tex),
                subC.get_part_by_tex(tex),
                run_time = 2,
            )
            for tex in ("a", "x^2", "+", "b", "=", "c")
        ] + [
            ReplacementTransform(
                formula.get_part_by_tex("x", substring=False),
                subC.get_part_by_tex("x", substring=False),
                run_time = 2,
            )
        ] + [
            FadeOut(formula.get_part_by_tex("0"))
        ])

        self.wait(1)  # wait for a moment to let the transformation complete

        self.play(*[
            ReplacementTransform(
                subC.get_part_by_tex(tex),
                divA.get_part_by_tex(tex),
                run_time = 2,
            )
            for tex in ("x^2", "+", "b", "=", "c")
        ] + [
            ReplacementTransform(
                subC.get_part_by_tex("x", substring=False),
                divA.get_part_by_tex("x", substring=False),
                run_time = 2,
            )
        ] + [
            ReplacementTransform(
                subC.get_part_by_tex("a"),
                divA.get_parts_by_tex("a"),
                run_time = 2,
            )
        ] + [
            Write(divA.get_parts_by_tex("over"))
        ])

        self.wait(1)  # wait for a moment to let the transformation complete

        square = Square(side_length=0.5, stroke_width=2)
        linear = Rectangle(height=0.5, width=0.25, stroke_width=2)
        const = Rectangle(height=0.75, width=0.5, stroke_width=2)
        plus = Tex("+")
        equal = Tex("=")
        geoEq = VGroup(square, plus, linear, equal, const).arrange(RIGHT, buff=0.25)
        geoEq.scale(0.8)  # scale down to fit the frame
        geoEq.move_to(ORIGIN)  # center the group

        # Move equation up and shrink it
        self.play(
            divA.animate.scale(0.5).shift(UP),
            run_time=2
        )

        geoEq.next_to(divA, DOWN)

        # Draw the geometric representation of the equation
        self.play(Create(geoEq))

        self.wait(1)  # wait for a moment to let the geometric representation appear

        # Label the square's sides with 'x'
        square_label1 = MathTex("x").scale(0.5)
        square_label2 = MathTex("x").scale(0.5)
        square_label1.next_to(square, LEFT, buff=0.05)
        square_label2.next_to(square, DOWN, buff=0.05)

        # Label the left rectangle's sides with 'x' and 'b/a'
        linear_label1 = MathTex("x").scale(0.5)
        linear_label2 = MathTex("\\frac{b}{a}").scale(0.3)
        linear_label1.next_to(linear, LEFT, buff=0.05)
        linear_label2.next_to(linear, DOWN, buff=0.05)

        # Animate the labels
        self.play(
            Write(square_label1),
            Write(square_label2),
            Write(linear_label1),
            Write(linear_label2),
        )

        # --- Animation: Replace b/a with 2b/2a in TeX equation ---
        divA2 = Tex(
            "x^2", "+", "2", "{b", "\\over \,", "2", "a}", "x", "=", "-{c", "\\over \,", "a}",
            arg_separator=" ",
            tex_environment="align*"
        ).scale(0.5)
        divA2.move_to(divA)
        self.play(*[
                ReplacementTransform(
                    divA.get_part_by_tex(tex),
                    divA2.get_part_by_tex(tex),
                    run_time = 2,
                ) for tex in ("x^2", "+", "=", "c")
            ] + [
                ReplacementTransform(
                    divA.get_part_by_tex("x", substring=False),
                    divA2.get_part_by_tex("x", substring=False),
                    run_time = 2,
                ),
                ReplacementTransform(
                    divA.get_part_by_tex("b"), 
                    divA2.get_part_by_tex("b"),
                    run_time = 2
                ),
                ReplacementTransform(
                    divA.get_part_by_tex("a"),
                    divA2.get_part_by_tex("a"),
                    run_time = 2,
                ),
                Write(
                    divA2.get_parts_by_tex("2", substring=False),
                    runtime = 2,
                ),
                Write(
                    divA2.get_part_by_tex("over"),
                    runtime = 2,
                ),
            ]
        )
        self.wait(1)

        # --- Animation: Split linear rectangle and replace b/a label ---
        # Create two half-rectangles
        linear_half = Line(linear.get_top(), linear.get_bottom(), stroke_width=2)

        # New labels
        linear_label_left = MathTex("\\frac{b}{2a}").scale(0.3)
        linear_label_right = MathTex("\\frac{b}{2a}").scale(0.3)
        linear_label_left.next_to(linear_half, DOWN + LEFT, buff=0.05)
        linear_label_right.next_to(linear_half, DOWN + RIGHT, buff=0.05)

        # Animate: fade out old label, show new rectangles and labels
        self.play(
            FadeOut(linear_label2),
            Write(linear_half),
            Write(linear_label_left),
            Write(linear_label_right),
        )
        self.wait(1)



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
