import praw
import requests
import os
import datetime
from random import randint


def reddit_setup():

    with open(r"C:\Users\Hifas\Google Drive\Python Projects\RedditBot\RedditCred.txt", "r") as f:
        user_agent, client_id, client_secret, username, password = f.read().splitlines()

    reddit = praw.Reddit(user_agent=user_agent,
                         client_id=client_id,
                         client_secret=client_secret,
                         username=username, password=password)

    sub_reddit = reddit.subreddit("wallpapers")
    hot_posts = sub_reddit.hot(limit=10)
    return hot_posts


def load_submission_ids():
    # submission_id.csv contains id's of files already downloaded
    # if file doesn't exist then create it
    # load id's to a list and return the list

    try:
        with open("submission_id.csv", "r") as f:
            ids = f.read().splitlines()
        return ids

    except FileNotFoundError:
        # Creates file if it doesn't exist
        with open("submission_id.csv", "w"):
            return []


def save_image(image_url, file_extension, sub_id):
    # sub_id is the post id

    # File name is made up of current date and time
    # Add a random number to end to prevent file name conflicts

    rand_num = str(randint(100, 999))
    img_data = requests.get(image_url).content
    file_name = datetime.datetime.now().strftime("%Y-%m-%d %H %M %S")
    file_name = f"{file_name}.{rand_num}{file_extension}"

    # download image file
    with open(file_name, "wb") as f:
        f.write(img_data)

    # append post id to submission_id.csv
    with open("submission_id.csv", "a") as f:
        f.write(f"{sub_id}\n")


def main():
    os.chdir(r"C:\Users\Hifas\Google Drive\Python Projects\RedditBot\Images")
    submissions = reddit_setup()    # Loads hot posts from subreddit
    submission_ids = load_submission_ids()      # loads already downloaded id's

    for submission in submissions:
        submission_id = submission.name
        if submission_id not in submission_ids:
            url = submission.url
            extension = url[-4:]

            # only save jpg and png files
            if extension in (".jpg", ".png"):
                print(f"Saving {url}")
                save_image(url, extension, submission_id)


main()
