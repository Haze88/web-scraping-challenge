from splinter import Browser 
from bs4 import BeautifulSoup as soup
import pandas as pd
#from webdriver_manager.chrome import ChromeDriverManager

def scrape_all (): 
    # Set up browser path    
    executable_path = {'executable_path': 'chromedriver.exe'}    
    #executable_path = {"executable_path":ChromeDriverManager().install()}   
    browser = Browser('chrome', **executable_path, headless=False)    
    news_title,news_p=mars_news_site(browser)    
    mars_data= {        
    "news_title":news_title,       
    "news_p":news_p,        
    "featured_image":featured_image(browser),        
    "mars_facts":mars_facts(),        
    "hemispheres":hemispheres(browser)   
    }
    browser.quit()    
    return mars_data

def mars_news_site(browser):    
    #Visit the Mars news site
    url = 'https://redplanetscience.com/'
    browser.visit(url)
    
    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)
   
    # Convert the browser html to a soup object
    html = browser.html
    news_soup = soup(html, 'html.parser')

    slide_elem = news_soup.select_one('div.list_text')
    
    #display the current title content
    slide_elem.find('div',class_="content_title")

    news_title=slide_elem.find('div',class_="content_title").getText()

    news_p=slide_elem.find('div',class_="article_teaser_body").getText()

    return news_title,news_p

def featured_image(browser):
    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    browser.find_by_css('button.btn').click()

    # Parse the resulting html with soup
    browser.find_by_css('img.fancybox-image')['src']

    html = browser.html
    imageSoup = soup(html,'html.parser')

    # find the relative image url
    img_url_rel=imageSoup.select_one('img',class_='fancybox-image').get('src')

    # Use the base url to create an absolute url

    img_url=url+"/"+img_url_rel

    return img_url
def mars_facts ():
    url='https://galaxyfacts-mars.com/'
    df=pd.read_html(url)[0]

    df.columns=["Description","Mars","Earth"]
    df.set_index("Description",inplace=True)

    return df.to_html(classes= ["table","table-striped"])

def hemispheres(browser):
    url = 'https://marshemispheres.com/'

    browser.visit(url)

    # Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # Get a list of all of the hemispheres
    links = browser.find_by_css('a.product-item img')

    # Next, loop through those links, click the link, find the sample anchor, return the href
    for i in range(len(links)):
        
        
        # We have to find the elements on each loop to avoid a stale element exception
        browser.find_by_css('a.product-item img')[i].click()
    
        # Next, we find the Sample image anchor tag and extract the href
        img_url=browser.find_by_text('Sample')[0]['href']
        
        # Get Hemisphere title
        hemp_title=browser.find_by_css('h2.title').text
        
        # Append hemisphere object to list
        hemisphere_image_urls.append({"img_url":img_url,"title":hemp_title})
        
        # Finally, we navigate backwards
        browser.back()

    return hemisphere_image_urls


if __name__ == "__main__":    
    print (scrape_all())




