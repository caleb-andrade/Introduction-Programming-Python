# template for "Stopwatch: The Game"
import simplegui

# define global variables
output = "00:00.0"
counter, x, y = 0, 0, 0
status = False

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    centisecond = str(t%10)
    second = str((t//10)%60)
    minute = str((t//600)%60)
    
    if (t//10)%60 < 10:
        second = str(0)+second
    if (t//600)%60 < 10:
        minute = str(0)+minute  
                
    return minute+":"+second+"."+centisecond
    
# define event handlers for buttons; "Start", "Stop", "Reset"
def start_timer():
    timer.start()
    global status, y
    if not status:
        y += 1
    status = True
    
        
def stop_timer():
    timer.stop()
    global status, x
    if format(counter)[-1] == "0" and status:
        x += 1
    status = False
    
def reset_timer():
    stop_timer()
    global output, counter, x, y
    output = "00:00.0"
    counter, x, y = 0, 0, 0

# define event handler for timer with 0.1 sec interval
def tick():
    global counter, output
    counter += 1
    output = format(counter)
    
# define draw handler
def draw(canvas):
    canvas.draw_text(output, [25, 120], 80, "white")
    canvas.draw_text("Score: "+str(x)+"/"+str(y), [100, 30], 40, "red") 

#Create frame
frame = simplegui.create_frame("Stopwatch", 300, 200)

# register event handlers
timer = simplegui.create_timer(100, tick)
frame.add_button("Start", start_timer,100)
frame.add_button("Stop", stop_timer,100)
frame.add_button("Reset", reset_timer,100)
frame.set_draw_handler(draw)

# start frame
frame.start()


# Please remember to review the grading rubric
