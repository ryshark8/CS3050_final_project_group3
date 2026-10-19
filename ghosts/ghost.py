import arcade
import random

class Ghost(arcade.Sprite):
    """
    when intialized, should only need ghost color, the rest should be handled internally
    """

    FRAME_DURATION = 0.1
    
    #TODO: create a dictionary of attributes based on color of the ghost
    def __init__(self):
        super().__init__(self)

        self.elapsed_time = 0
        self.scale = 3
        self.animation_timer = 0
        self.found = False
        self.speed = 3
        self.destination = (random.randint(0, 1280), random.randint(0, 720))
        self.dest_y = 400


    def update_animation(self, direction):
        # make sure eyes are correct
        if direction[0] == 'x':
            if direction[1] > 0:
                self.textures = self.frames['right']
            else:
                self.textures = self.frames['left']

        else:
            if direction[1] > 0:
                self.textures = self.frames['up']
            else:
                self.textures = self.frames['down']

        self.cur_texture_index = (self.cur_texture_index + 1) % len(self.textures)
        self.texture = self.textures[self.cur_texture_index]

    def update(self, delta_time):
        # movement logic

        #get new end point
        if self.center_x == self.destination[0] and self.center_y == self.destination[1]:
            self.destination = (random.randint(0, 1280), random.randint(0, 720))

        start_x = self.center_x
        start_y = self.center_y

        x_diff = self.destination[0] - start_x
        y_diff = self.destination[1] - start_y

        #can only move orthogonally
        if x_diff:
            
            speed = min(self.speed, abs(x_diff))
            sign = (x_diff > 0) - (x_diff < 0)
            self.center_x += speed * sign
            direction = ('x', x_diff)

        elif y_diff:
            speed = min(self.speed, abs(y_diff))
            sign = (y_diff > 0) - (y_diff < 0)
            self.center_y += speed * sign
            direction = ('y', y_diff)
        
        #update the animation
        if self.animation_timer >= self.FRAME_DURATION:
            self.update_animation(direction=direction)
            self.animation_timer = 0


        self.elapsed_time += delta_time
        self.animation_timer += delta_time
