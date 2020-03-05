import arena
import json

# Have https://arena-west1.conix.io/?scene=synchvideo
# open before running this script

def callback(msg):
    jsonMsg = json.loads(msg)
    if jsonMsg["action"] != "clientEvent":
        return
    if jsonMsg["object_id"] == "videoscreen":
        print(jsonMsg["type"])

arena.init(
    "arena-west1.conix.io",
    "realm",
    "synchvideo",
    port = 3003,
    callback = callback,
)
arena.Object(
    objName = "videoscreen",
    objType = arena.Shape.cube,
    scale = (16, 9, 0.1),
    location = (0, 5, -15),
    data = '{"material": {"src": "images/360falls.mp4"}}',
    clickable = True,
)
arena.handle_events()
