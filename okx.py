import requests
import time
import os
import urllib.parse
import json
import colorama
from colorama import Fore, Style
from concurrent.futures import ThreadPoolExecutor, as_completed
import random
from fake_useragent import UserAgent

class OKX:
    def __init__(self, init_data):
        self.x_telegram_init_data, self.ext_user_id, self.ext_user_name = self.parse_init_data(init_data)
        self.last_check_in_time = None

    def parse_init_data(self, init_data):
        parsed_data = urllib.parse.parse_qs(init_data)
        user_data = parsed_data.get('user', [])[0]
        user_info = urllib.parse.unquote(user_data)

        try:
            user_info_dict = json.loads(user_info)
        except json.JSONDecodeError:
            raise ValueError('Ошибка чтения JSON')

        ext_user_id = user_info_dict.get('id', '')
        ext_user_name = user_info_dict.get('username', '')

        return init_data, ext_user_id, ext_user_name

    def get_random_user_agent(self):
        ua = UserAgent()
        return ua.random
    def headers(self):
        return {
            'Accept': '*/*',
            'Content-Type': 'application/json',
            'Origin': 'https://www.okx.com',
            'Referer': 'https://www.okx.com/mini-app/racer',
            'User-Agent': self.get_random_user_agent(),
            'X-Telegram-Init-Data': self.x_telegram_init_data
        }

    def post_to_okx_api(self):
        url = f'https://www.okx.com/priapi/v1/affiliate/game/racer/info?t={int(time.time() * 1000)}'
        headers = self.headers()
        payload = {
            "extUserId": self.ext_user_id,
            "extUserName": self.ext_user_name,
            "gameId": 1,
            "linkCode": "88910038"
        }
        response = requests.post(url, headers=headers, json=payload)
        self.check_response(response)
        return response

    def assess_prediction(self, predict):
        url = f'https://www.okx.com/priapi/v1/affiliate/game/racer/assess?t={int(time.time() * 1000)}'
        headers = self.headers()
        payload = {
            "extUserId": self.ext_user_id,
            "predict": predict,
            "gameId": 1
        }
        response = requests.post(url, headers=headers, json=payload)
        self.check_response(response)
        return response


    def check_response(self, response):
        if response.status_code != 200:
            self.log(Fore.RED + f'Ошибка {response.status_code}' + Style.RESET_ALL)
            response.raise_for_status()
        try:
            response.json()
        except ValueError:
            self.log(Fore.RED + 'Ошибка чтения JSON' + Style.RESET_ALL)
            self.log(Fore.RED + f'Ответ: {response.text}' + Style.RESET_ALL)
            response.raise_for_status()

    def check_task(self):
        url = f'https://www.okx.com/priapi/v1/affiliate/game/racer/tasks?extUserId={self.ext_user_id}&t={int(time.time() * 1000)}'
        headers = self.headers()
        response = requests.get(url, headers=headers)
        self.check_response(response)
        tasks = response.json().get('data', [])


        time.sleep(1)
        for task in tasks:
            task_id = task['id']
            task_status = task['state']
            task_title = task["context"]["name"]

            if task_status == 0:
                url_claim = f'https://www.okx.com/priapi/v1/affiliate/game/racer/task?t={int(time.time() * 1000)}'
                headers = self.headers()
                payload = {
                    "extUserId": self.ext_user_id,
                    "id": task_id
                }
                requests.post(url_claim, headers=headers, json=payload)
                time.sleep(1)

                in_task = next((task for task in tasks), None)

                if in_task:
                    if in_task['state'] == 0:
                        self.log(f"{Fore.LIGHTYELLOW_EX}Выполнил задание '{task_title}' для {self.ext_user_name}!")

    def boost(self):
        url = f'https://www.okx.com/priapi/v1/affiliate/game/racer/boosts?extUserId={self.ext_user_id}&t={int(time.time() * 1000)}'
        headers = self.headers()
        response = requests.get(url, headers=headers)
        self.check_response(response)
        tasks = response.json().get('data', [])
        boost = next((task for task in tasks if task['id'] == 1), None)

        time.sleep(1)
        if boost:
            if boost['state'] == 0:
                    url_claim = f'https://www.okx.com/priapi/v1/affiliate/game/racer/boost?t={int(time.time() * 1000)}'
                    headers = self.headers()
                    payload = {
                        "extUserId": self.ext_user_id,
                        "id": 1
                    }
                    requests.post(url_claim, headers=headers, json=payload)
                    self.log(f"{Fore.LIGHTYELLOW_EX}Использовал буст Reload Fuel Tank для {self.ext_user_name}!")

    def log(self, message):
        print(message)

    def log_without_prefix(self, message):
        print(message, end='\r')

    def sleep(self, seconds):
        time.sleep(seconds)

    def countdown(self, seconds):
        for i in range(seconds, 0, -1):
            self.sleep(1)
        print()

    def wait_with_countdown(self, seconds):
        for i in range(seconds, 0, -1):
            self.sleep(1)
        print()

    def process(self, predict=None):
        while True:
            try:
                self.check_task()
                time.sleep(1)
                for _ in range(50):
                    response = self.post_to_okx_api()
                    balance_points = response.json().get('data', {}).get('balancePoints', 0)

                    if predict is None or predict not in [0, 1]:
                        predict = random.randint(0, 1)
                    assess_response = self.assess_prediction(predict)
                    assess_data = assess_response.json().get('data', {})
                    result = 'Win' if assess_data.get('won', False) else 'Lose'
                    calculated_value = assess_data.get('basePoint', 0) * assess_data.get('multiplier', 1)

                    output = f"""
{Fore.BLUE}Аккаунт {self.ext_user_name}{Style.RESET_ALL}
Баланс: {Fore.LIGHTYELLOW_EX}{balance_points}{Style.RESET_ALL}
Результат: {Style.BRIGHT}{result}{Style.RESET_ALL}
Получено: {Fore.LIGHTYELLOW_EX}{calculated_value}{Style.RESET_ALL}

                    """.strip()
                    self.log_without_prefix(output)
                    if assess_data.get('numChance') == 1:
                        self.boost()
                        self.countdown(5)
                        break
                    if assess_data.get('numChance', 0) > 1:
                        self.countdown(5)
                        continue
                    elif assess_data.get('secondToRefresh', 0) > 0:
                        self.countdown(assess_data['secondToRefresh'] + 5)
                    else:
                        break
            except Exception as e:
                self.log(Fore.RED + f'Error: {str(e)}' + Style.RESET_ALL)
            self.wait_with_countdown(60)


def main():
    colorama.init(autoreset=True)
    init_data_file = os.path.join(os.path.dirname(__file__), 'initdata.txt')

    if not os.path.exists(init_data_file):
        raise FileNotFoundError(f'{init_data_file} not found')

    with open(init_data_file, 'r', encoding='utf-8') as file:
        init_data_list = file.readlines()

    with ThreadPoolExecutor(max_workers=50) as executor:
        futures = [executor.submit(run_process, init_data.strip()) for init_data in init_data_list]

        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(Fore.RED + f'Error: {str(e)}' + Style.RESET_ALL)

def run_process(init_data):
    okx = OKX(init_data)
    okx.process()

if __name__ == '__main__':
    main()
