# implementation of card game - Memory

import simplegui
import random
exposed = [False for i in range(16)]
idx = []
state = 0
turns = 0

L1 = range(8)
L2 = range(8)

# helper function to initialize globals
def new_game():
    global L, exposed, idx, turns, state
    L = L1+ L2
    random.shuffle(L)
    exposed = [False for i in range(16)]
    idx = []
    turns = 0
    state = 0
    label.set_text('Turns = 0')
    pass  

     
# define event handlers
def mouseclick(pos):
    # add game state logic here
    global idx, state, turns
            
    cardIndex = pos[0]//50
    if state ==0:
        idx.append(cardIndex)
        flag = True
    elif not exposed[cardIndex]:
        idx.append(cardIndex)
        flag = True
        turns += 1
        label.set_text('Turns = '+str((turns+1)//2))
    else:
        flag = False
    exposed[cardIndex] = True
    
    if state == 0:
        state = 1
    elif state == 1 and len(idx) > 1:
        state = 2
    elif state == 2 and flag:
        if L[idx[0]] != L[idx[1]]:
            exposed[idx[0]] = False
            exposed[idx[1]] = False
        idx = []
        idx.append(cardIndex)
        state = 1
        flag = True
                         
# cards are logically 50x100 pixels in size    
def draw(canvas):
    for i in range(16):
        canvas.draw_text(str(L[i]), [50*i, 85], 100, "white")
    for i in range(16):
        if not exposed[i]:
            canvas.draw_polygon([[i*50,0], [(i+1)*50,0], [(i+1)*50, 100], [i*50, 100]], 2, "black", "green")
            


# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label('Turns = 0')

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()


# Always remember to review the grading rubric