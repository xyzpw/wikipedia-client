import re
from src import _hatnoteHandler

taxbox = [
    "infobox",
    "drugbox",
    "chembox",
    "automatic taxobox",
    "speciesbox",
    "subspeciesbox",
    "infraspeciesbox",
    "hybridbox",
    "ichnobox",
    "oobox",
    "virusbox",
    "paraphyletic group",
    "population taxobox",
]
boxlist = ''
for box in taxbox:
    if taxbox.index(box) == len(taxbox) - 1:
        boxlist += box
    else:
        boxlist += str(box) + '|'


def hatnoteExist(hatnoteName: str, pageContent: str) -> bool:
    if bool(re.search(r"\{\{"+hatnoteName+r"(?:\|(?:.*?))?\}\}", pageContent, re.DOTALL | re.MULTILINE)):
        return True
    return False

def lookupHatnoteContent(hatnoteName: str, pageContent) -> str:
    hatnoteSearch = re.search(r"(?:(?<=\{\{)"+hatnoteName+r"\|)(?P<txt>.*?)(?=\}\})", pageContent, re.DOTALL)
    if bool(hatnoteSearch):
        return hatnoteSearch.group("txt")
    return ''

def removeNbsp(pageContent: str) -> str:
    return re.sub(r"\{\{nbsp\}\}", ' ', pageContent)

def getInfoboxName(pageContent: str) -> str:
    # infoboxSearch = re.search(r"^\{\{infobox\s(?P<name>.*?)$", pageContent, flags=(re.DOTALL | re.MULTILINE | re.IGNORECASE))
    # infoboxSearch = re.search(r"^\{\{(?:infobox|drugbox|chembox|speciesbox)(?=\s)(?P<name>.*?)$", pageContent, flags=(re.DOTALL | re.MULTILINE | re.IGNORECASE))
    infoboxSearch = re.search(r"^\{\{(?:"+boxlist+r")(?=\s)(?P<name>.*?)$", pageContent, flags=(re.DOTALL | re.MULTILINE | re.IGNORECASE))
    if not bool(infoboxSearch):
        raise Exception("could not find infobox name")
    else:
        infoboxName = infoboxSearch.group("name").lstrip()
        return infoboxName

def getInfoboxContent(pageContent) -> str:
    # infoboxSearch = re.search(r"(?:\{\{(?:Infobox|drugbox|chembox|speciesbox).*?\n)(?P<box>\|.*?(?=\n\}\}))", pageContent, flags=(re.DOTALL | re.IGNORECASE | re.MULTILINE))
    infoboxSearch = re.search(r"(?:\{\{(?:"+boxlist+r").*?\n)(?P<box>\|.*?(?=\n\}\}))", pageContent, flags=(re.DOTALL | re.IGNORECASE | re.MULTILINE))
    if bool(infoboxSearch):
        infoboxContent = infoboxSearch.group("box")
        return infoboxContent
    raise Exception("could not find infobox content")

def removeHatnote(hatnoteName, pageContent) -> str:
    return re.sub(r"(?:\{\{"+hatnoteName+r"(?:\|(?:.*?))?)\}\}", '', pageContent, re.DOTALL)

def removeUnwantedModules(pageContent) -> str:
    pageContent = re.sub(r"\{\{other uses\}\}", '', pageContent, flags=(re.DOTALL | re.IGNORECASE))
    pageContent = re.sub(r"\{\{use \w+ date(?:s)?.*?\}\}", '', pageContent, flags=(re.DOTALL | re.IGNORECASE))
    pageContent = re.sub(r"\{\{pp-?(?:.*?)\}\}", '', pageContent, flags=(re.DOTALL | re.IGNORECASE))
    pageContent = re.sub(r"\{\{anchor(?:.*?)\}\}", '', pageContent, flags=(re.DOTALL | re.IGNORECASE))
    pageContent = re.sub(r"\{\{cs1 config(?:.*?)\}\}", '', pageContent, flags=(re.DOTALL | re.IGNORECASE))
    pageContent = re.sub(r"\{\{good article(?:.*?)\}\}", '', pageContent, flags=(re.DOTALL | re.IGNORECASE))
    pageContent = re.sub(r"\{\{use\s(?:.*?)\}\}", '', pageContent, flags=(re.DOTALL | re.IGNORECASE))
    pageContent = re.sub(r"\{\{featured article\}\}", '', pageContent, flags=(re.DOTALL | re.IGNORECASE))
    pageContent = re.sub(r"\{\{sprotect(?:.*?)\}\}", '', pageContent, flags=(re.DOTALL | re.IGNORECASE))
    return pageContent

def makePretty(pageTitle, pageContent) -> str:
    pageContent = removeNbsp(pageContent)
    aboutPage = _hatnoteHandler.aboutHatnoteText(pageTitle, pageContent)
    if bool(aboutPage):
        hatnoteMatch = re.search(r"(?P<all>\{\{about\|(?:.*?)\}\})", pageContent, flags=(re.DOTALL | re.IGNORECASE)).group("all")
        pageContent = pageContent.replace(hatnoteMatch, aboutPage)
    pageContent = _hatnoteHandler.removeShortDescription(pageContent)
    pageContent = removeUnwantedModules(pageContent)
    pageContent = _hatnoteHandler.replaceMainHatnotes(pageContent)
    pageContent = _hatnoteHandler.removeFiles(pageContent) #limited function
    distinguishText = _hatnoteHandler.distinguishHatnoteText(pageContent)
    if bool(distinguishText):
        hatnoteMatch = re.search(r"\{\{distinguish\|(?:.*?)\}\}", pageContent, flags=(re.DOTALL | re.IGNORECASE)).group(0)
        pageContent = pageContent.replace(hatnoteMatch, distinguishText)
    forHatnoteText = _hatnoteHandler.forHatnoteText(pageContent)
    if bool(forHatnoteText):
        hatnoteMatch = re.search(r"\{\{for\|(?:.*?)\|(?:.*?)\}\}", pageContent, flags=(re.DOTALL | re.IGNORECASE)).group(0)
        pageContent = pageContent.replace(hatnoteMatch, forHatnoteText)
    return pageContent.lstrip()

