from django.contrib.messages.api import get_messages
from django.contrib.messages import DEFAULT_LEVELS
from .constants import *
def bsprocessmessage(message):
    if message.level == DEFAULT_LEVELS["ERROR"]:
        return ["danger",message]
    elif message.level == DEFAULT_LEVELS["WARNING"]:
        return ["warning",message]
    elif message.level == DEFAULT_LEVELS["SUCCESS"]:
        return ["success",message]
    elif message.level == DEFAULT_LEVELS["INFO"]:
        return ["info",message]
    elif message.level == DEFAULT_LEVELS["DEBUG"]:
        return ["secondary",message]
def default_dict(request,origdic=dict()):
    dic = origdic
    messages = get_messages(request)
    dic["messages"] = []
    for message in messages:
        dic["messages"].append(bsprocessmessage(message))
    dic["APP_NAME"] = APP_NAME
    dic["APP_VERSION"] = APP_VERSION
    dic["APP_VERSYM"] = APP_VERSYM
    dic["CATEGORIES"] = CATEGORIES
    dic["S2NCATEGORY"] = S2NCATEGORY
    dic["SHOW_COLOR"] = SHOW_COLOR
    dic["ACCESS"] = ACCESS
    if request.session.get("firstvisit"):
        dic["firstvisit"] = True
        request.session.pop("firstvisit")
    return dic