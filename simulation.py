import pymunk
from constants import (
    GRAVITY, DAMPING, BOT_MASS, BOT_RADIUS,
    ROPE_SEGMENT_MASS, ROPE_SEGMENT_LENGTH, ROPE_SEGMENT_WIDTH, ROPE_SEGMENTS_COUNT,
    COLLISION_GROUP_ROPE, CATEGORY_BOT, CATEGORY_ROPE, CATEGORY_ENV
)

class Simulation:
    def __init__(self):
        self.space = pymunk.Space()
        self.space.gravity = GRAVITY
        self.space.damping = DAMPING
        
        self.bots = []
        self.rope_segments = []
        self.anchors = {} # bot -> joint

    def create_boundaries(self, width, height):
        static_body = self.space.static_body
        
        # Walls with high friction
        walls = [
            pymunk.Segment(static_body, (20, 20), (width - 20, 20), 5),           # Top
            pymunk.Segment(static_body, (20, height - 20), (width - 20, height - 20), 5), # Bottom
            pymunk.Segment(static_body, (20, 20), (20, height - 20), 5),         # Left
            pymunk.Segment(static_body, (width - 20, 20), (width - 20, height - 20), 5) # Right
        ]
        
        for wall in walls:
            wall.friction = 1.0
            wall.filter = pymunk.ShapeFilter(categories=CATEGORY_ENV)
            self.space.add(wall)

    def create_bot(self, pos):
        moment = pymunk.moment_for_circle(BOT_MASS, 0, BOT_RADIUS)
        body = pymunk.Body(BOT_MASS, moment)
        body.position = pos
        shape = pymunk.Circle(body, BOT_RADIUS)
        shape.friction = 0.7
        # Bot collides with ENV and other BOTs
        shape.filter = pymunk.ShapeFilter(
            categories=CATEGORY_BOT,
            mask=CATEGORY_ENV | CATEGORY_BOT
        )
        self.space.add(body, shape)
        self.bots.append(body)
        return body

    def create_rope(self, bot1, bot2):
        prev_body = bot1
        anchor_a = (0, 0)
        
        rope_filter = pymunk.ShapeFilter(
            group=COLLISION_GROUP_ROPE,
            categories=CATEGORY_ROPE,
            mask=CATEGORY_ENV
        )

        for i in range(ROPE_SEGMENTS_COUNT):
            mass = ROPE_SEGMENT_MASS
            moment = pymunk.moment_for_box(mass, (ROPE_SEGMENT_LENGTH, ROPE_SEGMENT_WIDTH))
            body = pymunk.Body(mass, moment)
            
            # Linear interpolation for initial position
            fraction = (i + 0.5) / ROPE_SEGMENTS_COUNT
            body.position = bot1.position + (bot2.position - bot1.position) * fraction
            
            shape = pymunk.Poly.create_box(body, (ROPE_SEGMENT_LENGTH, ROPE_SEGMENT_WIDTH))
            shape.friction = 1.0
            shape.filter = rope_filter
            self.space.add(body, shape)
            self.rope_segments.append(body)
            
            # Pivot joint connects end of prev to start of current
            anchor_b = (-ROPE_SEGMENT_LENGTH / 2, 0)
            joint = pymunk.PivotJoint(prev_body, body, anchor_a, anchor_b)
            joint.collide_bodies = False
            self.space.add(joint)
            
            # Add rotational friction to prevent endless oscillation
            friction_joint = pymunk.GearJoint(prev_body, body, 0, 1)
            friction_joint.max_force = 5000 
            self.space.add(friction_joint)
            
            prev_body = body
            anchor_a = (ROPE_SEGMENT_LENGTH / 2, 0)
            
        # Connect last segment to bot2
        final_joint = pymunk.PivotJoint(prev_body, bot2, anchor_a, (0, 0))
        self.space.add(final_joint)

    def anchor_bot(self, bot):
        if bot not in self.anchors:
            # Anchor to static body at current world position
            anchor_joint = pymunk.PinJoint(self.space.static_body, bot, bot.position, (0,0))
            anchor_joint.distance = 0
            self.space.add(anchor_joint)
            self.anchors[bot] = anchor_joint

    def release_bot(self, bot):
        if bot in self.anchors:
            self.space.remove(self.anchors[bot])
            del self.anchors[bot]

    def step(self, dt):
        self.space.step(dt)
