import pygame
import pymunk
from constants import WIDTH, HEIGHT, FPS, DT, COLOR_BLACK, COLOR_WHITE, COLOR_BOT1, COLOR_BOT2
from simulation import Simulation
from renderer import Renderer

class PhysicsApp:
    """
    Two Bots connected by a Segmented Rope.
    Controls:
    - Bot 1: Arrow Keys to move, SPACE to anchor.
    - Bot 2: WASD Keys to move, LEFT SHIFT to anchor.
    - R Key: Reset simulation.
    """
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Two Bots & Segmented Rope Simulation")
        
        self.simulation = Simulation()
        self.renderer = Renderer(self.window)
        self.clock = pygame.time.Clock()
        
        self.running = True
        self.bot1 = None
        self.bot2 = None

    def setup(self):
        self.simulation.create_boundaries(WIDTH, HEIGHT)
        
        # Create two bots
        self.bot1 = self.simulation.create_bot((WIDTH // 3, HEIGHT // 2))
        self.bot2 = self.simulation.create_bot((2 * WIDTH // 3, HEIGHT // 2))
        
        # Set colors for debug draw (if shapes have color attribute)
        list(self.bot1.shapes)[0].color = COLOR_BOT1 + (200,)
        list(self.bot2.shapes)[0].color = COLOR_BOT2 + (200,)
        
        # Connect them with a rope
        self.simulation.create_rope(self.bot1, self.bot2)

    def handle_input(self):
        keys = pygame.key.get_pressed()
        force_magnitude = 1000000.0 # Adjust force as needed for BOT_MASS=100
        
        # Bot 1 Locomotion (Arrows)
        b1_force = [0.0, 0.0]
        if keys[pygame.K_UP]: b1_force[1] -= force_magnitude
        if keys[pygame.K_DOWN]: b1_force[1] += force_magnitude
        if keys[pygame.K_LEFT]: b1_force[0] -= force_magnitude
        if keys[pygame.K_RIGHT]: b1_force[0] += force_magnitude
        self.bot1.apply_force_at_local_point(b1_force, (0, 0))
        
        # Bot 2 Locomotion (WASD)
        b2_force = [0.0, 0.0]
        if keys[pygame.K_w]: b2_force[1] -= force_magnitude
        if keys[pygame.K_s]: b2_force[1] += force_magnitude
        if keys[pygame.K_a]: b2_force[0] -= force_magnitude
        if keys[pygame.K_d]: b2_force[0] += force_magnitude
        self.bot2.apply_force_at_local_point(b2_force, (0, 0))

        # Anchoring
        # Bot 1: Space
        if keys[pygame.K_SPACE]:
            self.simulation.anchor_bot(self.bot1)
        else:
            self.simulation.release_bot(self.bot1)
            
        # Bot 2: Left Shift
        if keys[pygame.K_LSHIFT]:
            self.simulation.anchor_bot(self.bot2)
        else:
            self.simulation.release_bot(self.bot2)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r: # Reset
                    self.__init__()
                    self.setup()

    def run(self):
        self.setup()
        while self.running:
            self.handle_events()
            self.handle_input()
            
            # Fixed timestep simulation
            self.simulation.step(DT)
            
            self.renderer.draw(self.simulation.space)
            self.clock.tick(FPS)
        
        pygame.quit()

if __name__ == "__main__":
    app = PhysicsApp()
    app.run()
