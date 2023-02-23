from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Enum, Float, DateTime, Date
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
    avatar = Column(String(100), nullable=False,)
    user_role = Column(Enum(UserRole), default=UserRole.USER)

    def __str__(self):
        return self.name


# class DanhSachKhamBenh(db.Model):
#     id = Column (Integer, primary_key=True, autoincrement=True)
#     name =  Column(String(50), nullable=False, unique=True)
#     sex = Column(Boolean, default=True)
#     birth = Column(Date)
#     address = Column(String(100), nullable=False)
#     created_data = Column(DATETIME, default=datetime.now())

class medication(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    type = Column(String(10), nullable=True)
    price = Column(Float, default=0)


if __name__ == '__main__':

    # p1=[
    #     medication(name='Amoxicillin', type='Lo', price=random.randint(50000,1000000)),
    #     medication(name='Azithromycin', type='Vy', price=random.randint(50000,1000000)),
    #     medication(name='Albuterol', type='Chai', price=random.randint(50000,1000000)),
    #     medication(name='Clavulanate', type='Vy', price=random.randint(50000,1000000)),
    #     medication(name='Cefdinir', type='Lo', price=random.randint(50000,1000000)),
    #     medication(name='Cephalexin', type='Chai', price=random.randint(50000,1000000)),
    #     medication(name='Fluticasone', type='Lo', price=random.randint(50000,1000000)),
    #     medication(name='Prednisolone Sodium Phosphate', type='Lo', price=random.randint(50000,1000000)),
    #     medication(name='Ibuprofen', type='Vy', price=random.randint(50000,1000000)),
    #     medication(name='Singulair ', type='Chai', price=random.randint(50000,1000000)),
    #     medication(name='Trimethoprim', type='Lo', price=random.randint(50000,1000000)),
    #     medication(name='Tylenol ', type='Vy', price=random.randint(50000,1000000)),
    #     medication(name='Vicodin', type='Lo', price=random.randint(50000,1000000)),
    #     medication(name='Mupirocin', type='Chai', price=random.randint(50000,1000000)),
    #     medication(name='Nystatin', type='Lo', price=random.randint(50000,1000000)),
    #     medication(name='Methylphenidate', type='Lo', price=random.randint(50000,1000000)),
    #     medication(name='Cough and Cold Combinations', type='Lo', price=random.randint(50000,1000000)),
    #     medication(name='Mometasone', type='Chai', price=random.randint(50000,1000000)),
    #     medication(name='Triamcinolone', type='Chai', price=random.randint(50000,1000000)),
    #     medication(name='Prednisone', type='Vy', price=random.randint(50000,1000000)),
    #     medication(name='Sodium Fluoride', type='Lo', price=random.randint(50000,1000000)),
    #     medication(name='Multivitamins With Fluoride', type='Lo', price=random.randint(50000,1000000)),
    #     medication(name='Amphetamine', type='Lo', price=random.randint(50000,1000000)),
    #     medication(name='Hydrocortisone', type='Vy', price=random.randint(50000,1000000)),
    #     medication(name='Budesonide', type='Vy', price=random.randint(50000,1000000)),
    #     medication(name='Promethazine', type='Vy', price=random.randint(50000,1000000)),
    #     medication(name='Ciprofloxacin', type='Lo', price=random.randint(50000,1000000)),
    #     medication(name='Antipyrine', type='Chai', price=random.randint(50000,1000000)),
    #     medication(name='Lisdexamfetamine', type='Chai', price=random.randint(50000,1000000)),
    #     medication(name='Amoxicillixxx', type='Vy', price=random.randint(50000,1000000))
    # ]
    # db.session.bulk_save_objects(p1)

    # db.create_all()
    db.session.commit()
