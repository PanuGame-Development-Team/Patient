from flask import *
from ui import *
from model import *
from lib import *
from constances import *
from settings import *
app = Blueprint("admin","admin",url_prefix="/admin")
@app.route("/",methods=["GET"])
@ACCESS_REQUIRE_HTML(["ADMIN"])
def index(ses,user):
    return render_template("admin/index.html",headertype="admin",**default_dict(session,request))