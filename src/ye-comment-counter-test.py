from typing import Counter
import yeCommentCounter
import logging

replies = [ 
    "1. Yeezus 2. TLOP 3. College Dropout",
    "No order but 808s TLOP LR",
    """Kids see ghost 
    Jesus is king 
    808s & Heartbreak""",
    """1. Yeezus
    2. My Beautiful Dark Twisted Fantasy
    3. The Life Of Pablo
    4. The College Dropout
    5. 808s And Heartbreaks
    6. Late Registration
    7. Kids see ghosts
    8. Ye
    9. Graduation
    10. Watch the throne
    11. Jesus Is King""",
    """People will hate this but
    1. Graduation
    2. Yeezus
    3. The Life Of Pablo
    4. The College Dropout
    5. My Beautiful Dark Twisted Fantasy
    6. Late Registration
    7. Ye
    8. 808s And Heartbreaks
    9. Jesus Is King""",
    """College Dropout will always be number 1. Two and three fluctuate between four albums and it really depends on the day. Right now, it’s College Dropout
    Ye
    The Life of Pablo"""

]
logging.basicConfig(filename='example.log', level=logging.DEBUG)

def run_tests():
    for reply in replies:
        yeCommentCounter.parse_and_give_points(reply.upper())
        logging.info("Test")

def main_test():
    yeCommentCounter.main(True, replies)


#run_tests()
main_test()


