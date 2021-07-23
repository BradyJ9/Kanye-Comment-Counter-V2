import tweepy
import logging
from time import time
from typing import List
import yeCommentCounterQuoteTweets

CONSUMER_KEY = ''
CONSUMER_SECRET = ''
ACCESS_KEY = ''
ACCESS_SECRET = ''

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
                print("DONE")
                break

            except Exception as e:
                print("Failed while fetching replies {}".format(e))
                break
            
    
    ####PART 2####
    #PARSE QUOTE TWEETS
    quote_tweets = yeCommentCounterQuoteTweets.analyze_quote_tweets(False)

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