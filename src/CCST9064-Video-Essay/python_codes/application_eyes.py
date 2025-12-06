from manim import *

# APPLICATION - EYES SCENES

class Scene4_Chapter1Title(Scene):
    """Chapter Title: Application - Eyes"""
    def construct(self):
        # Text animation
        chapter = Tex("{\\scshape\\bfseries CHAPTER I}", font_size=50, color=YELLOW)
        title = Tex("{\\bfseries Genetic Blindness}", font_size=64, color=YELLOW)
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

class Scene5_LuxturnaAndLCATitle(Scene):
    """Title: Luxturna and LCA"""
    def construct(self):
        # Text animation
        title = Tex("{\\bfseries Luxturna}", font_size=64, color=BLUE)
        subtitle = Tex("A gene therapy for", font_size=36)
        disease = Tex("{\\bfseries Leber Congenital Amaurosis (LCA)}", font_size=40, color=RED)

        title.move_to(UP * 1)
        subtitle.move_to(DOWN * 0.2)
        disease.move_to(DOWN * 0.8)

        self.play(Write(title, run_time=0.75))
        self.wait(3)
        self.play(Write(subtitle), Write(disease), run_time=0.75)

        self.wait(3)

class Scene6_LuxturnaPacking(Scene):
    """Luxturna Packing Animation"""
    def construct(self):
        scene_title = Tex("{\\bfseries Luxturna Mechanism}", font_size=48, color=YELLOW)
        scene_title.move_to(UP * 3)
        self.play(Write(scene_title), run_time=1)
        self.wait(0.5)

        # 1. Create cDNA (green single strand) on the left
        cdna = ParametricFunction(
            lambda t: np.array([
                0.2 * np.sin(4 * PI * t),
                2 * t - 1,
                0
            ]),
            t_range=[0, 1],
            color=GREEN,
            stroke_width=6
        )
        
        cdna_label1 = Tex("\\textbf{cDNA}", font_size=28, color=GREEN)
        cdna_label2 = Tex("\\textbf{(functional RPE65)}", font_size=24, color=GREEN)
        cdna_labels = VGroup(cdna_label1, cdna_label2).arrange(DOWN, buff=0.2)
        
        cdna.move_to(LEFT * 4)
        cdna_labels.next_to(cdna, DOWN, buff=0.5)
        
        # 2. Create AAV viral vector (purple capsid) on the right
        # Represent as a hexagonal/circular capsid with inner space
        aav_capsid = RegularPolygon(n=6, radius=1.2, color=PURPLE, stroke_width=4, fill_color=PURPLE, fill_opacity=0.2)
        
        # Add spike proteins around the capsid
        spike_positions = [
            UP * 1.2,
            UP * 0.6 + RIGHT * 1.0,
            DOWN * 0.6 + RIGHT * 1.0,
            DOWN * 1.2,
            DOWN * 0.6 + LEFT * 1.0,
            UP * 0.6 + LEFT * 1.0
        ]
        
        spikes = VGroup()
        for pos in spike_positions:
            spike = Triangle(color=PURPLE, fill_color=PURPLE, fill_opacity=0.8)
            spike.scale(0.15)
            spike.move_to(pos)
            # Point spike outward from center
            angle = np.arctan2(pos[1], pos[0])
            spike.rotate(angle + PI/2)
            spikes.add(spike)
        
        aav_vector = VGroup(aav_capsid, spikes)
        
        aav_label = Tex("\\textbf{AAV therapeutic\\\\vector}", font_size=28, color=PURPLE)
        
        aav_vector.move_to(RIGHT * 4)
        aav_label.next_to(aav_vector, DOWN, buff=0.5)
        
        # Display both components
        self.play(
            Create(cdna),
            Write(cdna_labels),
            run_time=0.7
        )
        self.wait(1.5)
        self.play(
            Create(aav_vector),
            Write(aav_label),
            run_time=0.7
        )
        self.wait(2)
        
        # 3. Move cDNA into the viral vector
        # Scale down cDNA to fit inside
        self.play(
            cdna.animate.scale(0.4).move_to(aav_vector.get_center()),
            FadeOut(cdna_labels),
            run_time=1
        )
        self.wait(0.5)
        
        # Group the combination
        aav_with_cdna = VGroup(aav_vector, cdna)
        
        # 4. Zoom and move to center, transform label
        aav_new_label = Tex("\\textbf{AAV2 serotype}", font_size=32, color=PURPLE)
        aav_new_label.move_to(DOWN * 2.5)
        
        self.play(
            aav_with_cdna.animate.scale(1.5).move_to(ORIGIN),
            Transform(aav_label, aav_new_label),
            run_time=1
        )
        self.wait(3)
        
class Scene7_LuxturnaInjection(Scene):
    """Luxturna Injection Animation"""
    def construct(self):
        scene_title = Tex("{\\bfseries Luxturna Mechanism}", font_size=48, color=YELLOW)
        scene_title.move_to(UP * 3)
        self.add(scene_title)

        # 1. Start from where Scene 6 ended - recreate the AAV2 with cDNA at center
        aav_capsid = RegularPolygon(n=6, radius=1.2, color=PURPLE, stroke_width=4, fill_color=PURPLE, fill_opacity=0.2)
        
        spike_positions = [
            UP * 1.2,
            UP * 0.6 + RIGHT * 1.0,
            DOWN * 0.6 + RIGHT * 1.0,
            DOWN * 1.2,
            DOWN * 0.6 + LEFT * 1.0,
            UP * 0.6 + LEFT * 1.0
        ]
        
        spikes = VGroup()
        for pos in spike_positions:
            spike = Triangle(color=PURPLE, fill_color=PURPLE, fill_opacity=0.8)
            spike.scale(0.15)
            spike.move_to(pos)
            angle = np.arctan2(pos[1], pos[0])
            spike.rotate(angle + PI/2)
            spikes.add(spike)
        
        aav_vector = VGroup(aav_capsid, spikes)
        
        cdna = ParametricFunction(
            lambda t: np.array([
                0.2 * np.sin(4 * PI * t),
                2 * t - 1,
                0
            ]),
            t_range=[0, 1],
            color=GREEN,
            stroke_width=6
        ).scale(0.4)
        
        aav_with_cdna = VGroup(aav_vector, cdna).scale(1.5).move_to(ORIGIN)
        aav_label = Tex("\\textbf{AAV2 serotype}", font_size=32, color=PURPLE).move_to(DOWN * 2.5)
        
        self.add(aav_with_cdna, aav_label)
        
        # 2. Zoom out AAV2 and move to left, create impaired cell on right-center
        self.play(
            aav_with_cdna.animate.scale(0.5).move_to(LEFT * 4),
            FadeOut(aav_label),
            run_time=1
        )
        
        # Create cell with impaired DNA (red) in nucleus
        cell = Circle(radius=2, color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.1)
        nucleus = Circle(radius=0.8, color=PURPLE, stroke_width=3, fill_color=PURPLE, fill_opacity=0.15)
        
        # Impaired DNA (red)
        impaired_dna = ParametricFunction(
            lambda t: np.array([
                0.2 * np.sin(4 * PI * t),
                0.6 * t - 0.3,
                0
            ]),
            t_range=[0, 1],
            color=RED,
            stroke_width=4
        )
        
        cell_group = VGroup(cell, nucleus, impaired_dna)
        cell_group.move_to(RIGHT * 1.5)
        
        # Add cell label for impaired state
        cell_label = Tex("\\textbf{Cell (impaired DNA)}", font_size=32, color=RED)
        cell_label.next_to(cell_group, DOWN, buff=0.3)
        
        self.play(Create(cell_group), Write(cell_label), run_time=1)
        
        # 3. Vector moves towards cell and releases cDNA
        self.play(
            aav_with_cdna.animate.move_to(cell.get_left() + LEFT * 0.5),
            run_time=1.2
        )
        
        # Extract and scale up the cDNA for delivery
        cdna_delivery = cdna.copy().scale(2)
        
        # Create fixed cell label
        fixed_cell_label = Tex("\\textbf{Cell (fixed DNA)}", font_size=32, color=GREEN)
        fixed_cell_label.next_to(cell_group, DOWN, buff=0.3)
        
        self.play(
            cdna_delivery.animate.move_to(nucleus.get_center()),
            impaired_dna.animate.set_color(GREEN),
            Transform(cell_label, fixed_cell_label),
            run_time=1.5
        )
        
        # Remove the delivery cDNA and keep the transformed one
        self.remove(cdna_delivery)
        
        # 4. Vector fades out, cell moves to center and zooms slightly
        self.play(FadeOut(aav_with_cdna), run_time=0.5)
        
        self.play(
            cell_group.animate.scale(0.9).move_to(ORIGIN),
            cell_label.animate.next_to(ORIGIN + DOWN * 2, DOWN, buff=0),
            run_time=1
        )
        
        # 5. Cell produces functional retinoid isomerase (blue hexagons)
        enzyme_label = Tex("\\textbf{Functional Retinoid\\\\Isomerase (RPE65)}", font_size=32, color=BLUE)
        enzyme_label.move_to(DOWN * 3)
        
        # Create enzymes with fixed random positions
        enzyme_positions = [
            UP * 2 + LEFT * 5,
            UP * 1.5 + RIGHT * 5.5,
            UP * 0.5 + LEFT * 6,
            DOWN * 0.8 + RIGHT * 6,
            DOWN * 2 + LEFT * 5.5,
            DOWN * 2.5 + RIGHT * 4.5,
            UP * 2.8 + LEFT * 2,
            UP * 2.5 + RIGHT * 3,
            DOWN * 3 + LEFT * 3,
            DOWN * 2.8 + RIGHT * 2.5,
            UP * 1 + LEFT * 3.5,
            DOWN * 1.5 + LEFT * 4
        ]
        
        enzymes = VGroup()
        animations = []
        
        for i, pos in enumerate(enzyme_positions):
            enzyme = RegularPolygon(n=6, radius=0.15, color=BLUE, fill_color=BLUE, fill_opacity=0.7)
            enzyme.move_to(cell.get_center())
            enzymes.add(enzyme)
            
            # Stagger the animations slightly
            animations.append(
                AnimationGroup(
                    enzyme.animate.move_to(pos),
                    lag_ratio=0.1
                )
            )
        
        self.add(enzymes)
        
        # Animate enzymes leaving the cell
        self.play(
            LaggedStart(*[enzyme.animate.move_to(pos) for enzyme, pos in zip(enzymes, enzyme_positions)],
                       lag_ratio=0.08),
            Write(enzyme_label),
            run_time=2.8
        )
        
        self.wait(2)

class Scene8_ClinicalResultsEyes(Scene):
    """Clinical Results Text"""
    def construct(self):
        # Title
        title = Tex("{\\bfseries Clinical Results}", font_size=56, color=YELLOW)
        title.move_to(UP * 2.5)
        
        # Result statements
        result1 = Tex("$\\bullet$ Significant improvements in retinal function", font_size=32)
        result2 = Tex("$\\bullet$ Increased light sensitivity", font_size=32)
        result3 = Tex("$\\bullet$ Enhanced pupillary responses", font_size=32)
        result4 = Tex("$\\bullet$ Improved vision in dim environments", font_size=32, color=GREEN)
        
        results = VGroup(result1, result2, result3, result4).arrange(DOWN, buff=0.5, aligned_edge=LEFT)
        results.move_to(DOWN * 0.5)
        
        # Animate title
        self.play(Write(title), run_time=1)
        self.wait(0.5)
        
        # Animate results appearing one by one
        self.play(FadeIn(result1, shift=UP * 0.3), run_time=0.8)
        self.wait(0.3)
        self.play(FadeIn(result2, shift=UP * 0.3), run_time=0.8)
        self.wait(0.3)
        self.play(FadeIn(result3, shift=UP * 0.3), run_time=0.8)
        self.wait(0.3)
        self.play(FadeIn(result4, shift=UP * 0.3), run_time=0.8)
        
        self.wait(3)
