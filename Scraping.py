# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt


def scrape_all():
    # Initiate headless driver for deployment
    browser = Browser("chrome", executable_path="chromedriver", headless=True)

    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "hemi": mars_hemi(browser),
        "last_modified": dt.datetime.now()
    }

    # Stop webdriver and return data
    browser.quit()
    return data

### Mars News

def mars_news(browser):

    # Scrape Mars News
    # Visit the mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one("ul.item_list li.slide")
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find("div", class_="content_title").get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find("div", class_="article_teaser_body").get_text()

    except AttributeError:
        return None, None

    return news_title, news_p

### Mars Featured Image

def featured_image(browser):
    # Visit URL
    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

    # Use the base url to create an absolute url
    img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'

    return img_url

### Mars Facts

def mars_facts():
    # Add try/except for error handling
    try:
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('http://space-facts.com/mars/')[0]

    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars']
    df.set_index('Description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html(classes="table table-striped")

### Mars Hemispheres

def mars_hemi(browser):
    # Visit URL
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    
    # Create a list to hold the images and titles.
    hemisphere_image_urls = []
    
    # Parse the HTML
    html = browser.html
    hemisphere_soup = soup(html, 'html.parser')

    for t in hemisphere_soup.find_all('div', class_='description'):
    
    # Create Hemisphere dictionary
    hemispheres = {}
    
    # Collect title
    title = t.find('h3').string
    
    # Print to see if right title was grabbed
    #print(title)
    
    # Href to open window with download class
    href = t.find('a').get('href')
    
    # Create new browser to parse html for download class
    # This class contains the href for the wide-image
    new_browser = Browser('chrome', **executable_path, headless=True)
    new_browser.visit('https://astrogeology.usgs.gov' + href)
    
    # Get html from new browser page
    new_html = new_browser.html
    
    # Create new soup for new browser page
    new_soup = soup(new_html, 'html.parser')
    
    # Get img class from new soup
    img_class = new_soup.find('div',class_='downloads')
    
    # Get img url from img class
    img_url = img_class.find('a').get('href')
    
    # Print to see if right url grabbed
    #print(img_url)
    
    # Cache dictonary here using title and img_url variables
    hemispheres['img_url'] = img_url
    hemispheres['title'] = title
    
    # Create a copy of hemispheres dictionary
    hemi_copy = hemispheres.copy()
    
    # Send copy to hemispheres list
    hemisphere_image_urls.append(hemi_copy)
    
    return hemisphere_image_urls


if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())