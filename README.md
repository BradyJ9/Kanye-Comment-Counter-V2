## Kanye-Comment-Counter
A Twitter data parser from an open response poll conducted to gauge Kanye West album popularity.  
Tweepy API wrapper implementation used as well as Selenium web browser automation.

# src
- Main execution file: yeCommentCounter.py
   - Uses Tweepy API to gather list of all replies to original poll tweet
   - Iterates through replies searching for mention of albums and the order of mention (program assumes user mentions 1st place first, 2nd place second, and 3rd place third).  A dictionary containing alternate names and abbreviations/acronyms of each album is checked against to determine whether the album is mentioned in the tweet.
   - Increments an album's overall score based on the ranking the user gives: 1st = 3 points, 2nd = 2 points, 3rd = 1 point
- Calls Selenium browser automation for quote tweet scraping
   - Quote tweet data collection is not as easily accessible through the Twitter API as are tweet replies.  Rate limits are lower as well. 
   - Selenium is used to scrape the web page listing all tweets quoting the poll, slowly scrolling down the page analyzing each tweet.  
- Small tests and test data used for reply parsing unit testing

# program-logs
- Detailed logs of tweet parsing and album value identification.  
- Tweet-by-tweet analysis and album value parse results

# data-graphs
- Bar chart displaying score, 1st, 2nd, and 3rd place votes
- Bar chart displaying score, 1st, 2nd, and 3rd place votes sorted in descending order by score
- Column chart displaying score, 1st, 2nd, and 3rd place votes
- Bar chart displaying 1st, 2nd, and 3rd place votes
- Raw console results

