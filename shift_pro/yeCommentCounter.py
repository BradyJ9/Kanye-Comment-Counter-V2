import tweepy
import logging
from typing import List
from selenium import webdriver
from time import sleep, time
from selenium.webdriver.firefox.webdriver import WebDriver

#####DONT WORRY ABOUT THIS STUFF
CONSUMER_KEY = 'tlv3bPRNiLZiwJlLJAIoNcgtB'
CONSUMER_SECRET = 'FDSZmOnQF0XUBDpnjG2Eageoe1K5JFqFa2RyYZwswcQihO0ffl'
ACCESS_KEY = '830315469403852800-2pj5VcdVT31sWaU3fY85MkT2BYbK7lH'
ACCESS_SECRET = 'Jn7M5HzV7CbglfnuSzZaNJ75kkPN7KAuwvqzDwI33llg0'

###PUT IN YOUR USERNAME AND PASSWORD HERE
TWITTER_USER = ""
TWITTER_PASSWORD = ""

logging.basicConfig(filename='yeCommentCounter.log', level=logging.INFO)

tweet_id = 1417865751961251847
user_name = 'shift_pro'

CD_NAMES = ["CD", "COLLEGE DROPOUT", "DROP OUT"]
LR_NAMES = ["LR", "LATE REGISTRATION", "LATE REG"]
GRADUATION_NAMES = ["GRADUATION", "GRAD"]
HEARTBREAKS_NAMES = ["808","808S AND HEARTBREAKS", "808S"]
MBDTF_NAMES = ["MY BEAUTIFUL DARK TWISTED FANTASY", "MBDTF", "DARK FANTASY", "DARK TWISTED FANTASY"]
WTT_NAMES = ["WATCH THE THRONE", "WTT"]
YEEZUS_NAMES = ["YEEZUS"]
TLOP_NAMES = ["TLOP", "THE LIFE OF PABLO", "PABLO", "LIFE OF PABLO"]
YE_NAMES = ["YE ", "YE\n"]
KSG_NAMES = ["KSG", "KIDS SEE GHOSTS", "KIDS SEE GHOST"]
JIK_NAMES = ["JESUS IS KING", "JIK"]

REPLIES_COUNTED = 0

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
                        parse_and_give_points(quote_tweet)
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


#"album name":[points, 1st place votes, 2nd, 3rd]
POINTS = {
    "cd": [0, 0, 0, 0],
    "lr": [0, 0, 0, 0],
    "grad": [0, 0, 0, 0],
    "808": [0, 0, 0, 0],
    "mbdtf": [0, 0, 0, 0],
    "wtt": [0, 0, 0, 0],
    "yeezus": [0, 0, 0, 0],
    "tlop": [0, 0, 0, 0],
    "ye": [0, 0, 0, 0],
    "ksg": [0, 0, 0, 0],
    "jik": [0, 0, 0, 0]
}

def find_album_ref_in_reply(album_tokens, reply : str):
    for symbol in album_tokens:
        #print("Scanning:\n " + reply + "\nfor: " + symbol)
        temp_pos = reply.find(symbol)
        if temp_pos != -1: #was found
            #print("FOUND")
            return temp_pos
    #print("NOTHING FOUND FOR ALBUM\n")
    return -1

def parse_and_give_points(reply):
    reply = reply.upper()

    freq = {}

    cd_pos = find_album_ref_in_reply(CD_NAMES, reply)
    if cd_pos != -1:
        logging.debug("Found College Dropout in " + reply)
        freq["cd"] = cd_pos

    lr_pos = find_album_ref_in_reply(LR_NAMES, reply)
    if lr_pos != -1:
        logging.debug("Found Late Registration in " + reply)
        freq["lr"] = lr_pos

    grad_pos = find_album_ref_in_reply(GRADUATION_NAMES, reply)
    if grad_pos != -1:
        logging.debug("Found Graduation in " + reply)
        freq["grad"] = grad_pos

    heartbreaks_pos = find_album_ref_in_reply(HEARTBREAKS_NAMES, reply)
    if heartbreaks_pos != -1:
        logging.debug("Found 808s in " + reply)
        freq["808"] = heartbreaks_pos

    mbdtf_pos = find_album_ref_in_reply(MBDTF_NAMES, reply)
    if mbdtf_pos != -1:
        logging.debug("Found MBDTF in " + reply)
        freq["mbdtf"] = mbdtf_pos

    wtt_pos = find_album_ref_in_reply(WTT_NAMES, reply)
    if wtt_pos != -1:
        logging.debug("Found WTT in " + reply)
        freq["wtt"] = wtt_pos

    yeezus_pos = find_album_ref_in_reply(YEEZUS_NAMES, reply)
    if yeezus_pos != -1:
        logging.debug("Found Yeezus in " + reply)
        freq["yeezus"] = yeezus_pos

    tlop_pos = find_album_ref_in_reply(TLOP_NAMES, reply)
    if tlop_pos != -1:
        logging.debug("Found TLOP in " + reply)
        freq["tlop"] = tlop_pos

    ye_pos = find_album_ref_in_reply(YE_NAMES, reply)
    if ye_pos == -1: #nothing found, may still be at EOS
        ye_pos = find_album_ref_in_reply("YE", reply) 
        if ye_pos != -1: #YE found, could it be at EOS?
            if ye_pos + 2 == len(reply): #YE is in fact EOS
                try:
                    if (reply[ye_pos - 1] != 'n'): #and EOS YE is not at the end of 'kanye' 
                        logging.debug("Found Ye in " + reply)
                        freq["ye"] = ye_pos
                except Exception as e:
                    print(e)
    else:
        try:
            if (reply[ye_pos - 1] != 'n'): #any mention of kanye will trigger this 
                logging.debug("Found Ye in " + reply)
                freq["ye"] = ye_pos
        except Exception as e:
            print(e)

    ksg_pos = find_album_ref_in_reply(KSG_NAMES, reply)
    if ksg_pos != -1:
        logging.debug("Found KSG in " + reply)
        freq["ksg"] = ksg_pos

    jik_pos = find_album_ref_in_reply(JIK_NAMES, reply)
    if jik_pos != -1:
        logging.debug("Found Jesus Is King in " + reply)
        freq["jik"] = jik_pos

    global REPLIES_COUNTED
    REPLIES_COUNTED = REPLIES_COUNTED + 1

    #find which one occurs first
    sorted_freq = sorted(freq.items(), key=lambda x: x[1], reverse=False)
    print("\n*****PRINTING FREQUENCIES*****")
    for test_freq in sorted_freq:
        print(test_freq[0], test_freq[1])
    print("\n")

    first_place = ""
    second_place = ""
    third_place = ""
    try:
        first_place = sorted_freq[0][0]
        try:
            second_place = sorted_freq[1][0]
            try:
                third_place = sorted_freq[2][0]
            except Exception as e:
                print(e)
        except Exception as e:
            print(e)
    except Exception as e:
        print(e)

    print("1st: " + first_place)
    print("2nd: " + second_place)
    print("3rd: " + third_place)
    logging.info("Parsed Rankings from: " + reply)
    logging.info("1st: " + first_place)
    logging.info("2nd: " + second_place)
    logging.info("3rd: " + third_place)
    logging.info("\n")

    global POINTS

    if first_place != "":
        curr = POINTS[first_place][0] 
        POINTS[first_place][0] = curr + 3

        dataList = POINTS[first_place]
        firstVotes = dataList[1]
        POINTS[first_place][1] = firstVotes + 1

    if second_place != "":
        curr = POINTS[second_place][0] 
        POINTS[second_place][0] = curr + 2

        dataList = POINTS[second_place]
        secondVotes = dataList[2]
        POINTS[second_place][2] = secondVotes + 1

    if third_place != "":
        curr = POINTS[third_place][0] 
        POINTS[third_place][0] = curr + 1

        dataList = POINTS[third_place]
        thirdVotes = dataList[3]
        POINTS[third_place][3] = thirdVotes + 1

def main(test : bool, testReplies):
    if test:
        if testReplies != None:
            for reply in testReplies:
                parse_and_give_points(reply)
    else:
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
        api = tweepy.API(auth)

        replies = tweepy.Cursor(api.search, q='to:{}'.format(user_name), since_id=tweet_id, tweet_mode='extended').items()
        
        while True:
            try:
                reply = replies.next()
                if not hasattr(reply, 'in_reply_to_status_id_str'):
                    #print("Bad Reply1: \n" + reply.full_text + "\n")
                    continue
                if reply.in_reply_to_status_id == tweet_id:
                    parse_and_give_points(reply.full_text)
                    print("Parsing: " + reply.full_text + "\n----------\n\n")
                else:
                    #print("Bad Reply2: \n" + reply.full_text + "\n")
                    continue

            except tweepy.RateLimitError as e:
                print("Twitter api rate limit reached".format(e))
                time.sleep(60)
                continue

            except tweepy.TweepError as e:
                print("Tweepy error occured:{}".format(e))
                break

            except StopIteration:
                print("DONE Part 1...")
                break

            except Exception as e:
                print("Failed while fetching replies {}".format(e))
                break
            
    print("Start part 2...")
    ####PART 2####
    #PARSE QUOTE TWEETS
    quote_tweets = analyze_quote_tweets(False)

    print("FINAL POINTS")
    logging.info("*************")
    logging.info("FINAL POINTS")
    for album in POINTS:
        print(album + ": " + str(POINTS[album][0]) + "...1st: " + str(POINTS[album][1]) + " ...2nd: " + str(POINTS[album][2]) + " ...3rd: " + str(POINTS[album][3]))
        logging.info(album + ": " + str(POINTS[album][0]) + "...1st: " + str(POINTS[album][1]) + " ...2nd: " + str(POINTS[album][2]) + " ...3rd: " + str(POINTS[album][3]))
        logging.info("************")
    
    print("\nTotal Direct Replies Counted: " + str(REPLIES_COUNTED - quote_tweets))
    logging.info("\nTotal Direct Replies Counted: " + str(REPLIES_COUNTED - quote_tweets))

    print("Total Quote Tweets Counted: " + str(quote_tweets))
    logging.info("Total Quote Tweets Counted: " + str(quote_tweets))

    print ("TOTAL ENTRIES COUNTED: " + str(REPLIES_COUNTED))
    logging.info("TOTAL ENTRIES COUNTED: " + str(REPLIES_COUNTED))

main(False, None)
