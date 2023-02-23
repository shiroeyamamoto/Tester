from flask import render_template, request, redirect, flash, url_for
import utils, dao
from urllib.parse import unquote
from flask_login import current_user
from PhongMach import app, login
from flask_login import login_user, logout_user,login_required
from PhongMach.decorator import anonymous_user
from PhongMach.admin import *
import cloudinary.uploader


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/BooKAConsultation')
def Dat_Lich_Kham():
    return render_template(('BooKAConsultation.html'))


@app.route('/login', methods=['get', 'post'])
@anonymous_user
def login_my_user():
    if request.method.__eq__('POST'):
        username = request.form['username']
        password = request.form['password']

        user = dao.auth_user(username=username, password=password)

        if user:
            login_user(user=user)

            n = request.args.get('next')
            return redirect(n if n else '/')

    return render_template('login.html')

@app.route('/logout')
def logout_my_user():
    logout_user()
    return redirect('/login')

@app.route('/register', methods=['get','post'])
def register_my_user():
    err_msg = ''
    if request.method == 'POST':

        password = request.form['password']
        confirm = request.form['confirm']
        if password.__eq__(confirm):
            if dao.PasswordStrong(request.form['password'])==[]:
                    avatar = ''
                    if  request.files:
                        res = cloudinary.uploader.upload(request.files['avatar'])
                        avatar = res['secure_url']
                    try:
                        dao.register(name=request.form['name'],
                                     username=request.form['username'],
                                     password=password,
                                     avatar=avatar)
                        return redirect('/login')
                    except:
                        err_msg = 'Đã có lỗi xảy ra! Vui lòng quay lại sau!'
            else:
                err_msg = 'Mật khẩu phải có ít nhất 8 kí tự, có kí tự in hoa, có số, có kí tự đặc biệt!'
        else:
            err_msg = 'Mật khẩu KHÔNG khớp!'

    return render_template('register.html', err_msg=err_msg)


@app.route('/login-admin', methods=['post'])
def admin_login():
    username = request.form['username']
    password = request.form['password']

    user = dao.auth_user(username=username, password=password)

    if user:
        login_user(user=user)
    else:
        flash('Đăng nhập thất bại!')
    return redirect('/admin')


@login.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id)


if __name__ == '__main__':
    app.run(debug=True)
