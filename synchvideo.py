import arena
import json
import math
import time

is_video_playing = False
video_play_timestamp = 0
video_pause_timestamp = 0
video_paused_by = None

def callback(msg):
    global is_video_playing
    global video_play_timestamp
    global video_pause_timestamp
    global video_paused_by

    jsonMsg = json.loads(msg)

    if jsonMsg["action"] != "clientEvent":
        return
    if jsonMsg["object_id"] != "videoscreen":
        return

    print(msg)

    if jsonMsg["type"] != "mouseup":
        return

    is_video_playing = not is_video_playing
    if is_video_playing:
        video_play_timestamp = time.time() - (video_pause_timestamp - video_play_timestamp)
    else:
        video_pause_timestamp = time.time()
        video_paused_by = jsonMsg["data"]["source"]

arena.init(
    "oz.andrew.cmu.edu",
    "realm",
    "synchvideoscene",
    callback = callback,
)

screen = arena.Object(
    objName = "videoscreen",
    objType = arena.Shape.cube,
    scale = (16, 9, 0.1),
    location = (0, 7.2, -15),
    data = '{"material": {"src": "//commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4"}}',
    clickable = True
)

status = arena.Object(
    objName = "videostatus",
    objType = arena.Shape.text,
    location = (0, 12.4, -15),
    rotation = (0, 0, 0, 1),
    scale = (4, 4, 4)
)

timeline = arena.Object(
    objName = "videotimeline",
    objType = arena.Shape.text,
    location = (0, 2.2, -15),
    rotation = (0, 0, 0, 1),
    scale = (4, 4, 4)
)


def format_time_component (value):
    value = math.floor(value)
    return f"{value:02d}"

def format_timestamp (time_value):
    time_value = math.floor(time_value)

    time_seconds = time_value % 60
    time_value -= time_seconds
    time_value /= 60

    time_minutes = time_value % 60
    time_value -= time_minutes
    time_value /= 60

    time_hours = time_value

    return f"{math.floor(time_hours)}:{format_time_component(time_minutes)}:{format_time_component(time_seconds)}"

while True:
    if is_video_playing:
        state = "playing"
        position = time.time() - video_play_timestamp

        status_text = "Playing"
    else:
        state = "paused"
        position = video_pause_timestamp - video_play_timestamp

        status_text = "Paused"
        if video_paused_by is not None:
            status_text += " by " + video_paused_by

    screen.redraw()
    screen.update_video(state=state, position=position)

    status.update(data=json.dumps({
        "color": "white",
        "text": status_text
    }))

    timeline.update(data=json.dumps({
        "color": "white",
        "text": format_timestamp(position)
    }))

    arena.flush_events()
    time.sleep(0.1)
