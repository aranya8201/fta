from manimlib.imports import *
import mpmath

class Grid(VMobject):
    CONFIG = {
        "height": 10.0,
        "width": 10.0,
    }

    def __init__(self, rows, columns, **kwargs):
        digest_config(self, kwargs, locals())
        VMobject.__init__(self, **kwargs)

    def generate_points(self):
        x_step = self.width / self.columns
        y_step = self.height / self.rows

        for x in np.arange(0, self.width + x_step, x_step):
            self.add(Line(
                [x - self.width / 2., -self.height / 2., 0],
                [x - self.width / 2., self.height / 2., 0],
            ))
        for y in np.arange(0, self.height + y_step, y_step):
            self.add(Line(
                [-self.width / 2., y - self.height / 2., 0],
                [self.width / 2., y - self.height / 2., 0]
            ))


class ScreenGrid(VGroup):
    CONFIG = {
        "rows": 10,
        "columns": 10,
        "height": 6,
        "width": 6,
        "grid_stroke": 0.5,
        "grid_color": BLUE,
        "axis_color": BLUE,
        "axis_stroke": 2,
        "show_points": False,
        "point_radius": 0,
        "labels_scale": 0.5,
        "labels_buff": 0,
        "number_decimals": 2
    }

    def __init__(self, **kwargs):
        VGroup.__init__(self, **kwargs)
        rows = self.rows
        columns = self.columns
        grilla = Grid(width=self.width, height=self.height, rows=rows, columns=columns)
        grilla.set_stroke(self.grid_color, self.grid_stroke)

        vector_ii = ORIGIN + np.array((- self.width / 2, - self.height / 2, 0))
        vector_si = ORIGIN + np.array((- self.width / 2, self.height / 2, 0))
        vector_sd = ORIGIN + np.array((self.width / 2, self.height / 2, 0))

        ejes_x = Line(LEFT * self.width / 2, RIGHT * self.width / 2)
        ejes_y = Line(DOWN * self.height / 2, UP * self.height / 2)

        ejes = VGroup(ejes_x, ejes_y).set_stroke(self.axis_color, self.axis_stroke)

        divisiones_x = self.width / columns
        divisiones_y = self.height / rows

        direcciones_buff_x = [UP, DOWN]
        direcciones_buff_y = [RIGHT, LEFT]
        dd_buff = [direcciones_buff_x, direcciones_buff_y]
        vectores_inicio_x = [vector_ii, vector_si]
        vectores_inicio_y = [vector_si, vector_sd]
        vectores_inicio = [vectores_inicio_x, vectores_inicio_y]
        divisiones = [divisiones_x, divisiones_y]
        orientaciones = [RIGHT, DOWN]
        puntos = VGroup()
        leyendas = VGroup()
        set_changes = zip([columns, rows], divisiones, orientaciones, [0, 1], vectores_inicio, dd_buff)


        self.add(grilla, ejes, leyendas)
        if self.show_points:
            self.add(puntos)

class ComplexPlane(Scene):
    def construct(self):
        title = TextMobject("The Complex Plane").scale(0.8)
        title.to_edge(UP)
        self.play(Write(title))

        grid = ScreenGrid()

        self.play(ShowCreation(grid), run_time = 5)

        for j in range(-5,6,1):
            real = TextMobject(str(j)).scale(0.5)
            if j < 0:
                real.move_to(0.6*RIGHT*j+DOWN*0.2)
            elif j == 0:
                real.move_to(0.1*RIGHT+DOWN*0.2)
            else:
                real.move_to(0.6*RIGHT*j+DOWN*0.2)
            self.play(Write(real), run_time=0.1)

            start = np.array([0.6*j,0.05,0])
            end = np.array([0.6*j,-0.05,0])
            line = Line(start,end)

            self.play(Write(line), run_time=0.1)


        for k in range(5,-6,-1):
            if k == 0:
                pass
            elif k == 1:
                imaginary = TextMobject("i").scale(0.5)
            elif k == -1:
                imaginary = TextMobject("-i").scale(0.5)
            else:
                imaginary = TextMobject(str(k)+"i").scale(0.5)
            if k!= 0:
                imaginary.move_to(RIGHT*0.2+UP*k*0.6)

            start = np.array([-0.05,0.6*k,0])
            end = np.array([0.05,0.6*k,0])
            line = Line(start,end)

            self.play(Write(line), run_time=0.1)

            self.play(Write(imaginary),run_time = 0.1)

        z0 = Dot()
        self.play(DrawBorderThenFill(z0))

        self.wait(2)

        vector = np.array([0.3,0.3,0])
        pi_symbol = TexMobject(r"\pi")

        z1 = Dot(color=RED)
        z1.move_to(0.6*RIGHT)
        z1Text = TextMobject("(1+0i)", color=RED).scale(0.6)
        z1Text.move_to(z1.get_center()+vector)


        self.wait()
        self.play(ReplacementTransform(z0.copy(),z1))
        self.play(Write(z1Text))



        z2 = Dot(color=BLUE)
        z2.move_to(1.8*LEFT+1.2*UP)
        z2Text = TextMobject("(-3+2i)", color = BLUE).scale(0.6)
        z2Text.move_to(z2.get_center()+vector)


        self.wait()
        self.play(ReplacementTransform(z0.copy(),z2))
        self.play(Write(z2Text))

        z3 = Dot(color=GREEN)
        z3.move_to(2.1*RIGHT+1.35*DOWN)
        z3Text = TextMobject("(3.5-2.25i)", color = GREEN).scale(0.6)
        z3Text.move_to(z3.get_center()+vector)

        self.wait()
        self.play(ReplacementTransform(z0.copy(),z3))
        self.play(Write(z3Text))

        z4 = Dot(color=ORANGE)
        z4.move_to(0.6*PI*LEFT+0.6*PI*DOWN)
        z4Text = TexMobject(r"(-\pi -\pi i)", color = ORANGE).scale(0.6)
        z4Text.move_to(z4.get_center()+vector)

        self.wait()
        self.play(ReplacementTransform(z0.copy(),z4))
        self.play(Write(z4Text))

        self.wait(2)

        self.play(FadeOutAndShiftDown(z0), run_time = 0.1)

        self.play(FadeOutAndShiftDown(z1), run_time = 0.1)
        self.play(FadeOutAndShiftDown(z1Text), run_time = 0.1)

        self.play(FadeOutAndShiftDown(z2), run_time = 0.1)
        self.play(FadeOutAndShiftDown(z2Text), run_time = 0.1)

        self.play(FadeOutAndShiftDown(z3), run_time = 0.1)
        self.play(FadeOutAndShiftDown(z3Text), run_time = 0.1)

        self.play(FadeOutAndShiftDown(z4), run_time = 0.1)
        self.play(FadeOutAndShiftDown(z4Text), run_time = 0.1)

        self.play(FadeOutAndShiftDown(title), run_time=0.1)

class SetupProof(Scene):
    def construct(self):
        grid = ScreenGrid()
        input = ScreenGrid(height = 5, width = 5)
        output = ScreenGrid(height = 5, width = 5, grid_color = RED, axis_color = RED)
        inputTitle = TexMobject("Input (z)", color = BLUE)
        outputTitle = TexMobject(r"Output f\left(z\right) ", color = RED)
        self.add(grid)

        self.wait()
        input.move_to(LEFT*3.5 + UP*0.5)
        output.move_to(RIGHT*3.5 + UP*0.5)
        inputTitle.next_to(input, UP, buff = 0.2)
        outputTitle.next_to(output, UP, buff = 0.2)

        self.play(ReplacementTransform(grid, input))
        self.play(Write(inputTitle))
        self.play(ReplacementTransform(grid, output))
        self.play(Write(outputTitle))

        label0 = TextMobject("$-100$", color = BLUE).scale(0.4)
        label1 = TextMobject("$100$", color = BLUE).scale(0.4)
        label2 = TextMobject("$100i$", color = BLUE).scale(0.4)
        label3 = TextMobject("$-100i$", color = BLUE).scale(0.4)
        label4 = TextMobject("$-{100}^{n}$", color = RED).scale(0.4)
        label5 = TextMobject("${100}^{n}$", color = RED).scale(0.4)
        label6 = TextMobject("$i{100}^{n}$", color = RED).scale(0.4)
        label7 = TextMobject("$-i{100}^{n}$", color = RED).scale(0.4)

        label0.move_to(input.get_center()+2.5*LEFT+0.15*DOWN)
        label1.move_to(input.get_center()+2.5*RIGHT+0.15*DOWN)
        label2.move_to(input.get_center()+2.5*UP+0.3*RIGHT)
        label3.move_to(input.get_center()+2.5*DOWN+0.3*RIGHT)
        label4.move_to(output.get_center()+2.5*LEFT+0.15*DOWN)
        label5.move_to(output.get_center()+2.5*RIGHT+0.15*DOWN)
        label6.move_to(output.get_center()+2.5*UP+0.3*RIGHT)
        label7.move_to(output.get_center()+2.5*DOWN+0.3*RIGHT)

        self.play(Write(label0), run_time = 0.1)
        self.play(Write(label1), run_time = 0.1)
        self.play(Write(label2), run_time = 0.1)
        self.play(Write(label3), run_time = 0.1)
        self.play(Write(label4), run_time = 0.1)
        self.play(Write(label5), run_time = 0.1)
        self.play(Write(label6), run_time = 0.1)
        self.play(Write(label7), run_time = 0.1)

        formula = TexMobject(r"f\left( z \right) =", "{c}_{n}", "z^n", "+", "{c}_{n-1}", "{z}^{n-1}","+...+", "{c}_{1}", "z", "+", "{c}_{0}", color=RED).scale(0.8)
        formulaWhenZeroStageOne = TexMobject(
        r"f\left( 0 \right) =",
        "{c}_{n}",
        r"{\left(0 \right)}^{n}",
        "+",
        "{c}_{n-1}",
        r"{\left(0 \right)}^{n-1}",
        "+...+",
        "{c}_{1}",
        r"\left(0 \right)",
        "+",
        "{c}_{0}",
        color=RED).scale(0.8)
        formulaWhenZeroStageTwo = TexMobject(r"f\left(0 \right) = {c}_{0}", color = RED).scale(0.8)
        formulaWhenBigStageOne = TexMobject(
        r"f\left( 100 \right) =",
        "{c}_{n}",
        r"\left(100 \right)^n", "+",
        "{c}_{n-1}",
        r"{\left(100 \right)}^{n-1}",
        "+...+",
        "{c}_{1}",
        r"\left(100 \right)",
        "+",
        "{c}_{0}",
        color=RED).scale(0.8)
        formulaWhenBigStageTwo = TexMobject(r"f\left(100\right) \approx {c}_{n}{\left(100\right)^n", color = RED).scale(0.8)
        descriptionFirst = TextMobject("When $z=0$", color = BLUE)
        descriptionSecond = TextMobject("When $|z|$ is very big, first term dominates", color = BLUE)
        inputOne = Dot(color = BLUE)
        inputName = TexMobject("z", color = BLUE).scale(0.5)
        outputOne = Dot(color = RED)
        outputName = TexMobject(r"f\left(z\right)", color = RED).scale(0.5)
        inputTwo = Circle(color = BLUE, radius = 2.5)
        outputTwo = Circle(color = RED, radius = 2.3)

        descriptionFirst.to_edge(DOWN, buff = 1)
        descriptionSecond.to_edge(DOWN, buff = 1)
        formula.to_edge(DOWN, buff = 0.4)
        formulaWhenZeroStageOne.to_edge(DOWN,buff=0.4)
        formulaWhenZeroStageTwo.to_edge(DOWN,buff=0.4)
        inputOne.move_to(input.get_center())
        inputName.move_to(inputOne.get_center()+0.2*RIGHT+0.2*UP)
        outputOne.move_to(output.get_center()+RIGHT*0.2+DOWN*0.2)
        outputName.move_to(outputOne.get_center()+0.2*RIGHT+0.2*UP)
        formulaWhenBigStageOne.to_edge(DOWN,buff=0.4)
        formulaWhenBigStageTwo.to_edge(DOWN,buff=0.4)
        inputTwo.move_to(input.get_center())
        outputTwo.move_to(output.get_center()+0.2*RIGHT+0.2*DOWN)

        self.wait()
        self.play(Write(formula), run_time = 5)
        self.wait(2)
        self.play(Write(descriptionFirst))
        self.play(DrawBorderThenFill(inputOne))
        self.play(Write(inputName))
        self.wait(2)
        self.play(Transform(formula, formulaWhenZeroStageOne))
        self.wait(2)
        self.play(Transform(formula, formulaWhenZeroStageTwo))
        self.wait(2)
        self.play(ReplacementTransform(inputOne.copy(),outputOne))
        self.play(Write(outputName))
        self.wait(2)
        self.play(FadeOutAndShiftDown(inputOne), run_time = 0.1)
        self.play(FadeOutAndShiftDown(inputName), run_time = 0.1)
        self.play(FadeOutAndShiftDown(outputOne), run_time = 0.1)
        self.play(FadeOutAndShiftDown(outputName), run_time = 0.1)
        self.wait()

        inputName.next_to(inputTwo, RIGHT)
        outputName.next_to(outputTwo, RIGHT)

        self.play(Transform(descriptionFirst, descriptionSecond))
        self.wait()
        self.play(ShowCreation(inputTwo))
        self.play(ShowCreation(inputName))
        self.wait(2)
        self.play(Transform(formula, formulaWhenBigStageOne))
        self.wait(2)
        self.play(Transform(formula, formulaWhenBigStageTwo))
        self.wait(2)
        self.play(ReplacementTransform(inputTwo.copy(), outputTwo))
        self.play(ShowCreation(outputName))
        self.wait()

class FinalProof(Scene):
    def construct(self):
        input = ScreenGrid(height = 5, width = 5)
        output = ScreenGrid(height = 5, width = 5, grid_color = RED, axis_color = RED)
        inputTitle = TexMobject("Input (z)", color = BLUE)
        outputTitle = TexMobject(r"Output f\left(z\right) ", color = RED)

        input.move_to(LEFT*3.5 + UP*0.5)
        output.move_to(RIGHT*3.5 + UP*0.5)
        inputTitle.next_to(input, UP, buff = 0.2)
        outputTitle.next_to(output, UP, buff = 0.2)

        label0 = TextMobject("$-100$", color = BLUE).scale(0.4)
        label1 = TextMobject("$100$", color = BLUE).scale(0.4)
        label2 = TextMobject("$100i$", color = BLUE).scale(0.4)
        label3 = TextMobject("$-100i$", color = BLUE).scale(0.4)
        label4 = TextMobject("$-{100}^{n}$", color = RED).scale(0.4)
        label5 = TextMobject("${100}^{n}$", color = RED).scale(0.4)
        label6 = TextMobject("$i{100}^{n}$", color = RED).scale(0.4)
        label7 = TextMobject("$-i{100}^{n}$", color = RED).scale(0.4)

        label0.move_to(input.get_center()+2.5*LEFT+0.15*DOWN)
        label1.move_to(input.get_center()+2.5*RIGHT+0.15*DOWN)
        label2.move_to(input.get_center()+2.5*UP+0.3*RIGHT)
        label3.move_to(input.get_center()+2.5*DOWN+0.3*RIGHT)
        label4.move_to(output.get_center()+2.5*LEFT+0.15*DOWN)
        label5.move_to(output.get_center()+2.5*RIGHT+0.15*DOWN)
        label6.move_to(output.get_center()+2.5*UP+0.3*RIGHT)
        label7.move_to(output.get_center()+2.5*DOWN+0.3*RIGHT)

        self.add(input, output, inputTitle, outputTitle)
        self.add(label0,label1,label2,label3,label4,label5,label6,label7)

        inputCentre = Dot(color = BLUE)
        outputCentre = Dot(color = RED)
        inputCircle = Circle(color = BLUE, radius = 2.5)
        outputCircle = Circle(color = RED, radius = 2.3)

        inputCentre.move_to(input.get_center())
        outputCentre.move_to(output.get_center()+0.2*RIGHT+0.2*DOWN)
        inputCircle.move_to(input.get_center())
        outputCircle.move_to(output.get_center()+0.2*RIGHT+0.2*DOWN)

        self.play(ShowCreation(inputCentre), (ShowCreation(inputCircle)))
        self.wait()
        self.play(ReplacementTransform(inputCentre.copy(), outputCentre), ReplacementTransform(inputCircle.copy(), outputCircle))
        self.wait(2)


        r = 2.5
        while r >= 0.1:
            r -= 0.01
            newInputCircle = Circle(radius = r, color = BLUE)
            newInputCircle.move_to(input.get_center())

            newOutputCircle = Circle(radius = r-0.2, color = RED)
            newOutputCircle.move_to(outputCircle.get_center())

            self.play(Transform(inputCircle,newInputCircle), Transform(outputCircle, newOutputCircle), run_time = 0.01)

            if r < 0.50 and r > 0.49:
                markerOut = Dot(color = GOLD)
                markerOut.move_to(output.get_center())
                self.add(markerOut)
                self.play(Indicate(inputCircle), Flash(markerOut))
                self.wait()
                break

        markerIn = Dot(color = GOLD)
        markerIn.move_to(inputCircle.get_end())
        self.wait()
        self.play(ShowCreation(markerIn))
        self.play(Flash(markerIn))
        self.wait()

        text = TextMobject("If the largest power is $n$, there are $n$ solutions")
        formula = TextMobject(r"e.g. if largest power is 7, $f\left(z\right)={z}^{7} + 4z^5-(3+i)z^2+2z-4$")

        text.to_edge(DOWN, buff = 1)
        formula.to_edge(DOWN, buff = 0.4)

        self.play(Write(text), run_time = 3)
        self.play(Write(formula), run_time = 5)

        for start in range(7):
            arcInput = Arc(arc_center = input.get_center(), radius = 0.5, start_angle = start*TAU/7, angle = TAU/7)
            arcOutput = Arc(arc_center = 3.5*RIGHT + 0.5*UP + 0.2*RIGHT + 0.2*DOWN, radius = 0.3, start_angle = 135*DEGREES, angle = TAU)
            self.play(MoveAlongPath(markerIn, arcInput), MoveAlongPath(markerOut, arcOutput))
            self.play(Flash(markerOut, run_time = 0.2, num_lines = 6))

        self.wait()


        """
        oh my

        scale = 0.001
        for z in range(360):
            inputValues = [mpmath.mpc(str(scale*mpmath.cos(x*PI/180)),str(scale*mpmath.sin(x*PI/180))) for x in range(360)]
            outputValues = [z**4-2*z**3-11*z**2+42*z-40 for z in inputValues]

            inputDot = SmallDot(radius = 0.01, color = BLUE)
            outputDot = SmallDot(radius = 0.01, color = RED)

            inputMovementVector = np.array([0.025*float(inputValues[z].real),0.025*float(inputValues[z].imag),0])
            outputMovementVector = np.array([0.025*((1/scale)**3)*float(outputValues[z].real), 0.025*((1/scale)**3)*float(outputValues[z].imag),0])

            inputDot.move_to(input.get_center() + inputMovementVector)
            outputDot.move_to(output.get_center() + outputMovementVector)

            self.add(inputDot)
            self.add(outputDot)
        """
