from flask import *
from ui import *
from model import *
from lib import *
from constances import *
from settings import *
from api import app as api_blueprint
from admin import app as admin_blueprint
app = Flask(APP_NAME)
app.secret_key = SECRET_KEY
for conf in CONFIG:
    app.config[conf] = CONFIG[conf]
db.init_app(app)
app.register_blueprint(api_blueprint)
app.register_blueprint(admin_blueprint)
@app.route("/",methods=["GET"])
def index():
    ses = readSession(request.cookies)
    if ses[0] == -1:
        return redirect("/login/")
    user = User.query.get(ses[0])
    return render_template("index.html",headertype="root",user=user,**default_dict(ses[1],request))
@app.route("/login",methods=["GET","POST"])
@app.route("/login/",methods=["GET","POST"])
def login():
    ses = readSession(request.cookies)
    if ses[0] != -1:
        return redirect("/")
    if request.method == "GET":
        return render_template("login.html",**default_dict(ses[1],request,True))
    else:
        if lin(["username","password"],request.form):
            user = User.query.filter_by(username=request.form["username"]).first()
            if user:
                if check_password_hash(user.password,request.form["password"]):
                    user.latest_login_time = datetime.now()
                    db.session.add(user)
                    db.session.commit()
                    res = redirect("/")
                    res.set_cookie("sessionid",createSession(user.id,{}),max_age=8640000)
                    return res
                else:
                    flash("密码错误，请重新输入。","danger")
                    return redirect("/login/")
            elif len(request.form["username"]) >= 4 and len(request.form["username"]) <= 32:
                if len(request.form["password"]) >= 8:
                    user = User()
                    user.username = request.form["username"]
                    user.password = generate_password_hash(request.form["password"])
                    user.access = 0
                    db.session.add(user)
                    db.session.commit()
                    flash("注册成功，请重新登录","success")
                    return redirect("/login/")
                else:
                    flash("密码长度必须大于8位。","danger")
                    return redirect("/login/")
            else:
                flash("用户名长度必须在4-32位之间。","danger")
                return redirect("/login/")
        else:
            flash("表单信息不全，请重新输入。","danger")
            return redirect("/login/")
@app.route("/write/new",methods=["GET","POST"])                             # 图片添加按钮
@app.route("/write/new/",methods=["GET","POST"])
@app.route("/update/<int:postid>",methods=["GET","POST"])
@app.route("/update/<int:postid>/",methods=["GET","POST"])
@ACCESS_REQUIRE_HTML(["UPDATE"])
def write(ses,user,postid = -1):
    data = Data.query.get(postid)
    if not data:
        data = Data()
        data.uid = ses[0]
        data.machine_type = ""
        data.garage_id = ""
        data.error_id = ""
        data.detail = ""
        data.errdate = datetime.today()
    if data.uid != ses[0]:
        flash("您没有权限修改他人成果。","danger")
        return redirect("/")
    if request.method == "GET":
        return render_template("write.html",headertype="write",data=data,**default_dict(ses[1],request))
    else:
        if lin(["machine_type","garage_id","error_id","detail","errdate"],request.form):
            data.machine_type = request.form["machine_type"]
            data.garage_id = request.form["garage_id"]
            data.error_id = request.form["error_id"]
            data.detail = request.form["detail"]
            data.errdate = datetime.strptime(request.form["errdate"],"%Y-%m-%d")
            db.session.add(data)
            db.session.commit()
            flash("提交成功","success")
            return redirect("/")
        else:
            flash("某些字段为空，请重新输入。","danger")
            return redirect("/write/new/")
@app.route("/detail/<int:postid>",methods=["GET"])
@app.route("/detail/<int:postid>/",methods=["GET"])
@ACCESS_REQUIRE_HTML(["READ"])
def detail(ses,user,postid):
    data = Data.query.get(postid)
    if not data:
        flash("数据不存在","danger")
        return redirect("/")
    data_user = User.query.get(data.uid)
    return render_template("detail.html",headertype="detail",curuid=ses[0],data=data,data_user=data_user,**default_dict(ses[1],request))
@app.route("/logout",methods=["GET"])
@app.route("/logout/",methods=["GET"])
def logout():
    res = redirect("/")
    res.delete_cookie("sessionid")
    return res
@app.route("/favicon.ico")
def favicon():
    return send_from_directory(ospath.join(app.root_path,'static'),'favicon.ico',mimetype='image/jpeg')
if __name__ == '__main__':
    app.run(host=HOST,port=PORT,debug=True)