from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL
import yaml

app = Flask(__name__)
app = Flask(__name__, static_url_path='/static')
# Configure db

# <image src="{{url_for('static',filename = 'Images')}}" >

db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/make-a-Message/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Fetch form data
        userDetails = request.form
        name = userDetails['name']
        email = userDetails['email']
        collegename = userDetails['collegename']
        message = userDetails['message']
        iiti = userDetails['iiti']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users(name, email, collegename, message, iiti) VALUES(%s, %s, %s, %s,  %s)",(name, email, collegename, message, iiti))
        mysql.connection.commit()
        cur.close()
        return redirect('/')
    return render_template('Rate&submit.html')

@app.route('/users')
def users():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM users")
    if resultValue > 0:
        userDetails = cur.fetchall()
        return render_template('users.html',userDetails=userDetails)

if __name__ == '__main__':
    app.run(debug=True)