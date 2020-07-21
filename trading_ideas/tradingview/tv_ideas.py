from bs4 import BeautifulSoup
import time
import requests
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message).170s")

logger = logging.getLogger(__name__)

FILE = 'tv_ideas_stats.csv'


def append_new_data(data):
    with open(FILE, 'a', encoding="utf-8") as f:
        if f.tell() == 0:
            f.write('update_time,publish_time,author,title,url,likes,comments,views\n')

        f.write(data)


def fetch_tv_ideas(pair, base_urls, update_timestamp, least_likes_count=2):
    retrieved_url = dict()

    for base_url in base_urls:
        consecutive_no_data = 0

        for n in range(1, 10):
            try:
                if 'com/ideas' in base_url:
                    pair = pair.lower()
                else:
                    pair = pair.upper()

                url = base_url.format(pair, n)

                logger.info(url)
                result = requests.get(url)
                has_new_idea = False

                if result.status_code == 200:
                    soup = BeautifulSoup(result.content, 'html.parser')
                    all_ideas_in_page = soup.find_all("div", {"class": "tv-widget-idea"})

                    logger.info('all_ideas_in_page: %s', len(all_ideas_in_page))

                    for div in all_ideas_in_page:
                        title = div.find("a", {"class": "tv-widget-idea__title"})

                        if title:
                            title = title.text.replace(',', '')
                            url = div.find("p", {"class": "tv-widget-idea__description-row"})['data-href']

                            likes = div.find("div", {"class": "tv-social-row__start"}).find(
                                "span", {"class": "tv-card-social-item__count"}).text
                            comments = div.find("div", {"class": "tv-social-row__end"}).find(
                                "span", {"class": "tv-card-social-item__count"}).text

                            timestamp = div.find("span", {"class": "tv-card-stats__time"})['data-timestamp']

                            author = div.find("span", {"class": "tv-card-user-info__name"}).text.strip()

                            symbol = div.find("div", {"class": "tv-widget-idea__symbol-info"}).find(
                                "a", {"class": "tv-widget-idea__symbol"}).text.strip()

                            if int(likes) >= least_likes_count and url not in retrieved_url:
                                if 'symbols' in base_url or ('com/ideas' in base_url and symbol.lower() == pair.lower()):
                                    has_new_idea = True
                                    consecutive_no_data = 0
                                    retrieved_url[url] = 1

                                    data_to_append = ",".join([str(update_timestamp),
                                                               timestamp,
                                                               author,
                                                               title,
                                                               url,
                                                               likes,
                                                               comments]) + "\n"

                                    append_new_data(data_to_append)

                    if not has_new_idea:
                        consecutive_no_data += 1

                        if consecutive_no_data >= 5:
                            logger.info('Breaking because no data 5 times consecutively')
                            break
                else:
                    logger.info('Status code: %s', result.status_code)
            except Exception as e:
                logger.error(str(e))
            finally:
                time.sleep(8)


if __name__ == '__main__':
    pairs = [
        'btcusd',
        'xbtusd',
        'btcusdt'
    ]

    base_urls = ['https://www.tradingview.com/symbols/{}/ideas/page-{}/?sort=recent',
                 'https://www.tradingview.com/ideas/{}/page-{}/?sort=recent']

    for pair in pairs:
        logger.info(pair)
        fetch_tv_ideas(pair, base_urls, int(time.time()))


