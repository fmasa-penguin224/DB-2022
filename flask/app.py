
from flask import Flask, flash, render_template, request, session, redirect
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
    session["name"] = request.form["user"]
    session["password"] = request.form["password"]


    db=mysql.connector.connect(host="mysql", user="root", password="root", database="tmcit")
    cursor=db.cursor(buffered=True)

    #cursor.execute("INSERT INTO slack VALUES (%s, %s, %s, %s, %s, %s, %s)", (0 ,webhook_url, Cname, Cid, token, user, sub_date))
    #iru = cursor.execute("select exists (select * from admininfo where user = '%s')",('user',))
    cursor.execute("select user_password from userinfo where user_name = %s", (session["name"],))
    iru = str(cursor.fetchall())
    iru = re.sub(r"[^0-9a-zA-Z]", "", iru)

    #print(iru)
    db.commit()

    if iru == session["password"]:
        cursor.execute("select user_id from userinfo where user_name = %s and user_password = %s", (session["name"], session["password"],))
        user_id = str(cursor.fetchall())
        #print(user_id)
        session["id"] = re.sub(r"[^0-9a-zA-Z]", "", user_id)
        print(session["id"])
        return redirect("/health_home")
    else:
        flash("ユーザーが見つかりません")
        return redirect("/")


@app.route("/touroku")
def touroku():
    return render_template("touroku.html")

@app.route("/toures", methods=["POST"])
def toures():
    session.permanent = True
    user_name = request.form["user"]
    user_password = request.form["password"]
    user_mailaddress = request.form["mailaddress"]

    db=mysql.connector.connect(host="mysql", user="root", password="root", database="tmcit")
    cursor=db.cursor(buffered=True)

    cursor.execute("select user_name from userinfo where user_name = %s", (user_name,))
    check_name = str(cursor.fetchall())
    print(check_name)
    cursor.execute("select user_password from userinfo where user_password = %s", (user_password,))
    check_password = str(cursor.fetchall())

    if (check_name == "[]") and (check_password == "[]"):
        cursor.execute("INSERT INTO userinfo VALUES (NULL, %s, %s, %s, NULL, now(), now(), NULL)", (user_name, user_password, user_mailaddress))
        db.commit()

        session["name"] = user_name
        session["password"] = user_password
        cursor.execute("select user_id from userinfo where user_name = %s and user_password = %s", (session["name"], session["password"],))
        user_id = str(cursor.fetchall())
        #print(user_id)
        session["id"] = re.sub(r"[^0-9a-zA-Z]", "", user_id)
        #print(session["id"])

        return redirect("/health_home")

    else:
        flash("このユーザー名またはパスワードはすでに使用されています")
        return render_template("touroku.html")

@app.route("/health_home")
def health():
    db=mysql.connector.connect(host="mysql", user="root", password="root", database="tmcit")
    cursor=db.cursor(buffered=True)

    cursor.execute("select user_height from physicalinfo where user_id = %s", (session["id"],))
    user_height = re.sub(r"[^0-9a-zA-Z.]", "", str(cursor.fetchall()))
    cursor.execute("select user_weight from physicalinfo where user_id = %s", (session["id"],))
    user_weight = re.sub(r"[^0-9a-zA-Z.]", "", str(cursor.fetchall()))
    cursor.execute("select user_age from physicalinfo where user_id = %s", (session["id"],))
    user_age = re.sub(r"[^0-9a-zA-Z.]", "", str(cursor.fetchall()))
    cursor.execute("select calorie_intake from calorieinfo where user_id = %s", (session["id"],))
    calorie_intake = re.sub(r"[^0-9a-zA-Z.]", "", str(cursor.fetchall()))
    cursor.execute("select sleeping_minutes from sleepinginfo where user_id = %s", (session["id"],))
    sleeping_minutes = re.sub(r"[^0-9a-zA-Z.]", "", str(cursor.fetchall()))
    cursor.execute("select fluid_intake from fluidinfo where user_id = %s", (session["id"],))
    fluid_intake = re.sub(r"[^0-9a-zA-Z.]", "", str(cursor.fetchall()))
    #print(user_height, user_weight, user_age)

    return render_template("health_home.html", user = session["name"], height=user_height, weight=user_weight, age=user_age, calorie=calorie_intake, sleeping=sleeping_minutes, fluid=fluid_intake)

@app.route("/user_information")
def user_information():
    return render_template("setting.html")

@app.route("/user_information_res", methods=["POST"])
def user_information_res():
    session.permanent = True
    session["name"] = request.form["user"]
    session["password"] = request.form["password"]
    session["mailaddress"] = request.form["mailaddress"]

    db=mysql.connector.connect(host="mysql", user="root", password="root", database="tmcit")
    cursor=db.cursor(buffered=True)

    cursor.execute("update userinfo set user_name = %s, user_password = %s, user_mailaddress = %s where user_id = %s", (session["name"], session["password"], session["mailaddress"], session["id"],))
    db.commit()

    return redirect("/health_home")

#身長、体重、年齢の入力フォーム
@app.route("/health_physical")
def health_physical():
    return render_template("health_physical.html")

#身長、体重、年齢をDBに登録
@app.route("/health_physical_res", methods=["POST"])
def health_physical_res():
    session.permanent = True
    user_height = request.form["height"]
    user_weight = request.form["weight"]
    user_age = request.form["age"]

    db=mysql.connector.connect(host="mysql", user="root", password="root", database="tmcit")
    cursor=db.cursor(buffered=True)

    cursor.execute("select user_id from physicalinfo where user_id = %s", (session["id"],))
    check_id = str(cursor.fetchall())
    check_id = re.sub(r"[^0-9a-zA-Z]", "", check_id)
    #print(session["id"])→ok
    #print(check_id)→ok

    if check_id == "":
        cursor.execute("INSERT INTO physicalinfo VALUES (NULL, %s, %s, %s, %s, now(), now())", (str(session["id"]), user_height, user_weight, user_age))
        db.commit()

        return redirect("/health_home")

    else:
        flash("記録はすでに存在します。編集してください")
        return redirect("/health_physical_information")

@app.route("/health_physical_information")
def health_physical_information():
    return render_template("health_physical_information.html")

@app.route("/health_physical_information_res", methods=["POST"])
def health_physical_information_res():
    session.permanent = True
    user_height = request.form["height"]
    user_weight = request.form["weight"]
    user_age = request.form["age"]

    db=mysql.connector.connect(host="mysql", user="root", password="root", database="tmcit")
    cursor=db.cursor(buffered=True)

    cursor.execute("update physicalinfo set user_height = %s, user_weight = %s, user_age = %s, date_updated = now() where user_id = %s", (user_height, user_weight, user_age, session["id"],))
    db.commit()

    return redirect("/health_home")


@app.route("/health_healthiness")
def health_healthiness():
    return render_template("health_healthiness.html")

@app.route("/health_healthiness_res", methods=["POST"])
def health_healthiness_res():
    session.permanent = True
    calorie_intake = request.form["calorie"]
    sleeping_minutes = request.form["sleeping"]
    fluid_intake = request.form["fluid"]

    db=mysql.connector.connect(host="mysql", user="root", password="root", database="tmcit")
    cursor=db.cursor(buffered=True)

    cursor.execute("select user_id from calorieinfo where user_id = %s", (session["id"],))
    check_id_calorie = re.sub(r"[^0-9a-zA-Z]", "", str(cursor.fetchall()))
    cursor.execute("select user_id from sleepinginfo where user_id = %s", (session["id"],))
    check_id_sleeping = re.sub(r"[^0-9a-zA-Z]", "", str(cursor.fetchall()))
    cursor.execute("select user_id from fluidinfo where user_id = %s", (session["id"],))
    check_id_fluid = re.sub(r"[^0-9a-zA-Z]", "", str(cursor.fetchall()))
    #print(session["id"])→ok
    #print(check_id)→ok

    if check_id_calorie or check_id_sleeping or check_id_fluid== "":
        cursor.execute("INSERT INTO calorieinfo VALUES (NULL, %s, %s, now())", (str(session["id"]), calorie_intake))
        db.commit()
        cursor.execute("INSERT INTO sleepinginfo VALUES (NULL, %s, %s, now())", (str(session["id"]), sleeping_minutes))
        db.commit()
        cursor.execute("INSERT INTO fluidinfo VALUES (NULL, %s, %s, now())", (str(session["id"]), fluid_intake))
        db.commit()

        return redirect("/health_home")

    else:
        flash("記録はすでに存在します。編集してください")
        return redirect("/health_healthiness_information")

@app.route("/health_healthiness_information")
def health_healthiness_information():
    return render_template("health_healthiness_information.html")

@app.route("/health_healthiness_information_res", methods=["POST"])
def health_healthiness_information_res():
    session.permanent = True
    calorie_intake = request.form["calorie"]
    sleeping_minutes = request.form["sleeping"]
    fluid_intake = request.form["fluid"]

    db=mysql.connector.connect(host="mysql", user="root", password="root", database="tmcit")
    cursor=db.cursor(buffered=True)

    cursor.execute("update calorieinfo set calorie_intake = %s, date_updated = now() where user_id = %s", (calorie_intake, session["id"],))
    db.commit()
    cursor.execute("update sleepinginfo set sleeping_minutes = %s, date_updated = now() where user_id = %s", (sleeping_minutes, session["id"],))
    db.commit()
    cursor.execute("update fluidinfo set fluid_intake = %s, date_updated = now() where user_id = %s", (fluid_intake, session["id"],))
    db.commit()

    return redirect("/health_home")



@app.route("/task_home")
def task():
    return render_template("task_home.html", user = session["name"])


@app.route("/logout", methods=["GET"])
def logout():
    session.pop("user_id",None)
    session.pop("name",None)
    session.pop("password",None)
    session.pop("mailaddress",None)
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)