from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key =True)
    author = db.Column(db.String, nullable = False)
    text = db.Column(db.String, nullable = False)

with app.app_context():
     db.create_all()

@app.route("/")
def index():
    page = request.args.get('page', 1, type=int)
    messages = Message.query.order_by(desc(Message.id)).paginate(page=page, per_page=10)
    return render_template("index.html", messages=messages)

@app.route("/add-message", methods=["POST"])
def add_message():
    username = request.form.get("username")
    text = request.form.get("text")

    message = Message(author=username, text=text)
    db.session.add(message)
    db.session.commit()

    return redirect("/")

if __name__ == '__main__':
    app.run()

    