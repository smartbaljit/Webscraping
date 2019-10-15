from splinter import Browser
from bs4 import BeautifulSoup
import time
import os
import pandas as pd
import time
import requests

executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)
    
def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    return browser

def scrape():
    browser = init_browser()
    mars_results = {}

    newsResults = marsNews()
    mars_results["news_title"] = newsResults[0]
    mars_results["news_paragraph"] = newsResults[1]
    mars_results["mars_image"] = marsImage()
    mars_results["mars_weather"] = marsWeather()
    mars_results["mars_facts"] = marsFacts()
    mars_results["mars_hemisphere"] = marsHem()

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_results



# NASA Mars News
def marsNews():
    url_1 = "https://mars.nasa.gov/news/"
    browser.visit(url_1)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    
    article = soup.find("div", class_='list_text')
    news_title = article.find("div", class_="content_title").text
    news_p = article.find("div", class_ ="article_teaser_body").text
    news_result = [news_title, news_p]
    return news_result


# JPL Mars Space Images - Featured Image
def marsImage():
    image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(image_url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    image = soup.find("img", class_="thumb")["src"]
    featured_image_url = "https://www.jpl.nasa.gov" + image
    return featured_image_url


# Mars Weather
def marsWeather():
    url_3 = 'https://twitter.com/marswxreport?lang=en'
    response = requests.get(url_3)
    soup = BeautifulSoup(response.text, 'html.parser')
    tweet_results = soup.find_all("div", class_="js-tweet-text-container")
    mars_weather=tweet_results[1].text
    return mars_weather


# Mars Facts
def marsFacts():
    import pandas as pd
    url_table = 'https://space-facts.com/mars/'
    tables = pd.read_html(url_table)
    df = pd.DataFrame(tables[1])
    html_table = df.to_html(header = False, index = False)
    return html_table


# Mars Hemispheres
def marsHem():
    import time 
    hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemispheres_url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    mars_hemisphere = []

    products = soup.find("div", class_ = "result-list" )
    hemispheres = products.find_all("div", class_="item")

    for hemisphere in hemispheres:
        title = hemisphere.find("h3").text
        title = title.replace("Enhanced", "")
        end_link = hemisphere.find("a")["href"]
        image_link = "https://astrogeology.usgs.gov/" + end_link    
        browser.visit(image_link)
        html = browser.html
        soup=BeautifulSoup(html, "html.parser")
        downloads = soup.find("div", class_="downloads")
        image_url = downloads.find("a")["href"]
        dictionary = {"title": title, "img_url": image_url}
        mars_hemisphere.append(dictionary)
    return mars_hemisphere

