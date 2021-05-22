from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask import g
import sqlite3
import datetime

app = Flask(__name__)


def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


app.config['SECRET_KEY'] = 'dev'
DATABASE = 'project.db'
app.config['DATABASE'] = DATABASE


def connect_db():
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.before_request
def before_request():
    g.db = connect_db()


@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        username = request.form['username']
        password = request.form['password']

        if username == 'admin' and password == 'password':
            return redirect('/dashboard')

    return render_template('login.html')


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if session['username'] == 'admin':
        cur = g.db.execute("SELECT * FROM posts")

        res = cur.fetchall()

        posts = [dict(id=r[0], post_date=r[1], title=r[2], author=r[3], content=r[4]) for r in res]

        return render_template("dashboard.html", posts=posts)
    else:
        return redirect(url_for('/login'))


@app.route('/add_post', methods=('GET', 'POST'))
def add_post():
    if session['username'] == 'admin':
        if request.method == 'POST':
            title = request.form['post_title']
            post_content = request.form['content']
            g.db = get_db()
            g.db.execute("INSERT INTO posts(post_title) values(?)", (title,))
            g.db.execute("INSERT INTO posts(content) values(?)", (post_content,))
            g.db.commit()
            return redirect(url_for('/dashboard'))
        else:
            return render_template("add_post.html")
    else:
        return redirect(url_for('/login'))


@app.route('/post/<id>')
def view_posts(id):
    cur = g.db.execute(
        "SELECT posts.id, posts.post_date, posts.author, posts.title, posts.content "
        "FROM posts WHERE posts.id = ?", [id]
    )
    res = cur.fetchall()
    search_results = [dict(id=r[0], post_date=r[1], author=r[2], title=r[3], content=r[4]) for r in res]
    return render_template("myblog_post.html", search_results=search_results)


@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    post = view_posts(id)
    if session['username'] == 'admin':
        if request.method == 'POST':
            title = request.form['title']
            content = request.form['content']
            g.db.execute('UPDATE posts SET title = ?, content = ?'
                         ' WHERE id = ?', (id))

            g.db.commit()
            return redirect(url_for('dashboard'))
        else:
            return render_template('edit_post.html', post=post)

    else:
        return redirect(url_for('/login'))


if __name__ == "__main__":
    app.run(debug=True)
