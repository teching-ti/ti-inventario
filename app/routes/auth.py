from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from app.models.userModels import User, db
from app.forms import AdminLoginForm, AdminRegisterForm

#uso de blueprints para el manejo de rutas
auth_bp = Blueprint('auth', __name__)

#se establece como ruta principal, ya que se debe hacer un login desde la ruta auth para poder acceder al sistema

@auth_bp.route('/')
@login_required
def inicio():
    return render_template('index.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('auth.inicio'))

    form = AdminLoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('auth.inicio'))
        else:
            print("Error")
            #print(username)
            #print(password)
            #se podría colocar un mensaje
            #flash('Invalid username or password.', 'danger')
    return render_template('login.html', form=form)


@auth_bp.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    form = AdminRegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            #flash('Username already exists. Please choose a different one.', 'danger')
            print("")
        else:
            new_user = User(username=username)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('auth.inicio'))
    return render_template('register.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.inicio'))