# from bs4 import BeautifulSoup
# import pandas as pd
# import datetime as dt
from flask import Flask, render_template, redirect
#from flask_pymongo import PyMongo
from pymongo import MongoClient as MC
import pymongo
import mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
# app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_database"
# mongo = PyMongo(app)
# mars_collection = mongo.mars_collection
# Use PyMongo to establish Mongo connection
mongo = MC()
db = mongo.mars_app
col = db.mars_data

@app.route("/")
def index():
    #mars2 = mongo.db.mars2.find_one()
    # To view the content of table mars
    mars2=col.find_one({}, sort=[("_id", pymongo.DESCENDING)])

    print(mars2)
    return render_template("index.html", mars=mars2)


@app.route("/scrape")
def scrape():
    #mars2 = mongo.db.mars2
    mars_data= mars.scrape_all()
    # print(mars_data)
    col.insert(mars_data)
    #mars.replace_one({}, mars_database, upsert=True)
    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
