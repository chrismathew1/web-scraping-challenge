from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

def scrape():
    # Set up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    # Visit website NASA Mars News
    url = "https://redplanetscience.com/"
    browser.visit(url)

    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # Get the first article title and paragraph
    news_title = soup.find("div", class_="content_title").text
    news_p = soup.find("div", class_="article_teaser_body").text


    # Visit website JPL Mars Space Images
    url = "https://spaceimages-mars.com/"
    browser.visit(url)

    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # Featured space image
    feature_image_url = soup.find("img", class_="headerimage fade-in")["src"]
    feature_image_url = url + feature_image_url
    feature_image_url

    # Load website Mars facts into table
    url = "https://galaxyfacts-mars.com/"
    tables = pd.read_html(url)
    tables

    mars_df = tables[0]

    mars_df.columns = mars_df.iloc[0]
    mars_df = mars_df.drop([0])
    mars_df = mars_df.set_index(mars_df["Mars - Earth Comparison"])
    mars_df = mars_df.drop(["Mars - Earth Comparison"], axis=1)

    # DF to html
    html_table = mars_df.to_html().replace("\n", "").replace('<table border="1" class="dataframe">', "").replace('</table>', "")

    # Visit website Mars hemispheres
    url = "https://marshemispheres.com/"
    browser.visit(url)

    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    #Scrape image links
    hemisphere_image_urls = []

    for i in range(4):
        browser.links.find_by_partial_text('Hemisphere')[i].click()

        html = browser.html
        soup = bs(html, "html.parser")

        url1 = soup.find("div", class_="downloads")
        url1 = url + url1.find("li").a["href"]

        title1 = soup.find("h2", class_="title").text

        dict1 = {"title":title1, "img_url": url1}
        hemisphere_image_urls.append(dict1)

        browser.back()

    #Close browser
    browser.quit()
    
    mars_data = {
        "news_title": news_title,
        "news_p": news_p,
        "feature_image_url": feature_image_url,
        "html_table": html_table,
        "hemisphere_image_urls": hemisphere_image_urls
    }

    return mars_data
    





