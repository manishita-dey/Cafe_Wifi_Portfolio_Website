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

cafe1 = Cafe(name = 'Science Gallery London',
                        map_url = 'https://g.page/scigallerylon?share',
                        img_url = 'https://atlondonbridge.com/wp-content/uploads/2019/02/Pano_9758_9761-Edit-190918_LTS_Science_Gallery-Medium-Crop-V2.jpg',
                        location = 'London Bridge',
                        seats = '50+',
                        has_toilet = '1',
                        has_wifi = '0',
                        has_sockets = '1',
                        can_take_calls = '1',
                        coffee_price = '£2.40')


cafe2 = Cafe(name='Social - Copeland Road',
                map_url='https://g.page/CopelandSocial?share',
                img_url='https://images.squarespace-cdn.com/content/v1/5734f3ff4d088e2c5b08fe13/1555848382269-9F13FE1WQDNUUDQOAOXF/ke17ZwdGBToddI8pDm48kAeyi0pcxjZfLZiASAF9yCBZw-zPPgdn4jUwVcJE1ZvWQUxwkmyExglNqGp0IvTJZUJFbgE-7XRK3dMEBRBhUpzV8NE8s7067ZLWyi1jRvJklJnlBFEUyq1al9AqaQ7pI4DcRJq_Lf3JCtFMXgpPQyk/copeland-park-bar-peckham',
                location='Peckham',
                seats='20-30',
                has_toilet='1',
                has_wifi='1',
                has_sockets='1',
                can_take_calls='0',
                coffee_price='£2.75')

cafe3 = Cafe(name='One & All Cafe Peckham',
                map_url='https://g.page/one-all-cafe?share',
                img_url='https://lh3.googleusercontent.com/p/AF1QipOMzXpKAQNyUvrjTGHqCgWk8spwnzwP8Ml2aDKt=s0',
                location='Peckham',
                seats='20-30',
                has_toilet='1',
                has_wifi='1',
                has_sockets='1',
                can_take_calls='0',
                coffee_price='£2.75')

db.session.add(cafe1)
db.session.add(cafe2)
db.session.add(cafe2)
db.session.commit()

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
