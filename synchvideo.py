import arena
import json
import time

is_video_playing = False
video_play_timestamp = 0
video_pause_timestamp = 0

def callback(msg):
    global is_video_playing
    global video_play_timestamp
    global video_pause_timestamp

    jsonMsg = json.loads(msg)

    if jsonMsg["action"] != "clientEvent":
        return
    if jsonMsg["object_id"] != "videoscreen":
        return
    if jsonMsg["type"] != "mouseup":
        return

    is_video_playing = not is_video_playing
    if is_video_playing:
        video_play_timestamp = time.time() - (video_pause_timestamp - video_play_timestamp)
    else:
        video_pause_timestamp = time.time()

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
    location = (0, 5, -15),
    data = '{"material": {"src": "//commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4"}}',
    clickable = True
)

while True:
    if is_video_playing:
        state = "playing"
        position = time.time() - video_play_timestamp
    else:
        state = "paused"
        position = video_pause_timestamp - video_play_timestamp
    screen.redraw()
    screen.update_video(state=state, position=position)

    arena.flush_events()
    time.sleep(0.1)
