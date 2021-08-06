from flask import Flask,render_template,request,redirect
import mysql.connector
app = Flask(__name__)
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="flasktodolist"
)
mycursor = mydb.cursor()
@app.route('/')
def hello():
    mycursor.execute("SELECT * FROM todolist order by id DESC")
    todoList = mycursor.fetchall()
    return render_template('todo.html' ,todoList=todoList)

@app.route('/add_todo', methods = ['POST'])
def add_todo():
    name = request.form.get("name")
    status = request.form.get("status")
    if name != "" and status != "" :
        sql = "INSERT INTO todolist (name, status) VALUES (%s, %s)"
        val = (name, status)
        mycursor.execute(sql, val)
        mydb.commit()

        print(mycursor.rowcount, "record inserted.")
        return redirect("/")
    else:
        return redirect("/?error=true")

@app.route('/delete_todo/<id>')
def delete_todo(id):
    sql = "DELETE FROM todolist WHERE id = %s"
    adr = (id,)
    mycursor.execute(sql, adr)
    mydb.commit()

    return redirect("/")

@app.route('/edit-todo/<id>', methods = ['POST'])
def editModal(id):
    name = request.form.get("name")
    status = request.form.get("status")
    if name != "" and status != "" :
        sql = "UPDATE todolist SET name = %s ,  status = %s WHERE id = %s"
        val = (name, status, id)
        mycursor.execute(sql, val)
        mydb.commit()
        print(mycursor.rowcount, "record(s) affected")
    return redirect("/")


if __name__ == '__main__':
    app.run()