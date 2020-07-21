from datetime import datetime
import logging

from market.coingecko.coingeko_api import CoinGeckoAPI

logger = logging.getLogger(__name__)
api_mgr = CoinGeckoAPI()

if __name__ == "__main__":
    coin_id = 'bitcoin'
    dtm = datetime(2020, 1, 1)

    data = api_mgr.get_coin_history_by_id(coin_id, dtm.strftime("%d-%m-%Y"))

    if data.get('developer_data', None) or data.get('community_data', None):
        dev_data = data['developer_data']
        comm_data = data['community_data']
        pbl_interest_data = data['public_interest_stats']

        sentiment_data = ((coin_id, dtm,
                           comm_data.get('facebook_likes', None),
                           comm_data.get('twitter_followers', None),
                           comm_data.get('reddit_average_posts_48h', None),
                           comm_data.get('reddit_average_comments_48h', None),
                           comm_data.get('reddit_subscribers', None),
                           comm_data.get('reddit_accounts_active_48h', None),
                           comm_data.get('telegram_channel_user_count', None),
                           dev_data.get('forks', None),
                           dev_data.get('stars', None),
                           dev_data.get('subscribers', None),
                           dev_data.get('total_issues', None),
                           dev_data.get('closed_issues', None),
                           dev_data.get('pull_requests_merged', None),
                           dev_data.get('pull_request_contributors', None),
                           dev_data.get('commit_count_4_weeks', None),
                           pbl_interest_data.get('alexa_rank', None),
                           pbl_interest_data.get('bing_matches', None)))

        print(sentiment_data)
    else:
        logger.info('No data for {} at {}'.format(coin_id, dtm.strftime("%d-%m-%Y")))
