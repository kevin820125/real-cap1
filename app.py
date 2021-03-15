import os

from flask import Flask, render_template, request, flash, redirect, session, g,jsonify
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
import requests

from forms import SignUpForm,LoginForm , EditForm , SearchForm
from models import db, connect_db, User , default_img , Favorite


CURR_USER_KEY = "curr_user"
app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgres:///capstone1_db'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")
toolbar = DebugToolbarExtension(app)

connect_db(app)


@app.before_request
def add_user_to_g():
    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])
    else:
        g.user = None

def do_login(user):
    session[CURR_USER_KEY] = user.id


def do_logout():
    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]



@app.route('/')
def main_page():
    res = requests.get(
        'https://www.thecocktaildb.com/api/json/v1/1/random.php')
    data = res.json()
    random_drink = data['drinks'][0]['strDrink']
    if g.user:
        user = g.user
        return render_template('main_page.html' , user = user , drink = random_drink )
    return render_template('main_page.html' , drink = random_drink )


@app.route('/search' ,methods=[ "POST"])
def search():
    value = request.form['search']
    res = requests.get(
        f'https://www.thecocktaildb.com/api/json/v1/1/search.php?s={value}'
    )
    data = res.json()['drinks']
    if data:
        return render_template('show_cocktail_list.html' , data = data)
    else:
        flash('OH oh! We can not find that cocktail for you!')
        return redirect('/')



@app.route('/signup' , methods=["GET", "POST"])
def signUp():
    form = SignUpForm()
    if form.validate_on_submit():
        try:
            user  = User.signUp(username = form.username.data,
                password=form.password.data,
                email=form.email.data,
                image_url=form.image_url.data or None,
                birthday = form.birthday.data)
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            flash("Username/Email is already taken", 'danger')
            return render_template('SignUp.html', form=form)

        do_login(user)
        return redirect('/')

    else:
        return render_template('SignUp.html' , form = form)


@app.route('/login' , methods=["GET", "POST"])
def LogIn():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.auth(username , password)
        if user:
            flash(f'Welcome Home! {user.username} ' , 'success')
            do_login(user)
            return redirect('/')
        else:
            flash('Password/Username invalid , please try again' , 'danger')
            return redirect('/login')

    else:
        return render_template('login.html' , form = form)


@app.route('/logout')
def logout():
    do_logout()
    return redirect('/')

@app.route('/about-me')
def about_us():
    return render_template('about_me.html')


@app.route('/profile')
def profile():
    if g.user:
        user = g.user
        fav_name = [i.fav_name for i in user.favs]
        fav_url = [i.fav_URL for i in user.favs]
        return render_template('profile.html' , user = user , fav_name = fav_name , fav_url = fav_url)

    else:
        flash('Unauthorized' , 'danger')
        return redirect('/login')

@app.route('/edit' , methods=["GET", "POST"])
def edit():
    form = EditForm()
    if g.user:
        if form.validate_on_submit():
            try:
                user = g.user
                user.username = form.username.data
                user.email = form.email.data
                user.image_url = form.image_url.data or default_img
                db.session.commit()
                return redirect('/profile')
            except IntegrityError:
                flash("Username/Email is already taken", 'danger')
                return redirect('/edit')
        else:
            return render_template('edit.html' , form = form)



    else:
        flash('Unauthorized' , 'danger')
        return redirect('/login')

@app.route('/sprit/<name>')
def show_spirit_cocktial(name):
    user = g.user
    res = requests.get(f'https://www.thecocktaildb.com/api/json/v1/1/filter.php?i={name}')
    data = res.json()['drinks']
    return render_template('show_cocktail_list.html' , data = data , name = name , user = user)

@app.route('/cocktail/<name>')
def show_cocktail_detail(name):
    user = g.user
    res = requests.get(f'https://www.thecocktaildb.com/api/json/v1/1/search.php?s={name}')
    # import pdb; pdb.set_trace()
    data = res.json()['drinks'][0]
    if user:
        favs = [i.fav_cocktail_id for i in user.favs]
        return render_template('showCocktail.html' , data = data , name = name ,user = user  , favs = favs)
    else:
        return render_template('showCocktail.html' , data = data , name = name ,user = user)


@app.route('/addcocktail' , methods=["POST"])
def add_fav():
    res = request.json
    cockid = res["cocktail_id"]
    user = g.user
    find_cock = Favorite.query.filter_by(user_id = user.id , fav_cocktail_id = cockid).first()
    # import pdb; pdb.set_trace()
    if find_cock:
        db.session.delete(find_cock)
        db.session.commit()
        return str('Unfavorited')
    else:
        res = requests.get(f'https://www.thecocktaildb.com/api/json/v1/1/lookup.php?i={cockid}')
        # import pdb; pdb.set_trace()
        cock_name = res.json()['drinks'][0]['strDrink']
        cock_url = res.json()['drinks'][0]['strDrinkThumb']
        addFav = Favorite(user_id = user.id , fav_cocktail_id = cockid , fav_URL = cock_url , fav_name = cock_name)

        db.session.add(addFav)
        db.session.commit()
        return str('add to favorite')