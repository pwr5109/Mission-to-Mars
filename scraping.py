from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt


def scrape_all():
    # Start driver
    browser = Browser("chrome", executable_path="chromedriver", headless=True)

    news_title, news_paragraph = mars_news(browser)

    # Run scraping functions and store data
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "hemi": mars_hemi(browser),
        "last_modified": dt.datetime.now()
    }

    # Stop driver and show data
    browser.quit()
    return data

### Mars News

def mars_news(browser):

    # Visit Mars Site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    # Convert to soup object
    html = browser.html
    news_soup = soup(html, 'html.parser')
    
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

    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url)

    # Click image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the soup result
    html = browser.html
    img_soup = soup(html, 'html.parser')

    try:
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

    img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'

    return img_url

### Mars Facts

def mars_facts():
    
    try:
        
        df = pd.read_html('http://space-facts.com/mars/')[0]

    except BaseException:
        return None

    # Assign dataframe
    df.columns=['Description', 'Mars']
    df.set_index('Description', inplace=True)

    # Convert dataframe
    return df.to_html(classes="table table-striped")

### Mars Hemispheres

def mars_hemi(browser):
  
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    
    # Create a list
    hemisphere_image_urls = []
    
    # Parse HTML
    html = browser.html
    hemisphere_soup = soup(html, 'html.parser')

    for t in hemisphere_soup.find_all('div', class_='description'):
    
    # Create Hemisphere dictionary
    hemispheres = {}
    
    # Collect title
    title = t.find('h3').string
    
    # Print
    print(title)
    
    # Href download class
    href = t.find('a').get('href')
    
    # Create new browser to parse html for download class
    new_browser = Browser('chrome', **executable_path, headless=True)
    new_browser.visit('https://astrogeology.usgs.gov' + href)
    
    # Get new browser page
    new_html = new_browser.html
    
    # Get new soup for new browser page
    new_soup = soup(new_html, 'html.parser')
    
    # Get img class 
    img_class = new_soup.find('div',class_='downloads')
    
    # Get img url
    img_url = img_class.find('a').get('href')
    
    # Print
    print(img_url)
    
    # Cache dictonary
    hemispheres['img_url'] = img_url
    hemispheres['title'] = title
    
    # Create Copy of hemispheres dictionary
    hemi_copy = hemispheres.copy()
  
    # Copy of hemispheres list
    hemisphere_image_urls.append(hemi_copy)
    
    return hemisphere_image_urls


if __name__ == "__main__":

    
    print(scrape_all())
