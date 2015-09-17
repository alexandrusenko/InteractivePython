import simplegui
time = 0
x = 0
y = 0

def format(t):
    a = t % 10
    b = t / 10
    c = 0
    cnt = b / 60
    if cnt > 0:
        b = b - (cnt * 60)
        c = cnt
    return "%d:%02d.%d" % (c, b, a)
    

def start_handler():
    timer.start()


def stop_handler():
    global time, x, y
    if(time % 10 == 0):
        x += 1
    y += 1
    timer.stop()


def reset_handler():
    global time, x, y
    time = 0
    x = 0
    y = 0


def timer_handler():
    global time
    time += 1


def draw_handler(canvas):
    canvas.draw_text(format(time), (40, 125), 50, 'White')
    canvas.draw_text("%d/%d" % (x, y), (150, 30), 25, 'White')


frame = simplegui.create_frame("Stopwatch: The Game", 200, 200)

frame.add_button("Start", start_handler)
frame.add_button("Stop", stop_handler)
frame.add_button("Reset", reset_handler)
frame.set_draw_handler(draw_handler)
timer = simplegui.create_timer(100, timer_handler)

frame.start()