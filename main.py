from flask import *
from ui import *
from model import *
from lib import *
from constances import *
from settings import *
from api import app as api_blueprint
app = Flask(APP_NAME)
app.secret_key = SECRET_KEY
for conf in CONFIG:
    app.config[conf] = CONFIG[conf]
db.init_app(app)
app.register_blueprint(api_blueprint)
@app.route("/",methods=["GET"])
def index():#######################################
    ses = readSession(request.cookies)
    if ses[0] == -1:
        return redirect("/login/")
    user = User.query.get(ses[0])
    return render_template("index.html",headertype="root",user=user,**default_dict(ses[1],request))
@app.route("/login",methods=["GET","POST"])
@app.route("/login/",methods=["GET","POST"])
def login():#######################################
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