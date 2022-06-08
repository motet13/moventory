from flask import render_template, url_for, flash, redirect, request, jsonify, make_response
from app import db
from app.users.forms import LoginForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Feedback
from werkzeug.urls import url_parse
from flask import Blueprint

users = Blueprint('users', __name__)

@users.route('/feedback', methods=['GET', 'POST'])
def feedback():
    user = current_user
    feedbacks = Feedback.query.order_by(Feedback.timestamp.desc()).all()

    return render_template('feedback.html', title='Feedback', feedbacks=feedbacks, user=user)

@users.route('/login', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', 'danger mt-2')
            return redirect(url_for('users.login'))

        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')

        flash(f'Welcome {form.username.data.title()}!', 'success mt-2')
        return redirect(next_page)

    return render_template('login.html', title='Login', form=form)


@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))