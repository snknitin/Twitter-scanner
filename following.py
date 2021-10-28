import os
import tweepy
import json
import time

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
    following_list = []
    # Print out each one
    for follower in limit_handled(tweepy.Cursor(api.get_friends,count=200).items()):
    #for follower in api.get_friends(count=200):
        # Running this snippet will print all users you follow that themselves follow less than 300 people total
        # - to exclude obvious spambots, for example
        # if follower.friends_count < 600:
        #     print(follower.screen_name)
        following_list.append(follower)
    # Save the credentials object to file
    with open((os.path.join(os.getcwd(), "followers.json")), "w") as file:
        json.dump(following_list, file)
    return following_list


if __name__ == "__main__":
    # save_cred()
    credentials= load_creds()
    api = get_api(credentials)
    # Get all the people the user follows using
    # the screen_name of the targeted user
    screen_name = "Nitin_wysiwyg"
    following_list = get_following(api)