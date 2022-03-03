from main import app, db, login_manager
from flask import render_template, redirect, url_for
from forms import RegisterProfile, Login, RegisterPost
from flask_login import login_user, login_required, current_user, logout_user
from models import Profile, Post, Vote
from sqlalchemy import and_
from flask import request, jsonify
from flask_jwt_extended import create_access_token
from datetime import datetime

@app.route('/')
def main():
    posts = Post.query.all()
    return render_template('main.html', posts=posts)


@app.route('/post/<id>')
def post(id):
    post = Post.query.filter_by(id=id).first()
    posts_liked = Vote.query.filter_by(vote="Like").filter_by(post_id=id).count()
    posts_disliked = Vote.query.filter_by(vote="Dislike").filter_by(post_id=id).count()
    return render_template('post.html', post=post, posts_liked=posts_liked, posts_disliked=posts_disliked)


@app.route('/like/<user_id>/<post_id>/')
def like(user_id, post_id):
    vote = Vote.query.filter_by(user_id=user_id).filter_by(post_id=post_id).filter_by(vote="Like").first()
    if vote is not None:
        db.session.delete(vote)
        db.session.commit()
    else:
        vote = Vote.query.filter_by(user_id=user_id).filter_by(post_id=post_id).filter_by(vote="Dislike").first()
        if vote is not None:
            db.session.delete(vote)
            db.session.commit()
            vote = Vote(user_id=user_id, post_id=post_id, vote="Like")
            db.session.add(vote)
            db.session.commit()
        else:
            vote = Vote(user_id=user_id, post_id=post_id, vote="Like")
            db.session.add(vote)
            db.session.commit()
    return redirect(url_for('post', id=post_id))


@app.route('/dislike/<user_id>/<post_id>/')
def dislike(user_id, post_id):
    vote = Vote.query.filter_by(user_id=user_id).filter_by(post_id=post_id).filter_by(vote="Dislike").first()
    if vote is not None:
        db.session.delete(vote)
        db.session.commit()
    else:
        vote = Vote.query.filter_by(user_id=user_id).filter_by(post_id=post_id).filter_by(vote="Like").first()
        if vote is not None:
            db.session.delete(vote)
            db.session.commit()
            vote = Vote(user_id=user_id, post_id=post_id, vote="Dislike")
            db.session.add(vote)
            db.session.commit()
        else:
            vote = Vote(user_id=user_id, post_id=post_id, vote="Dislike")
            db.session.add(vote)
            db.session.commit()
    return redirect(url_for('post', id=post_id))


@app.route('/sign_in', methods=['GET', 'POST'])
def login_page():
    form = Login()
    if form.validate_on_submit():
        profile = Profile.query.filter_by(email=form.email.data).first()
        if profile.check_password(form.password.data) and profile:
            login_user(profile)
    return render_template('sign_in.html', form=form)


@app.route('/sign_up', methods=['GET', 'POST'])
def register_page():
    form = RegisterProfile()
    if form.validate_on_submit():
        profile = Profile(username=form.username.data, email=form.email.data, password=form.password1.data)
        db.session.add(profile)
        db.session.commit()
    else:
        print('Account already exists')
    return render_template('sign_up.html', form=form)


@app.route('/logout_page', methods=['GET', 'POST'])
@login_required
def logout_page():
    logout_user()
    return redirect(url_for('main'))


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile_page():
    form = RegisterPost()
    if form.validate_on_submit():
        post = Post(name=form.name.data, body=form.body.data, owner_id=current_user.id)
        db.session.add(post)
        db.session.commit()
    return render_template('profile_page.html', form=form)


@app.before_request
def last_login():
    if current_user.is_authenticated:
        current_user.last_login = datetime.utcnow()


@app.route('/api/auth/username=<string:username>/password=<string:password>', methods=['GET', 'POST'])
def auth(username, password):

    profile = Profile.query.filter_by(username=username).first()
    if not profile.check_password(password) or not password:
        return jsonify({"msg": "Incorrect username or password"})
    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)


@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect(url_for('login_page'))
