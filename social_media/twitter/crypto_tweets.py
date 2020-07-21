from tweepy import Stream
import tweepy
import logging
from tweepy.streaming import StreamListener

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message).170s")


logger = logging.getLogger(__name__)

# consumer key & secret
CONSUMER_KEY = "YOUR_CONSUMER_KEY"
CONSUMER_SECRET = "YOUR_CONSUMER_SECRET"

# access token
ACCESS_TOKEN = "YOUR_ACCESS_TOKEN"
ACCESS_TOKEN_SECRET = "YOUR_ACCESS_TOKEN_SECRET"

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)


class CustomStreamListener(StreamListener):

    def on_connect(self):
        logger.info('Stream starting...')

    def on_status(self, status):
        author = status.author.screen_name

        if not status.in_reply_to_status_id and \
                not status.in_reply_to_screen_name and \
                not status.in_reply_to_user_id:

            # is_retweet = hasattr(status, 'retweeted_status')
            # tweet_url = f"https://twitter.com/{author}/status/{status.id_str}"

            logger.info("New Tweet by %s: %s",
                        author,
                        status.text)
        else:
            logger.info('Tweet by %s is reply: %s',
                        author,
                        status.text)

    def on_error(self, status):
        logger.error(status)


if __name__ == '__main__':
    twitterStream = Stream(auth, CustomStreamListener())

    twitterStream.filter(track=['bitcoin'])

    # user_ids_to_follow = ['14379660', '295218901']
    # twitterStream.filter(follow=user_ids_to_follow)
