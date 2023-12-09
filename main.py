from flask import Flask,  render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'

db = SQLAlchemy(app)

with app.app_context():
    db.create_all()

class Articule(db.Model):
    __tablename__ = 'articule'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow())




@app.route('/home')
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route("/posts")
def posts():
    articles = Articule.query.order_by(Articule.date.desc()).all()
    return render_template("posts.html", articles=articles)

@app.route('/posts/<int:id>')
def posts_detail(id):
    article = Articule.query.get(id)
    return render_template('post_detail.html', article=article)

@app.route('/posts/delete/<int:id>')
def posts_delete(id):
    article = Articule.query.get(id)
    try:
        db.session.delete(article)
        db.session.commit()
        return redirect('/posts')
    except Exception as e:
        print(e)
        return 'При удалении произошла ошибка'


@app.route('/create-article', methods=['POST', 'GET'])
def create_article():
    if request.method == 'POST':
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']

        article = Articule(title=title, intro=intro, text=text)

        with app.app_context():
            db.create_all()

        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/')


        except Exception as e:
            print(e)
            return 'При добавлении статьи произошла ошибка'





    else:
        return render_template('create_article.html')




@app.route('/user/<string:name>/<int:id>')
def user(name, id):
    return f'Имя: {name}, ID:{id}'


if __name__ == '__main__':
    app.run(debug=True)