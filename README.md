# Команда Spaces
## :robot: [Case "NAUMEN Telegram Бот"](https://drive.google.com/file/d/1EyuxQHTg5V7LGInKZFtsyVkFNT3FBaEz/view)

>Наше решение позволяет HR-ам быстро и удобно обрабатывать анкеты будущих стажеров. Вся информация собирается в одном месте, [Гугл-Таблице](https://docs.google.com/spreadsheets/d/1OMjENvfDnax3xV9saBWAbM111KxTskO-CBaNUTYfQTk/edit?usp=sharing), где ее очень просто анализировать. Помимо удобства для HR-ов, [Telegram Бот](https://t.me/spaces_naumen_bot) будет полезен и будущим стажерам, показывая актуальную информацию о доступных стажировках и образовательных программах. Также бот может оповещать стажеров об открывшихся стажировках в их городе и давать возможность заполнить анкету в [Гугл-Форме](https://forms.gle/8RoffafEfF9fW1wPA).

## :package: Наш стек
- Google Sheets API
- Google Forms API
- Golang Telegram API
- Python Flask (Backend Server)
- PostgreSQL
- Redis
- Docker

## :question: Как это работает?
1. Студент общается с ботом и получает ссылку на Гугл-Форму для прохождения анкеты.
2. Студент отправляет анкету с тестовым заданием.
3. Форма отправляет запрос к серверу, который считывает таблицу с ответами, и форматирует ее в более читабельный вид.
4. HR видит изменения в таблице.

## Python Flask Backend
- `[GET]` `get/interns` - возвращает json с инфрмацией о стажировках с сайта https://www.naumen.ru/career/trainee/
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
- `[GET]` `/get/wait/<chat_id>` - получить информацию о том, находится ли пользователь в списке уведомлений
- `[POST]` `/set/wait/<chat_id>` - добавить пользователя в список уведомлений 
- `[POST]` `/delete/wait/<chat_id>` - удалить напоминание пользователя
- `[POST]` `/update/table` - отправка запроса об обновлении Google Таблицы
- `[POST]` `/notify` - уведомить пользователей об открытых стажировках

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
  UrlFetchApp.fetch('http://*ip*:*port*/update/table', options)
}
```

## Docker
- Приложение докеризировано и может быть собрано с помощью команды `make build-docker`
- После сборки приложение вместе с Postgres можно запустить с помощью команды `make run-all`

# :fireworks: Result [1st place](https://vk.com/hackathon_urfu?w=wall-170322615_591)
