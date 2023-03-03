import os.path

from flask import Flask
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# db
project_dir = os.path.dirname(os.path.abspath(__file__))
db_file = f'sqlite:///{os.path.join(project_dir, "book.db")}'
app.config['SECRET_KEY'] = 'A secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = db_file
db = SQLAlchemy(app)


class Book(db.Model):
    title = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)

    def __repr__(self):
        return f"<Title: {self.title}"


@app.route('/', methods=["GET", "POST"])
def home():
    if request.form:
        title = request.form.get('title')
        error = None
        if title:
            book = Book(title=title)
            db.session.add(book)
            db.session.commit()
        else:
            error = 'Title is required.'
        if error:
            flash(error)
    books = Book.query.all()
    return render_template('home.html', books=books)


@app.route('/update', methods=["POST"])
def update():
    newtitle = request.form.get('newtitle')
    oldtitle = request.form.get('oldtitle')
    book = Book.query.filter_by(title=oldtitle).first()
    book.title = newtitle
    db.session.commit()
    return redirect('/')


@app.route('/delete', methods=["POST"])
def delete():
    title = request.form.get('title')
    book = Book.query.filter_by(title=title).first()
    db.session.delete(book)
    db.session.commit()
    return redirect('/')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)
