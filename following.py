import os

# import the module
import tweepy


import json

def save_cred(filename="my_creds.json"):
    """
    Keep track of your credentials in a separate file
    :param filename:
    :return:
    """

    # Enter your keys/secrets as strings in the following fields
    credentials = {}
    credentials['CONSUMER_KEY'] =
    credentials['CONSUMER_SECRET'] =
    credentials['ACCESS_TOKEN'] =
    credentials['ACCESS_SECRET'] =

    # Save the credentials object to file
    with open((os.path.join(os.getcwd(),filename)), "w") as file:
        json.dump(credentials, file)

# authorization of consumer key and consumer secret
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

# set access to user's access key and access secret
auth.set_access_token(access_token, access_token_secret)

# calling the api
api = tweepy.API(auth)

# the screen_name of the targeted user
screen_name = "geeksforgeeks"

# printing the latest 20 followers of the user
for follower in api.followers(screen_name):
    print(follower.screen_name)





if __name__ == "__main__":
    save_cred()
    print("Done")