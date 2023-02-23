from PhongMach import admin, db
from PhongMach.models import medication, User, UserRole
from flask_admin import Admin,BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask import redirect
from flask_login import logout_user, current_user


class AuthenticatedModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN

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
        'type':'Loại',
        'price':'Giá'
    }
class userAdmin(AuthenticatedModelView):
    column_display_pk = True

class StatsView(AuthenticatedBaseView):
    @expose('/')
    def index(self):
        return self.render('admin/stats.html')

class LogoutView(AuthenticatedBaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')


admin.add_view(MedicationView(medication, db.session, name='Thuốc'))
admin.add_view(userAdmin(User, db.session, name='Người dùng'))
admin.add_view(StatsView(name='THỐNG KÊ BÁO CÁO'))
admin.add_view(LogoutView(name='Đăng xuất'))