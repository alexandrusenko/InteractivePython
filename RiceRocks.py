# implementation of Spaceship - program template for RiceRocks
import simplegui
import math
import random
   
# globals for user interface and game mechanics
WIDTH = 800
HEIGHT = 600
score = 0
initial_score = 1000
high_score = 0
extra_life = 5000
lives = 3
time = 0
started = False
game_over_flag = False
first_high_score = True

# controls speed of asteroids
vel_const = .3

# ImageInfo class, processes images
class ImageInfo:
    
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2013.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image1 = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")
explosion_image2 = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_orange.png")

# sound assets purchased from sounddogs.com, please do not redistribute
# .ogg versions of sounds are also available, just replace .mp3 by .ogg
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")
# free sound assets from freesfx.co.uk
# mp3 only
high_score_sound = simplegui.load_sound("https://dl-web.dropbox.com/get/correct_sound.mp3?_subject_uid=164632267&w=AADE4aKlfneb1CU_F1vSpKiH17d0K9faxMGCCys47Pug2g")
extra_life_sound = simplegui.load_sound("https://dl-web.dropbox.com/get/classic_video_game_level_up.mp3?_subject_uid=164632267&w=AAC-H74Od0kTi5_1LhRA9gpBquGmApd696Zla2BO7hcDDA")
death_sound = simplegui.load_sound("https://dl-web.dropbox.com/get/robotic_transition.mp3?_subject_uid=164632267&w=AAAMnZel24Htd3LaHeaBqv7oyllODlNaEiVNBfsNPsahfg")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p, q):
    return math.sqrt((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2)


# Ship class
class Ship:

    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0], pos[1]]
        self.vel = [vel[0], vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.explosion = 2
        
    def draw(self, canvas):
        
        # if ship is thrusting, draw ship with thrust
        if self.thrust:
            canvas.draw_image(self.image, [self.image_center[0] + self.image_size[0], self.image_center[1]] , self.image_size,
                              self.pos, self.image_size, self.angle)
        # otherwise, just draw ship
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size,
                              self.pos, self.image_size, self.angle)

    def update(self):
        # update angle
        self.angle += self.angle_vel
        
        # update position
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT

        # update velocity
        if self.thrust:
            acc = angle_to_vector(self.angle)
            self.vel[0] += acc[0] * .1
            self.vel[1] += acc[1] * .1
            
        self.vel[0] *= .99
        self.vel[1] *= .99
        
    # play thrust sound if ship is thrusting
    def set_thrust(self, on):
        self.thrust = on
        if on:
            ship_thrust_sound.rewind()
            ship_thrust_sound.play()
        else:
            ship_thrust_sound.pause()
    # turn ship   
    def increment_angle_vel(self):
        self.angle_vel += .05
        
    def decrement_angle_vel(self):
        self.angle_vel -= .05
        
    # shoot missile    
    def shoot(self):
        global a_missile
        forward = angle_to_vector(self.angle)
        missile_pos = [self.pos[0] + self.radius * forward[0], self.pos[1] + self.radius * forward[1]]
        missile_vel = [self.vel[0] + 6 * forward[0], self.vel[1] + 6 * forward[1]]
        a_missile = Sprite(missile_pos, missile_vel, self.angle, 0, missile_image, missile_info, missile_sound)
        missile_group.add(a_missile)
    
# Sprite class
class Sprite:
    
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.image_scale = self.image_size
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        self.explosion = 1
        if sound:
            sound.rewind()
            sound.play()
   
    def draw(self, canvas):
        
        # if the sprite is an animation, iterate through the sprite sheet and draw the animation
        if self.animated == True:
            current_explosion_index = (self.age % self.lifespan) // 1
            current_explosion_center = [self.image_center[0] +  current_explosion_index * self.image_center[0], self.image_center[1]]
            canvas.draw_image(self.image, current_explosion_center, self.image_size, self.pos, self.image_size) 
            self.age += 1  
        # otherwise it's just a plain image, so draw it
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size,
                self.pos, self.image_scale, self.angle)
        
    def update(self):
        
        # update angle
        self.angle += self.angle_vel
        
        # update position
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        
        # update missile lifespan
        self.age += 1
        if self.age >= self.lifespan:
            return True
        else:
            return False
        
    def collide(self, other_object):
        
        # check if two sprites collide
        if dist(self.pos, other_object.pos) <= (self.radius + other_object.radius):
            return True
        else:
            return False
         
# key handlers to control ship   
def keydown(key):
    if key == simplegui.KEY_MAP['left']:
        my_ship.decrement_angle_vel()
    elif key == simplegui.KEY_MAP['right']:
        my_ship.increment_angle_vel()
    elif key == simplegui.KEY_MAP['up']:
        my_ship.set_thrust(True)
    elif key == simplegui.KEY_MAP['space']:
        my_ship.shoot()
        
def keyup(key):
    if key == simplegui.KEY_MAP['left']:
        my_ship.increment_angle_vel()
    elif key == simplegui.KEY_MAP['right']:
        my_ship.decrement_angle_vel()
    elif key == simplegui.KEY_MAP['up']:
        my_ship.set_thrust(False)
        
# mouseclick handlers that reset UI and conditions whether splash image is drawn
def click(pos):
    global started, lives, extra_life, score, initial_score, first_high_score, vel_const
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:
        started = True
        first_high_score = True
        lives = 3
        extra_life = 5000
        score = 0
        initial_score = 0
        vel_const = .3
        soundtrack.play()
        my_ship.pos = [WIDTH / 2, HEIGHT / 2]
        my_ship.vel = [0, 0]
        my_ship.angle = 0

def draw(canvas):
    global time, started, lives, score, high_score, first_high_score, initial_score, extra_life, rock_val, rock_group, missile_group, explosion_group, game_over_flag, vel_const
    
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    # draw UI
    canvas.draw_text("Lives", [50, 50], 22, "White")
    canvas.draw_text("Score", [150, 50], 22, "White")
    canvas.draw_text("High Score", [655, 50], 22, "White")
    canvas.draw_text(str(lives), [50, 80], 22, "White")
    canvas.draw_text(str(score), [150, 80], 22, "White")
    canvas.draw_text(str(high_score), [655, 80], 22, "White")
    
    # draw splash screen if not started
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], 
                          splash_info.get_size())
        if game_over_flag:
            canvas.draw_text("Game Over!", [350, 50], 22, "White")
            
        rock_group = set([])
        missile_group = set([])
        explosion_group = set([])
        return
    
    # every 1000 points scored, increase speed of asteroids
    if score >= initial_score:
        vel_const += .3
        initial_score = score + 1000
        
    # every 5000 points scored, add an extra life    
    if score >= extra_life:
        lives += 1
        extra_life_sound.play()
        extra_life = score + 5000
        
    # if player exceeds high score, update high score    
    if score > high_score:
        if first_high_score:
            high_score_sound.play()
        high_score += rock_val
        first_high_score = False
    
    # draw rocks, missiles, and explosions if any
    process_sprite_group(rock_group, canvas)
    process_sprite_group(missile_group, canvas)
    process_sprite_group(explosion_group, canvas)
    
    # draw ship
    my_ship.draw(canvas)
    
    # update ship
    my_ship.update()
    
    # if asteroid collides with ship, subtract lives/restart game
    if group_collide(rock_group, my_ship):
        lives -= 1
        if lives == 0:
            started = False
            game_over_flag = True
            death_sound.play()
            soundtrack.rewind()
            
    # check if any missiles collide with any rocks        
    group_group_collide(rock_group, missile_group)

# timer handler that spawns a rock    
def rock_spawner():
    global a_rock, rock_group, vel_const
    if len(rock_group) <= 12:
        rock_pos = [random.randrange(0, WIDTH), random.randrange(0, HEIGHT)]
        rock_vel = [random.random() * vel_const - .3, random.random() * vel_const - .3]
        rock_avel = random.random() * .2 - .1
        a_rock = Sprite(rock_pos, rock_vel, 0, rock_avel, asteroid_image, asteroid_info)
        if dist(a_rock.pos, my_ship.pos) <= (a_rock.radius + my_ship.radius):
            return
        rock_group.add(a_rock)
    else:
        return
    
# draw all the sprites and if the sprite is a missile, remove it after its lifespan is over    
def process_sprite_group(group, canvas):
    for sprite in set(group):
        sprite.draw(canvas)
        if sprite.update():
            group.remove(sprite)
            
# check if an object collides with a sprite in a group        
def group_collide(group, other_object):
    global explosion_group
    collided = False
    
    for sprite in set(group):
        if sprite.collide(other_object):
            # draw different explosions depending on what object hits what
            if other_object.explosion == 1:
                explosion = Sprite(sprite.pos, [0,0], 0, 0, explosion_image1, explosion_info, explosion_sound)
                explosion_group.add(explosion)
            elif other_object.explosion == 2:
                explosion = Sprite(sprite.pos, [0,0], 0, 0, explosion_image2, explosion_info, explosion_sound)
                explosion_group.add(explosion)
                
            group.remove(sprite)
            collided = True
    
    return collided

# check if an object in a group collides with an object in another group
def group_group_collide(group1, group2):
    global score, rock_val, vel_const
    
    for sprite in set(group1):
        if group_collide(group2, sprite):
            group1.discard(sprite)
            # if the asteroid hit is a small asteroid, score + 50 and remove it
            if sprite.image_scale == [sprite.image_size[0]/2, sprite.image_size[1]/2]:
                score += 50
                rock_val = 50
            # otherwise it's a big asteroid, score + 100 and break it into 2 smaller asteroids
            else:
                score += 100
                rock_val = 100
                small_rock1 = Sprite(sprite.pos, [1.5*(random.random() * vel_const - .3), 1.5*(random.random() * vel_const - .3)], sprite.angle, random.random() * .2 - .1, asteroid_image, asteroid_info)
                small_rock2 = Sprite(sprite.pos, [1.5*(random.random() * vel_const - .3), 1.5*(random.random() * vel_const - .3)], sprite.angle, random.random() * .2 - .1, asteroid_image, asteroid_info)
                small_rock1.image_scale = [sprite.image_size[0]/2, sprite.image_size[1]/2]
                small_rock2.image_scale = [sprite.image_size[0]/2, sprite.image_size[1]/2]
                group1.add(small_rock1)
                group1.add(small_rock2)
            
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)
frame.add_label("Big asteroid +100 points")
frame.add_label("Small asteroid +50 points")
frame.add_label("Every 1000 points, asteroids start moving faster")
frame.add_label("Every 5000 points, +1 life")
               
# initialize ship and sprite groups
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
rock_group = set([])
missile_group = set([])
explosion_group = set([])

# register handlers
frame.set_keyup_handler(keyup)
frame.set_keydown_handler(keydown)
frame.set_mouseclick_handler(click)
frame.set_draw_handler(draw)

timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()