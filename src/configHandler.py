import json
import pathlib

__all__ = [
    "readConfig",
]

def readConfig(args: dict):
    if not pathlib.Path("config.json").exists():
        return args
    with open("config.json", "r") as f:
        configContents = f.read()
    configContents = json.loads(configContents)
    try:
        if not configContents["hatnotes"]:
            args["no_hatnotes"] = True
        if not configContents["prettify"]:
            args["make_pretty"] = False
        if not configContents["cites"]:
            args["no_cites"] = True
    except:
        pass
    return args
