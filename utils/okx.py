from pyrogram.raw.functions.messages import RequestAppWebView
from pyrogram.raw.types import InputBotAppShortName

from urllib.parse import unquote
from utils.core import logger

from fake_useragent import UserAgent
from pyrogram import Client
from data import config

import asyncio
import aiohttp
import random
import time
import json

class Okx:
    def __init__(self, thread: int, account: str, proxy : str):
        self.thread = thread
        self.name = account
        if random.randint(0,4) == 0:
            self.ref = 'linkCode_67665606'
        else:
            self.ref = config.REF_CODE
        if proxy:
            proxy_client = {
                "scheme": config.PROXY_TYPE,
                "hostname": proxy.split(':')[0],
                "port": int(proxy.split(':')[1]),
                "username": proxy.split(':')[2],
                "password": proxy.split(':')[3],
            }
            self.client = Client(name=account, api_id=config.API_ID, api_hash=config.API_HASH, workdir=config.WORKDIR, proxy=proxy_client)
        else:
            self.client = Client(name=account, api_id=config.API_ID, api_hash=config.API_HASH, workdir=config.WORKDIR)

        if proxy:
            self.proxy = f"{config.PROXY_TYPE}://{proxy.split(':')[2]}:{proxy.split(':')[3]}@{proxy.split(':')[0]}:{proxy.split(':')[1]}"
        else:
            self.proxy = None

        headers = {
                    'Accept': 'application/json',
                    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,bg;q=0.6,mk;q=0.5',
                    'Content-Type': 'application/json',
                    'Connection': 'keep-alive',
                    'Origin': 'https://www.okx.com',
                    'Referer': 'https://www.okx.com/',
                    'Sec-Fetch-Dest': 'empty',
                    'Sec-Fetch-Mode': 'cors',
                    'Sec-Fetch-Site': 'same-site',
                    'Sec-Ch-Ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
                    'Sec-Ch-Ua-mobile': '?1',
                    'Sec-Ch-Ua-platform': '"Android"',
                    'User-Agent': UserAgent(os='android').random,
                }
        self.session = aiohttp.ClientSession(headers=headers, trust_env=True, connector=aiohttp.TCPConnector(verify_ssl=False))

    async def main(self):
        await asyncio.sleep(random.uniform(*config.ACC_DELAY))
        asyncio.create_task(self.continuous_guess_price())
        while True:
            await self.login()
            info = (await self.get_info())
            tasks = (await self.get_tasks())
            if 'data' not in tasks:
                logger.error(f'Задание | Поток {self.thread} | {self.name}.session | {tasks}')
                await asyncio.sleep(random.uniform(*config.MINI_SLEEP))
            else:
                tasks = tasks['data']
                for task in tasks:
                    if random.randint(0, 3) == 1:
                        if task['state'] == 1 or task['id'] in config.BLACKLIST:
                            continue
                        is_do = await self.do_task(id_=task['id'])
                        if is_do:
                            logger.success(
                                f'Выполнил | Поток {self.thread} | {self.name}.session | Забрал {task["points"]} points for {task["context"]["name"]}')

            boosts = (await self.get_boosts())
            if 'data' not in boosts:
                logger.error(f'Буст | Поток {self.thread} | {self.name}.session | {boosts}')
                await asyncio.sleep(random.uniform(*config.MINI_SLEEP))
            else:
                boosts = boosts['data']

                specific_boost_id = 3
                specific_boost = next((boost for boost in boosts if boost['id'] == specific_boost_id), None)

                if specific_boost:
                    if 'isLocked' in specific_boost and specific_boost['isLocked']:
                        logger.info(f'Буст {specific_boost_id} заблокирован')
                    else:
                        is_can_buy = await self.can_buy(boost=specific_boost)
                        if is_can_buy:
                            bought = await self.do_boost(id_=specific_boost_id)
                            if bought:

                                logger.success(
                                    f'Взял буст | Поток {self.thread} | {self.name}.session | {specific_boost["context"]["name"]} ')
                else:
                    logger.info(f'Буст с ID {specific_boost_id} не найден')


            sleep = random.uniform(*config.BIG_SLEEP)
            logger.info(f'| Поток {self.thread} | {self.name}.session | Ушел в сон заданий на {sleep} сек')

            await asyncio.sleep(sleep)

    async def continuous_guess_price(self):
        await asyncio.sleep(30)
        while True:

            await self.guess_price()


    async def get_tg_web_data(self):
        await self.client.connect()
        try:
            bot = await self.client.resolve_peer('OKX_official_bot')
            app = InputBotAppShortName(bot_id=bot, short_name="OKX_Racer")


            web_view = await self.client.invoke(RequestAppWebView(
                    peer=bot,
                    app=app,
                    platform='android',
                    write_allowed=True,
                    start_param=self.ref
                ))

            auth_url = web_view.url

            info = json.loads((unquote(string=unquote(string=auth_url.split('tgWebAppData=')[1].split('&tgWebAppVersion')[0])))[5:].split('&chat_instance')[0])

            self.user_id = info['id']
            self.first_name = info['first_name']
            self.last_name = info['last_name']

        except Exception as err:
            logger.error(f" | Поток{self.thread} | {self.name}.session | {err}")
            if 'USER_DEACTIVATED_BAN' in str(err):
                logger.error(f"Авторизация | Поток {self.thread} | {self.name}.session | USER BANNED")
                await self.client.disconnect()
                return False
        await self.client.disconnect()
        return unquote(string=auth_url.split('tgWebAppData=')[1].split('&tgWebAppVersion')[0])

    async def login(self):
        telegram_data = await self.get_tg_web_data()
        self.session.headers['X-Telegram-Init-Data'] = telegram_data

    async def get_info(self):
        json_data = {
            "extUserId": self.user_id,
            'extUserName': f'{self.first_name} {self.last_name}',
            'linkCode': self.ref[9:],
        }
        params = {
            't' : str(int(time.time()*1000)),
        }
        response = await self.session.post(
            'https://www.okx.com/priapi/v1/affiliate/game/racer/info',
            json=json_data,
            params=params,
            proxy=self.proxy
        )
        await asyncio.sleep(random.uniform(*config.MINI_SLEEP))
        return (await response.json())

    async def get_boosts(self):
        params = {
            't': str(int(time.time()*1000)),
        }

        response = await self.session.get(
            'https://www.okx.com/priapi/v1/affiliate/game/racer/boosts',
            params=params,
            proxy = self.proxy
        )
        await asyncio.sleep(random.uniform(*config.MINI_SLEEP))
        return (await response.json())

    async def do_boost(self, id_ : int):
        params = {
            't': str(int(time.time()*1000)),
        }

        json_data = {
            "extUserId": self.user_id,
            'id': id_,
        }

        response = await self.session.post(
            'https://www.okx.com/priapi/v1/affiliate/game/racer/boost',
            params=params,
            json=json_data,
            proxy=self.proxy
        )

        await asyncio.sleep(random.uniform(*config.BOOST_SLEEP))

        if (await response.json())['code'] == 0:
            return True
        else:
            logger.error(f"Буст| Поток {self.thread} | {self.name}.session | {(await response.json())}")
            return False

    async def can_buy(self,boost : dict):
        balance = (await self.get_info())
        if 'data' not in balance:
            logger.error(f'Можно купить | Поток {self.thread} | {self.name}.session | {balance}')
            await asyncio.sleep(random.uniform(*config.MINI_SLEEP))
            return False
        else:
            balance = balance['data']['balancePoints']
        curStage = boost['curStage']
        totalStage = boost['totalStage']
        pointCost = boost['pointCost']
        if curStage < totalStage and pointCost <= balance:
            return True
        return False

    async def get_tasks(self):
        params = {
            't': str(int(time.time()*1000)),
        }

        response = await self.session.get(
            'https://www.okx.com/priapi/v1/affiliate/game/racer/tasks',
            params=params,
            proxy = self.proxy
        )
        await asyncio.sleep(random.uniform(*config.MINI_SLEEP))
        return (await response.json())

    async def do_task(self, id_ : int):
        params = {
            't': str(int(time.time()*1000)),
        }
        json_data = {
            "extUserId": self.user_id,
            'id': id_,
        }

        response = await self.session.post(
            'https://www.okx.com/priapi/v1/affiliate/game/racer/task',
            params=params,
            json=json_data,
            proxy = self.proxy
        )

        await asyncio.sleep(random.uniform(*config.TASK_SLEEP))

        if (await response.json())['code'] == 0:
            return True
        else:
            logger.error(f"Задание | Поток {self.thread} | {self.name}.session | {id_} {(await response.json())}")
            return False

    async def guess_price(self):
        params = {
            't': str(int(time.time() * 1000)),
        }

        json_data = {
            'predict': random.randint(0, 1),
        }

        if json_data['predict'] == 0:
            logger.info(f"Игра | Поток {self.thread} | {self.name}.session | SHORT")
        else:
            logger.info(f"Игра | Поток {self.thread} | {self.name}.session | LONG")


        response = await self.session.post(
            'https://www.okx.com/priapi/v1/affiliate/game/racer/assess',
            params=params,
            json=json_data,
            proxy=self.proxy
        )




        try:
            response_json = await response.json()
            is_won = response_json.get('data', {}).get('won')
            claimed = response_json.get('data', {}).get('basePoint')
            num = response_json.get('data', {}).get('numChance')
            sec = response_json.get('data', {}).get('secondToRefresh')
        except Exception as e:
            logger.error(f"guess_price | Поток {self.thread} | {self.name}.session | {str(e)}")
            return False

        await asyncio.sleep(5)

        if is_won:
            logger.success(f"Игра | Поток {self.thread} | {self.name}.session | Выиграл : получено {claimed}")
        else:
            logger.error(f"Игра | Поток {self.thread} | {self.name}.session | Проиграш")

        if num == 1:
            boosts = (await self.get_boosts())
            boosts = boosts['data']
            specific_boost = next((boost for boost in boosts if boost['id'] == 1), None)

            if specific_boost and specific_boost['state'] == 0:
                await self.do_boost(id_=1)
                logger.success(f'Взял буст | Поток {self.thread} | {self.name}.session | Восполнение бака')
        if sec is None:
            sec = 0
            await asyncio.sleep(65)
        if sec > 0 and (num == 1 or num == 0):
            await asyncio.sleep(sec + 10)

        return response_json



