"""Render authentication-related pages."""

from flask import g, Blueprint, request, redirect, render_template, url_for
from flask.ext.login import login_user, logout_user, login_required

from glossary import models
from glossary.config import config


auth_blueprint = Blueprint('auth',
                           __name__,
                           url_prefix='%s/auth' % config.get('url', 'base'))


@auth_blueprint.route('/', methods=['GET'])
def render_auth_page():
    return render_template('auth.html')


@auth_blueprint.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    registered_user = models.User.get(username, password)
    if registered_user is None:
        logout_user()
        return render_template('auth.html')

    login_user(registered_user)
    return redirect(url_for('index.render_index_page'))


@auth_blueprint.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    g.user = None
    return redirect(url_for('index.render_index_page'))
