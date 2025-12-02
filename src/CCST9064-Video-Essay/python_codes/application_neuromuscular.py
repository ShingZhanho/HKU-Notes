from manim import *

# NEUROMUSCULAR DISEASE APPLICATION SCENES

class Scene17_Chapter4Title(Scene):
    def construct(self):
        # Text animation
        chapter = Tex("{\\scshape\\bfseries CHAPTER IV}", font_size=50, color=YELLOW)
        title = Tex("{\\bfseries Spinal Muscular Atrophy}", font_size=64, color=YELLOW)
        separator = Line(start=LEFT * 3, end=RIGHT * 3, color=ORANGE, stroke_width=4)

        chapter.move_to(UP * 0.75)
        title.move_to(DOWN * 0.75)
        separator.move_to(ORIGIN)

        self.play(
            Write(chapter, run_time=1.5),
            Create(separator, run_time=1.5),
            Write(title, run_time=1.5)
        )

        self.wait(3)

class Scene18_BackupSMN2Gene(Scene):
    def construct(self):
        # title
        title = Tex("\\textbf{SMN2 Gene As a Backup}", font_size=48, color=YELLOW)
        title.move_to(UP * 3)
        self.play(Write(title), run_time=1)
        self.wait(1)

        # A segment of SMN2 RNA, represented by two parallel wavy lines (sine waves)
        x_start = -6
        x_end = 6
        amplitude = 0.3
        frequency = 1
        wave_func = lambda x: amplitude * np.sin(frequency * x)
        smn2_rna = VGroup(
            ParametricFunction(
                lambda t: np.array([t, wave_func(t) + 0.3, 0]),
                t_range=[x_start, x_end],
                color=BLUE,
                stroke_width=4
            ),
            ParametricFunction(
                lambda t: np.array([t, wave_func(t) - 0.3, 0]),
                t_range=[x_start, x_end],
                color=BLUE,
                stroke_width=4
            )
        )
        smn2_rna.scale(1.3)

        smn2_label = Tex("\\textbf{SMN2 RNA}", font_size=32, color=BLUE).next_to(smn2_rna, UP, buff=0.5)
        smn2_label.shift(LEFT * 1.7 + DOWN * 1)

        self.add(smn2_rna)
        self.play(Write(smn2_label), run_time=1)
        self.wait(1)

        # An error marker (red exclamation mark, with a circle around) pops on the RNA
        exclamation_mark = Tex("!", font_size=56, color=RED)
        error_circle = Circle(radius=0.3, color=RED, stroke_width=3)
        error_marker = VGroup(error_circle, exclamation_mark).move_to(smn2_rna.get_center() + RIGHT * 2 + UP * 0.35)
        error_flash = Flash(error_marker.get_center(), color=YELLOW, flash_radius=0.4, line_stroke_width=6)

        self.play(Create(error_marker), error_flash, run_time=1)
        self.wait(1)

        # two dashed lines to indicate splicing
        splice_line1 = DashedLine(
            start=smn2_rna[0].point_from_proportion(0.5),
            end=smn2_rna[1].point_from_proportion(0.5),
            color=WHITE,
            stroke_width=4,
            dash_length=0.06,
            buff=0
        )
        splice_line2 = DashedLine(
            start=smn2_rna[0].point_from_proportion(0.8),
            end=smn2_rna[1].point_from_proportion(0.8),
            color=WHITE,
            stroke_width=4,
            dash_length=0.06,
            buff=0
        )
        exon7_text = Tex("\\textbf{Exon 7} \\\\excluded", font_size=28, color=RED).next_to(splice_line2, RIGHT, buff=0.3)
        exon7_text.next_to(error_marker, DOWN, buff=0.2)
        self.play(Create(splice_line1), Create(splice_line2), Write(exon7_text), run_time=1)
        self.wait(1)

        # arrow down
        arrow = Arrow(
            start=splice_line1.get_bottom() + DOWN * 0.2,
            end=splice_line1.get_bottom() + DOWN * 1.2,
            color=YELLOW,
            buff=0,
            stroke_width=6
        )

        # 3/4 circle to represent truncated protein
        truncated_protein = Arc(
            radius=0.4,
            start_angle=PI / 4,
            angle=3 * PI / 2,
            color=ORANGE,
            stroke_width=6
        ).move_to(arrow.get_end() + DOWN * 0.5)
        truncated_label = Tex("\\textbf{Truncated SMN Protein}", font_size=28, color=ORANGE).next_to(truncated_protein, DOWN, buff=0.3)

        self.play(
            Create(arrow),
            Write(truncated_label),
            Create(truncated_protein),
            run_time=1
        )
        self.wait(1)

class Scene19_NusinersenTherapy(Scene):
    def construct(self):
        # recreate the ending state of Scene 18
        # title
        title = Tex("\\textbf{SMN2 Gene As a Backup}", font_size=48, color=YELLOW)
        title.move_to(UP * 3)
        self.add(title)

        # SMN2 RNA
        x_start = -6
        x_end = 6
        amplitude = 0.3
        frequency = 1
        wave_func = lambda x: amplitude * np.sin(frequency * x)
        smn2_rna = VGroup(
            ParametricFunction(
                lambda t: np.array([t, wave_func(t) + 0.3, 0]),
                t_range=[x_start, x_end],
                color=BLUE,
                stroke_width=4
            ),
            ParametricFunction(
                lambda t: np.array([t, wave_func(t) - 0.3, 0]),
                t_range=[x_start, x_end],
                color=BLUE,
                stroke_width=4
            )
        )
        smn2_rna.scale(1.3)
        smn2_label = Tex("\\textbf{SMN2 RNA}", font_size=32, color=BLUE).next_to(smn2_rna, UP, buff=0.5)
        smn2_label.shift(LEFT * 1.7 + DOWN * 1)
        self.add(smn2_rna, smn2_label)

        # error marker
        exclamation_mark = Tex("!", font_size=56, color=RED)
        error_circle = Circle(radius=0.3, color=RED, stroke_width=3)
        error_marker = VGroup(error_circle, exclamation_mark).move_to(smn2_rna.get_center() + RIGHT * 2 + UP * 0.35)
        self.add(error_marker)

        # splice lines
        splice_line1 = DashedLine(
            start=smn2_rna[0].point_from_proportion(0.5),
            end=smn2_rna[1].point_from_proportion(0.5),
            color=WHITE,
            stroke_width=4,
            dash_length=0.06,
            buff=0
        )
        splice_line2 = DashedLine(
            start=smn2_rna[0].point_from_proportion(0.8),
            end=smn2_rna[1].point_from_proportion(0.8),
            color=WHITE,
            stroke_width=4,
            dash_length=0.06,
            buff=0
        )
        exon7_text = Tex("\\textbf{Exon 7} \\\\excluded", font_size=28, color=RED).next_to(splice_line2, RIGHT, buff=0.3)
        exon7_text.next_to(error_marker, DOWN, buff=0.2)
        self.add(splice_line1, splice_line2, exon7_text)

        # arrow
        arrow = Arrow(
            start=splice_line1.get_bottom() + DOWN * 0.2,
            end=splice_line1.get_bottom() + DOWN * 1.2,
            color=YELLOW,
            buff=0,
            stroke_width=6
        )
        self.add(arrow)

        # truncated protein
        truncated_protein = Arc(
            radius=0.4,
            start_angle=PI / 4,
            angle=3 * PI / 2,
            color=ORANGE,
            stroke_width=6
        ).move_to(arrow.get_end() + DOWN * 0.5)
        truncated_label = Tex("\\textbf{Truncated SMN Protein}", font_size=28, color=ORANGE).next_to(truncated_protein, DOWN, buff=0.3)
        self.add(truncated_protein, truncated_label)

        self.wait(1)

        #### NEW SCENE

        new_title = Tex("\\textbf{Nusinersen Therapy}", font_size=48, color=YELLOW)
        new_title.move_to(UP * 3)
        self.play(
            Transform(title, new_title),
            FadeOut(exon7_text),
            FadeOut(splice_line1), FadeOut(splice_line2),
            run_time=1
        )

        # Proofreader (a purple oval)
        proofreader = Ellipse(width=1.8, height=1.3, color=PURPLE, fill_color=PURPLE, fill_opacity=0.5, stroke_width=3)
        proofreader_label = Tex("\\textbf{Nusinersen}", font_size=32, color=WHITE)
        proofreader_label.move_to(proofreader.get_center())
        proofreader_group = VGroup(proofreader, proofreader_label)
        # move out of screen on the right
        proofreader_group.move_to(error_marker.get_center() + RIGHT * 8 + UP * 0.5)

        # animate proofreader moving to the error site
        self.play(
            proofreader_group.animate.move_to(error_marker.get_center() + UP * 0.5),
            run_time=1
        )
        # animate proofreader fixing the error
        self.play(
            FadeOut(error_marker),
            Flash(error_marker.get_center(), color=GREEN, flash_radius=0.4, line_stroke_width=6),
            run_time=1
        )
        self.wait(1)

        # fixed protein
        fixed_protein = Circle(radius=0.4, color=GREEN, stroke_width=6)
        fixed_label = Tex("\\textbf{Full-length SMN Protein}", font_size=28, color=GREEN)
        fixed_protein.move_to(truncated_protein.get_center())
        fixed_label.move_to(truncated_label.get_center())

        # animate splicing and protein change
        self.play(
            Transform(truncated_protein, fixed_protein),
            Transform(truncated_label, fixed_label),
            run_time=1
        )

        self.wait(2)