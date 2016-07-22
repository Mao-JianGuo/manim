from mobject.tex_mobject import TexMobject
from mobject import Mobject
from mobject.image_mobject import ImageMobject
from mobject.vectorized_mobject import VMobject

from animation.animation import Animation
from animation.transform import *
from animation.simple_animations import *
from topics.geometry import *
from topics.characters import *
from topics.functions import *
from topics.number_line import *
from topics.numerals import *
from scene import Scene
from camera import Camera
from mobject.svg_mobject import *
from mobject.tex_mobject import *
from mobject.vectorized_mobject import *

from eola.matrix import *
from eola.two_d_space import *

class OpeningQuote(Scene):
    def construct(self):
        words = TextMobject([
            "Unfortunately, no one can be told what the",
            "Matrix",
            "is. You have to",
            "see it for yourself.",
        ])
        words.scale_to_fit_width(2*SPACE_WIDTH - 2)
        words.to_edge(UP)
        words.split()[1].highlight(GREEN)
        words.split()[3].highlight(GREEN)
        author = TextMobject("-Morpheus")
        author.highlight(YELLOW)
        author.next_to(words, DOWN, buff = 0.5)
        comment = TextMobject("""
            (Surprisingly apt words on the importance 
            of understanding matrix operations visually.)
        """)
        comment.scale(0.7)
        comment.next_to(author, DOWN, buff = 1)

        self.play(FadeIn(words))
        self.dither(3)
        self.play(Write(author, run_time = 3))
        self.dither()
        self.play(Write(comment))
        self.dither()


class Introduction(TeacherStudentsScene):
    def construct(self):
        title = TextMobject("Matrices as linear transformations")
        title.to_edge(UP)
        title.highlight(YELLOW)
        self.add(title)
        self.setup()
        self.teacher_says("""
            Listen up folks, this one is
            particularly important
        """, height = 3)
        self.random_blink(2)
        self.teacher_says("We'll start by just watching", height = 3)
        self.random_blink()
        self.teacher_thinks(VMobject())
        everything = VMobject(*self.get_mobjects())
        def spread_out(p):
            p = p + 3*DOWN
            return (SPACE_WIDTH+SPACE_HEIGHT)*p/np.linalg.norm(p)
        self.play(ApplyPointwiseFunction(spread_out, everything))


class ShowGridCreation(Scene):
    def construct(self):
        plane = NumberPlane()
        coords = VMobject(*plane.get_coordinate_labels())
        self.play(ShowCreation(plane, run_time = 3))
        self.play(Write(coords, run_time = 3))
        self.dither()

class IntroduceLinearTransformations(LinearTransformationScene):
    CONFIG = {
        "show_basis_vectors" : False,
        "include_background_plane" : False
    }
    def construct(self):
        self.setup()
        self.dither()
        self.apply_transposed_matrix([[2, 1], [1, 2]])
        self.dither()

        lines_rule = TextMobject("Lines remain lines")
        lines_rule.shift(2*UP).to_edge(LEFT)
        origin_rule = TextMobject("Origin remains fixed")
        origin_rule.shift(2*UP).to_edge(RIGHT)
        arrow = Arrow(origin_rule, ORIGIN)
        dot = Dot(ORIGIN, radius = 0.1, color = RED)

        for rule in lines_rule, origin_rule:
            rule.add_background_rectangle()

        self.play(
            # FadeIn(lines_rule_rect),            
            Write(lines_rule, run_time = 2),
        )
        self.dither()
        self.play(
            # FadeIn(origin_rule_rect),            
            Write(origin_rule, run_time = 2),
            ShowCreation(arrow),
            GrowFromCenter(dot)
        )
        self.dither()


class SimpleLinearTransformationScene(LinearTransformationScene):
    CONFIG = {
        "show_basis_vectors" : False,
        "transposed_matrix" : [[2, 1], [1, 2]]
    }
    def construct(self):
        self.setup()
        self.dither()
        self.apply_transposed_matrix(self.transposed_matrix)
        self.dither()

class SimpleNonlinearTransformationScene(LinearTransformationScene):
    CONFIG = {
        "show_basis_vectors" : False,
        "words" : "Not linear: some lines get curved"
    }
    def construct(self):
        self.setup()
        self.dither()
        self.apply_nonlinear_transformation(self.func)
        words = TextMobject(self.words)
        words.to_corner(UP+RIGHT)
        words.highlight(RED)
        words.add_background_rectangle()
        self.play(Write(words))
        self.dither()

    def func(self, point):
        x, y, z = point
        return (x+np.cos(y))*RIGHT + (y+np.sin(x))*UP

class MovingOrigin(SimpleNonlinearTransformationScene):
    CONFIG = {
        "words" : "Not linear: Origin moves"
    }
    def setup(self):
        LinearTransformationScene.setup(self)
        dot = Dot(ORIGIN, color = RED)
        self.add_transformable_mobject(dot)

    def func(self, point):
        matrix_transform = self.get_matrix_transformation([[2, 0], [1, 1]])
        return matrix_transform(point) + 2*UP+3*LEFT

class SneakyNonlinearTransformation(SimpleNonlinearTransformationScene):
    CONFIG = {
        "words" : "\\dots"
    }
    def func(self, point):
        x, y, z = point
        new_x = np.sign(x)*SPACE_WIDTH*smooth(abs(x) / SPACE_WIDTH)
        new_y = np.sign(y)*SPACE_HEIGHT*smooth(abs(y) / SPACE_HEIGHT)
        return [new_x, new_y, 0]

class SneakyNonlinearTransformationExplained(SneakyNonlinearTransformation):
    CONFIG = {
        "words" : "Not linear: diagonal lines get curved"
    }
    def setup(self):
        LinearTransformationScene.setup(self)
        diag = Line(
            SPACE_HEIGHT*LEFT+SPACE_HEIGHT*DOWN,
            SPACE_HEIGHT*RIGHT + SPACE_HEIGHT*UP
        )
        diag.insert_n_anchor_points(20)
        diag.change_anchor_mode("smooth")
        diag.highlight(YELLOW)
        self.play(ShowCreation(diag))
        self.add_transformable_mobject(diag)


class AnotherLinearTransformation(SimpleLinearTransformationScene):
    CONFIG = {
        "transposed_matrix" : [
            [3, 0],
            [1, 2]
        ]
    }
    def construct(self):
        SimpleLinearTransformationScene.construct(self)
        text = TextMobject([
            "Grid lines remain",
            "parallel",
            "and",
            "evenly spaced",
        ])
        glr, p, a, es = text.split()
        p.highlight(YELLOW)
        es.highlight(GREEN)
        text.add_background_rectangle()
        text.shift(-text.get_bottom())
        self.play(Write(text))
        self.dither()


class Rotation(SimpleLinearTransformationScene):
    CONFIG = {
        "angle" : np.pi/3,
    }
    def construct(self):
        self.transposed_matrix = [
            [np.cos(self.angle), np.sin(self.angle)], 
            [-np.sin(self.angle), np.cos(self.angle)]
        ]
        SimpleLinearTransformationScene.construct(self)



class YetAnotherLinearTransformation(SimpleLinearTransformationScene):
    CONFIG = {
        "transposed_matrix" : [
            [-1, 1],
            [3, 2],
        ]
    }


class MoveAroundAllVectors(LinearTransformationScene):
    CONFIG = {
        "show_basis_vectors" : False,
        "focus_on_one_vector" : False,
    }
    def construct(self):
        self.setup()
        vectors = VMobject(*[
            Vector([x, y])
            for x in np.arange(-int(SPACE_WIDTH)+0.5, int(SPACE_WIDTH)+0.5)
            for y in np.arange(-int(SPACE_HEIGHT)+0.5, int(SPACE_HEIGHT)+0.5)
        ])
        vectors.submobject_gradient_highlight(PINK, BLUE_E)        
        dots = VMobject(*[
            Dot(v.get_end(), color = v.get_color())
            for v in vectors.split()
        ])

        self.dither()
        self.play(ShowCreation(dots))
        self.dither()
        self.play(Transform(dots, vectors))
        self.dither()
        self.remove(dots)
        if self.focus_on_one_vector:
            vector = vectors.split()[43]#yeah, great coding Grant
            self.remove(vectors)
            self.add_vector(vector)
            self.play(*[
                FadeOut(v) 
                for v in vectors.split()
                if v is not vector
            ])
            self.dither()
            self.add(vector.copy().highlight(DARK_GREY))
        else:
            for vector in vectors.split():
                self.add_vector(vector)
        self.apply_transposed_matrix([[3, 0], [1, 2]])
        self.dither()


class MoveAroundJustOneVector(MoveAroundAllVectors):
    CONFIG = {
        "focus_on_one_vector" : True,
    }


class RotateIHat(LinearTransformationScene):
    CONFIG = {
        "show_basis_vectors" : False
    }
    def construct(self):
        self.setup()
        i_hat, j_hat = self.get_basis_vectors()
        i_label, j_label = self.get_basis_vector_labels()
        self.add_vector(i_hat)
        self.play(Write(i_label, run_time = 1))
        self.dither()
        self.play(FadeOut(i_label))
        self.apply_transposed_matrix([[0, 1], [-1, 0]])
        self.dither()
        self.play(Write(j_label, run_time = 1))
        self.dither()



class TransformationsAreFunctions(Scene):
    def construct(self):
        title = TextMobject([
            """Linear transformations are a
            special kind of""",
            "function"
        ])
        title_start, function = title.split()
        function.highlight(YELLOW)
        title.to_edge(UP)

        equation = TexMobject([
            "L",
            "(",
            "\\vec{\\textbf{v}}",
            ") = ",
            "\\vec{\\textbf{w}}",
        ])
        L, lp, _input, equals, _output = equation.split()
        L.highlight(YELLOW)
        _input.highlight(MAROON_C)
        _output.highlight(BLUE)
        equation.scale(2)
        equation.next_to(title, DOWN, buff = 1)

        starting_vector = TextMobject("Starting vector")
        starting_vector.shift(DOWN+3*LEFT)
        starting_vector.highlight(MAROON_C)
        ending_vector = TextMobject("The vector where it lands")
        ending_vector.shift(DOWN).to_edge(RIGHT)
        ending_vector.highlight(BLUE)

        func_arrow = Arrow(function.get_bottom(), L.get_top(), color = YELLOW)
        start_arrow = Arrow(starting_vector.get_top(), _input.get_bottom(), color = MAROON_C)
        ending_arrow = Arrow(ending_vector, _output, color = BLUE)


        self.add(title)
        self.play(
            Write(equation),
            ShowCreation(func_arrow)
        )
        for v, a in [(starting_vector, start_arrow), (ending_vector, ending_arrow)]:
            self.play(Write(v), ShowCreation(a), run_time = 1)
        self.dither()


class UsedToThinkinfOfFunctionsAsGraphs(VectorScene):
    def construct(self):
        self.show_graph()
        self.show_inputs_and_output()

    def show_graph(self):
        axes = self.add_axes()
        graph = FunctionGraph(lambda x : x**2, x_min = -2, x_max = 2)
        name = TexMobject("f(x) = x^2")
        name.next_to(graph, RIGHT).to_edge(UP)
        point = Dot(graph.point_from_proportion(0.8))
        point_label = TexMobject("(x, x^2)")
        point_label.next_to(point, DOWN+RIGHT, buff = 0.1)

        self.play(ShowCreation(graph))
        self.play(Write(name, run_time = 1))
        self.play(
            ShowCreation(point),
            Write(point_label),
            run_time = 1
        )
        self.dither()

        def collapse_func(p):
            return np.dot(p, [RIGHT, RIGHT, OUT]) + (SPACE_HEIGHT+1)*DOWN
        self.play(
            ApplyPointwiseFunction(
                collapse_func, axes, 
                submobject_mode = "all_at_once",
            ),
            ApplyPointwiseFunction(collapse_func, graph),
            ApplyMethod(point.shift, 10*DOWN),
            ApplyMethod(point_label.shift, 10*DOWN),
            ApplyFunction(lambda m : m.center().to_edge(UP), name),
            run_time = 1
        )
        self.clear()
        self.add(name)
        self.dither()

    def show_inputs_and_output(self):
        numbers = range(-3, 4)
        inputs = VMobject(*map(TexMobject, map(str, numbers)))
        inputs.arrange_submobjects(DOWN, buff = 0.5, aligned_edge = RIGHT)
        arrows = VMobject(*[
            Arrow(LEFT, RIGHT).next_to(mob)
            for mob in inputs.split()
        ])
        outputs = VMobject(*[
            TexMobject(str(num**2)).next_to(arrow)
            for num, arrow in zip(numbers, arrows.split())
        ])
        everyone = VMobject(inputs, arrows, outputs)
        everyone.center().to_edge(UP, buff = 1.5)

        self.play(Write(inputs, run_time = 1))
        self.dither()
        self.play(
            Transform(inputs.copy(), outputs),
            ShowCreation(arrows)
        )
        self.dither()




























