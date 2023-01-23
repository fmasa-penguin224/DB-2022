
from flask import Flask, flash, render_template, request, session
import mysql.connector, re
from datetime import timedelta


app = Flask(__name__)

app.secret_key = 'tmcit'
app.permanent_session_lifetime = timedelta(days=10)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/result", methods=["POST"])
def result():
    session.permanent = True
    user_name = request.form["user"]
    session["name"] = user_name
    user_password = request.form["password"]
    session["password"] = user_password


    db=mysql.connector.connect(host="mysql", user="root", password="root", database="tmcit")
    cursor=db.cursor(buffered=True)

    #cursor.execute("INSERT INTO slack VALUES (%s, %s, %s, %s, %s, %s, %s)", (0 ,webhook_url, Cname, Cid, token, user, sub_date))
    #iru = cursor.execute("select exists (select * from admininfo where user = '%s')",('user',))
    cursor.execute("select user_password from userinfo where user_name = %s", (session["name"],))
    iru = str(cursor.fetchall())
    iru = re.sub(r"[^0-9a-zA-Z]", "", iru)

    #print(iru)
    db.commit()

    if iru == user_password:
        cursor.execute("select user_id from userinfo where user_name = %s and user_password = %s", (session["name"], session["password"],))
        user_id = str(cursor.fetchall())
        #session["id"] = int(user_id[2])
        return render_template("health_home.html", user = session["name"],  password = session["password"])
    else:
        flash("ユーザーが見つかりません")
        return render_template("index.html", user = session["name"], password = session["password"])


@app.route("/touroku")
def touroku():
    return render_template("touroku.html")

@app.route("/toures", methods=["POST"])
def toures():
    user_name = request.form["user"]
    user_password = request.form["password"]
    user_mailaddress = request.form["mailaddress"]

    db=mysql.connector.connect(host="mysql", user="root", password="root", database="tmcit")
    cursor=db.cursor(buffered=True)

    cursor.execute("select user_name from userinfo where user_name = %s", (user_name,))
    check_name = str(cursor.fetchall())

    if check_name == "[]":
        cursor.execute("INSERT INTO userinfo VALUES (NULL, %s, %s, %s, NULL, now(), now(), NULL)", (user_name, user_password, user_mailaddress))
        db.commit()

        session["name"] = user_name
        session["password"] = user_password
        cursor.execute("select user_id from userinfo where user_name = %s and user_password = %s", (session["name"], session["password"],))
        user_id = cursor.fetchall()
        #session["id"] = int(user_id[2])

        return render_template("health_home.html", user = session["name"], password = session["password"])

    else:
        flash("使用されているユーザー名です")
        return render_template("touroku.html")

@app.route("/health_home")
def health():
    return render_template("health_home.html", user = session["name"])

@app.route("/user_information")
def user_information():
    return render_template("setting.html")

@app.route("/user_information_res", methods=["POST"])
def user_information_res():
    session["name"] = request.form["user"]
    session["password"] = request.form["password"]
    session["mailaddress"] = request.form["mailaddress"]

    db=mysql.connector.connect(host="mysql", user="root", password="root", database="tmcit")
    cursor=db.cursor(buffered=True)

    cursor.execute("update userinfo set user_name = %s, user_password = %s, user_mailaddress = %s where user_id = %s", (session["name"], session["password"], session["mailaddress"], session["id"],))
    db.commit()

    return render_template("health_home.html", user = session["name"])


@app.route("/task_home")
def task():
    return render_template("task_home.html", user = session["name"])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)
