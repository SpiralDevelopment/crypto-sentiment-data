import time
import requests
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message).170s")

logger = logging.getLogger(__name__)

SUB_REDDITS = ['Bitcoin', 'CryptoCurrency', 'ethereum']
URL_PLACEHOLDER = "https://www.reddit.com/r/{}/about.json"


def fetch_reddit_stats(sub_reddit):
    try:
        url = URL_PLACEHOLDER.format(sub_reddit)

        response = requests.get(url, headers={'User-agent': 'your bot 0.1'})
        response = response.json()

        return response
    except Exception as e:
        logger.error(str(e))


if __name__ == "__main__":
    data_to_append = ""

    for sub_reddit in SUB_REDDITS:
        response = fetch_reddit_stats(sub_reddit)

        if response:
            if 'error' in response:
                logger.info(str(response))
                continue

            response = response['data']

            logger.info("{},{},{}".format(sub_reddit,
                                          response['active_user_count'],
                                          response['subscribers']))
        time.sleep(4)
