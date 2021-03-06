from splinter import Browser
from bs4 import BeautifulSoup as BS
import pandas as pd
import requests
import selenium
from selenium import webdriver                   
from selenium.webdriver.common.keys import Keys   
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
# from pymongo import MongoClient

# def scrape_info():

# driver = webdriver.Firefox(executable_path= "geckodriver.exe")
# driver.maximize_window()



feature="https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
facts="https://space-facts.com/mars/"


# Connect to MongoDB
#connecting to the local host
# client =  MongoClient("mongodb://localhost:27017")
# #creating database
# db = client['mars_database']

def mars_news():
    driver = webdriver.Firefox()
    news="https://mars.nasa.gov/news/"
    driver.get(news)

        # Retrieve the latest news title
    title_elements = driver.find_elements_by_class_name("content_title")
    title_htmls = [title_element.get_attribute("innerHTML") for title_element in title_elements]
    title_html = title_htmls[1]
    news_soup = BS(title_html, 'lxml')
    news_title = news_soup.get_text()
    #news_title

    teaser_element = driver.find_element_by_class_name("article_teaser_body")
    news_p = teaser_element.get_attribute("innerHTML")
    #news_p
    # news_page_id=browser.find_by_id('site_body')
    news = {
    "title":news_title,
    "summary":news_p,
    }

    # timeout = 20
    # Find an ID on the page and wait before executing anything until found: 
    # try:
    #     WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.ID, "site_body")))
    # except TimeoutException:
    driver.quit()
    return news


def featured_image_url():
    driver = webdriver.Firefox()
    driver.implicitly_wait(10)
    driver.get(feature)

    # timeout = 20
    # #Find an ID on the page and wait before executing anything until found: 
    # try:
    #     WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.ID, "full_image")))
    # except TimeoutException:
    #     # driver.quit()
    #     print("Atribute Error")
    #LOOK FOR AN ID FIRST, THEN FIND THE ATTRIBUTE
    feature_image = driver.find_element_by_id("full_image")
    # featured_image = [image_element.get_attribute("data-link") for image_element in feature_image]
    # image_link=feature+featured_image[0]
    # driver.get(image_link)
    feature_image.click()

    featured_image_next = driver.find_element_by_partial_link_text("more info") #.get_attribute('href')
    featured_image_next.click()
    time.sleep(1)
    # featured_image_next = [image_element.get_attribute("data-link") for image_element in feature_image_next]
    # image_link_forrealz=feature+featured_image_next[0]
    # image_link_forrealz
    # driver.get(image_link_forrealz)

    # featured_soup = BeautifulSoup(html, 'html.parser')

    #main_image= featured_soup.find('img', class_='main_image')
    # try:
    featured_image_url = driver.find_element_by_tag_name('img[class="main_image"]').get_attribute('src')
    # except AttributeError:
    #     print("atrribute error")
    # driver.implicitly_wait(10)
    # large_image = driver.find_elements_by_class_name("main_image")

    # feat_images=[]
    # for feat_image in large_image:
    #     feat_images.append(feat_image.get_attribute("src"))

    # featured_image_url=feat_images[0]
    # featured_image_url = feat_image
    # main_image
    driver.quit()
    return featured_image_url


def mars_table():
    tables = pd.read_html(facts)
    mars_table=tables[0].to_html()
    return mars_table

def hemispheres_images():
    driver = webdriver.Firefox()
    hemisphere="https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    driver.get(hemisphere)
    driver.implicitly_wait(10)
    hemisphere_image_urls = []
    hemisphere_links = driver.find_elements_by_tag_name('h3')
    for link in range(len(hemisphere_links)):
        hemisphere_data = {}
    #     starting point
        hemisphere_links = driver.find_elements_by_tag_name('h3')
    #     print(hemisphere_links[link].text)   
        title = hemisphere_links[link].text
        hemisphere_data['title'] = title
    #     navigate to the h3 tag and get href attribute for the sample image
    #     append the href url to the dictionary
        hemisphere_links[link].click()
        sample = driver.find_element_by_link_text('Sample').get_attribute('href')
        #sample.click()
        hemisphere_data['img_url'] = sample
    #     append the image title and img url to the empty list
        hemisphere_image_urls.append(hemisphere_data)
        
    #     return to previous page to iterate through remaining images
        driver.back()
    #hemisphere_image_urls
    driver.quit()
    return hemisphere_image_urls

    

# A dictionary that will become a MongoDB document
def scrape_all():
    mars_dictionary = {
        'title': mars_news(),
        #'paragraph': news_p(),
        'image': featured_image_url(),
        'table': mars_table(),
        'urls': hemispheres_images(),
    }
    return mars_dictionary
    
    # # Declare the collection
    # mars_collection = db.mars_scrape
    # # Insert document into collection
    # mars_collection.insert_one(mars_dictionary)


