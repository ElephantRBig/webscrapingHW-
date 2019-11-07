# Import our pymongo library, which lets us connect our Flask app to our Mongo database.
# import pymongo

# Create an instance of our Flask app.


# Setup connection to mongodb
# conn = "mongodb://localhost:27017"
# client = pymongo.MongoClient(conn)

# Select database and collection to use
# db = client.marsScrape
# collection = db.marsItems

# inserting the dictionary 'marsDict' into the marsScrape database
# collection.insert(marsDict)
from flask import Flask, render_template, escape, url_for
import json

app = Flask(__name__)

@app.route('/')
def echo():
    # Import our pymongo library, which lets us connect our Flask app to our Mongo database.
    import pymongo

    # Setup connection to mongodb
    conn = "mongodb://localhost:27017"
    client = pymongo.MongoClient(conn)

        # Select database and collection to use
    db = client.marsScrape
    collection = db.collection
    data = collection.find({})[0]
    return render_template("index.html", data = data)


@app.route('/scrape')
def scrape():

    from bs4 import BeautifulSoup as soup

    from urllib.request import urlopen as uReq

    myurl = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'

    # Opening a connection and grabbing the page 
    uClient = uReq(myurl)

    page_html = uClient.read()

    #uClient.close()

    # Html parsing
    page_soup = soup(page_html,"html.parser")

    contentContainer = page_soup.findAll("div",{"class":"content_title"})

    #Creating the dictionary
    marsDict = {}

    # grabs each product 
    news_title = contentContainer[0].a.text.strip()
    news_title
    marsDict['news_title'] = news_title

    contentContainer = page_soup.findAll("div",{"class":"image_and_description_container"})[0]

    news_p = contentContainer.div.div.text.strip()
    news_p
    marsDict['news_p'] = news_p

    # Retrieving the featured image URL 
    from splinter import Browser

    executable_path = {'executable_path':'chromedriver.exe'}
    browser = Browser('chrome',**executable_path, headless = False)

    #with Browser() as browser:
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)

    html = browser.html 
    page_soup = soup(html, "html.parser")

    featured_image_url = page_soup.find_all('div', class_="carousel_items")

    image_url = featured_image_url[0].article['style'][23:75]

    image_url

    marsDict['image_url'] = image_url

    featured_image_url = 'https://www.jpl.nasa.gov'+image_url

    featured_image_url

    marsDict['image_url'] = featured_image_url
    

    # Scraping the Mars Weather twitter page for the latest tweet
    url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url)

    html = browser.html
    page_soup = soup(html,'html.parser')

    mars_weather = page_soup.find_all('div', class_='js-tweet-text-container')[0].text.strip()#mars_weather =  

    mars_weather

    marsDict['mars_weather'] = mars_weather

    # Scraping the Mars Facts webpage 
    import pandas as pd
    import requests

    # Pandas scraping the URL for a table containing facts about Mars 

    url = 'https://space-facts.com/mars/'
    mars_table = pd.read_html(url)

    marsTable = mars_table[0]

    marsTableHtml = marsTable.to_html().replace('\n','')

    marsTableHtml


    marsDict['img_url'] = []
    marsDict['title'] = []

    # Here i am setting up the code to retrieve the mars pic titles and img urls

    #img url 1
    url = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced'
    imgUrl1 = requests.get(url)
    page_soup = soup(imgUrl1.text, 'html.parser')
    img_url1 = "https://astrogeology.usgs.gov"+ page_soup.find_all('img', class_ = 'wide-image')[0]['src']
    url1Title = page_soup.find_all('h2',class_ = 'title')[0].text

    marsDict['img_url'].append(img_url1)
    marsDict['title'].append(url1Title)


    marsDict

    #img url 2
    url = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced'
    imgUrl1 = requests.get(url)
    page_soup = soup(imgUrl1.text, 'html.parser')
    img_url1 = "https://astrogeology.usgs.gov"+ page_soup.find_all('img', class_ = 'wide-image')[0]['src']
    url1Title = page_soup.find_all('h2',class_ = 'title')[0].text

    marsDict['img_url'].append(img_url1)
    marsDict['title'].append(url1Title)

    #img url 3
    url = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced'
    imgUrl1 = requests.get(url)
    page_soup = soup(imgUrl1.text, 'html.parser')
    img_url1 = "https://astrogeology.usgs.gov"+ page_soup.find_all('img', class_ = 'wide-image')[0]['src']
    url1Title = page_soup.find_all('h2',class_ = 'title')[0].text

    marsDict['img_url'].append(img_url1)
    marsDict['title'].append(url1Title)

    #img url 4
    url = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced'
    imgUrl1 = requests.get(url)
    page_soup = soup(imgUrl1.text, 'html.parser')
    img_url1 = "https://astrogeology.usgs.gov"+ page_soup.find_all('img', class_ = 'wide-image')[0]['src']
    url1Title = page_soup.find_all('h2',class_ = 'title')[0].text

    marsDict['img_url'].append(img_url1)
    marsDict['title'].append(url1Title)

    marsDict


    # Import our pymongo library, which lets us connect our Flask app to our Mongo database.
    import pymongo

    # Setup connection to mongodb
    conn = "mongodb://localhost:27017"
    client = pymongo.MongoClient(conn)

        # Select database and collection to use
    db = client.marsScrape
    collection = db.marsItems


if __name__=="__main__":
    app.run(debug=True)