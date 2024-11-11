from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time
from bs4 import BeautifulSoup
import csv
import os

# Setup Selenium driver
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
driver.get("https://twitter.com/login")

# Wait for manual login
print("Please log in manually within 60 seconds.")
time.sleep(60)  # Allow time for manual login

# Infinite scroll and tweet extraction
tweet_data = []
scroll_pause_time = 2  # Adjust pause to prevent overloading requests
action = ActionChains(driver)

# File setup
csv_file = 'tweets.csv'

# Initialize CSV if it doesn't exist
if not os.path.isfile(csv_file):
    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=["user", "content", "timestamp"])
        writer.writeheader()  # Write header only once

try:
    while True:
        # Scroll down
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scroll_pause_time)

        # Parse tweets on the page
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, "html.parser")
        tweets = soup.find_all("div", class_="css-175oi2r")  # Adjust for precise divs containing tweets

        for tweet in tweets:
            # Extract basic info - user name, tweet content, timestamp
            user = tweet.find("div", {"data-testid": "User-Name"})
            content = tweet.find("div", {"data-testid": "tweetText"})
            timestamp = tweet.find("time")

            if user and content and timestamp:
                tweet_info = {
                    "user": user.text,
                    "content": content.text,
                    "timestamp": timestamp['datetime']
                }
                tweet_data.append(tweet_info)
                print("Scraped Tweet:", tweet_info)  # Log each scraped tweet

                # Write each tweet to CSV
                with open(csv_file, mode='a', newline='', encoding='utf-8') as file:
                    writer = csv.DictWriter(file, fieldnames=["user", "content", "timestamp"])
                    writer.writerow(tweet_info)

                

except Exception as e:
    print("An error occurred:", e)

finally:
    driver.quit()
    print("Scraping completed and data saved to files.")
