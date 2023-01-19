from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.models import Post
from flaskblog.posts.forms import PostForm

posts = Blueprint('posts', __name__)


@posts.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
	form = PostForm()
	if form.validate_on_submit():
		post = Post(title=form.title.data, content=form.content.data, author=current_user)
		db.session.add(post)
		db.session.commit()
		flash('Your post has been created!', 'success')
		return redirect(url_for('main.home'))
	return render_template('create_post.html', title='New Post', form=form, legend='Share a post')


@posts.route('/post/<int:post_id>')
def post(post_id):
	post_ = Post.query.get_or_404(post_id)
	return render_template('post.html', title=post_.title, post=post_)


@posts.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
	post_ = Post.query.get_or_404(post_id)
	if post_.author != current_user:
		abort(403)
	form = PostForm()
	if form.validate_on_submit():
		post_.title = form.title.data
		post_.content = form.content.data
		db.session.commit()
		flash('Your post has been updated!', 'success')
		return redirect(url_for('posts.post', post_id=post_.id))
	elif request.method == 'GET':
		form.title.data = post_.title
		form.content.data = post_.content
	return render_template('create_post.html', title='Update Post', form=form, legend='Update Post')


@posts.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
	post_ = Post.query.get_or_404(post_id)
	if post_.author != current_user:
		abort(403)
	db.session.delete(post_)
	db.session.commit()
	flash('Your post has been deleted!', 'success')
	return redirect(url_for('main.home'))


