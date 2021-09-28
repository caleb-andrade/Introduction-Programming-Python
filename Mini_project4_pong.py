# Implementation of classic arcade game Pong

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
p1_key = 0
p2_key = 0
score = [0,0]
factor = 1

# initialize ball_pos and ball_vel for new bal in middle of table
ball_vel = [1, 1]
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    global factor
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    ball_vel = [float(random.randrange(120, 240))/60,-float(random.randrange(60, 180))/60]
    factor += 0.1 
    ball_vel = [factor*ball_vel[0], factor*ball_vel[1]]
    if not direction:
        ball_vel[0] = -ball_vel[0]

# define event handlers
def new_game():
    global pad1_pos, pad2_pos, paddle1_vel, paddle2_vel, factor  # these are numbers
    global score1, score2  # these are ints
    paddle1_vel = 0
    paddle2_vel = 0
    pad1_pos = HEIGHT / 2
    pad2_pos = HEIGHT / 2
    p1_key = 0
    p2_key = 0
    score[0] = score[1] = 0
    spawn_ball([LEFT, RIGHT][random.randrange(0,2)])
    factor = 1

def draw(canvas):
    global score1, score2, pad1_pos, pad2_pos, ball_pos, ball_vel
      
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
            
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 1, "white", "white")
    
    # update paddle's vertical position, keep paddle on the screen
    pad1_pos = pad1_pos + paddle1_vel
    if pad1_pos <= PAD_HEIGHT / 2:
        pad1_pos = PAD_HEIGHT / 2
    elif pad1_pos >= HEIGHT - (1 + PAD_HEIGHT / 2):
        pad1_pos = HEIGHT - (1 + PAD_HEIGHT / 2)
    
    pad2_pos = pad2_pos + paddle2_vel
    if pad2_pos <= PAD_HEIGHT / 2:
        pad2_pos = PAD_HEIGHT / 2
    elif pad2_pos >= HEIGHT - (1 + PAD_HEIGHT / 2):
        pad2_pos = HEIGHT - (1 + PAD_HEIGHT / 2)
        
    # determine whether the ball collides with top and bottom
    if ball_pos[1] >= HEIGHT-(1 + BALL_RADIUS) or ball_pos[1] <= BALL_RADIUS:
        ball_vel[1] = -ball_vel[1]
    
    # determine whether the ball collides with the glutter or paddle
    if ball_pos[0] <= BALL_RADIUS + PAD_WIDTH:
        if pad1_pos - PAD_HEIGHT / 2 < ball_pos[1] < pad1_pos + PAD_HEIGHT / 2:
            ball_vel[0] = -ball_vel[0]
        else:
            spawn_ball(RIGHT)
            score[1] += 1
    if ball_pos[0] >= WIDTH - (BALL_RADIUS + PAD_WIDTH):
        if pad2_pos - PAD_HEIGHT / 2 < ball_pos[1] < pad2_pos + PAD_HEIGHT / 2:
            ball_vel[0] = -ball_vel[0]
        else:
            spawn_ball(LEFT)
            score[0] += 1
               
    # draw paddles
    canvas.draw_polygon([[0, pad1_pos + PAD_HEIGHT / 2], [PAD_WIDTH, pad1_pos + PAD_HEIGHT / 2],[PAD_WIDTH, pad1_pos - PAD_HEIGHT / 2], [0, pad1_pos - PAD_HEIGHT / 2]],2 , "Blue", "Blue")
    canvas.draw_polygon([[WIDTH - (PAD_WIDTH + 1), pad2_pos + PAD_HEIGHT / 2], [WIDTH - 1, pad2_pos + PAD_HEIGHT / 2], [WIDTH - 1, pad2_pos - PAD_HEIGHT / 2], [WIDTH - (PAD_WIDTH + 1), pad2_pos - PAD_HEIGHT / 2]], 2, "red", "red")
 
    # draw scores
    canvas.draw_text(str(score[0]), [250,50], 40, "blue")
    canvas.draw_text(str(score[1]), [350,50], 40, "red")    
    
def keydown(key):
    global paddle1_vel, paddle2_vel, p1_key, p2_key
    if key==simplegui.KEY_MAP["w"]:
        paddle1_vel -= 7
        p1_key = 1
    if key==simplegui.KEY_MAP["s"]:
        paddle1_vel += 7
        p1_key = 2
    if key==simplegui.KEY_MAP["up"]:
        paddle2_vel -= 7
        p2_key = 3
    if key==simplegui.KEY_MAP["down"]:
        paddle2_vel += 7
        p2_key = 4
            
def keyup(key):
    global paddle1_vel, paddle2_vel, p1_key, p2_key
    if p1_key == 1:
        paddle1_vel = 0
        p1_key = 0
    if p1_key == 2:
        paddle1_vel = 0
        p1_key = 0
    if p2_key == 3:
        paddle2_vel = 0
        p2_key = 0
    if p2_key == 4:
        paddle2_vel = 0   
        p2_key = 0
        
# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("Restart", new_game, 150)


# start frame
new_game()
frame.start()
