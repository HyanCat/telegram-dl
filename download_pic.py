from telethon import TelegramClient, sync
import os
# import socks #如果你不需要通过代理连接Telegram，可以删掉这一行
from telethon.tl.types import InputMessagesFilterPhotos
import json

# 读取 config
f = open('config.json', 'r')
content = f.read()
config = json.loads(content)

# =============需要被替换的值=================
'''
api_id 你的api id
api_hash 你的api hash
proxy 将localhost改成代理地址,1080改成代理端口
'''
api_id = config['api_id']
api_hash = config['api_hash']
# proxy =(socks.SOCKS5,"0.0.0.0",1080) #不需要代理的话删掉该行


def download(channel):
    channel_link = "https://t.me/"+channel
    picture_storage_path = "data/"+channel
    # ==========================================

    photos = client.get_messages(
        channel_link, None, max_id=100000, min_id=0, filter=InputMessagesFilterPhotos)

    total = len(photos)
    index = 0
    for photo in photos:
        ext = photo.file.ext
        filename = picture_storage_path + "/" + \
            channel + "_" + str(photo.id) + ext
        index = index + 1
        print("downloading:", index, "/", total, " : ", filename)
        if os.path.exists(filename) == False:
            client.download_media(photo, filename)
            print('done!')
        else:
            print('exist!')


client = TelegramClient('my_session', api_id=api_id,
                        api_hash=api_hash).start()
for channel in config['channels']:
    print('Start downloading channel: ', channel)
    download(channel)
    print('Finish downloading channel: ', channel)

client.disconnect()
