from manim import *
import random

# BLOOD CANCER APPLICATION SCENES

class Scene12_Chapter3Title(Scene):
    """Chapter 3 Title: Leukaemia and Lymphoma"""
    def construct(self):
        # Text animation
        chapter = Tex("{\\scshape\\bfseries CHAPTER III}", font_size=50, color=YELLOW)
        title = Tex("{\\bfseries Leukaemia and Lymphoma}", font_size=64, color=YELLOW)
        separator = Line(start=LEFT * 3, end=RIGHT * 3, color=ORANGE, stroke_width=4)

        chapter.move_to(UP * 0.75)
        title.move_to(DOWN * 0.75)
        separator.move_to(ORIGIN)

        self.wait(1) # for editing

        self.play(
            Write(chapter, run_time=1.5),
            Create(separator, run_time=1.5),
            Write(title, run_time=1.5)
        )

        self.wait(3)

class Scene13_WBCDivision(Scene):
    """White Blood Cell Division and Mutation Introduction Scene"""
    def construct(self):
        # Create initial white blood cell
        initial_cell = Circle(radius=0.3, color=WHITE, fill_opacity=0.8, fill_color=WHITE, stroke_width=2)
        initial_cell.move_to(ORIGIN)

        # Store all cells in a list
        cells = [initial_cell]
        
        self.add(initial_cell)
        self.wait(1)

        # Division loop
        max_cells = 100
        division_interval = 0.15  # Time between divisions
        cell_radius = 0.3

        def find_non_overlapping_position(parent_pos, existing_cells, max_attempts=50):
            """Find a position for new cell that doesn't overlap with existing cells"""
            for attempt in range(max_attempts):
                angle = np.random.uniform(0, 2 * np.pi)
                distance = cell_radius * 2.5  # Start at safe distance
                offset = np.array([np.cos(angle), np.sin(angle), 0]) * distance
                new_pos = parent_pos + offset
                
                # Check if position is valid (not overlapping and within frame)
                if abs(new_pos[0]) < config.frame_width / 2 - cell_radius and \
                   abs(new_pos[1]) < config.frame_height / 2 - cell_radius:
                    
                    # Check overlap with existing cells
                    overlapping = False
                    for cell in existing_cells:
                        dist = np.linalg.norm(new_pos - cell.get_center())
                        if dist < cell_radius * 2.2:  # Minimum safe distance
                            overlapping = True
                            break
                    
                    if not overlapping:
                        return new_pos
            
            # If no good position found, return random position with larger offset
            angle = np.random.uniform(0, 2 * np.pi)
            distance = cell_radius * 4
            offset = np.array([np.cos(angle), np.sin(angle), 0]) * distance
            return parent_pos + offset

        while len(cells) < max_cells:
            # Select a random cell to divide from all existing cells
            if len(cells) > 0:
                parent = random.choice(cells)
                parent_pos = parent.get_center()
                
                # Find positions for two daughter cells
                pos1 = find_non_overlapping_position(parent_pos, cells)
                
                # Create first daughter cell
                new_cell1 = Circle(radius=cell_radius, color=WHITE, fill_opacity=0.8, fill_color=WHITE, stroke_width=2)
                new_cell1.move_to(parent_pos)
                
                # Temporarily add to list to check for second position
                temp_cells = cells + [new_cell1]
                pos2 = find_non_overlapping_position(parent_pos, temp_cells)
                
                # Create second daughter cell
                new_cell2 = Circle(radius=cell_radius, color=WHITE, fill_opacity=0.8, fill_color=WHITE, stroke_width=2)
                new_cell2.move_to(parent_pos)
                
                # Remove parent cell and add daughter cells
                self.remove(parent)
                cells.remove(parent)
                
                cells.append(new_cell1)
                cells.append(new_cell2)
                
                self.add(new_cell1, new_cell2)
                
                # Animate cells moving to their positions
                self.play(
                    new_cell1.animate.move_to(pos1),
                    new_cell2.animate.move_to(pos2),
                    run_time=0.3,
                    rate_func=smooth
                )
                
                if len(cells) >= max_cells:
                    break

        self.wait(2)

class Scene14_CARTCellTherapy(Scene):
    """CAR T-cell Therapy Process"""
    def construct(self):
        # Text animation
        title = Tex("{\\bfseries CAR-T Cell Therapy}", font_size=72, color=YELLOW)

        self.wait(2)  # for editing

        self.play(Write(title, run_time=1))

        self.wait(3)

class Scene15_HighRateBut(Scene):
    def construct(self):
        # Text animation
        text = Tex("\\textbf{High Remission Rate}", font_size=64, color=YELLOW)
        text.move_to(UP * 0.5)
        self.wait(1.5)
        self.play(Write(text, run_time=1))
        self.wait(1)

        but_text = Tex("\\textbf{But...?}", font_size=64, color=RED)
        but_text.move_to(DOWN * 0.5)
        self.play(Write(but_text, run_time=1))
        self.wait(2)

class Scene16_CytokineStorm(Scene):
    """Cytokine Storm Explanation Scene"""
    def construct(self):
        # 1. T cell
        t_cell = Circle(radius=0.5, color=BLUE, fill_color=BLUE, fill_opacity=0.5, stroke_width=3)
        t_cell.move_to(UP * 2.5)
        t_cell_label = Tex("\\textbf{T Cell}", font_size=24, color=BLUE).next_to(t_cell, DOWN, buff=0.3)
        t_cell_group = VGroup(t_cell, t_cell_label)

        # 2. Cancer Cell
        cancer_cell = Circle(radius=0.5, color=RED, fill_color=RED, fill_opacity=0.5, stroke_width=3)
        cancer_cell.move_to(DOWN * 2.5 + LEFT * 3)
        cancer_cell_label = Tex("\\textbf{Cancer Cell}", font_size=24, color=RED).next_to(cancer_cell, DOWN, buff=0.3)
        cancer_cell_group = VGroup(cancer_cell, cancer_cell_label)

        # 3. Healthy Cell
        healthy_cell = Circle(radius=0.5, color=GREEN, fill_color=GREEN, fill_opacity=0.5, stroke_width=3)
        healthy_cell.move_to(DOWN * 2.5 + RIGHT * 3)
        healthy_cell_label = Tex("\\textbf{Healthy Cell}", font_size=24, color=GREEN).next_to(healthy_cell, DOWN, buff=0.3)
        healthy_cell_group = VGroup(healthy_cell, healthy_cell_label)

        # arrows
        arrow_to_cancer = Arrow(
            start=t_cell_group.get_bottom(),
            end=cancer_cell_group.get_top() + DOWN * 0.1,
            color=YELLOW,
            buff=0.5,
            stroke_width=6
        )

        arrow_to_healthy = Arrow(
            start=t_cell_group.get_bottom(),
            end=healthy_cell_group.get_top() + DOWN * 0.1,
            color=YELLOW,
            buff=0.5,
            stroke_width=6
        )

        # text
        text = Tex("\\textbf{Cytokine Storm}", font_size=48, color=ORANGE)
        text.next_to(arrow_to_healthy.get_center(), RIGHT, buff=1)

        self.wait(1)
        self.play(
            Create(t_cell), Write(t_cell_label), 
            Create(cancer_cell), Write(cancer_cell_label),
            Create(healthy_cell), Write(healthy_cell_label),
            run_time=0.5
        )
        self.wait(1)
        self.play(Create(arrow_to_cancer), run_time=0.5)
        self.play(Create(arrow_to_healthy), Write(text), run_time=0.5)

        self.wait(3)