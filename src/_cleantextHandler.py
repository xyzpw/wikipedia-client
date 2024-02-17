import re

def removeHatnotes(pageContent: str) -> str:
    return re.sub(r"(?:\{\{(?!cite).*?\}\})", '', pageContent, flags=(re.DOTALL | re.IGNORECASE))

def removeCites(pageContent: str) -> str:
    return re.sub(r"(?:\{\{cite.*?\}\})|(?:\{\{#tag:ref(?:.*?)\}\})", '', pageContent, flags=(re.DOTALL | re.IGNORECASE))

def removeSelected(pageContent: str, cites=False, hatnotes=False):
    if cites:
        pageContent = removeCites(pageContent)
    if hatnotes:
        pageContent = removeHatnotes(pageContent)
    return pageContent
