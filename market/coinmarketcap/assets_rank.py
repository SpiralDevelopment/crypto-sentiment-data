import requests
import logging

logger = logging.getLogger(__name__)

URL = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'


def get_assets_and_ticker_from_api(start, limit):
    try:
        params = {
            'start': start,
            'limit': limit,
            'sort': 'market_cap',
            'CMC_PRO_API_KEY': 'YOUR_API_KEY_HERE'
        }

        response = requests.get(URL, params=params)
        if response:
            return response.json()
    except Exception as e:
        logger.error(str(e))


if __name__ == '__main__':
    # get information (rank, supply, ...) for top 100 assets
    response_dict = get_assets_and_ticker_from_api(1, 100)
    print(response_dict)
