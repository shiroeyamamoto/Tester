from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Enum, Float, DateTime, Date, Time
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects.mssql import TINYINT
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship, scoped_session, sessionmaker
from PhongMach import db
import random
from datetime import datetime
from enum import Enum as UserEnum
from flask_login import UserMixin


class UserRole(UserEnum):
    ADMIN = 1
    DOCTOR = 2
    NURSE = 3
    CASHIER = 4
    USER = 5


class User(db.Model, UserMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    active = Column(Boolean, default=True)
    joined_date = Column(DateTime, default=datetime.now())
    avatar = Column(String(100), nullable=False, )
    user_role = Column(Enum(UserRole), default=UserRole.USER)

    def __str__(self):
        return self.name


class NhanVien(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)
    lastname = Column(String(50), nullable=False)
    firstname = Column(String(50), nullable=False)
    sex = Column(Boolean, default=True, nullable=False)
    phone = Column(String(100), nullable=False)
    address = Column(String(100), nullable=False)

    def __str__(self):
        return self.name


class DataPatient(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    ngay_dieu_tri = Column(Date, nullable=False)
    patient_dataperson = relationship('Patient', backref='datapatient', lazy=True)

    def __str__(self):
        return self.name

class ThoiGianBieu(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    bat_dau = Column(Time, default='9:00')
    ket_thuc = Column(Time, default='18:00')
    thoi_gian_bieu_doctor = relationship('Doctor', backref='thoigianbieu', lazy=True)
    def __str__(self):
        return self.name



class Doctor(NhanVien):
    __tablename__ = 'Doctor'
    kinh_nghiem = Column(Integer, default=8, nullable=False)
    patient_doctor = relationship('Patient', backref='doctor', lazy=True)
    donthuoc_doctor = relationship('DonThuoc', backref='doctor', lazy=True)
    thoi_gian_bieu_id = Column(Integer, ForeignKey(ThoiGianBieu.id), nullable=False)
    def __str__(self):
        return self.name

class Nurse(NhanVien):
    __tablename__ = 'Nurse'
    doctor_nurse = relationship('Nurse', secondary='nurse_doctor', lazy='subquery',
                             backref=backref('doctor', lazy=True))
    def __str__(self):
        return self.name

nurse_doctor = db.Table('nurse_doctor',
                                     Column('doctor_id', ForeignKey(Doctor.id), nullable=False,
                                            primary_key=True),
                                     Column('nurse_id', ForeignKey(Nurse.id), nullable=False,
                                            primary_key=True))

class danhsachbenhnhan(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    lastname = Column(String(50), nullable=False)
    firstname = Column(String(50), nullable=False)
    sex = Column(Boolean, default=True, nullable=False)
    birth = Column(Date, nullable=False)
    address = Column(String(100), nullable=False)
    phone = Column(String(100), nullable=False)
    thoi_gian_kham = Column(DateTime, default=datetime.now())
    created_data = Column(DateTime, default=datetime.now())
    nurse_danhsachbenhnhan = relationship('danhsachbenhnhan', secondary='nurse_danhsachbenhnhan', lazy='subquery',
                                backref=backref('nurse', lazy=True))
    def __str__(self):
        return self.name

nurse_danhsachbenhnhan = db.Table('nurse_danhsachbenhnhan',
                                     Column('danhsachbenhnhan_id', ForeignKey(danhsachbenhnhan.id), nullable=False,
                                            primary_key=True),
                                     Column('nurse_id', ForeignKey(Nurse.id), nullable=False,
                                            primary_key=True))

class danhsachkhambenh(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    lastname = Column(String(50), nullable=False)
    firstname = Column(String(50), nullable=False)
    sex = Column(Boolean, default=True, nullable=False)
    birth = Column(Date, nullable=False)
    address = Column(String(100), nullable=False)
    phone = Column(String(100), nullable=False)
    thoi_gian_kham = Column(DateTime, default=datetime.now())
    created_data = Column(DateTime, default=datetime.now())
    nurse_danhsachkhambenh = relationship('danhsachkhambenh', secondary='nurse_danhsachkhambenh', lazy='subquery',
                                          backref=backref('nurse', lazy=True))
    def __str__(self):
        return self.name

nurse_danhsachkhambenh = db.Table('nurse_danhsachkhambenh',
                                     Column('danhsachkhambenh_id', ForeignKey(danhsachkhambenh.id), nullable=False,
                                            primary_key=True),
                                     Column('nurse_id', ForeignKey(Nurse.id), nullable=False,
                                            primary_key=True))

class Patient(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    lastname = Column(String(50), nullable=False)
    firstname = Column(String(50), nullable=False)
    sex = Column(Boolean, default=True, nullable=False)
    phone = Column(String(100), nullable=False)
    address = Column(String(100), nullable=False)
    data_patient_id = Column(Integer, ForeignKey(DataPatient.id), nullable=False)
    doctor_id = Column(Integer, ForeignKey(Doctor.id), nullable=False)
    def __str__(self):
        return self.name



class Cashier(NhanVien):
    __tablename__ = 'Cashier'
    donthuoc_cashier = relationship('DonThuoc', backref='cashier', lazy=True)
    bill_cashier = relationship('Bill', backref='cashier', lazy=True)
    def __str__(self):
        return self.name

class Bill(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    tong_tien=Column(String(100), nullable=False, default=0)
    cashier_id = Column(Integer, ForeignKey(Cashier.id), nullable=False)
    def __str__(self):
        return self.name

class DonThuoc(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    chieu_trung = Column(String(100), nullable=False)
    don_thuoc = relationship('DonThuoc', secondary='medication_donthuoc', lazy='subquery',
                             backref=backref('medication', lazy=True))
    doctor_id = Column(Integer, ForeignKey(Doctor.id), nullable=False)
    donthuoc_cashier_id = Column(Integer, ForeignKey(Cashier.id), nullable=False)
    def __str__(self):
        return self.name





class UnitMedication(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name_unit = Column(String(50), nullable=False)
    unit_medications = db.relationship('Medication', backref='unitmedication')

    def __str__(self):
        return self.name_unit



class Medication(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    price = Column(Float, default=0)
    unitmedication_id = db.Column(db.Integer, db.ForeignKey(UnitMedication.id))
    typemedications = relationship('Medication', secondary='medication_typemedication', lazy='subquery',
                                   backref=backref('typemedication', lazy=True))

    def __str__(self):
        return self.name


class TypeMedication(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)

    def __str__(self):
        return self.name

medication_typemedication = db.Table('medication_typemedication',
                                     Column('medication_id', ForeignKey(Medication.id), nullable=False,
                                            primary_key=True),
                                     Column('typemedication_id', ForeignKey(TypeMedication.id), nullable=False,
                                            primary_key=True))

medication_donthuoc = db.Table('medication_donthuoc',
                               Column('medication_id', ForeignKey(Medication.id), nullable=False, primary_key=True),
                               Column('donthuoc_id', ForeignKey(DonThuoc.id), nullable=False, primary_key=True))

class rule(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable = False)
    value = Column(Integer)

if __name__ == '__main__':
    ###Làm theo hướng dẫn để tạo database
    ################################################### Chạy lệnh create_all ở hàng 220 ################################
    # db.create_all()
    #Chạy xong nhớ đóng lệnh haàng 220.

    ##Cách lệnh bên dưới là các lệnh nạp dữ liệu, chỉ chạy các lệnh bên dưới sau khi đã tạo database ở hàng 220.
    ## ---------------- LƯU Ý: Chạy lần lượt các lệnh bên dưới theo một đoạn được ngăn cách mới 2 dấu Enter. Nếu chạy một loạt sẽ phát sinh lỗi.
    ## ---------------- Chạy xong đoạn nào nhớ đóng đoạn đó lại để dữ liệu không bị nạp lại vào lần thứ 2.

    # p1=UnitMedication(name_unit='Chai')
    # p2=UnitMedication(name_unit='Lo')
    # p3=UnitMedication(name_unit='Vi')
    # db.session.add(p1)
    # db.session.add(p2)
    # db.session.add(p3)


    # p4=[
    #     Medication(name='Amoxicillin', price=random.randint(50000,1000000),unitmedication_id=random.randint(1,3)),
    #     Medication(name='Azithromycin',  price=random.randint(50000,1000000),unitmedication_id=random.randint(1,3)),
    #     Medication(name='Albuterol',  price=random.randint(50000,1000000),unitmedication_id=random.randint(1,3)),
    #     Medication(name='Clavulanate',  price=random.randint(50000,1000000),unitmedication_id=random.randint(1,3)),
    #     Medication(name='Cefdinir', price=random.randint(50000,1000000),unitmedication_id=random.randint(1,3)),
    #     Medication(name='Cephalexin', price=random.randint(50000,1000000),unitmedication_id=random.randint(1,3)),
    #     Medication(name='Fluticasone',  price=random.randint(50000,1000000),unitmedication_id=random.randint(1,3)),
    #     Medication(name='Prednisolone Sodium Phosphate', price=random.randint(50000,1000000),unitmedication_id=random.randint(1,3)),
    #     Medication(name='Ibuprofen',price=random.randint(50000,1000000),unitmedication_id=random.randint(1,3)),
    #     Medication(name='Singulair ',  price=random.randint(50000,1000000),unitmedication_id=random.randint(1,3)),
    #     Medication(name='Trimethoprim', price=random.randint(50000,1000000),unitmedication_id=random.randint(1,3)),
    #     Medication(name='Tylenol ', price=random.randint(50000,1000000),unitmedication_id=random.randint(1,3)),
    #     Medication(name='Vicodin', price=random.randint(50000,1000000),unitmedication_id=random.randint(1,3)),
    #     Medication(name='Mupirocin', price=random.randint(50000,1000000),unitmedication_id=random.randint(1,3)),
    #     Medication(name='Nystatin', price=random.randint(50000,1000000),unitmedication_id=random.randint(1,3)),
    #     Medication(name='Methylphenidate', price=random.randint(50000,1000000),unitmedication_id=random.randint(1,3)),
    #     Medication(name='Cough and Cold Combinations', price=random.randint(50000,1000000),unitmedication_id=random.randint(1,3)),
    #     Medication(name='Mometasone',  price=random.randint(50000,1000000),unitmedication_id=random.randint(1,3)),
    #     Medication(name='Triamcinolone', price=random.randint(50000,1000000),unitmedication_id=random.randint(1,3)),
    #     Medication(name='Prednisone', price=random.randint(50000,1000000),unitmedication_id=random.randint(1,3)),
    #     Medication(name='Sodium Fluoride',  price=random.randint(50000,1000000),unitmedication_id=random.randint(1,3)),
    #     Medication(name='Multivitamins With Fluoride',  price=random.randint(50000,1000000),unitmedication_id=random.randint(1,3)),
    #     Medication(name='Amphetamine',  price=random.randint(50000,1000000),unitmedication_id=random.randint(1,3)),
    #     Medication(name='Hydrocortisone', price=random.randint(50000,1000000),unitmedication_id=random.randint(1,3)),
    #     Medication(name='Budesonide', price=random.randint(50000,1000000),unitmedication_id=random.randint(1,3)),
    #     Medication(name='Promethazine',  price=random.randint(50000,1000000),unitmedication_id=random.randint(1,3)),
    #     Medication(name='Ciprofloxacin', price=random.randint(50000,1000000),unitmedication_id=random.randint(1,3)),
    #     Medication(name='Antipyrine',  price=random.randint(50000,1000000),unitmedication_id=random.randint(1,3)),
    #     Medication(name='Lisdexamfetamine',  price=random.randint(50000,1000000),unitmedication_id=random.randint(1,3)),
    #     Medication(name='Amoxicillixxx',  price=random.randint(50000,1000000),unitmedication_id=random.randint(1,3))
    # ]
    # db.session.bulk_save_objects(p4)


    # ruleValue = {
    #     rule(id=1, name="Số lượng bệnh nhân", value=40),
    #     rule(id=2, name="Tiền khám bệnh", value=100000)
    # }
    # db.session.bulk_save_objects(ruleValue)  # Bang quy dinh



    db.session.commit()





