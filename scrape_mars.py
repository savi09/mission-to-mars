#!/usr/bin/env python
# coding: utf-8

# ## Mission to Mars

# In[1]:


# Dependencies
import os
from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


# ### NASA Mars News

# In[2]:


# URL of page to be scraped
url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'


# In[3]:


# Retrieve page with the requests module
response = requests.get(url, verify=False)
print(response.text)


# In[4]:


# Create BeautifulSoup object; parse with 'html.parser'
soup = bs(response.text, 'html.parser')


# In[5]:


# Examine the results, then determine element that contains sought info
print(soup.prettify())


# In[6]:


# results are returned as an iterable list
results = soup.find_all("div", class_ = "slide")
results


# In[7]:


for result in results:
       
    # Identify and return description of article
    news_desc = result.find("div", class_ = "rollover_description_inner").text
        
    # Identify and return title of article
    news_title = result.find("div", class_ = "content_title").a.text
    
    print("--------------------")
    print("Article Title: ", news_title)
    print("Description: ", news_desc)


# ### JPL Mars Space Images - Featured Image

# In[8]:


# Setup splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


image_url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
browser.visit(image_url)


# In[9]:


# Parsing HTML
html = browser.html
soup = bs(html, 'html.parser')
soup


# In[10]:


# Finding the header
header = soup.find_all('div', class_='header')
header


# In[11]:


# Searching Header for image src
for result in header:
       
    # Identify and return featured image src
    href = result.find("img", class_ = "headerimage fade-in")['src']
    
href


# In[12]:


# Creating link
link = f'{image_url}/{href}'
link


# In[13]:


browser.quit()


# ### Mars Facts

# In[14]:


# URL for Mar's facts
facts_url = 'https://space-facts.com/mars/'


# In[15]:


# Reading in tables
tables = pd.read_html(requests.get(facts_url).text)
tables


# In[16]:


# What type is tables
type(tables)


# In[17]:


df = tables[0]
df


# In[18]:


html_table = df.to_html()
html_table


# ### Mars Hemispheres

# In[22]:


# Setup splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

astro_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(astro_url)


# In[23]:


# Dependencies to fix an error below
# source: https://stackoverflow.com/questions/53052277/add-string-to-dictionary-without-quotes-in-python
import json
import ast


# In[24]:


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
  


# In[25]:


hemisphere_image_urls


# In[26]:


browser.quit()


# In[ ]:




