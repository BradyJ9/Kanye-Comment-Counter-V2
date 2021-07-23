from selenium import webdriver
from random import randrange
import sys
from time import sleep, time
from selenium.webdriver.firefox.webdriver import WebDriver
import logging

logging.basicConfig(filename='yeCommentCounterQuoteTweets.log', level=logging.INFO)

TWITTER_USER = ""
TWITTER_PASSWORD = ""

def login(username, password, headless):
    firefoxOptions = webdriver.FirefoxOptions()
    firefoxOptions.headless = headless
    browser = webdriver.Firefox(options=firefoxOptions) #new browser with no cookies/history
    browser.implicitly_wait(3)

    browser.get('https://www.twitter.com/login') #login page if no cookies/cached data
    sleep(4)

    username_input = browser.find_element_by_xpath("/html/body/div/div/div/div[2]/main/div/div/div[2]/form/div/div[1]/label/div/div[2]/div/input")
    username_input.click()    
    username_input.send_keys(username)
                                         
    password_input = browser.find_element_by_xpath("/html/body/div/div/div/div[2]/main/div/div/div[2]/form/div/div[2]/label/div/div[2]/div/input")
    password_input.click()
    password_input.send_keys(password)

    sleep(1)

    login_button = browser.find_element_by_xpath("/html/body/div/div/div/div[2]/main/div/div/div[2]/form/div/div[3]/div/div")
    login_button.click()

    sleep(4)

    return browser

def get_statuses_quote_tweets(browser: WebDriver):
    browser.get("https://twitter.com/shift_pro/status/1417865751961251847/retweets/with_comments")
    sleep(3)

    num_quote_tweets = 500
    print("Scrolling to bottom")
    
    """for i in range(int(num_quote_tweets / 8)):
        # Scroll down to bottom
        browser.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", sub_window)

        # Wait to load page
        sleep(1)
    """
    SCROLL_PAUSE_TIME = .5
    last_height = browser.execute_script("return document.body.scrollHeight")
    scroll_length = last_height / 16

    USERS_ANALYZED = []
    TWEETS_ANALYZED = 0
    y = 200
    for i in range(num_quote_tweets * 2):
        # Scroll down to bottom
        browser.execute_script("window.scrollTo(0, "+str(y)+");")
        y+=500

        # Wait to load page
        sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        """
        new_height = browser.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
        """
        #user handle
        #/html/body/div/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/section/div/div/div[1]/div/div/article/div/div/div/div[2]/div[2]/div[1]/div/div/div[1]/div[1]/a/div/div[2]/div/span
        #tweet text
        #/html/body/div/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/section/div/div/div[2]/div/div/article/div/div/div/div[2]/div[2]/div[2]/div[1]/div/span

        #get palette of 8 tweets and analyze
        for i in range(8):
            try:
                user_handle = browser.find_element_by_xpath("/html/body/div/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/section/div/div/div[" + str(i + 1) + "]/div/div/article/div/div/div/div[2]/div[2]/div[1]/div/div/div[1]/div[1]/a/div/div[2]/div/span").text
                if user_handle not in USERS_ANALYZED:
                    if len(USERS_ANALYZED) > 50: #list to check against doesn't need to be that big, we are crawling down line
                        USERS_ANALYZED.clear()
                    USERS_ANALYZED.append(user_handle)
                    print(user_handle + " Tweet found")
                    try:
                        #handle tweet
                        quote_tweet = browser.find_element_by_xpath("/html/body/div/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/section/div/div/div[" + str(i + 1) + "]/div/div/article/div/div/div/div[2]/div[2]/div[2]/div[1]/div/span").text
                        yeCommentCounter.parse_and_give_points(quote_tweet)
                        #print("Analyzing Tweet: \n" + quote_tweet + "\n")
                        logging.info("Analyzing Quote Tweet: \n" + quote_tweet + "\n")
                        TWEETS_ANALYZED = TWEETS_ANALYZED + 1
                        print("TWEETS ANALYZED: " + str(TWEETS_ANALYZED))
                    except Exception as e:
                        print(e)
                else:
                    #the way we crawl incrementally down the webpage through unevenly ordered elements means
                    #we need to track the user handle before analyzing a tweet.  We are using an overly careful
                    #method of iterating through tweets as to not miss any, so it is likely we will not be grabbing
                    #new tweets after every scroll
                    pass
            except Exception as e:
                print(e)

    print("FINISHED")
    sleep(10)
    return TWEETS_ANALYZED

#def main():
def analyze_quote_tweets(headless : bool):
    tweets_analyzed = 0
    try:
        browser = login(TWITTER_USER, TWITTER_PASSWORD, headless)

        tweets_analyzed = get_statuses_quote_tweets(browser)
    except Exception as e:
        print(e)
    finally:
        print("Ending Selenium Session...")
        browser.quit()

    return tweets_analyzed

#main()
import yeCommentCounter