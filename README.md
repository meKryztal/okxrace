# Автофарм Steamify

![photo_2024-07-25_15-00-33](https://github.com/user-attachments/assets/3e6df2a4-2141-4796-b09d-203d3381a61b)



-  Клеймит каждые 6 часов поинты
-  Забирает дейли ревард
-  Можно загрузить сотни акков
-  Работа по ключу, без авторизации
-  Забирает бусты
-  Выполняет задания 
-  Забирает награду с рефки


# Установка:
1. Установить python (Протестировано на 3.11)

2. Зайти в cmd(терминал) и вписывать
   ```
   git clone https://github.com/meKryztal/steamify.git
   ```
   
   ```
   cd steamify
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
   python tabi.py
   ```

   или

   ```
   python3 tabi.py
   ```
   
# Или через Pycharm ГАЙД на любых системах и решения ошибок внизу гайда
https://telegra.ph/Avtoklikker-dlya-BLUM-GAJD-05-29
   



## Вставить в файл init_data ключи такого вида, каждый новый ключ с новой строки:
   ```
   query_id=xxxxxxxxxx&user=xxxxxxfirst_namexxxxxlast_namexxxxxxxusernamexxxxxxxlanguage_codexxxxxxxallows_write_to_pmxxxxxxx&auth_date=xxxxxx&hash=xxxxxxx
   query_id=xxxxxxxxxx&user=xxxxxxfirst_namexxxxxlast_namexxxxxxxusernamexxxxxxxlanguage_codexxxxxxxallows_write_to_pmxxxxxxx&auth_date=xxxxxx&hash=xxxxxxx
   query_id=xxxxxxxxxx&user=xxxxxxfirst_namexxxxxlast_namexxxxxxxusernamexxxxxxxlanguage_codexxxxxxxallows_write_to_pmxxxxxxx&auth_date=xxxxxx&hash=xxxxxxx
   query_id=xxxxxxxxxx&user=xxxxxxfirst_namexxxxxlast_namexxxxxxxusernamexxxxxxxlanguage_codexxxxxxxallows_write_to_pmxxxxxxx&auth_date=xxxxxx&hash=xxxxxxx
   ```
Вместо query_id= может быть user=, разницы нету
# Как получить query_id:
Заходите в telegram web, открываете бота, жмете F12 или в десктопной версии открывайте окно, правой кнопкой жмете и выбираете самое нижнее "проверить" и переходите в Network, жмете старт в веб версии или перезагружаете страницу в десктопной, ищете запрос с именем info, в правой колонке находите Rawdata: query_id=бла бла бла или user=

![photo_2024-07-25_15-02-24](https://github.com/user-attachments/assets/af7eafb9-32d5-49f3-bf15-617a18b0f6ca)
