# Автофарм okx race





-  Играет сам в игры, рандомно выбирая шорт или лонг
-  Забирает дейли ревард
-  Можно загрузить много акков
-  Работа по сессии pyrogram с прокси или без
-  Выполняет задания
-  Улучшает буст turbo charger
-  Если нету попыток для игры и есть буст на их восполнение, юзает его
-  Регает акк по вашей рефке


# Установка:
1. Установить python (Протестировано на 3.11)

2. Зайти в cmd(терминал) и вписывать
   ```
   git clone https://github.com/meKryztal/okxrace.git
   ```
   
   ```
   cd okxrace
   ```
3. Установить модули
   
   ```
   pip install -r requirements.txt
   ```
 
   или
   
   ```
   pip3 install -r requirements.txt
   ```



4. Запуск
   ```
   python main.py
   ```

   или

   ```
   python3 main.py
   ```
   
# Или через Pycharm ГАЙД на любых системах и решения ошибок внизу гайда
https://telegra.ph/Avtoklikker-dlya-BLUM-GAJD-05-29
   

### Получить API_ID and API_HASH можно тут: https://my.telegram.org

## Настройте data/config.py перед запуском

### Прокси добавьте в файл proxy.txt такого вида:

```
ip:port:login:password имя файла сессии
ip:port:login:password имя файла сессии
ip:port:login:password имя файла сессии
ip:port:login:password имя файла сессии
```

Выбрав первый пункт, создание сессии, вы воодите имя sec1 и у вас появляется файл sec1.session, пример:
192.168.1.1:8000:mylog:mypass sec1

## Если у вас сразу на руках есть файлы сессий, то создайте папку sessions и в нее добавьте их
