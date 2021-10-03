from flask import Flask, render_template, redirect
import pymongo
import scrape_mars

# Create an instance of our Flask app.
app = Flask(__name__)

# Create connection variable
conn = 'mongodb://localhost:27017'

# Pass connection to the pymongo instance.
client = pymongo.MongoClient(conn)

# Connect to a database. Will create one if not already available.
db = client.mars_db

# Drops collection if available to remove duplicates
db.mars.drop()



@app.route('/')
def index():
    mars = db.mars.find_one()
    return render_template('index.html', mars=mars)


@app.route('/scrape')
def scrape():
    mars = db.mars
    data = scrape_mars.scrape()
    mars.update(
        {},
        data,
        upsert=True
    )
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)