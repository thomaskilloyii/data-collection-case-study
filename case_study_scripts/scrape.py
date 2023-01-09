import snscrape.modules.twitter as twitter_scraper
import snscrape.modules.telegram as tele_scraper
import settings
import requests
import json

from bs4 import BeautifulSoup


def twit_scraper():
    outer_list = []
    for i, handle in enumerate(settings.twitter_handles):
        # If handle in row is blank then skip a row
        if handle == "":
            outer_list.append([" "])
            continue
        # Initiate scraper with handle from list
        twitter_profile = twitter_scraper.TwitterUserScraper(handle[1:])

        user_data = []
        twitter_user_scrape = []

        # Access returned profile data
        for x, profile in enumerate(twitter_profile.get_items()):
            user_object = profile.user
            # If there is no link available
            if user_object.link is None:
                # Append available data points and add Not Available
                user_data = [user_object.displayname, user_object.followersCount, "None Available"]
                # Append None for no data to scrape Telegram
                # and YouTube handles from Twitter website URLs
                settings.telegram_handles_from_scrape[1].append(["None"])
                settings.youtube_handles_from_scrape[1].append(["None"])
                print("No Website")
            if user_object.link is not None:
                user_data = [user_object.displayname, user_object.followersCount, user_object.link.url]
                # if Twitter website link starts with Telegram URL
                if user_object.link.url.startswith("https://t.me/"):
                    # Filter out handle
                    twitter_telegram_handle = user_object.link.url.replace("https://t.me/", "")
                    # Append to list object that will write to Spreadsheet
                    settings.telegram_handles_from_scrape[1].append([f"@{twitter_telegram_handle}"])
                    print(settings.telegram_handles_from_scrape)
                else:
                    # If none available append None
                    settings.telegram_handles_from_scrape[1].append(["None"])

                # Filter by URL list
                youtube_array = ["https://www.youtube.com/",
                                 "http://www.youtube.com/",
                                 "https://YouTube.com/",
                                 "http://youtube.com/",
                                 "https://youtube.com/"]
                # Filter by end of URL snippets
                url_snippets = ["c/",
                                "user/",
                                "channel/"]
                no_handle = True
                format_youtube = ""

                for link in youtube_array:
                    # If our scraped user has a URL matching our array
                    if user_object.link.url.startswith(link):
                        print(f"youtube link: {link}")
                        for url in url_snippets:
                            # Filter out channel ID from URL
                            twitter_youtube_handle = user_object.link.url.replace(link, "")
                            if twitter_youtube_handle.startswith(url):
                                # Filter out URL snippets
                                format_youtube = twitter_youtube_handle.replace(url, "")
                                print(f"if: {format_youtube}")
                                break
                            else:
                                # If nothing to filter then assign channel ID
                                format_youtube = twitter_youtube_handle
                                print(f"else: {format_youtube}")
                        no_handle = False

                if no_handle is True:
                    # If there is no handle scraped append None
                    settings.youtube_handles_from_scrape[1].append(["None"])
                else:
                    # If there is a handle scraped append the channel ID
                    settings.youtube_handles_from_scrape[1].append([format_youtube])

                print("Has Website")

            twitter_user_scrape = user_data

            break

        outer_list.append(twitter_user_scrape)

    settings.list_of_scrapes.append(outer_list)


def telegram_scraper():
    telegram_outer_list = []
    # Iterate through telegram handles from Spreadsheet
    for tele_handle in settings.telegram_handles:
        print(f"telegram_handles: {settings.telegram_handles}")
        # If there is a handle
        if tele_handle != "None":
            try:
                # First format the handle for scraping
                format_tele_handle = tele_handle[1:]
                # Secondly initiate the scrape
                telegram_profile = tele_scraper.TelegramChannelScraper(format_tele_handle)._get_entity()
                # Extract data points
                telegram_user_scrape = [telegram_profile.title,
                                        telegram_profile.members,
                                        telegram_profile.verified,
                                        f'https://t.me/s/{telegram_profile.username}']

                pass
            except AttributeError:
                # Except when an error occurs
                # our data points report Not Available
                telegram_user_scrape = ["Not Available",
                                        "Not Available",
                                        "Not Available",
                                        "Not Available"]
            # Append to outer list for storage
            telegram_outer_list.append(telegram_user_scrape)
            continue
        # Else if handle is "None"
        else:
            # Data points return "None"
            telegram_outer_list.append(["None",
                                        "None",
                                        "None",
                                        "None"])
            continue
    print(telegram_outer_list)
    # Append after loop to global variable for writing to Spreadsheet
    settings.list_of_scrapes.append(telegram_outer_list)


def youtube_scraper():

    youtube_outer_list = []

    # You will need to set up an API key
    # Please refer to the README.md to follow along on Medium
    api_key = ""

    index = 0
    # Iterate through global channel ids
    for i in range(len(settings.channel_ids)):
        id_ = settings.channel_ids
        titles_ = settings.youtube_titles

        print(f"youtube channel titles: {titles_}")

        channel_data = [titles_[index]]

        # If channel id is available
        if id_[index] != "Not Available":

            # Create URL string for request
            url = f"""https://www.googleapis.com/youtube/v3/channels?part=statistics&id={id_[index]}&key={api_key}"""

            # Request json
            json_return = requests.get(url)

            # Parse to text
            youtube_data = json.loads(json_return.text)
            print(f"youtube data: {youtube_data}")

            try:

                # Use items and statistics keys in json
                # This leaves us with our data points
                youtube_data = youtube_data["items"][0]["statistics"]
                print(f"statistics:{youtube_data}")

            # In case a channel returns empty
            except KeyError as err:
                print(err)

                # Data points report "Not Available"
                channel_data.extend(["Not Available",
                                     "Not Available",
                                     "Not Available"])

                # Append to outer list
                youtube_outer_list.append(channel_data)
                print("error")

            # Extract data points from parsed json object
            finally:
                sub_count = youtube_data["subscriberCount"]
                video_count = youtube_data['videoCount']
                view_count = youtube_data["viewCount"]

                channel_data.extend([sub_count,
                                    video_count,
                                    view_count])

            # Set channel_data to scrape
            youtube_user_scrape = channel_data
            print(f"user scrape: {youtube_user_scrape}")
        # Else if id_ is "Not Available"
        else:
            # Data points report "Not Available"
            channel_data = ["Not Available",
                            "Not Available",
                            "Not Available",
                            "Not Available"]

            # Set channel_data to scrape
            youtube_user_scrape = channel_data

        # Append scrape to outer list
        youtube_outer_list.append(youtube_user_scrape)
        print(f"youtube_outer_list: {youtube_outer_list}")
        index = index + 1

    # Append outer list to global list of scrapes
    settings.list_of_scrapes.append(youtube_outer_list)
    print(settings.list_of_scrapes[2])


def y_channel_id_scraper():
    # Iterate through global YouTube handles
    for youtube_handle in settings.youtube_handles:

        # Format handle before search
        format_youtube_handle = f"@{youtube_handle}"
        print(format_youtube_handle)

        # If there is a handle
        if youtube_handle != "None":

            # Create URL string for request
            url = f"https://www.youtube.com/{format_youtube_handle}"

            # Generate request
            html_text = requests.get(url)

            # Process html_text with Beautiful Soup
            # We use Beautiful Soup to isolate by HTML classes
            soup = BeautifulSoup(html_text.text, 'lxml')

            yt_title = soup.find("title").text
            format_yt_title = yt_title.replace(" - YouTube", "")

            # If the text found doesn't have a title of "404 Not Found"
            if soup.find("title").text != "404 Not Found":
                print(url)
                # Iterate through all meta tags found
                for tag in soup.find_all("meta"):

                    # If a meta tag has a itemprop equal to "channelId"
                    if tag.get("itemprop", None) == "channelId":

                        # Set the content of the meta tag to channel_id object
                        channel_id = tag.get("content", None)

                # Append content channel_id to global channel_ids
                settings.channel_ids.append(channel_id)
                settings.youtube_titles.append(format_yt_title)

            # If the text found does have a title of "404 Not Found"
            else:
                # Initiate list of snippets to try
                url_snippets = ["c/",
                                "user/",
                                "channel/"]
                channel_id_out = ""
                channel_title_out = ""
                for snippet in url_snippets:
                    # Create URL string to re-attempt request
                    url = f"https://www.youtube.com/{snippet}{youtube_handle}"
                    print(f"else url:{url}")

                    # Generate request
                    html_text = requests.get(url)

                    # Process html_text with Beautiful Soup
                    # We use Beautiful Soup to isolate by HTML classes
                    soup = BeautifulSoup(html_text.text, 'lxml')

                    yt_title = soup.find("title").text
                    format_yt_title = yt_title.replace(" - YouTube", "")

                    # If the text found doesn't have a title of "404 Not Found"
                    if soup.find("title").text != "404 Not Found":

                        # Iterate through all meta tags found
                        for tag in soup.find_all("meta"):

                            # If a meta tag has a itemprop equal to "channelId"
                            if tag.get("itemprop", None) == "channelId":

                                # Set the content of the meta tag to channel_id object
                                channel_id = tag.get("content", None)
                                print(f"type of: {type(channel_id)}")
                                # Append channel_id to global channel_ids
                                channel_id_out = channel_id
                                channel_title_out = format_yt_title
                        break
                    else:
                        # Set channel_id to "Not Available"
                        channel_id = "Not Available"
                        channel_title = "Not Available"
                        channel_title_out = channel_title
                        channel_id_out = channel_id
                settings.youtube_titles.append(channel_title_out)
                settings.channel_ids.append(channel_id_out)
        # If there isn't a handle
        else:
            # Set channel_id to "Not Available"
            channel_id = "Not Available"
            yt_title = "Not Available"
            # Append channel_id to global channel_ids
            settings.channel_ids.append(channel_id)
            settings.youtube_titles.append(yt_title)

    print(settings.channel_ids)
