# Implementation of classic arcade game Pong
# Two problems remain – ball spawns down instead of up
# and ball alternates rather than going toward last winner

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
paddle_vel = 3
score1 = 0
score2 = 0

# initialize ball_pos and ball_vel for new ball in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
    
def spawn_ball(direction):
# If RIGHT is True, spawn ball in opposite direction, else stay the same direc.
    global ball_pos, ball_vel
    global WIDTH, HEIGHT, RIGHT
    RIGHT = direction
    ball_pos = [WIDTH/2, HEIGHT/2]
    ball_vel = [random.randrange(3, 5), random.randrange(-3, 3)]
    if ball_vel[0]==0:
        ball_vel[0]=-1
    if ball_vel[1]==0:
        ball_vel[1]=-1
        
    if RIGHT == True:
        ball_vel[0] *= 1
    elif LEFT == True:
        ball_vel[0] *= -1

# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel 
    global score1, score2 
    score1 = 0
    score2 = 0
    paddle1_pos = HEIGHT/2
    paddle2_pos = HEIGHT/2
    paddle1_vel = 0
    paddle2_vel = 0
    spawn_ball(RIGHT)
    
def draw(c):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
    global paddle1_vel, paddle2_vel, RIGHT, LEFT
    
   
    # draw mid line and gutters
    c.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    c.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    c.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    ball_pos[0]+= ball_vel[0]
    ball_pos[1]+= ball_vel[1]
    # reflect off of top and bottom
    if ball_pos[1] >= HEIGHT - BALL_RADIUS:
        ball_vel[1] *= -1
    elif ball_pos[1] <= BALL_RADIUS:
        ball_vel[1] *= -1
    # reflect if ball hits paddles
    if ball_pos[0] >= (WIDTH - BALL_RADIUS - PAD_WIDTH) or ball_pos[0] <= (BALL_RADIUS + PAD_WIDTH):
        if paddle1_pos < ball_pos[1] < paddle1_pos+ PAD_HEIGHT and ball_vel[0] < 0:
            ball_vel[0] *= -1 if (ball_vel[0]>9 or ball_vel[0]<-9) else -1.2
            ball_vel[1] *= 1 if (ball_vel[1]>9 or ball_vel[1]<-9) else 1.2
        elif paddle2_pos < ball_pos[1] < paddle2_pos + PAD_HEIGHT and ball_vel[0] > 0:
            ball_vel[0] *= -1 if (ball_vel[0]>9 or ball_vel[0]<-9) else -1.2
            ball_vel[1] *= 1 if (ball_vel[1]>9 or ball_vel[1]<-9) else 1.2
        else:    # ball hits gutter and opponent scores
            if ball_vel[0] > 0:
                score1 += 1
                RIGHT = False
                LEFT = True
            else:
                score2 += 1
                RIGHT = True
                LEFT = False
            spawn_ball(RIGHT)
            
    # draw ball
    c.draw_circle(ball_pos, BALL_RADIUS, 1, "Yellow", "Yellow")
    
    # update paddle's vertical position, keep paddle on the screen
    if (paddle1_pos <= HEIGHT - PAD_HEIGHT) or (paddle1_pos >=0):
        paddle1_pos += paddle1_vel
    if (paddle2_pos <= HEIGHT - PAD_HEIGHT) or (paddle2_pos >=0):
        paddle2_pos += paddle2_vel
        
    if paddle1_pos>HEIGHT-PAD_HEIGHT:
        paddle1_pos=HEIGHT-PAD_HEIGHT
    if paddle1_pos<0:
        paddle1_pos=0
    if paddle2_pos>HEIGHT-PAD_HEIGHT:
        paddle2_pos=HEIGHT-PAD_HEIGHT
    if paddle2_pos<0:
        paddle2_pos=0
    
    # draw paddles
    c.draw_polygon([[0, paddle1_pos], [PAD_WIDTH, paddle1_pos], [PAD_WIDTH, (paddle1_pos)+PAD_HEIGHT], [0, (paddle1_pos)+PAD_HEIGHT]], 1, "White", "White")
    c.draw_polygon([[WIDTH, paddle2_pos], [WIDTH - PAD_WIDTH, paddle2_pos], [WIDTH - PAD_WIDTH, (paddle2_pos)+PAD_HEIGHT], [WIDTH, (paddle2_pos)+PAD_HEIGHT]], 1, "White", "White")
    
    # draw scores
    c.draw_text(str(score1), [(WIDTH/2 - 55), 50], 40, "White")
    c.draw_text(str(score2), [(WIDTH/2 + 35), 50], 40, "White")
        
def keydown(key):
    global paddle1_vel, paddle2_vel,paddle_vel
    
    if key == simplegui.KEY_MAP["down"]:
        paddle2_vel = paddle_vel
    elif key == simplegui.KEY_MAP["up"]:
        paddle2_vel = -paddle_vel
   
    if key == simplegui.KEY_MAP["s"]:
        paddle1_vel = paddle_vel
    elif key == simplegui.KEY_MAP["w"]:
        paddle1_vel = -paddle_vel
        
def keyup(key):
    global paddle1_vel, paddle2_vel
    
    if key == simplegui.KEY_MAP["down"] or key == simplegui.KEY_MAP["up"]:
        paddle2_vel = 0
   
    elif key == simplegui.KEY_MAP["s"] or key == simplegui.KEY_MAP["w"]:
        paddle1_vel = 0

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
start_btn = frame.add_button("Restart", new_game, 100)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)


# start frame
new_game()
frame.start()