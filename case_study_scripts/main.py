import settings
import read_sheet
import scrape
import write_sheet

# Initialize list of handles to scrape with
settings.handle_list()

# Initialize list of post scrape content
settings.scrape_list()

# Populate list of handles from spreadsheet A
read_sheet.main()

# Scrape Twitter with list of handles
scrape.twit_scraper()

# Write Twitter User Data to spreadsheet A
write_twitter_scrape = settings.list_of_scrapes[0]
write_sheet.batch_update_values(read_sheet.SPREADSHEET_ID, "Handles!G2", "USER_ENTERED", write_twitter_scrape)

# Write scraped Telegram and YouTube handles to spreadsheet A
# Telegram Handles:
write_telegram_handles_scrape = settings.telegram_handles_from_scrape[1]
write_sheet.batch_update_values(read_sheet.SPREADSHEET_ID, "Handles!B2", "USER_ENTERED", write_telegram_handles_scrape)

# YouTube Handles:
write_youtube_handles_scrape = settings.youtube_handles_from_scrape[1]
write_sheet.batch_update_values(read_sheet.SPREADSHEET_ID, "Handles!D2", "USER_ENTERED", write_youtube_handles_scrape)


# Repopulate list of handles after Twitter scrape
# Only use if starting spreadsheet from scratch
# read_sheet.main()


# Scrape Telegram
scrape.telegram_scraper()
# Write Telegram scrape to sheet
write_tele_scrape = settings.list_of_scrapes[1]
write_sheet.batch_update_values(read_sheet.SPREADSHEET_ID, "Handles!J2", "USER_ENTERED", write_tele_scrape)

# Scrape YouTube Channel IDs & Titles
scrape.y_channel_id_scraper()
# Scrape YouTube API
scrape.youtube_scraper()
# Write YouTube scrape to sheet
write_youtube_scrape = settings.list_of_scrapes[2]
write_sheet.batch_update_values(read_sheet.SPREADSHEET_ID, "Handles!N2", "USER_ENTERED", write_youtube_scrape)
