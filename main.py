import pygame
import pymunk
import pymunk.pygame_util
import math

pygame.init()

WIDTH, HEIGHT =1500, 800
window = pygame.display.set_mode((WIDTH, HEIGHT))

def draw(space, window, draw_options, pressed_body=None):
    window.fill("black")
    space.debug_draw(draw_options)
    
    if pressed_body:
        pos = pygame.mouse.get_pos()
        pygame.draw.line(window, (255, 255, 255), (int(pressed_body.position.x), int(pressed_body.position.y)), pos, 2)
        
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

def create_ball(space, radius, mass, pos=(400, 300)):
    body = pymunk.Body()
    body.position = pos
    shape = pymunk.Circle(body, radius)
    shape.mass = mass
    shape.color = (255, 0, 0, 100)
    space.add(body, shape)
    return shape

def run(window, width, height):
    run = True
    clock = pygame.time.Clock()
    fps = 60
    dt = 1 / fps

    space = pymunk.Space()
    space.gravity = (0, 200)

    create_ball(space, 50, 50)
    create_boundaries(space, width, height)

    draw_options = pymunk.pygame_util.DrawOptions(window)

    pressed_body = None
    grabbed = False

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3:  # Right Click
                    create_ball(space, 20, 10, event.pos)
                
                elif event.button == 1:  # Left Click
                    res = space.point_query_nearest(event.pos, 0, pymunk.ShapeFilter())
                    if res.shape and res.shape.body.body_type == pymunk.Body.DYNAMIC:
                        pressed_body = res.shape.body
                        if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                            grabbed = True
                        else:
                            grabbed = False

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and pressed_body:
                    if not grabbed:
                        # Slingshot mechanic
                        mouse_pos = pygame.mouse.get_pos()
                        force = (pressed_body.position.x - mouse_pos[0], pressed_body.position.y - mouse_pos[1])
                        pressed_body.apply_impulse_at_local_point((force[0] * 50, force[1] * 50))
                    
                    pressed_body = None
                    grabbed = False

            if event.type == pygame.MOUSEMOTION:
                if grabbed and pressed_body:
                    pressed_body.position = event.pos
                    pressed_body.velocity = (0, 0)
            
        draw(space, window, draw_options, pressed_body if not grabbed else None)
        space.step(dt)
        clock.tick(fps)
    
    pygame.quit()

if __name__ == "__main__":
    run(window, WIDTH, HEIGHT)
