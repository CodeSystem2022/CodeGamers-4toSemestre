from flask import render_template, redirect, url_for, flash, request
from app import app
from flask_login import login_user, logout_user, login_required, current_user
from app.models import Paginas, Remeras, Users, Cart, Domicilios, Orders, OrderItems
from .forms import SignupForm, LoginForm, DomicilioForm
from urllib.parse import urlparse


@app.route('/')
@app.route('/remeras')
def home():
    remeras = Remeras.query.all()
    return render_template('index.html', remeras=remeras)


@app.route("/remera-<int:remera_id>")
def remera(remera_id):
    remera = Remeras.query.filter_by(remera_id=remera_id).first()
    return render_template('remera.html', remera=remera)


@app.route('/acerca')
def acerca():
    pagina = Paginas.query.filter_by(pagina_id=1).first()
    return render_template('pagina.html', pagina=pagina)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.get_by_email(form.email.data)
        if user is not None and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Email o contraseña incorrectos', 'danger')
    return render_template('login_form.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Cierre de sesión exitoso', category='success')
    return redirect(url_for('home'))


@app.route('/signup', methods=["GET", "POST"])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = SignupForm()
    error = None
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data
        # Comprobamos que no hay ya un usuario con ese email
        user = Users.get_by_email(email)
        if user is not None:
            error = f'El email {email} ya está siendo utilizado por otro usuario'
        else:
            # Creamos el usuario y lo guardamos
            user = Users(name=name, email=email)
            user.set_password(password)
            user.save()
            # Dejamos al usuario logueado
            login_user(user, remember=True)
            next_page = request.args.get('next', None)
            if not next_page or urlparse(next_page).netloc != '':
                next_page = url_for('home')
            return redirect(next_page)

    return render_template("signup_form.html", form=form, error=error)


@app.route('/cart')
@login_required
def cart():
    id = current_user.id
    cart_items = Cart.query.filter_by(cart_user_id=id).all()
    remeras = []
    total = 0
    for item in cart_items:
        remera = Remeras.query.get(item.cart_remera_id)
        remera.cantidad = item.cantidad
        total += remera.Precio * remera.cantidad
        remeras.append(remera)
    return render_template('cart.html', cart=remeras, total=total)


@app.route('/remera-<int:remera_id>/add_to_cart', methods=["POST", "GET"])
def add_to_cart(remera_id):
    if current_user.is_authenticated:
        id = current_user.id
        cart_item = Cart.query.filter_by(cart_remera_id=remera_id, cart_user_id=id).first()
        if cart_item:
            cart_item.cantidad += 1
            cart_item.save()
        else:
            cart = Cart(cart_remera_id=remera_id, cart_user_id=id, cantidad=1)
            cart.save()
    else:
        flash('Necesitas ingresar para agregar items al carro', category='danger')
        return redirect(url_for('login'))
    return redirect(url_for('cart'))


@app.route('/cart/remera-<int:remera_id>/sub', methods=["POST", "GET"])
def sub_from_cart(remera_id):
    id = current_user.id
    cart_item = Cart.query.filter_by(cart_remera_id=remera_id, cart_user_id=id).first()

    if not cart_item:
        return redirect(url_for('cart'))

    if cart_item.cantidad > 1:
        cart_item.cantidad -= 1
        cart_item.save()
    else:
        cart_item.delete()

    return redirect(url_for('cart'))


@app.route('/cart/remera-<int:remera_id>/add', methods=["POST", "GET"])
def add_from_cart(remera_id):
    id = current_user.id
    cart_item = Cart.query.filter_by(cart_remera_id=remera_id, cart_user_id=id).first()

    if not cart_item:
        return redirect(url_for('cart'))

    if cart_item.cantidad >= 1:
        cart_item.cantidad += 1
        cart_item.save()
    else:
        cart_item.delete()

    return redirect(url_for('cart'))

@app.route('/cart/remera-<int:remera_id>/remove', methods=["POST", "GET"])
def remove_from_cart(remera_id):
    id = current_user.id
    cart_item = Cart.query.filter_by(cart_remera_id=remera_id, cart_user_id=id).first()

    if not cart_item:
        return redirect(url_for('cart'))
    else:
        cart_item.delete()

    return redirect(url_for('cart'))


@app.route('/domicilio_envio', methods=['GET', 'POST'])
def domicilio_envio():
    form = DomicilioForm()
    domicilio = Domicilios.query.filter_by(domicilio_user_id=current_user.id).first()  # Busca el domicilio del usuario actual

    if form.validate_on_submit():
        if domicilio:
            # Actualiza los datos del domicilio existente
            domicilio.nombre = form.nombre.data
            domicilio.direccion = form.direccion.data
            domicilio.ciudad = form.ciudad.data
            domicilio.cp = form.cp.data
            domicilio.provincia = form.provincia.data
            domicilio.telefono = form.telefono.data
        else:
            # Crea un nuevo domicilio si el usuario no tiene uno
            domicilio = Domicilios(
                domicilio_user_id=current_user.id,
                nombre=form.nombre.data,
                direccion=form.direccion.data,
                ciudad=form.ciudad.data,
                cp=form.cp.data,
                provincia=form.provincia.data,
                telefono=form.telefono.data)
        order_id = crear_orden(current_user.id, domicilio.domicilio_id)
        domicilio.save()
        return redirect(url_for('forma_pago', order_id=order_id))

    # Si el usuario ya tiene un domicilio, llena el formulario con esos datos
    if domicilio:
        form.nombre.data = domicilio.nombre
        form.direccion.data = domicilio.direccion
        form.ciudad.data = domicilio.ciudad
        form.cp.data = domicilio.cp
        form.provincia.data = domicilio.provincia
        form.telefono.data = domicilio.telefono

    domicilio = Domicilios.query.filter_by(domicilio_user_id=current_user.id).first()
    return render_template('domicilio_form.html', form=form)

@app.route('/forma_pago-<int:order_id>', methods=['GET', 'POST'])
def forma_pago(order_id):
    order = Orders.query.filter_by(order_id=order_id).first()
    return render_template('pago.html', total=order.costo_total)


def crear_orden(user_id, domicilio_id):
    # Crear una nueva orden en la base de datos
    order = Orders(order_user_id=user_id, order_domicilio_id=domicilio_id)
    order.save()

    # Obtener los elementos del carrito del usuario
    cart_items = Cart.query.filter_by(cart_user_id=user_id).all()
    costo_total = 0

    # Agregar cada elemento del carrito como un elemento de la orden
    for cart_item in cart_items:
        remera = Remeras.query.get(cart_item.cart_remera_id)
        order_item = OrderItems(
            orderitem_order_id=order.order_id,
            orderitem_remera_id=cart_item.cart_remera_id,
            cantidad=cart_item.cantidad
        )
        costo_total += remera.Precio * cart_item.cantidad
        order_item.save()

    # Actualizar el costo total en la orden
    order.costo_total = costo_total
    order.save()

    # Vaciar el carrito del usuario
    for cart_item in cart_items:
        cart_item.delete()

    return order.order_id

