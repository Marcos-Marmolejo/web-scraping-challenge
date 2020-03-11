from bs4 import BeautifulSoup 
import pymongo
from splinter import Browser
import pandas as pd
import time


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

def scrape_info():
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    time.sleep(1)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")


    news_title = soup.find("div", class_="content_title").text

    news_p = soup.find("div", class_="article_teaser_body").text

    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    image = soup.find("img", class_="thumb")["src"]
    featured_image_url = "https://www.jpl.nasa.gov" + image


    url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    mars_weather = soup.find('p', class_="tweet-text")


    url = "http://space-facts.com/mars/"
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    mars_facts = pd.read_html(url)[0]
    mars_facts.columns = ["Description", "Value"]
    mars_facts = mars_facts.set_index("Description")
    mars_facts = mars_facts.to_html(index = True, header =True)


    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    root_url = "https://astrogeology.usgs.gov"
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    xpath = "//div[@class='description']//a[@class='itemLink product-item']/h3"
    results = browser.find_by_xpath(xpath)
    results[0].html
    hemisphere_image_urls = []

    for i in range(4):

        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')

        # find the new Splinter elements
        results = browser.find_by_xpath(xpath)

        # Save the name of the hemisphere
        header = results[i].html

        # Click on the header to go to the hemisphere details page 
        details_link = results[i]
        details_link.click()

        # Load hemisphere details page into Beautiful Soup
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')

        # Save the image url
        hemisphere_image_urls.append({"title": header, "image_url": soup.find("div", class_="downloads").a["href"]})
    
    # Go back to the original page
    browser.back()

    

    costa_data = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "mars_weather": mars_weather,
        "mars_facts":mars_facts,
        "hemisphere_image_urls":hemisphere_image_urls
        }

    return costa_data
