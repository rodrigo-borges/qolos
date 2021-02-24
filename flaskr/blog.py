from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db
from flaskr.models import Post, User


bp = Blueprint("blog", __name__)


def get_post(id, check_author=True):

	post = get_db().query(Post).filter(Post.id == id).first()

	if post is None:
		abort(404, "Post id {} doesn't exist".format(id))

	if check_author and post.author_id != g.user.id:
		abort(403)

	return post


@bp.route("/")
def index():

	db = get_db()
	posts = db.query(Post).order_by(Post.created.desc()).all()

	return render_template("blog/index.html", posts=posts)


@bp.route("/create", methods=["GET", "POST"])
@login_required
def create():

	if request.method == "POST":
		
		title = request.form["title"]
		body = request.form["body"]
		error = None

		if not title:
			error = "Title is required."

		if error is not None:
			flash(error)
		else:
			db = get_db()
			post = Post(title=title, body=body, author_id=g.user.id)
			db.add(post)
			db.commit()
			return redirect(url_for("blog.index"))

	return render_template("blog/create.html")


@bp.route("/<int:id>/update", methods=["GET", "POST"])
@login_required
def update(id):

	post = get_post(id)

	if request.method == "POST":

		title = request.form["title"]
		body = request.form["body"]
		error = None

		if error is not None:
			flash(error)
		else:
			
			db = get_db()
			post.title = title
			post.body = body
			db.commit()

			return redirect(url_for("blog.index"))

	return render_template("blog/update.html", post=post)


@bp.route("/<int:id>/delete", methods=["POST"])
@login_required
def delete(id):

	post = get_post(id)
	db = get_db()
	db.delete(post)
	db.commit()

	return redirect(url_for("blog.index"))