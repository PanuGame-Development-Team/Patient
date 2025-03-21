from flask import *
from ui import *
from model import *
from lib import *
from constances import *
from settings import *
from datetime import datetime,timedelta
app = Blueprint("db_api","db_api",url_prefix="/api")
@app.route("/latestid",methods=["GET"])
@app.route("/latestid/",methods=["GET"])
@ACCESS_REQUIRE(["READ"])
def latestid(ses,user):
    return jsonify({"latestid":Data.query.count(),"status":"OK"})
@app.route("/data",methods=["GET"])
@app.route("/data/",methods=["GET"])
@ACCESS_REQUIRE(["READ"])
def data(ses,user):
    if lin(["date","machine","garage","range"],request.args):
        query = Data.query
        if request.args["date"]:
            date = datetime.strptime(request.args["date"],"%Y-%m-%d")
            query = query.filter(Data.created_time.between(date,date + timedelta(days=1)))
        if request.args["machine"]:
            query = query.filter(Data.machine_type==request.args["machine"])
        if request.args["garage"]:
            query = query.filter(Data.garage_id==request.args["garage"])
        if request.args["range"]:
            l,r = request.args["range"].split(",")
            if l == "undefined" or r == "undefined":
                return jsonify({"status":"No Range Data","data":[]}),400
            try:
                l = int(l)
                r = int(r)
            except TypeError:
                return jsonify({"status":"Bad Request","data":[]}),400
            if l > r:
                return jsonify({"status":"OK","data":[]})
            else:
                query = query.filter(Data.id.between(l,r))
        return jsonify({"status":"OK","data":[i.__todict__() for i in query.all()]})
    return jsonify({"status":"Bad Request","data":[]}),400
@app.route("/logging",methods=["GET"])
@app.route("/logging/",methods=["GET"])
@ACCESS_REQUIRE(["ADMIN"])
def get_logging(ses,user):
    if not lin(["limit","category"],request.args):
        return jsonify({"status":"Bad Request","data":[]}),400
    try:
        limit = int(request.args["limit"])
        category = int(request.args["category"])
    except ValueError:
        return jsonify({"status":"Bad Request","data":[]}),400
    if limit < 10 or limit > 300 or category < 0 or category > 5:
        return jsonify({"status":"Bad Request","data":[]}),400
    return jsonify({"status":"OK","data":[i.__todict__() for i in Logging.query.filter(Logging.category>=category).order_by(Logging.id.desc()).limit(limit).all()]})