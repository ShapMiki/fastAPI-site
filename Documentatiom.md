





## 4. Архитектура HTML данных

### 4.1 personal_account_page.html

    Общая схема json:

    {
    'user_data': {
        ......
        }
    'activ_lot_data': {
        ......
        }
    'another_data': {
        ......
        }
    }
    'property_data': {
        ......
        }
    }


    Для данных о пользователе:
    - Имя - `name`
    - Фамилия - `surname`
    - email - `email`
    - номер паспорта - `passport`
    - балланс


### 4.2 Чаты

    Схема json для окна чатов (chats_page.html):

    {
    'user_data': {
        ......
        }
    'chat_list_data': [{
        'chat_name': #ИМЯ ДРУГОГО ПОЛЬЗОВАТЕЛЯ#,
        'not_readed_messages': #КОЛИЧЕСТВО НЕПРОЧИТАННЫХ СООБЩЕНИЙ#,
        'last_message': chat.last_message,
        'last_message_date': chat.last_message_date
         ......
        }]
    }
#
    Схема json для окна чата (chat_page.html):

    {
    'user_data': {
        ......
        }
    'chat_data': {
        'chat_name': #ИМЯ ДРУГОГО ПОЛЬЗОВАТЕЛЯ#,
        }
    'message_list_data': [{
        'message_id": message.id,
        'text': message.text,
        'sending_date': message.sending_date,
        'is_read': message.is_resd,
        'owner': message.owner
        ......
    }]
    }