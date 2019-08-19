from bs4 import BeautifulSoup as bs
import requests

from splinter import Browser
import time
import pandas as pd


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/Users/reena/Downloads/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape_info():
    browser = init_browser()

    # Visit visitcostarica.herokuapp.com
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # Get news title and paragraph text
    news_title = soup.find('div', class_='content_title').get_text()
    news_p = soup.find('div', class_='article_teaser_body').get_text()
    print(news_title)
    print(news_p)

    # Get featured image url
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    time.sleep(1)
    html = browser.html
    soup = bs(html, 'html.parser')

    image = soup.find('div', class_='carousel_items').find('article')['style']
    image_url = image.split("'")[1]
    url_base = "https://www.jpl.nasa.gov"
    featured_image_url = url_base + image_url
    print(featured_image_url)

    # Get mars facts
    url = "https://space-facts.com/mars/"
    tables = pd.read_html(url)
    df2 = tables[1]
    df2.columns = ["Parameter", "Values"]
    table = df2.to_dict('records')



    # Get mars hemispheres
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    url_base = "https://astrogeology.usgs.gov"

    browser.visit(url)
    time.sleep(1)
    html = browser.html
    soup = bs(html, 'html.parser')

    result = soup.find_all('div', class_="item")
    url_list = []

    for y in result:
        link = y.find('a')['href']
        url_list.append(link)

    hemisphere_image_urls = []

    for x in url_list:
        url1 = url_base + x
        
        
        browser.visit(url1)
        html = browser.html
        soup = bs(html, 'html.parser')
        time.sleep(1)
        
        result1 = soup.find('img', class_="wide-image")
        image = url_base + result1["src"]

        result2 = soup.find('h2', class_='title')
        title = result2.text
        title = title.rsplit(' ', 1)[0]
        
        mars_hemi = {"title": title, "img_url": image}
        hemisphere_image_urls.append(mars_hemi)

    print(hemisphere_image_urls)

    # Store data in a dictionary
    results = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "table": table,
        "hemisphere_image_urls": hemisphere_image_urls
    }

    # Close the browser after scraping
    browser.quit()
    print(results)

    # Return results
    return results

if __name__ == "__main__":
    scrape_info()
