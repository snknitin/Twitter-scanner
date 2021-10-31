import collections
import os
import tweepy
import json
import time
import sys
import numpy as np
import pandas as pd
import csv

def save_cred(filename="my_creds.json"):
    """
    Keep track of your credentials in a separate file
    :param filename:
    :return:
    """
    # Enter your keys/secrets as strings in the following fields
    credentials = {}
    credentials['CONSUMER_KEY'] = "<Insert your creds here>"
    credentials['CONSUMER_SECRET'] = "<Insert your creds here>"
    credentials['ACCESS_TOKEN'] = "<Insert your creds here>"
    credentials['ACCESS_SECRET'] = "<Insert your creds here>"

    # Save the credentials object to file
    with open((os.path.join(os.getcwd(),filename)), "w") as file:
        json.dump(credentials, file)
    print("Done ! Saved your credentials")

def load_creds(filename = "my_creds.json"):
    """
    Loading credentials to use the twitter API
    :param filename:
    :return:
    """
    cred_file = os.path.join(os.getcwd(),filename)
    with open(cred_file, "r") as file:
        credentials = json.load(file)
    return credentials

def get_api(credentials):
    """
    Use credentials to get authenticated and star using the api object
    :param credentials:
    :return:
    """
    consumer_key,consumer_secret = credentials['CONSUMER_KEY'], credentials['CONSUMER_SECRET']
    access_token, access_token_secret = credentials['ACCESS_TOKEN'], credentials['ACCESS_SECRET']
    # authorization of consumer key and consumer secret
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    # set access to user's access key and access secret
    auth.set_access_token(access_token, access_token_secret)
    # calling the api
    api = tweepy.API(auth)
    return api


def limit_handled(cursor):
    """
    Helper code to exceed the count of get_friends method and obtain the full list
    :param cursor:
    :return:
    """
    while True:
        try:
            yield next(cursor)
        except:
            print("Waiting for 15 mins")
            time.sleep(15*60)

def get_following(api):
    """
    Get the list of people you follow on twitter
    :param api:
    :return:
    """
    filename = os.path.join(os.getcwd(), "following.json")
    if not os.path.exists(filename):
        # getting the friends list
        friends = api.get_friend_ids()
        print(" This account follows: {} accounts".format((len(friends))))

        batch_len = 100
        num_batches = np.ceil(len(friends) / 100)
        batches = (friends[i:i + batch_len] for i in range(0, len(friends), batch_len))
        all_data = []
        for batch_count, batch in enumerate(batches):
            sys.stdout.write("\r")
            sys.stdout.flush()
            sys.stdout.write("Fetching batch: " + str(batch_count) + "/" + str(num_batches))
            sys.stdout.flush()
            users_list = api.lookup_users(user_id=batch)
            users_json = (map(lambda t: t._json, users_list))
            all_data += users_json

        # Save the credentials object to file
        with open(filename, "w") as file:
            json.dump(all_data, file)
    else:
        with open(filename, "r") as file:
            all_data = json.load(file)

    return all_data


if __name__ == "__main__":
    # save_cred()
    credentials= load_creds()
    api = get_api(credentials)
    # Get all the people the user follows using
    # the screen_name of the targeted user
    screen_name = "Nitin_wysiwyg"
    following = get_following(api)
    print("Got the list")
    keys = set().union(*(d.keys() for d in following))
    with open(os.path.join(os.getcwd(),'following.csv'), 'w', encoding='utf-8', newline='')  as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(following)