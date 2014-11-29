# Implementation of classic arcade game Pong

import simplegui
import random


WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
PAD_VELOCITY = 5
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True


def spawn_ball(direction):
    global ball_pos, ball_vel
    
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    ball_vel = [random.randrange(120, 240), random.randrange(60, 180)]
    ball_vel = [2, 2]
    
    if direction == LEFT:
        ball_vel[0] = - ball_vel[0]
        ball_vel[1] = - ball_vel[1]
    elif direction == RIGHT:
        ball_vel[1] = - ball_vel[1]


def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel
    global score1, score2
    
    spawn_ball(RIGHT)
    
    paddle1_pos = 0
    paddle1_vel = 0
    paddle2_pos = 0
    paddle2_vel = 0
    score1 = 0
    score2 = 0


def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
        
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    
    if ((ball_pos[1] <= BALL_RADIUS) or 
        (ball_pos[1] >= HEIGHT - 1 - BALL_RADIUS)):
        ball_vel[1] = - ball_vel[1]
    elif ball_pos[0] - PAD_WIDTH <= BALL_RADIUS:
        
        if (ball_pos[1] >= paddle1_pos and
           ball_pos[1] <= paddle1_pos + PAD_HEIGHT):
            ball_vel[0] *=  -1.1
            ball_vel[1] *= 1.1
        else:
            score2 += 1
            spawn_ball(RIGHT)
            
    elif ball_pos[0] >= WIDTH - PAD_WIDTH - 1 - BALL_RADIUS:
        
        if (ball_pos[1] >= paddle2_pos and
           ball_pos[1] <= paddle2_pos + PAD_HEIGHT):
            ball_vel[0] *=  -1.1
            ball_vel[1] *= 1.1
        else:
            score1 += 1
            spawn_ball(LEFT)
        
    canvas.draw_circle(ball_pos, BALL_RADIUS, 1, "White", "White")
    
    # Paddles
    if (paddle1_pos + paddle1_vel >= 0 and
        paddle1_pos + paddle1_vel <= HEIGHT - PAD_HEIGHT):
        paddle1_pos += paddle1_vel
    
    if (paddle2_pos + paddle2_vel >= 0 and 
        paddle2_pos + paddle2_vel <= HEIGHT - PAD_HEIGHT):
        paddle2_pos += paddle2_vel 
        
    canvas.draw_line((HALF_PAD_WIDTH, paddle1_pos),
                     (HALF_PAD_WIDTH, paddle1_pos + PAD_HEIGHT),
                     PAD_WIDTH, "White")

    canvas.draw_line((WIDTH - HALF_PAD_WIDTH, paddle2_pos),
                     (WIDTH - HALF_PAD_WIDTH, paddle2_pos + PAD_HEIGHT),
                     PAD_WIDTH, "White")
    
    # Score:
    canvas.draw_text(str(score1), (WIDTH // 4, HEIGHT / 2), 50, "White", "serif")
    canvas.draw_text(str(score2), (WIDTH // 4 * 3, HEIGHT / 2), 50, "White", "serif")


def keydown(key):
    global paddle1_vel, paddle2_vel
    
    if key == simplegui.KEY_MAP['w']:
        paddle1_vel -= PAD_VELOCITY
    elif key == simplegui.KEY_MAP['s']:
        paddle1_vel += PAD_VELOCITY
    elif key == simplegui.KEY_MAP['up']:
        paddle2_vel -= PAD_VELOCITY
    elif key == simplegui.KEY_MAP['down']:
        paddle2_vel += PAD_VELOCITY
       

def keyup(key):
    global paddle1_vel, paddle2_vel
    
    if key in (simplegui.KEY_MAP['w'], simplegui.KEY_MAP['s']):
        paddle1_vel = 0
    elif key in (simplegui.KEY_MAP['up'], simplegui.KEY_MAP['down']):
        paddle2_vel = 0

        
# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("Restart", new_game, 100)


# start frame
new_game()
frame.start()
