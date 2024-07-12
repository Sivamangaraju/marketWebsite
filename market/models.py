
from market import db
from market import bcrypt

class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username=db.Column(db.String(length=30),nullable=False,unique=True)
    email_address=db.Column(db.String(length=50),nullable=False,unique=True)
    password_hash=db.Column(db.String(length=60),nullable=False)
    budget=db.Column(db.Integer(),nullable=False,default=1000)
    items=db.relationship('Item',backref='owned_user',lazy=True)
    
    @property
    def password(self):
        #raise AttributeError('Password is not a readable attribute.')
        return self.password
    @password.setter
    def password(self, passText):
        self.password_hash = bcrypt.generate_password_hash(passText).decode('utf-8')


class Item(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    price = db.Column(db.Integer(), nullable=False)
    barcode = db.Column(db.String(length=4), nullable=False, unique=True)
    description = db.Column(db.String(length=1024), nullable=False, unique=True)
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'))

    def __repr__(self):
        return f'Item {self.name}{self.barcode}{self.description}{self.price}{self.id}'