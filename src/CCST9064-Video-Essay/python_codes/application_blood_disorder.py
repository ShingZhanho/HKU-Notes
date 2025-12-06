from manim import *

# BLOOD DISORDER APPLICATION SCENES

class Scene9_Chapter2Title(Scene):
    """Chapter 2 Title: Gene Therapy for Blood Disorders"""
    def construct(self):
        # Text animation
        chapter = Tex("{\\scshape\\bfseries CHAPTER II}", font_size=50, color=YELLOW)
        title = Tex("{\\bfseries Blood Disorders}", font_size=64, color=YELLOW)
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

class Scene10_SickleCellDiseaseTitle(Scene):
    """Sickle Cell Disease Title Scene"""
    def construct(self):
        # Text animation
        title = Tex("{\\bfseries Sickle Cell Disease}", font_size=72, color=YELLOW)

        self.play(Write(title, run_time=1))

        self.wait(3)

class Scene11_CRISPRTreatment(Scene):
    """CRISPR-Cas9 Treatment for Sickle Cell Disease"""
    def construct(self):
        # Part 1: Show BCL11A gene suppressing fetal hemoglobin
        bcl11a_gene = Rectangle(width=2, height=0.8, color=RED, fill_color=RED, fill_opacity=0.3)
        bcl11a_label = Tex("\\textbf{BCL11A\\\\gene}", font_size=24, color=RED)
        bcl11a_label.next_to(bcl11a_gene, UP, buff=0.3)
        
        bcl11a_group = VGroup(bcl11a_gene, bcl11a_label)
        bcl11a_group.move_to(UP * 2 + LEFT * 3)
        
        # Fetal hemoglobin (suppressed, shown as small gray circles)
        fetal_hb_suppressed = VGroup(*[
            Circle(radius=0.15, color=GRAY, fill_color=GRAY, fill_opacity=0.4)
            for _ in range(3)
        ]).arrange(RIGHT, buff=0.3)
        fetal_hb_suppressed.move_to(DOWN * 1 + LEFT * 3)
        
        fetal_label = Tex("\\textbf{Fetal Hb\\\\(suppressed)}", font_size=20, color=GRAY)
        fetal_label.next_to(fetal_hb_suppressed, DOWN, buff=0.3)
        
        # Suppression arrow
        suppression_arrow = Arrow(
            start=bcl11a_gene.get_bottom(),
            end=fetal_hb_suppressed.get_top(),
            color=RED,
            stroke_width=6
        )
        
        self.play(
            Create(bcl11a_group),
            Create(suppression_arrow),
            Create(fetal_hb_suppressed),
            Write(fetal_label),
            run_time=1.5
        )
        self.wait(1)
        
        # Part 2: Show CRISPR-Cas9 coming in to edit BCL11A
        crispr_cas9 = VGroup(
            Rectangle(width=1.5, height=0.6, color=BLUE, fill_color=BLUE, fill_opacity=0.5),
            Tex("\\textbf{CRISPR-\\\\Cas9}", font_size=20, color=BLUE)
        )
        crispr_cas9[1].move_to(crispr_cas9[0].get_center())
        crispr_cas9.move_to(UP * 2 + RIGHT * 2)
        
        self.play(Create(crispr_cas9), run_time=1)
        self.wait(0.5)
        
        # CRISPR moves to BCL11A
        self.play(crispr_cas9.animate.move_to(bcl11a_gene.get_center()), run_time=1.5)
        
        # Flash effect showing gene editing
        flash = Flash(bcl11a_gene.get_center(), color=YELLOW, flash_radius=1)
        self.play(flash)
        
        # BCL11A becomes deactivated (crossed out)
        cross_line1 = Line(
            start=bcl11a_gene.get_corner(UL),
            end=bcl11a_gene.get_corner(DR),
            color=YELLOW,
            stroke_width=6
        )
        cross_line2 = Line(
            start=bcl11a_gene.get_corner(UR),
            end=bcl11a_gene.get_corner(DL),
            color=YELLOW,
            stroke_width=6
        )
        
        deactivated_label = Tex("\\textbf{BCL11A\\\\(deactivated)}", font_size=24, color=GRAY)
        deactivated_label.move_to(bcl11a_label.get_center())
        
        self.play(
            Create(cross_line1),
            Create(cross_line2),
            Transform(bcl11a_label, deactivated_label),
            FadeOut(crispr_cas9),
            suppression_arrow.animate.set_color(GRAY).set_opacity(0.3),
            run_time=1.5
        )
        self.wait(1)
        
        # Part 3: Fetal hemoglobin production resumes
        fetal_hb_active = VGroup(*[
            Circle(radius=0.2, color=GREEN, fill_color=GREEN, fill_opacity=0.7)
            for _ in range(6)
        ]).arrange_in_grid(rows=2, cols=3, buff=0.3)
        fetal_hb_active.move_to(fetal_hb_suppressed.get_center() + DOWN * 0.5)
        
        active_label = Tex("\\textbf{Fetal Hb\\\\(high-level)}", font_size=20, color=GREEN)
        active_label.next_to(fetal_hb_active, DOWN, buff=0.3)
        
        self.play(
            Transform(fetal_hb_suppressed, fetal_hb_active),
            Transform(fetal_label, active_label),
            run_time=1.5
        )
        self.wait(1)
        
        # Part 4: Show effect on red blood cells
        # Fade everything out
        self.play(
            FadeOut(bcl11a_group),
            FadeOut(cross_line1),
            FadeOut(cross_line2),
            FadeOut(suppression_arrow),
            FadeOut(fetal_hb_suppressed),
            FadeOut(fetal_label),
            run_time=1
        )
        
        # 1. Create sickle cells and normal hemoglobin scattered across screen
        # Sickle cells (red crescents)
        sickle_positions = [
            UP * 2.5 + LEFT * 4,
            UP * 1.5 + LEFT * 1,
            UP * 0.5 + LEFT * 5,
            DOWN * 0.5 + LEFT * 2.5,
            DOWN * 1.5 + LEFT * 5.5,
            UP * 2 + RIGHT * 1,
            DOWN * 2 + LEFT * 0.5,
        ]
        
        sickle_cells = VGroup()
        for pos in sickle_positions:
            arc1 = Arc(radius=0.3, angle=PI, color=RED, stroke_width=3, fill_color=RED, fill_opacity=0.4)
            arc2 = Arc(radius=0.25, angle=-PI, color=RED, stroke_width=3, fill_color=RED, fill_opacity=0.4).next_to(arc1, RIGHT, buff=0)
            sickle = VGroup(arc1, arc2).rotate(PI/4)
            sickle.move_to(pos)
            sickle_cells.add(sickle)
        
        # Normal hemoglobin (green circles)
        normal_hb_positions = [
            UP * 3 + LEFT * 2,
            UP * 1 + RIGHT * 4,
            DOWN * 1 + RIGHT * 5,
            DOWN * 2.5 + RIGHT * 2,
            UP * 0.5 + RIGHT * 2,
        ]
        
        normal_hbs = VGroup()
        for pos in normal_hb_positions:
            normal_hb = Circle(radius=0.25, color=GREEN, fill_color=GREEN, fill_opacity=0.5, stroke_width=3)
            normal_hb.move_to(pos)
            normal_hbs.add(normal_hb)
        
        # Legend at bottom left
        legend_box = Rectangle(width=3.5, height=1.8, color=WHITE, stroke_width=2)
        legend_box.move_to(DOWN * 2.7 + LEFT * 4.5)
        
        # Legend items
        sickle_legend_icon = VGroup(
            Arc(radius=0.15, angle=PI, color=RED, stroke_width=2, fill_color=RED, fill_opacity=0.4),
        )
        sickle_legend_icon[0].next_to(sickle_legend_icon[0], RIGHT, buff=0)
        sickle_legend_label = Tex("Sickle Hb", font_size=18, color=RED)
        sickle_legend = VGroup(sickle_legend_icon, sickle_legend_label).arrange(RIGHT, buff=0.3)
        
        normal_legend_icon = Circle(radius=0.15, color=GREEN, fill_color=GREEN, fill_opacity=0.5, stroke_width=2)
        normal_legend_label = Tex("Normal Hb", font_size=18, color=GREEN)
        normal_legend = VGroup(normal_legend_icon, normal_legend_label).arrange(RIGHT, buff=0.3)
        
        fetal_legend_icon = Circle(radius=0.15, color=BLUE, fill_color=BLUE, fill_opacity=0.5, stroke_width=2)
        fetal_legend_label = Tex("Fetal Hb", font_size=18, color=BLUE)
        fetal_legend = VGroup(fetal_legend_icon, fetal_legend_label).arrange(RIGHT, buff=0.3)
        
        legend_items = VGroup(sickle_legend, normal_legend, fetal_legend).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        legend_items.move_to(legend_box.get_center())
        
        legend_group = VGroup(legend_box, legend_items)
        
        # 2. Counter at bottom right showing functional hemoglobin percentage
        counter_box = Rectangle(width=3, height=1.2, color=WHITE, stroke_width=2)
        counter_box.move_to(DOWN * 2.9 + RIGHT * 4.5)
        
        counter_label = Tex("\\textbf{Functional Hb}", font_size=20)
        counter_label.move_to(counter_box.get_center() + UP * 0.3)
        
        initial_percentage = int((len(normal_hbs) / (len(sickle_cells) + len(normal_hbs))) * 100)
        counter_value = Tex(f"\\textbf{{{initial_percentage}\\%}}", font_size=32, color=YELLOW)
        counter_value.move_to(counter_box.get_center() + DOWN * 0.25)
        
        counter_group = VGroup(counter_box, counter_label, counter_value)
        
        # Fade in everything
        self.play(
            Create(sickle_cells),
            Create(normal_hbs),
            Create(legend_group),
            Create(counter_group),
            run_time=1.5
        )
        self.wait(1)
        
        # 3. Fade in fetal hemoglobin (blue circles) and update counter
        fetal_hb_positions = [
            UP * 2.8 + RIGHT * 3.5,
            UP * 0.8 + LEFT * 3.5,
            UP * 1.8 + RIGHT * 5.5,
            DOWN * 0.3 + RIGHT * 0.5,
            DOWN * 1.8 + RIGHT * 4.5,
            DOWN * 2.5 + LEFT * 3,
            UP * 3.2 + LEFT * 0.5,
            DOWN * 0.8 + LEFT * 4.5,
        ]
        
        fetal_hbs = VGroup()
        for pos in fetal_hb_positions:
            fetal_hb = Circle(radius=0.25, color=BLUE, fill_color=BLUE, fill_opacity=0.5, stroke_width=3)
            fetal_hb.move_to(pos)
            fetal_hbs.add(fetal_hb)
        
        # Calculate new percentage
        new_percentage = int((len(normal_hbs) + len(fetal_hbs)) / (len(sickle_cells) + len(normal_hbs) + len(fetal_hbs)) * 100)
        new_counter_value = Tex(f"\\textbf{{{new_percentage}\\%}}", font_size=32, color=GREEN)
        new_counter_value.move_to(counter_value.get_center())
        
        self.play(
            FadeIn(fetal_hbs, lag_ratio=0.1),
            Transform(counter_value, new_counter_value),
            run_time=2
        )
        self.wait(1.5)
        
        # Final message
        cure_text = Tex("\\textbf{Malfunctioned Haemoglobin Diluted}", font_size=40, color=WHITE)
        cure_text_box = Rectangle(width=8, height=1, color=GREEN, stroke_width=3, fill_color=GREEN, fill_opacity=0.3)
        cure_text.move_to(ORIGIN)
        
        self.play(Create(cure_text_box), Write(cure_text), run_time=1)
        self.wait(2)
