import json

def getErrorDetails(requestText: str) -> str | bool:
    error_details = json.loads(requestText).get("detail")
    return error_details
