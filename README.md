# Spaces
## :robot: [CASE "NAUMEN Telegram Бот"](https://drive.google.com/file/d/1EyuxQHTg5V7LGInKZFtsyVkFNT3FBaEz/view)

>Наше решение позволяет HR-ам быстро и удобно обрабатывать анкеты будущих стажеров. Вся информация собирается в одном месте, [Гугл-Таблице](https://docs.google.com/spreadsheets/d/1OMjENvfDnax3xV9saBWAbM111KxTskO-CBaNUTYfQTk/edit?usp=sharing), где ее очень просто анализировать. Помимо удобства для HR-ов, [Telegram Бот](https://t.me/spaces_naumen_bot) будет полезен и будущим стажерам, показывая актуальную информацию о доступных стажировках и образовательных программах. Также бот может оповещать стажеров об открывшихся стажировках в их городе и давать возможность заполнить анкету в [Гугл-Форме](https://forms.gle/8RoffafEfF9fW1wPA).

## Наш стек
- Google Sheets API
- Google Forms API
- Golang Telegram API
- Python Flask (Backend Server)
- Docker

## Как это работает?
1. Студент общается с ботом и получает ссылку на Гугл-Форму для прохождения анкеты.
2. Студент отправляет анкету с тестовым заданием.
3. Форма отправляет запрос к серверу, который считывает таблицу с ответами, и форматирует ее в более читабельный вид.
4. HR видит изменения в таблице.

## Python Flask Backend
#### **server** = http://82.146.61.94:5000
- **server**/get/interns - **[GET]** возвращает json с инфрмацией о стажировках с сайта https://www.naumen.ru/career/trainee/
```json
{
"Краснодар": {
    "count": 1,
    "interns": [
      [
        "Стажер-разработчик Java",
        "https://www.naumen.ru/career/trainee/krasnodar/java_sd/"
      ]
    ]
    },
"Другие города..."
}
```
- **server**/get/wait/<chat_id> **[GET]** получить 
- **server**/set/wait/<chat_id> **[POST]** установить 
- **server**/delete/wait/<chat_id> **[POST]** удалить напоминание пользователя
- **server**/update/table - **[POST]** отправка запроса об обновлении Google Таблицы
- **server**/notify **[POST]** уведомить пользователей об открытых стажировках

## Google Forms Script
Функция, которая отправляет запрос на обновление данных в таблице.
Вызывается после отправки [формы](https://forms.gle/8RoffafEfF9fW1wPA).
```js
function myFunction() {
  var formData = {
    'update': 'true'
  };
  var options = {
    'method' : 'post',
    'payload' : formData
  };
  UrlFetchApp.fetch('http://82.146.61.94:5000/update/table', options)
}
```

## Docker
- Приложение докеризировано и может быть собрано с помощью команды `make build-docker`
- После сборки приложение вместе с Postgres можно запустить с помощью команды `make run-all`
