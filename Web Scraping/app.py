from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import ScrapeMars

app=Flask(__name__)

# Create connection and Pass connection to the pymongo instance.
app.config["MONGO_URI"] = "mongodb://127.0.0.1:27017/marsdb"
mongo = PyMongo(app)
#collection = mongo.db.mars

#index route to render mongo database
@app.route("/")
def home():
    # Find data from the mongo database
    mars = mongo.db.mars.find_one()
    # Return template and data
    return render_template("index.html",mars=mars )

    #route to render scrape template
@app.route("/scrape")
def scraper():
    mars_data = ScrapeMars.scrape_all()
    mongo.db.mars.update_one({},{'$set':mars_data},upsert=True)
    return redirect ("/")
if __name__ == "__main__":
    app.run(debug=True)