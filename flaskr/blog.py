from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, send_file, Response
)
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import numpy as np
from io import BytesIO
import io
import random

bp = Blueprint('blog', __name__)


@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('blog/index.html', posts=posts)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (title, body, author_id)'
                ' VALUES (?, ?, ?)',
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')


def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(id))

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
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ?'
                ' WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)  # ?
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.index'))


@bp.route('/main.png')
def main_plot():
    img = get_main_image()
    return send_file(img, mimetype='image/png', cache_timeout=0)


def get_main_image():
    """Rendering the scatter chart"""
    # yearly_temp = []
    # yearly_hum = []
    #
    # for city in data:
    #     yearly_temp.append(sum(get_city_temperature(city))/12)
    #     yearly_hum.append(sum(get_city_humidity(city))/12)
    #
    # plt.clf()
    # plt.scatter(yearly_hum, yearly_temp, alpha=0.5)
    # plt.title('Yearly Average Temperature/Humidity')
    # plt.xlim(70, 95)
    # plt.ylabel('Yearly Average Temperature')
    # plt.xlabel('Yearly Average Relative Humidity')
    # for i, txt in enumerate(CITIES):
    #     plt.annotate(txt, (yearly_hum[i], yearly_temp[i]))

    xpoints = np.array([1, 2, 6, 8])
    ypoints = np.array([3, 8, 1, 10])

    plt.clf()
    plt.plot(xpoints, ypoints)  # , marker = 'o'
    plt.title("Sample Plot Graph")
    plt.xlabel("X Axis")
    plt.ylabel("Y Axis")

    # plt.savefig('static/images/plot.png')

    # https://www.jetbrains.com/help/pycharm/creating-web-application-with-flask.html
    img = BytesIO()
    plt.savefig(img)
    # ?fig.savefig('path/to/save/image/to.png')
    # pylab.savefig('foo.png')
    img.seek(0)
    return img


@bp.route('/main2.png')
def main_plot_2():
    # Generate the figure **without using pyplot**.
    # also maybe use https://gist.github.com/illume/1f19a2cf9f26425b1761b63d9506331f...?
    # use chart.js instead of matplotlib?  plotly?
    fig = create_figure()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


def create_figure():
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    xs = range(100)
    ys = [random.randint(1, 50) for x in xs]
    axis.plot(xs, ys)
    return fig
