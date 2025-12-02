from manim import *
import random

# ETHICAL DISCUSSION SCENES

class Scene20_EthicalTitle(Scene):
    """Chapter Title: Ethical Considerations"""
    def construct(self):
        # Text animation
        chapter = Tex("{\\scshape\\bfseries CHAPTER V}", font_size=50, color=YELLOW)
        title = Tex("{\\bfseries Gene Therapy Ethics}", font_size=64, color=YELLOW)
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

class Scene21_HumanWithQuestionMarks(Scene):
    def construct(self):
        # human svg
        human = SVGMobject("./human_outline.svg", fill_color=BLUE, fill_opacity=0.3, stroke_color=BLUE, stroke_width=2, should_center=True)
        human.scale(5)
        human.move_to(DOWN*1.5)
        self.play(Create(human), run_time=2)

        # Create question marks with different properties
        question_marks = []
        colors = [RED, YELLOW, GREEN, PURPLE, ORANGE, PINK, TEAL]
        positions = [
            DOWN * 2 + LEFT * 3,
            UP * 3 + RIGHT * 2,
            LEFT * 4 + UP * 1,
            RIGHT * 4 + UP * 0.5,
            DOWN * 2.5 + RIGHT * 4,
            LEFT * 3.5 + UP * 3,
            RIGHT * 3 + DOWN * 3.5,
            LEFT * 2 + UP * 1.5,
            RIGHT * 2.5 + UP * 2,
            LEFT * 5 + UP * 2.5,
            RIGHT * 5 + UP * 1.5,
            DOWN * 3.5 + LEFT * 1.5,
        ]
        
        # Predefined sizes for each question mark
        sizes = [65, 72, 48, 55, 78, 43, 69, 51, 76, 58, 62, 71]

        for i, (pos, color, size) in enumerate(zip(positions, colors * 2, sizes)):
            qmark = Tex("?", font_size=size, color=color)
            qmark.move_to(pos)
            question_marks.append(qmark)

        # Fade in question marks with lag
        self.play(
            LaggedStart(*[FadeIn(qmark) for qmark in question_marks],
                       lag_ratio=0.5,
                       run_time=6)
        )
        
        # text
        philosophical_text = Tex("$\\bullet$ Philosophical question?", font_size=50, color=WHITE)
        medical_safety_text = Tex("$\\bullet$ Medical safety!", font_size=50, color=WHITE)

        philosophical_text.move_to(DOWN * 2.6 + LEFT * 4)
        medical_safety_text.next_to(philosophical_text, DOWN, aligned_edge=LEFT, buff=0.2)

        self.play(Write(philosophical_text, run_time=1))
        self.wait(0.5)
        self.play(Write(medical_safety_text, run_time=1))
        self.wait(3)

class Scene22_JesseGelsingerCaseTimeline(Scene):
    def construct(self):
        # Title
        title = Tex("\\textbf{Jesse Gelsinger Case Timeline}", font_size=48, color=YELLOW)
        title.move_to(UP * 3.5)
        self.play(Write(title, run_time=0.5))
        self.wait(0.5)

        # Timeline arrow
        timeline = Arrow(start=LEFT * 6 + UP * 3, end=LEFT * 6 + DOWN * 4, color=YELLOW, stroke_width=4)
        self.play(Create(timeline), run_time=0.5)
        self.wait(0.5)

        # Events
        events = [
            ("{\\bfseries 18 Jun 1981:}", "Jesse Gelsinger born, later diagnosed with OTC deficiency"),
            ("{\\bfseries 13 Sept 1999:}", "At 18, Gelsinger injected with experimental gene therapy"),
            ("{\\bfseries 17 Sept 1999:}", "Gelsinger died from organ failure due to immune response"),
        ]

        for i, event_text in enumerate(events):
            event = VGroup(
                Tex(event_text[0], font_size=28, color=WHITE),
                Tex(event_text[1], font_size=32, color=WHITE)
            )
            event.arrange(DOWN, aligned_edge=LEFT)
            x_pos = LEFT * 6
            y_pos = UP * 2 + (DOWN * 4) * (i / (len(events) - 1))
            marker = Dot(point=x_pos + y_pos, color=RED, radius=0.1)
            event.next_to(marker, RIGHT, buff=0.3)
            self.play(Create(marker), Write(event, run_time=1))
            self.wait(0.5)

        self.wait(3)

class Scene23_BubbleBoy(Scene):
    def construct(self):
        # Create 4 stick figures in blue bubbles arranged in 2x2 grid
        stick_figures = []
        bubbles = []
        
        # Positions for 2x2 grid
        positions = [
            UP * 1.5 + LEFT * 2,   # Top left
            UP * 1.5 + RIGHT * 2,  # Top right
            DOWN * 1.5 + LEFT * 2, # Bottom left
            DOWN * 1.5 + RIGHT * 2 # Bottom right
        ]
        
        for pos in positions:
            # Create stick figure
            stick = VGroup(
                Circle(radius=0.15, color=WHITE, fill_opacity=1),  # Head
                Line(start=UP * 0.25, end=DOWN * 0.5, color=WHITE),   # Body
                Line(start=UP * 0.25, end=DOWN * 0.15 + LEFT * 0.25, color=WHITE),  # Left arm
                Line(start=UP * 0.25, end=DOWN * 0.15 + RIGHT * 0.25, color=WHITE), # Right arm
                Line(start=DOWN * 0.5, end=DOWN * 0.8 + LEFT * 0.2, color=WHITE),  # Left leg
                Line(start=DOWN * 0.5, end=DOWN * 0.8 + RIGHT * 0.2, color=WHITE), # Right leg
            )
            stick[0].move_to(UP * 0.4)
            stick.scale(0.8)
            stick.move_to(pos)
            
            # Create bubble
            bubble = Circle(radius=1.2, color=BLUE, stroke_width=4, fill_opacity=0.3, fill_color=BLUE)
            bubble.move_to(pos)
            
            stick_figures.append(stick)
            bubbles.append(bubble)
        
        # Show all stick figures and blue bubbles
        self.play(
            *[Create(bubble) for bubble in bubbles],
            *[Create(stick) for stick in stick_figures],
            run_time=1
        )
        self.wait(0.5)
        
        # Change colors: bottom right to red, others to green
        # Also create warning text for bottom right
        warning_text = Tex("Accidental activation\\\\ of leukaemia (25\\%)", font_size=32, color=RED)
        warning_text.next_to(bubbles[3], DOWN, buff=0.2)
        
        self.play(
            bubbles[3].animate.set_color(RED),  # Bottom right to red
            *[bubbles[i].animate.set_color(GREEN) for i in range(3)],  # Others to green
            Write(warning_text),
            run_time=1
        )
        
        self.wait(3)

class Scene24_ImmuneToGeneTherapy(Scene):
    """Scene showing immune response to gene therapy"""
    def construct(self):
        # 1. Create green human outline on the right half
        human = SVGMobject("./human_outline.svg", fill_color=GREEN, fill_opacity=0.3, stroke_color=GREEN, stroke_width=3, should_center=True)
        human.scale(3)
        human.move_to(RIGHT * 3)
        
        # Create AAV viral vector with RNA strand (upper-left)
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
        
        # RNA strand inside
        rna_strand = ParametricFunction(
            lambda t: np.array([
                0.2 * np.sin(4 * PI * t),
                1.5 * t - 0.75,
                0
            ]),
            t_range=[0, 1],
            color=GREEN,
            stroke_width=6
        ).scale(0.3)
        
        aav_capsid.scale(0.5)
        spikes.scale(0.5)
        aav_vector = VGroup(aav_capsid, spikes, rna_strand)
        aav_vector.move_to(UP * 2 + LEFT * 4)
        
        # Create CRISPR-Cas9 protein (lower-left)
        crispr_cas9 = VGroup(
            Rectangle(width=1.5, height=0.6, color=BLUE, fill_color=BLUE, fill_opacity=0.5),
            Tex("\\textbf{CRISPR-\\\\Cas9}", font_size=20, color=BLUE)
        )
        crispr_cas9.scale(1.4)
        crispr_cas9[1].move_to(crispr_cas9[0].get_center())
        crispr_cas9.move_to(DOWN * 2 + LEFT * 4)
        
        # Display all elements
        self.play(
            Create(human),
            Create(aav_vector),
            Create(crispr_cas9),
            run_time=1
        )
        self.wait(1)
        
        # 2. Vector approaches human but is bounced back
        target_pos = human.get_left() + LEFT * 0.5
        self.play(
            aav_vector.animate.move_to(target_pos),
            run_time=1
        )
        # self.wait(0.3)
        
        # Bounce back with shake
        self.play(
            aav_vector.animate.shift(LEFT * 0.3),
            run_time=0.2
        )
        # self.play(
        #     aav_vector.animate.shift(LEFT * 1.5),
        #     run_time=0.8,
        #     rate_func=smooth
        # )
        self.wait(0.5)
        
        # 3. Red cross forms on vector and it turns gray
        cross_line1 = Line(
            start=UP * 0.5 + LEFT * 0.5,
            end=DOWN * 0.5 + RIGHT * 0.5,
            color=RED,
            stroke_width=8
        )
        cross_line2 = Line(
            start=UP * 0.5 + RIGHT * 0.5,
            end=DOWN * 0.5 + LEFT * 0.5,
            color=RED,
            stroke_width=8
        )
        red_cross_vector = VGroup(cross_line1, cross_line2)
        red_cross_vector.move_to(aav_vector.get_center())
        
        self.play(
            Create(red_cross_vector),
            aav_capsid.animate.set_color(GRAY),
            aav_capsid.animate.set_fill(GRAY, opacity=0.2),
            *[spike.animate.set_color(GRAY).set_fill(GRAY, opacity=0.2) for spike in spikes],
            aav_vector.animate.set_stroke(GRAY),
            rna_strand.animate.set_color(GRAY),
            run_time=1
        )
        self.wait(1)
        
        # 4. CRISPR-Cas9 enters the human
        self.play(
            crispr_cas9.animate.move_to(human.get_center()),
            run_time=2
        )
        self.wait(0.5)
        
        # Cross forms on human and human turns gray
        cross_line3 = Line(
            start=UP * 1.5 + LEFT * 1.5,
            end=DOWN * 1.5 + RIGHT * 1.5,
            color=RED,
            stroke_width=10
        )
        cross_line4 = Line(
            start=UP * 1.5 + RIGHT * 1.5,
            end=DOWN * 1.5 + LEFT * 1.5,
            color=RED,
            stroke_width=10
        )
        red_cross_human = VGroup(cross_line3, cross_line4)
        red_cross_human.move_to(human.get_center())
        
        self.play(
            Create(red_cross_human),
            human.animate.set_color(GRAY).set_fill(GRAY, opacity=0.3),
            crispr_cas9.animate.set_color(GRAY).set_opacity(0.3),
            run_time=1.5
        )
        self.wait(2)

class Scene25_PublicOpinionSurvey(Scene):
    """Public opinion survey on gene therapy"""
    def construct(self):
        # Title
        title = Tex("\\textbf{Public Opinion Survey}", font_size=48, color=YELLOW)
        title.move_to(UP * 3.2)
        
        # Create 100 people icons in 10x10 grid
        people_icons = VGroup()
        rows, cols = 10, 10
        spacing = 0.6
        
        for row in range(rows):
            for col in range(cols):
                person = Circle(radius=0.08, color=WHITE, fill_opacity=1, fill_color=WHITE)
                person[0].move_to(UP * 0.1)
                
                x_pos = (col - cols / 2) * spacing + spacing / 2
                y_pos = (rows / 2 - row) * spacing - spacing / 2
                person.move_to(RIGHT * x_pos + UP * y_pos + DOWN * 0.5)
                
                people_icons.add(person)
        
        self.play(
            Write(title),
            LaggedStart(*[FadeIn(person) for person in people_icons], lag_ratio=0.01),
            run_time=1
        )
        self.wait(1)

        # Group them randomly (predefined random)
        oppose_indices = (
            2,  5,  8,  13, 14, 19, 20, 23, 27, 28,
            30, 42, 45, 47, 50, 51, 52, 60, 63, 68,
            69, 94, 97, 99, 92
        )
        oppose_people = [people_icons[i] for i in oppose_indices]
        support_people = [people_icons[i] for i in range(100) if i not in oppose_indices]
        
        # Highlight 75% in green (supporting gene therapy)
        support_label = Tex("\\textbf{75\\% believe in\\\\gene therapy}", font_size=48, color=GREEN)
        support_label.move_to(LEFT * 5)
        
        self.play(
            *[support_people[i].animate.set_color(GREEN) for i in range(75)],
            Write(support_label),
            run_time=1
        )
        self.wait(0.5)
        
        # Show the remaining 25% in red
        oppose_label = Tex("\\textbf{25\\% uncertain\\\\or opposed}", font_size=48, color=RED)
        oppose_label.move_to(RIGHT * 5)
        
        self.play(
            *[oppose_people[i].animate.set_color(RED) for i in range(25)],
            Write(oppose_label),
            run_time=1
        )
        
        self.wait(3)

class Scene26_EthicalConcerns(Scene):
    """Ethical concerns about gene therapy"""
    def construct(self):
        # Title
        title = Tex("{\\bfseries Ethical Concerns}", font_size=56, color=YELLOW)
        title.move_to(UP * 3)
        
        # Concern statements
        concern1_title = Tex("$\\bullet$ \\textbf{``Playing God''}", font_size=36, color=RED)
        concern1_detail = Tex("Changing nature may cause unexpected dangerous results", font_size=28)
        concern1 = VGroup(concern1_title, concern1_detail).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        
        concern2_title = Tex("$\\bullet$ \\textbf{Fairness and Access}", font_size=36, color=ORANGE)
        concern2_detail = Tex("Treatments cost millions, risking a permanent genetic divide", font_size=28)
        concern2 = VGroup(concern2_title, concern2_detail).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        
        concern3_title = Tex("$\\bullet$ \\textbf{Threat to Human Identity}", font_size=36, color=PURPLE)
        concern3_detail = Tex("Brain-editing errors could cause catastrophic damage", font_size=28)
        concern3 = VGroup(concern3_title, concern3_detail).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        
        concerns = VGroup(concern1, concern2, concern3).arrange(DOWN, buff=0.7, aligned_edge=LEFT)
        concerns.move_to(DOWN * 0.3)
        
        # Animate title
        self.play(Write(title), run_time=1)
        self.wait(0.5)
        
        # Animate concerns appearing one by one
        self.play(FadeIn(concern1, shift=UP * 0.3), run_time=1)
        self.wait(0.5)
        self.play(FadeIn(concern2, shift=UP * 0.3), run_time=1)
        self.wait(0.5)
        self.play(FadeIn(concern3, shift=UP * 0.3), run_time=1)
        
        self.wait(3)

