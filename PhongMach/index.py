from flask import render_template, request, redirect, flash, url_for, jsonify
import dao, datetime
from urllib.parse import unquote
from flask_login import current_user
from PhongMach import app, login
from flask_login import login_user, logout_user, login_required
from PhongMach.decorator import anonymous_user
from PhongMach.admin import *
import cloudinary.uploader


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/BooKAConsultation', methods=['get', 'post'])
def Dat_Lich_Kham():
    msg = ''
    if request.method.__eq__('POST'):
        sex = ''
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        if request.form['optradio'] == 'male':
            sex = 'True'
        else:
            sex = 'False'
        birth = request.form['birth']
        arrbirth = birth.split('-')
        arrbday = request.form['bday'].split('-')
        arrappt = request.form['appt'].split(':')
        phone = request.form['phone']
        address = request.form['address']
        dao.BookAConsultation(lastname=lastname, firstname=firstname, sex=bool(sex),
                              birth=datetime.date(int(arrbirth[0]), int(arrbirth[1]), int(arrbirth[2])),
                              address=address,
                              thoi_gian_kham=datetime.datetime(int(arrbday[0]), int(arrbday[1]), int(arrbday[2]),
                                                               int(arrappt[0]), int(arrappt[1])),
                              phone=phone)
        dao.BookAConsultation2(lastname=lastname, firstname=firstname, sex=bool(sex),
                              birth=datetime.date(int(arrbirth[0]), int(arrbirth[1]), int(arrbirth[2])),
                              address=address,
                              thoi_gian_kham=datetime.datetime(int(arrbday[0]), int(arrbday[1]), int(arrbday[2]),
                                                               int(arrappt[0]), int(arrappt[1])),
                              phone=phone)
        msg = 'Đăng kí khám bệnh thành công!'
    return render_template(('BooKAConsultation.html'), msg=msg)

@app.route('/api/creatlist' , methods=['post'])
def add_to_book():
    #tao danh sach
    return jsonify({
        'total_amount':100,
        'total_quantity':100
    })

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




@app.route('/register', methods=['get', 'post'])
def register_my_user():
    err_msg = ''
    if request.method == 'POST':

        password = request.form['password']
        confirm = request.form['confirm']
        if password.__eq__(confirm):
            if dao.PasswordStrong(request.form['password']) == []:
                avatar = ''
                if request.files:
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

@app.route('/creatlist')
def create_list():
    pass

@login.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id)


if __name__ == '__main__':
    app.run(debug=True)
