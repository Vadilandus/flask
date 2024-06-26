from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db


bp = Blueprint('blog', __name__)
@bp.route('/')
def index():
    db = get_db()
    posts = db.cursor().execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM posts p JOIN users u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchallmap()
    return render_template('blog/index.html', posts=posts)
    return render_template('blog/index.html', posts=posts)
@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        phone = request.form['phone']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.cursor().execute(
                'INSERT INTO posts (title, body, author_id)'
                ' VALUES (?, ?, ?)',
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')
def get_post(id, check_author=True):
    post = get_db().cursor().execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM posts p JOIN users u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchonemap()

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post
@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        phone = request.form['phone']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.cursor().execute(
                'UPDATE posts SET title = ?, body = ?'
                ' WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.cursor().execute('DELETE FROM posts WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.index'))
@bp.route('/main')
def main():
    return render_template('deal_center/main.html')
@bp.route('/audi')
def audi():
    return render_template('deal_center/audi.html')
@bp.route('/bmw')
def bmw():
    return render_template('deal_center/bmw.html')
@bp.route('/lada')
def lada():
    return render_template('deal_center/lada.html')
@bp.route('/hyundai')
def hyundai():
    return render_template('deal_center/hyundai.html')
@bp.route('/toyota')
def toyota():
    return render_template('deal_center/toyota.html')
@bp.route('/ford')
def ford():
    return render_template('deal_center/ford.html')