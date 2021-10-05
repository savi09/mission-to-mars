from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of our Flask app.
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection

mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

@app.route('/')
def index():
    mars = mongo.db.mars.find_one()
    links = mongo.db.links.find_one()
    return render_template('index.html', mars=mars)


@app.route('/scrape')
def scrape():
    mars = mongo.db.mars
    links = mongo.db.links
    data = scrape_mars.scrape()
    mars.update({}, data[0], upsert=True)
    links.update({}, data[1], upsert=True)
    return redirect('/', code=302)


if __name__ == "__main__":
    app.run(debug=True)