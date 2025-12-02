from manim import *

# INTRODUCTION SCENES

class Scene1_TitleText(Scene):
    """Opening shot: Somatic Gene Therapy"""
    def construct(self):
        # Text animation
        text = Tex("Science Fiction", font_size=48, color=GREEN)
        self.play(Write(text))
        self.wait(2)

        newText = Tex("Somatic Gene Therapy", font_size=48, color=RED)
        self.play(Transform(text, newText))
        self.wait(3)
        
        self.play(FadeOut(text))

class Scene2_FixingGeneErrorsInACell(Scene):
    """Scene: Fixing Gene Errors in a Cell"""
    def construct(self):
        # Create cell (outer circle) with background
        cell = Circle(radius=2.5, color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.3)
        
        # Create nucleus (inner circle) - smaller size with background
        nucleus = Circle(radius=0.9, color=PURPLE, stroke_width=3, fill_color=PURPLE, fill_opacity=0.35)
        
        # Create problematic DNA (red double helix)
        # Simple representation using two intertwined curves
        dna_strand1 = ParametricFunction(
            lambda t: np.array([
            0.3 * np.cos(2 * PI * t),
            0.8 * t - 0.4,
            0
            ]),
            t_range=[0, 1],
            color=RED
        )
        dna_strand2 = ParametricFunction(
            lambda t: np.array([
            -0.3 * np.cos(2 * PI * t),
            0.8 * t - 0.4,
            0
            ]),
            t_range=[0, 1],
            color=RED
        )
        problematic_dna = VGroup(dna_strand1, dna_strand2)
        
        # Create text labels
        cell_label = Tex("$\\textbf{Cell}$", font_size=28, color=BLUE).next_to(cell, DOWN, buff=0.3)
        problematic_dna_label = Tex("\\textbf{Problematic \\\\DNA}", font_size=24, color=RED).next_to(problematic_dna, RIGHT, buff=0.7)
        
        # Display cell, nucleus, problematic DNA, and labels at the start
        self.add(cell, nucleus, problematic_dna, cell_label, problematic_dna_label)
        self.wait(2)
        
        # Create fixed DNA (green double helix)
        fixed_strand1 = ParametricFunction(
            lambda t: np.array([
            0.3 * np.cos(2 * PI * t),
            0.8 * t - 0.4,
            0
            ]),
            t_range=[0, 1],
            color=GREEN
        )
        fixed_strand2 = ParametricFunction(
            lambda t: np.array([
            -0.3 * np.cos(2 * PI * t),
            0.8 * t - 0.4,
            0
            ]),
            t_range=[0, 1],
            color=GREEN
        )
        fixed_dna = VGroup(fixed_strand1, fixed_strand2)
        
        # Create fixed DNA label
        fixed_dna_label = Tex("\\textbf{Fixed \\\\DNA}", font_size=24, color=GREEN).next_to(fixed_dna, RIGHT, buff=1.0)
        
        # Flash effect
        flash = Flash(problematic_dna.get_center(), color=YELLOW, flash_radius=0.8)
        
        # Morph DNA to green with pop effect and morph the label
        self.play(
            Transform(problematic_dna, fixed_dna),
            Transform(problematic_dna_label, fixed_dna_label),
            flash,
            problematic_dna.animate.scale(1.3).set_color(GREEN)
        )
        self.play(problematic_dna.animate.scale(1/1.3))
        self.wait(2)

class Scene3_NoPassing(Scene):
    """Scene: No Passing"""
    def construct(self):
        # Start with the ending status of Scene 2
        cell = Circle(radius=2.5, color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.3)
        nucleus = Circle(radius=0.9, color=PURPLE, stroke_width=3, fill_color=PURPLE, fill_opacity=0.35)
        
        # Fixed DNA (green double helix)
        dna_strand1 = ParametricFunction(
            lambda t: np.array([
            0.3 * np.cos(2 * PI * t),
            0.8 * t - 0.4,
            0
            ]),
            t_range=[0, 1],
            color=GREEN
        )
        dna_strand2 = ParametricFunction(
            lambda t: np.array([
            -0.3 * np.cos(2 * PI * t),
            0.8 * t - 0.4,
            0
            ]),
            t_range=[0, 1],
            color=GREEN
        )
        fixed_dna = VGroup(dna_strand1, dna_strand2)
        
        # Create labels
        cell_label = Tex("$\\textbf{Cell}$", font_size=28, color=BLUE).next_to(cell, DOWN, buff=0.3)
        fixed_dna_label = Tex("\\textbf{Fixed \\\\DNA}", font_size=24, color=GREEN).next_to(fixed_dna, RIGHT, buff=1.0)
        
        # Group the cell components
        cell_group = VGroup(cell, nucleus, fixed_dna)
        
        # Add everything at the start
        self.add(cell_group, cell_label, fixed_dna_label)
        
        # Fade out the text labels
        self.play(FadeOut(cell_label), FadeOut(fixed_dna_label), run_time=0.25)
        
        # Create stick figures
        # Parent (taller, on the left)
        parent_head = Circle(radius=0.3, color=WHITE, stroke_width=2)
        parent_body = Line(start=ORIGIN, end=DOWN * 1.5, color=WHITE, stroke_width=2)
        parent_arms = Line(start=LEFT * 0.5, end=RIGHT * 0.5, color=WHITE, stroke_width=2)
        parent_legs = VGroup(
            Line(start=ORIGIN, end=DOWN * 0.8 + LEFT * 0.4, color=WHITE, stroke_width=2),
            Line(start=ORIGIN, end=DOWN * 0.8 + RIGHT * 0.4, color=WHITE, stroke_width=2)
        )
        
        parent = VGroup(parent_head, parent_body, parent_arms, parent_legs)
        parent_head.next_to(parent_body.get_start(), UP, buff=0.1)
        parent_arms.next_to(parent_body.get_start(), DOWN, buff=0.3)
        parent_legs.next_to(parent_body.get_end(), DOWN, buff=0)
        
        parent.move_to(LEFT * 3 + DOWN * 0.5)
        parent_label = Tex("\\textbf{Parent}", font_size=24, color=WHITE).next_to(parent, DOWN, buff=0.3)
        
        # Child (shorter, on the right)
        child_head = Circle(radius=0.25, color=WHITE, stroke_width=2)
        child_body = Line(start=ORIGIN, end=DOWN * 1.0, color=WHITE, stroke_width=2)
        child_arms = Line(start=LEFT * 0.4, end=RIGHT * 0.4, color=WHITE, stroke_width=2)
        child_legs = VGroup(
            Line(start=ORIGIN, end=DOWN * 0.6 + LEFT * 0.3, color=WHITE, stroke_width=2),
            Line(start=ORIGIN, end=DOWN * 0.6 + RIGHT * 0.3, color=WHITE, stroke_width=2)
        )
        
        child = VGroup(child_head, child_body, child_arms, child_legs)
        child_head.next_to(child_body.get_start(), UP, buff=0.1)
        child_arms.next_to(child_body.get_start(), DOWN, buff=0.2)
        child_legs.next_to(child_body.get_end(), DOWN, buff=0)
        
        child.move_to(RIGHT * 3 + DOWN * 0.3)
        child_label = Tex("\\textbf{Child}", font_size=24, color=WHITE).next_to(child, DOWN, buff=0.3)
        
        # Fade in stick figures and their labels
        self.play(
            FadeIn(parent), FadeIn(parent_label),
            FadeIn(child), FadeIn(child_label),
            cell_group.animate.scale(0.3).shift(parent.get_center() + RIGHT * 1.2),
            run_time=1
        )
        
        # Move cell next to parent
        self.play(cell_group.animate.move_to(parent.get_center() + RIGHT * 1.2), run_time=0.5)
        self.wait(0.25)
        
        # Draw arrow from left to right
        arrow = Arrow(
            start=LEFT * 1.5,
            end=RIGHT * 1.5,
            color=YELLOW,
            buff=0,
            stroke_width=6
        ).move_to(DOWN * 0.5)
        self.play(Create(arrow), run_time=0.25)
        
        # Cell attempts to move along arrow but is stopped by red cross
        # Create red cross in the middle
        cross_line1 = Line(start=UP * 0.3 + LEFT * 0.3, end=DOWN * 0.3 + RIGHT * 0.3, color=RED, stroke_width=8)
        cross_line2 = Line(start=UP * 0.3 + RIGHT * 0.3, end=DOWN * 0.3 + LEFT * 0.3, color=RED, stroke_width=8)
        red_cross = VGroup(cross_line1, cross_line2).move_to(DOWN * 0.5)
        
        # Animate cell moving and being stopped
        self.play(
            cell_group.animate.move_to(cell_group.get_center() + RIGHT * 1.5),
            run_time=1,
            rate_func=rush_into
        )
        
        # Show red cross appearing and cell bouncing back slightly
        self.play(Create(red_cross), cell_group.animate.shift(LEFT * 0.3), run_time=0.5)
        self.wait(2)