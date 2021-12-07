from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')


# CONNECT TO DATABASE
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL1', "sqlite:///cafes.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
Bootstrap(app)


# CREATING AND CONFIGURING TABLES
class Cafe(db.Model):
    __tablename__ = 'cafe'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Integer, nullable=False)
    has_wifi = db.Column(db.Integer, nullable=False)
    has_sockets = db.Column(db.Integer, nullable=False)
    can_take_calls = db.Column(db.Integer, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)
# db.create_all()


@app.route('/')
def home_page():
    all_cafes = db.session.query(Cafe).all()
    return render_template('index.html', cafes=all_cafes)

@app.route('/add_cafe', methods = ['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        map_url = request.form['map_url']
        img_url = request.form['img_url']
        location = request.form['location']
        seats = request.form['seats']
        has_toilet = request.form['has_toilet']
        has_wifi = request.form['has_wifi']
        has_sockets = request.form['has_sockets']
        can_take_calls = request.form['can_take_calls']
        coffee_price = request.form['coffee_price']

        new_cafe = Cafe(name = name,
                        map_url = map_url,
                        img_url = img_url,
                        location = location,
                        seats = seats,
                        has_toilet = has_toilet,
                        has_wifi = has_wifi,
                        has_sockets = has_sockets,
                        can_take_calls = can_take_calls,
                        coffee_price = coffee_price)
        db.session.add(new_cafe)
        db.session.commit()
        return redirect(url_for('home_page'))
    return render_template('right-sidebar.html')


@app.route('/search', methods = ['GET', 'POST'])
def search():
    if request.method == 'POST':
        location = request.form['search']
        all_matching_cafes = Cafe.query.filter_by(location=location).all()
        print(all_matching_cafes)
        return render_template('left-sidebar.html', cafes = all_matching_cafes)
    return render_template('left-sidebar.html')


@app.route('/delete/<int:cafe_id>', methods = ['GET'])
def delete(cafe_id):
    cafe_to_delete = Cafe.query.get(cafe_id)
    db.session.delete(cafe_to_delete)
    db.session.commit()
    return redirect(url_for('home_page'))


if __name__ == '__main__':
    app.run(debug=True)
