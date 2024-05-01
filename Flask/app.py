
from flask import Flask, render_template, redirect, request, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

#  connection
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "Vbiru@1516"
app.config["MYSQL_DB"] = "firstproject"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"
mysql = MySQL(app)

#   Page
@app.route("/")
def home():
    con = mysql.connection.cursor()
    sql = "SELECT * FROM customerdetails"
    con.execute(sql)
    res = con.fetchall()
    con.close()
    return render_template("home.html", datas=res)

#  customer data
@app.route("/addUser", methods=['GET', 'POST'])
def addUser():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        city = request.form['city']
        con = mysql.connection.cursor()
        sql = "INSERT INTO customerdetails (Name, Age, Gender, City) VALUES (%s, %s, %s, %s)"
        con.execute(sql, [name, age, gender, city])
        mysql.connection.commit()
        con.close()
        return redirect(url_for("home"))

    return render_template("addUser.html")

# Updating customer details
@app.route("/editUser/<int:id>", methods=['GET', 'POST'])
def editUser(id):
    con = mysql.connection.cursor()

    if request.method == "POST":
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        city = request.form['city']
        sql = "UPDATE customerdetails SET Name=%s, Age=%s, Gender=%s, City=%s WHERE id=%s"
        con.execute(sql, [name, age, gender, city, id])
        mysql.connection.commit()
        con.close()
        return redirect(url_for("home"))

    sql = "SELECT * FROM customerdetails WHERE id=%s"
    con.execute(sql, [id])
    res = con.fetchone()
    con.close()
    return render_template("editUser.html", datas=res)


#DeleteUser
@app.route("/deleteUser/<string:id>",methods=['GET','POST'])
def deleteUser(id):
    con=mysql.connection.cursor()
    sql="delete from customerdetails where id=%s"
    con.execute(sql,[id])
    mysql.connection.commit()
    con.close()
    return redirect(url_for("home"))


if __name__ == '__main__':
    app.run(debug=True)
