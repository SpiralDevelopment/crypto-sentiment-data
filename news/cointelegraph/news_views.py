import calendar
from datetime import datetime, timezone
import time
import xmltodict
import requests
from bs4 import BeautifulSoup
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message).170s")

logger = logging.getLogger(__name__)

SAVE_FILE = "views_count.csv"


def get_news_url():
    try:
        response = requests.get('https://cointelegraph.com/rss',
                                headers={'User-Agent': 'perceval'})
        response = xmltodict.parse(response.text)
        all_news = response['rss']['channel']['item']
        res = []

        for news in all_news:
            pub_date = datetime.strptime(news['pubDate'], '%a, %d %b %Y %H:%M:%S %z')
            pub_date = pub_date.astimezone(tz=timezone.utc)
            pub_date = calendar.timegm(pub_date.utctimetuple())

            res.append({
                'link': news['link'],
                'pubDate': pub_date
            })

        return res
    except Exception as e:
        logger.error(str(e))


def scrap_views_count(news_list):
    res = dict()
    time_now = int(time.time())

    for news in news_list:
        try:
            link = news['link']
            pub_date = news['pubDate']

            logger.info(link)
            page = requests.get(link, headers={'User-Agent': 'perceval'})
            soup = BeautifulSoup(page.content, 'html.parser')
            views_count_span = soup.findAll("span", {"class": "total-qty"})

            if views_count_span:
                total_views = views_count_span[0].text
                total_shares = views_count_span[1].text

                res[link] = (str(time_now), str(pub_date), total_views, total_shares)
        except Exception as e:
            logger.error(str(e))
        finally:
            time.sleep(3.5)

    return res


def save_data(stat_dict):
    data_to_append = "\n".join([",".join([url, cur[0], cur[1], cur[2], cur[3]])
                                for url, cur in stat_dict.items()])

    with open(SAVE_FILE, 'a') as f:
        f.write(data_to_append + "\n")


if __name__ == "__main__":
    urls_to_scrap = get_news_url()
    stat_dict = scrap_views_count(urls_to_scrap)
    save_data(stat_dict)
