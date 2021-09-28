# SimpleGUI program template

# Import the module
import simplegui

# Define global variables (program state)
counter = 0
output = "00:00:00"

# Define "helper" functions
def increment():
    global counter
    counter +=1
    
def time_format(t):
    milisecond = str(t%100)
    second = str((t//100)%60)
    minute = str((t//6000)%60)
    
    if t%100 < 10:
        milisecond = str(0)+milisecond
    if (t//100)%60 < 10:
        second = str(0)+second
    if (t//6000)%60 < 10:
        minute = str(0)+minute  
                
    return minute+":"+second+":"+milisecond
    
# Define event handler functions
def tick():
    increment()
    global output
    output = time_format(counter)
    
def start_timer():
    timer.start()

def stop_timer():
    timer.stop()

def reset_timer():
    global output
    global counter
    output = "00:00:00"
    counter = 0
    
def draw(canvas):
    canvas.draw_text(output, [75,275], 250, "white")
    

# Create a frame
frame = simplegui.create_frame("SimpleGui Test", 1050, 400)

# Register event handlers
timer = simplegui.create_timer(10, tick)
frame.add_button("Start", start_timer)
frame.add_button("Stop", stop_timer)
frame.add_button("Reset", reset_timer)
frame.set_draw_handler(draw)


# Start frame 
frame.start()


