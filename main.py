import pygame
import pymunk
import pymunk.pygame_util
import math

pygame.init()

WIDTH, HEIGHT =1500, 800
window = pygame.display.set_mode((WIDTH, HEIGHT))

def draw(space, wincow, draw_options):
    window.fill("black")
    space.debug_draw(draw_options)
    pygame.display.update()

def create_boundaries(space, width, height):
    rects = [[(width/2, height-1), (width, 10)],
             [(width/2, 5), (width, 10)], 
             [(5, height/2), (10, height)], 
             [(width-10, height/2), (10, height)]]

    for pos, size in rects:
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        body.position = pos
        shape = pymunk.Poly.create_box(body, size)
        space.add(body, shape)

def create_ball(space, radius, mass):
    body =pymunk.Body()
    body.position = (400, 300)
    shape = pymunk.Circle(body, radius)
    shape.mass = mass
    shape.color = (255, 0, 0, 50)
    space.add(body,shape)
    return shape

def run(window, width, height):
    run = True
    clock = pygame.time.Clock()
    fps = 60
    dt = 1 / fps

    space = pymunk.Space()
    space.gravity = (0, 200)

    ball = create_ball(space, 50, 50)
    create_boundaries(space, width, height)

    draw_options = pymunk.pygame_util.DrawOptions(window)

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            
        draw(space, window, draw_options)
        space.step(dt)
        clock.tick(fps)
    
    pygame.quit

if __name__ == "__main__":
    run(window, WIDTH, HEIGHT)
