import os
import re

import pandas as pd
import requests
from bs4 import BeautifulSoup
from data.config import TGSTAT_TOKEN
from loader import dp
from utils.db_api.db_commands import create_row, get_links, add_err, add_citate, get_info, delete_info

CLEANR = re.compile('<.*?>')


async def clean_html(raw_html):
    clean_text = re.sub(CLEANR, '', raw_html)
    return clean_text


headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive'}


async def get_channels(key, telegram_id, limit):
    url = f'https://api.tgstat.ru/channels/search?token={TGSTAT_TOKEN}&q={key}&country=ru&limit={limit}'

    r = requests.get(url=url)

    data = r.json()['response']['items']

    for row in data:
        if 't.me/joinchat/' in row['link']:
            pass
        else:
            await create_row(telegram_id=telegram_id,
                             channel_name=row['title'],
                             count=row['participants_count'],
                             link=row['link'])

    await get_stat(telegram_id, key)


async def get_stat(telegram_id, key):
    links = await get_links(telegram_id)

    for link in links:
        current_link = link.split('/')[1]
        url = f'https://tgstat.ru/channel/@{current_link}/stat'
        r = requests.get(url=url, headers=headers)
        try:
            soup = BeautifulSoup(r.text, 'html.parser')

            parse = soup.find('div', class_='row mb-1 mt-0')
            get_err = parse.find('h2', class_='text-dark')
            get_err_24 = parse.find('h2', class_='text-dark text-right')
            err = get_err.text
            err_24 = get_err_24.text

            if err_24 is None:
                err_24 = '0%'

            await add_err(
                telegram_id=telegram_id,
                link=link,
                err=err,
                err_24=err_24
            )

            await get_citate(link=link, telegram_id=telegram_id, key=key)
        except AttributeError:
            try:
                current_link = link.split('/')[1]
                url = f'https://tgstat.ru/channel/@{current_link}/stat'
                r = requests.get(url=url, headers=headers)
                soup = BeautifulSoup(r.text, 'html.parser')

                parse = soup.find('div', class_='row mb-1 mt-0')
                new_get_err = parse.find('h2', class_='text-dark')
                new_err = new_get_err.text
                if new_err is None:
                    new_err = '0%'

                await add_err(
                    telegram_id=telegram_id,
                    link=link,
                    err=new_err,
                    err_24='Нет информации'
                )
            except AttributeError:

                await add_err(
                    telegram_id=telegram_id,
                    link=link,
                    err="Нет информации",
                    err_24='Нет информации'
                )
                await get_citate(link=link, telegram_id=telegram_id, key=key)

    await create_table(key=key, telegram_id=telegram_id)


async def get_citate(link, telegram_id, key):
    username = link.split('/')[1]

    url = f'https://tgstat.ru/channel/@{username}/stat/citation-index'

    r = requests.get(url, headers=headers)

    soup = BeautifulSoup(r.text, 'html.parser')
    try:
        try:
            parse = soup.find_all('a',
                                  class_='list-group-item list-group-item-action list-group-item-body border-0 py-1 popup_ajax')[
                4]

            parser = BeautifulSoup(str(parse), 'html.parser')

            rows = parser.find_all('div', class_='col col-3 text-right font-12')

            array = []
            for row in rows:
                clean = await clean_html(str(row))
                array.append(clean.replace('\n', '').replace(' ', ''))

            await add_citate(
                link=link,
                telegram_id=telegram_id,
                citate_amount=array[0],
                citate_percent=array[1]

            )

        except IndexError:
            await add_citate(
                link=link,
                telegram_id=telegram_id,
                citate_amount='Нет информации',
                citate_percent='Нет информации'

            )

    except AttributeError:

        await add_citate(
            link=link,
            telegram_id=telegram_id,
            citate_amount='0%',
            citate_percent='0%'

        )


async def create_table(key, telegram_id):
    data = await get_info(telegram_id=telegram_id)

    df = pd.DataFrame(
        {
            'Название канала': data[0],
            'Участники': data[1],
            'Ссылка на канал': data[2],
            'ERR': data[3],
            'ERR 24': data[4],
            'Цитирование в накрученных каналах, кол-во': data[5],
            'Цитирование в накрученных каналах, %': data[6]
        }
    )
    df.to_excel(f'./tables/key - {key}.xlsx', sheet_name='Результат', index=False)

    table = open(f'./tables/key - {key}.xlsx', 'rb')
    await delete_info(telegram_id)
    await dp.bot.send_document(
        chat_id=telegram_id,
        document=table,
        caption='🔔 Таблица готова!'
    )
    os.remove(f'./tables/key - {key}.xlsx')


async def get_stat_subscribe():
    url = f'https://api.tgstat.ru/usage/stat?token={TGSTAT_TOKEN}'

    r = requests.get(url=url)

    data = r.json()['response'][0]['spentRequests']
    expiredAt = r.json()['response'][0]['expiredAt']
    return [data, expiredAt]