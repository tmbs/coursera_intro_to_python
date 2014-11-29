# Stopwatch: The Game

import simplegui

RESOLUTION_MS = 100 # stopwatch resolution in milliseconds
COLOR_ACTIVE = "#FCB03C"
COLOR_INACTIVE = "#068587"

elapsed_time = 0
reflex_stops = 0
total_stops = 0
start_button_color = COLOR_INACTIVE
stop_button_color = COLOR_INACTIVE


def format_output(time_ms):
    """ Formats elapsed time in a A:BC.D format. """
    
    deciseconds = str(time_ms % 1000 // 100)
    
    seconds = str(time_ms // 1000 % 60)
    if len(seconds) < 2:
        seconds = "0" + seconds
        
    minutes = str(time_ms // 1000 // 60)
    
    return minutes + ":" + seconds + "." + deciseconds


def start_handler():
    """
    Start button handler,
    changes canvas button colors and starts the timer.
    """
    
    global start_button_color, stop_button_color
    
    start_button_color = COLOR_ACTIVE
    stop_button_color = COLOR_INACTIVE
    
    timer.start()


def stop_handler():
    """
    Stop button handler,
    changes canvas button colors and stops the timer.
    """
    
    global start_button_color, stop_button_color
    global reflex_stops, total_stops
    
    if timer.is_running():
        start_button_color = COLOR_INACTIVE
        stop_button_color = COLOR_ACTIVE
        
        total_stops += 1
        if elapsed_time % 1000 == 0:
            reflex_stops += 1
    
    timer.stop()


def reset_handler():
    """
    Reset button handler,
    changes canvas button colors, and resets the timer,
    stops counters too.
    """
    
    global elapsed_time, start_button_color, stop_button_color
    global reflex_stops, total_stops
    
    start_button_color = COLOR_INACTIVE
    stop_button_color = COLOR_INACTIVE
    
    elapsed_time = 0
    reflex_stops = 0
    total_stops = 0
    
    timer.stop()


def timer_handler():
    """ Measures elapsed time. """
    
    global elapsed_time
    
    elapsed_time += RESOLUTION_MS


def draw_handler(canvas):
    """ Draws a stylised stopwatch on the canvas. """
    
    stops_summary = str(reflex_stops) + "/" + str(total_stops)
    
    canvas.draw_line((150, 60), (150, 150), 10, start_button_color)
    canvas.draw_line((90, 90), (150, 150), 10, stop_button_color)
    canvas.draw_circle((150, 150), 60, 5, "#068587", "#112F41")
    
    canvas.draw_text(stops_summary, (136, 125), 15, "#FC5B3F", "monospace")
    canvas.draw_text(format_output(elapsed_time), (105, 158), 24, "#6FB07F", "monospace")


stopwatch = simplegui.create_frame("Stopwatch", 300, 300)
stopwatch.add_button("Start", start_handler, 100)
stopwatch.add_button("Stop", stop_handler, 100)
stopwatch.add_button("Reset", reset_handler, 100)
stopwatch.set_draw_handler(draw_handler)

timer = simplegui.create_timer(RESOLUTION_MS, timer_handler)

stopwatch.start()
