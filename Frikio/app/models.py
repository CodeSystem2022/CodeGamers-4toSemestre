from sqlalchemy import Integer, Text, String, BLOB, REAL, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class Base(DeclarativeBase):  # Subclase de DeclarativeBase
    pass

db = SQLAlchemy(model_class=Base)

class Paginas(db.Model):
    __tablename__ = 'paginas'
    pagina_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    contenido: Mapped[str] = mapped_column(Text)


class Remeras(db.Model):
    __tablename__ = 'remeras'
    remera_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    Titulo: Mapped[str] = mapped_column(Text, nullable=False)
    Precio: Mapped[float] = mapped_column(REAL, nullable=False)
    Imagen: Mapped[str] = mapped_column(Text, nullable=True)
    Descripcion: Mapped[str] = mapped_column(BLOB, nullable=True)
    cantidad: Mapped[int] = mapped_column(Integer)


class Users(db.Model, UserMixin):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(80), nullable=False)
    email: Mapped[str] = mapped_column(String(256), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(128), nullable=False)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)

    def __init__(self, name, email):
        self.name = name
        self.email = email

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def save(self):
        if not self.user_id:
            db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return '<User {}>'.format(self.email)

    @staticmethod
    def get_by_id(user_id):
        return Users.query.get(id)

    @staticmethod
    def get_by_email(email):
        return Users.query.filter_by(email=email).first()

class Cart(db.Model):
    __tablename__ = 'cart'
    cart_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    cart_user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)
    cart_remera_id: Mapped[int] = mapped_column(Integer, ForeignKey('remeras.remera_id'), nullable=False)
    cantidad: Mapped[int] = mapped_column(Integer, default=1)

    def __init__(self, cart_user_id, cart_remera_id, cantidad=1):
        self.cart_user_id = cart_user_id
        self.cart_remera_id = cart_remera_id
        self.cantidad = cantidad

    def actualizar_cantidad(self, cantidad):
        self.cantidad += cantidad
        db.session.commit()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Domicilios(db.Model):
    __tablename__ = 'domicilios'
    domicilio_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    domicilio_user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)
    nombre: Mapped[str] = mapped_column(Text, nullable=False)
    direccion: Mapped[str] = mapped_column(Text, nullable=False)
    ciudad: Mapped[str] = mapped_column(Text, nullable=False)
    cp: Mapped[str] = mapped_column(Text, nullable=False)
    provincia: Mapped[str] = mapped_column(Text, nullable=False)
    telefono: Mapped[str] = mapped_column(Text, nullable=False)

    def __init__(self, domicilio_user_id, nombre, direccion, ciudad, cp, provincia, telefono):
        self.domicilio_user_id = domicilio_user_id
        self.nombre = nombre
        self.direccion = direccion
        self.ciudad = ciudad
        self.cp = cp
        self.provincia = provincia
        self.telefono = telefono

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()



class Orders(db.Model):
    __tablename__ = 'orders'
    order_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    order_user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)
    order_domicilio_id: Mapped[int] = mapped_column(Integer, ForeignKey('domicilios.domicilio_id'), nullable=False)
    costo_total: Mapped[int] = mapped_column(Integer, nullable=False)

    def __init__(self, order_user_id, order_domicilio_id):
        self.order_user_id = order_user_id
        self.order_domicilio_id = order_domicilio_id

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class OrderItems(db.Model):
    __tablename__ = 'orderitems'
    orderitem_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    orderitem_order_id: Mapped[int] = mapped_column(Integer, ForeignKey('orders.order_id'), nullable=False)
    orderitem_remera_id: Mapped[int] = mapped_column(Integer, ForeignKey('remeras.remera_id'), nullable=False)
    cantidad: Mapped[int] = mapped_column(Integer, nullable=False)

    def __init__(self, orderitem_order_id, orderitem_remera_id, cantidad):
        self.orderitem_order_id = orderitem_order_id
        self.orderitem_remera_id = orderitem_remera_id
        self.cantidad = cantidad

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

