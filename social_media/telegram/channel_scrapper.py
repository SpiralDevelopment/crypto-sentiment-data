from telethon.tl.functions.channels import GetFullChannelRequest
import asyncio
import json
import telethon
from telethon.errors import SessionPasswordNeededError
from telethon.tl.types import Channel
import logging
import os
import time
import calendar

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message).170s")

logger = logging.getLogger(__name__)

CONFIG_FILE_PATH = os.path.join(os.getcwd(), 'config.json')


def from_utc_dtm_to_utc_timestamp(utc_date_time):
    return calendar.timegm(utc_date_time.utctimetuple())


def is_msg_valid(msg):
    return msg and not msg.startswith('/') and any(c.isalpha() for c in msg)


async def save_channel_posts():
    try:
        with open(CONFIG_FILE_PATH) as f:
            cfg = json.load(f)

        client = telethon.TelegramClient(cfg['SESSION_ID'], cfg['API_ID'], cfg['API_HASH'])
        await client.connect()

        if not await client.is_user_authorized():
            logger.error('User is not authorized')
            await client.send_code_request(cfg['PHONE'])

            try:
                await client.sign_in(cfg['PHONE'], input('Enter auth code: '))
            except SessionPasswordNeededError:
                await client.sign_in(password=cfg['TWO_STEP_AUTH_PWD'])

        # To get channels from your own dialogs:
        # async for dialog in client.iter_dialogs():
        #     if isinstance(dialog.entity, Channel):
        #         channel_name = dialog.name
        #         client_id = dialog.entity.id

        # To get channels by their link/id
        for channel_name in ['@relative_strength_index']:
            logger.info(channel_name)
            dialog = await client(GetFullChannelRequest(channel_name))
            update_time = int(time.time())
            client_id = dialog.full_chat.id

            async for message in client.iter_messages(client_id, limit=30):
                post_id = message.id
                post_views = message.views
                publish_time = message.date
                msg = message.message

                if is_msg_valid(msg) and post_views:
                    logger.info(msg)
                    logger.info("{},{},{},{},{}".format(update_time,
                                                        channel_name,
                                                        post_id,
                                                        from_utc_dtm_to_utc_timestamp(publish_time),
                                                        post_views))

            time.sleep(5)
    except Exception as e:
        logger.error(str(e))


if __name__ == '__main__':
    aio_loop = asyncio.get_event_loop()

    try:
        left_pub_comm = aio_loop.run_until_complete(save_channel_posts())
    except RuntimeError:
        pass
    finally:
        if not aio_loop.is_closed():
            aio_loop.close()
