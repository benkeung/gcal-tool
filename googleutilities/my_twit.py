import twitter
import argparse

api = twitter.Api(consumer_key='RjAxiiBxDg6aN4AA5d9ZQ',
        consumer_secret='J5jSRU7d2TiP2l9uPHPlMm3IQqWbnQC9Y5wPwj73dc',
        access_token_key='20874366-P6W9o0skHnSjSsLEC9vsCveJ3ecwqKjYVJ1PFtCuV',
        access_token_secret='Zask93spBUEZU3hGi3i7l8rXKhMFafWddj1dA2w')

def getTweets():
    tweets = api.GetFriendsTimeline()

    for tweet in reversed(tweets):
        print '%s\t\n%s (%s)\n' % (tweet.text, tweet.user.name,
            tweet.user.screen_name)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-g', '--gettweets', help='Returns the 20 recent tweets',
        action='store_true')
    args = parser.parse_args()

    if args.gettweets:
        getTweets()
