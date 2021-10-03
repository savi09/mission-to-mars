
# ## Mission to Mars

# Dependencies
import os
from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

def scrape():
    # ### NASA Mars News

    # Setup splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # URL of page to be scraped
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)

    # Parsing HTML
    nasa_html = browser.html
    nasa_soup = bs(nasa_html, 'html.parser')
    print(nasa_soup.prettify())

    # results are returned as an iterable list
    results = nasa_soup.find_all("li", class_ = "slide")
    results

    news_titles = []
    news_descriptions = []
    for result in results:
        
        # Identify and return description of article
        news_desc = result.find("div", class_ = "article_teaser_body").text
            
        # Identify and return title of article
        news_title = result.find("div", class_ = "content_title").a.text
        news_titles.append(news_title)
        news_descriptions.append(news_desc)
        
        print("--------------------")
        print("Article Title: ", news_title)
        print("Description: ", news_desc)

    # Latest news article info
    latest_news_title = news_titles[0]
    latest_news_desc = news_descriptions[0]
    print(latest_news_title)
    print(latest_news_desc)

    browser.quit()


    # ### JPL Mars Space Images - Featured Image

    # Setup splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)


    image_url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(image_url)

    # Parsing HTML
    html = browser.html
    soup = bs(html, 'html.parser')
    soup

    # Finding the header
    header = soup.find_all('div', class_='header')
    header

    # Searching Header for image src
    for result in header:
        
        # Identify and return featured image src
        href = result.find("img", class_ = "headerimage fade-in")['src']
        
    href

    # Creating link
    link = f'{image_url}/{href}'
    link

    browser.quit()


    # ### Mars Facts

    # URL for Mar's facts
    facts_url = 'https://space-facts.com/mars/'

    # Reading in tables
    tables = pd.read_html(requests.get(facts_url).text)
    tables

    # What type is tables
    type(tables)

    # Returning the first table
    df = tables[0]
    df

    # Converting table to html
    html_table = df.to_html()
    html_table


    # ### Mars Hemispheres

    # Setup splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    astro_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(astro_url)

    # Dependencies to fix an error below
    # source: https://stackoverflow.com/questions/53052277/add-string-to-dictionary-without-quotes-in-python
    import json
    import ast

    # Parsing Astro HTML
    astro_html = browser.html 
    astro_soup = bs(astro_html, 'html.parser')
    images = astro_soup.find_all('div', class_='item')
    hemisphere_image_urls = []

    for image in images: 
        div = image.find('div', class_='description')
        link = div.find("a")
        href = link["href"]
        title = link.find("h3").text
        hemis_url = f'https://astrogeology.usgs.gov{href}'
        browser.visit(hemis_url)
        astro_img_html = browser.html
        astro_img_soup = bs(astro_img_html, 'html.parser')
        containers = astro_img_soup.find_all('div', class_='downloads')
        
        for container in containers: 
            link = container.find("a")
            astro_img_href = link["href"]
        dic = '{"title": "' + title + '", "image_url": "' + astro_img_href + '"}'
        hemisphere_image_urls.append(ast.literal_eval(dic))
        
        print("----------")
        print(f'Title: {title}')
        print(f'Hemisphere Link: {hemis_url}')
        print(f'Image Link: {astro_img_href}')

    # Images url dictionaries
    hemisphere_image_urls

    browser.quit()

    # Store data in a dictionary
    mars_data = {
        "latest_news_title": latest_news_title,
        "latest_news_desc": latest_news_desc,
        "link": link,
        "html_table": html_table,
        "hemisphere_image_urls": hemisphere_image_urls
    }


    return mars_data

