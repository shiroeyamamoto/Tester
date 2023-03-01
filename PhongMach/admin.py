from flask_admin.actions import action

from PhongMach import admin, db, app
from PhongMach.models import Medication, User, UserRole, danhsachbenhnhan, danhsachkhambenh, Cashier, DonThuoc, rule
from flask_admin import Admin,BaseView, expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask import redirect, flash
from flask_login import logout_user, current_user


class AuthenticatedModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN

class AuthenticatedNurse(ModelView):
    def is_accessible(self):
        return (current_user.is_authenticated and current_user.user_role == UserRole.NURSE) or (current_user.is_authenticated and current_user.user_role == UserRole.ADMIN)

class AuthenticatedDocter(ModelView):
    def is_accessible(self):
        return (current_user.is_authenticated and current_user.user_role == UserRole.DOCTOR) or (current_user.is_authenticated and current_user.user_role == UserRole.ADMIN)

class AuthenticatedCashier(ModelView):
    def is_accessible(self):
        return (current_user.is_authenticated and current_user.user_role == UserRole.CASHIER) or (current_user.is_authenticated and current_user.user_role == UserRole.ADMIN)

class AuthenticatedBaseView(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated


class MedicationView(AuthenticatedModelView):
    column_display_pk = True
    can_view_details = True
    edit_modal = True
    details_modal = True
    create_modal = True
    column_filters = ['name','price']
    column_searchable_list = ['name']
    column_labels = {
        'id':'Mã sản phẩm',
        'name':'Tên',
        'unitmedication':'Loại',
        'price':'Giá'
    }

class DanhSachDangKi(AuthenticatedNurse):
    column_display_pk = True
    can_view_details = True
    can_edit = False
    can_delete = True
    can_create = False
    details_modal = True
    can_export = True
    column_labels = {
        'id': 'Mã danh sách',
        'lastname': 'Tên',
        'firstname': 'Họ',
        'sex': 'giới tính',
        'birth': 'ngày sinh',
        'phone': 'số điện thoại',
        'thoi_gian_kham': 'Ngày giờ hẹn',
        'created_data': 'Ngày tạo'
    }
    @action('/creatlist', 'Tạo danh sách đang kí', 'Bạn có chắc muốn tạo danh sách đăng kí không?')
    def action_recalculate(self, ids):
        count = 0
        x=''
        for _id in ids:
            count= count+1
            for u in self:
                x=str(u)
        flash("Admin " + x)

class userAdmin(AuthenticatedModelView):
    column_display_pk = True

class ruleView(AuthenticatedModelView):
    column_display_pk = True
    can_view_details = True
    can_delete = False
    can_create = False
    details_modal = True
    column_labels = {
        'id': 'Mã quy định',
        'name': 'Tên',
        'value': 'Giá trị'
    }

class StatsView(AuthenticatedBaseView):
    @expose('/')
    def index(self):
        return self.render('admin/stats.html')

class LogoutView(AuthenticatedBaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')

class MyAdminView(AdminIndexView):
    @expose('/')
    def index(self):
        return self.render('admin/index.html', msg='TEST')

admin.add_view(ruleView(rule, db.session, name='Quản lý quy định'))
admin.add_view(MedicationView(Medication, db.session, name='Thuốc'))
admin.add_view(userAdmin(User, db.session, name='Người dùng'))
admin.add_view(DanhSachDangKi(danhsachbenhnhan, db.session, name='Danh sách đăng kí'))

admin.add_view(StatsView(name='THỐNG KÊ BÁO CÁO'))
admin.add_view(LogoutView(name='Đăng xuất'))
