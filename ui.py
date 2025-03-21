from lib import *
from settings import *
from constances import *
from model import *
def default_dict(session,request,loginpage=False):
    dic = dict()
    dic["loginpage"] = loginpage
    if loginpage:
        dic["firstvisit"] = False
    elif session.get("onevisit"):
        dic["firstvisit"] = False
    else:
        dic["firstvisit"] = True
        session["onevisit"] = True
        saveSession(request.cookies.get("sessionid"),session)
    
    dic["APP_NAME"] = APP_NAME
    dic["APP_VERSION"] = APP_VERSION
    dic["APP_VERSYM"] = APP_VERSYM
    dic["CATEGORIES"] = CATEGORIES
    dic["SHOW_COLOR"] = SHOW_COLOR
    dic["ACCESS"] = ACCESS
    
    dic["GARAGE_AVAILABLE"] = GARAGE_AVAILABLE
    dic["TYPE_OF_MACHINE"] = TYPE_OF_MACHINE
    
    dic["split_access"] = split_access
    return dic