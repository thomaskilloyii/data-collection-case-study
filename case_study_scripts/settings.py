# The lists of names that will be used to scrape social media content
def handle_list():
    # Lists from Spreadsheets
    global twitter_handles
    twitter_handles = []
    global telegram_handles
    telegram_handles = []
    global youtube_handles
    youtube_handles = []
    global channel_ids
    channel_ids = []
    global youtube_titles
    youtube_titles = []

    # Lists from scrapes
    global telegram_handles_from_scrape
    telegram_handles_from_scrape = [[" "], []]
    global youtube_handles_from_scrape
    youtube_handles_from_scrape = [[" "], []]


# A list of lists containing scraped content
# Current Index:
#   0 = Twitter 1 = Telegram 2 = YouTube
def scrape_list():
    global list_of_scrapes
    list_of_scrapes = []
