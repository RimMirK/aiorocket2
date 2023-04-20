# SDK для работы с TON Rocket

## 🔐 Авторизация

Как получить токен написано [тут](https://pay.ton-rocket.com/api/).

Mainnet:

```python
import aiorocket
api = aiorocket.Rocket('токен')
```

Testnet:

```python
import aiorocket
api = aiorocket.Rocket('токен', testnet=True)
```

## 🚀 Методы

### Получение информации о приложении
[Документация](https://pay.ton-rocket.com/api/#/app/AppsController_getAppInfo)

Пример:
```python
await api.info()
```

### Перевод
Все параметры как в [документации](https://pay.ton-rocket.com/api/#/app/AppsController_transfer)

Пример:
```python
await api.send(
    tgUserId=1448705322,
    currency="TONCOIN",
    amount=0.123,
    description="Всем совятам привет!"
)
```

### Вывод

Все параметры как в [документации](https://pay.ton-rocket.com/api/#/app/AppsController_withdrawal)

Пример:
```python
await api.withdraw(
    address="EQAJkw0RC9s_FAEmKr4GftJsNbA0IK0o4cfEH3bNoSbKJHAy",
    currency="TONCOIN",
    amount=0.123,
    comment="Всем совятам привет!"
)
```

### Создание чека
Все параметры как в [документации](https://pay.ton-rocket.com/api/#/multi-cheques/ChequesController_createCheque)

Пример:
```python
cheque = await api.create_cheque({
    chequePerUser=0.005,
    usersNumber=100,
    refProgram=50,
    password="пароль :D",
    description="Чек для вас",
    sendNotifications=True,
    enableCaptcha=True,
    telegramResourcesIds=[
        "-1001799549067"
    ]
})
```

### Получение чеков
[Документация](https://pay.ton-rocket.com/api/#/multi-cheques/ChequesController_getCheques)

Пример:
```python
await api.get_cheques()
```

### Получение чека по ID
Все параметры как в [документации](https://pay.ton-rocket.com/api/#/multi-cheques/ChequesController_getCheque)

Пример:
```python
await api.get_cheque(1234)
```

### Удаление чека
Все параметры как в [документации](https://pay.ton-rocket.com/api/#/multi-cheques/ChequesController_deleteCheque)

Пример:
```python
await api.delete_cheque(1234)
# ИЛИ ТАК
await cheque.delete() # в стиле ООП
```

### Создание счёта
Все параметры как в [документации](https://pay.ton-rocket.com/api/#/tg-invoices/InvoicesController_createInvoice)

Пример:
```python
invoice = await api.createInvoice(
    amount=1.23,
    description="покупка лучшой вещи в мире",
    hiddenMessage="спасибо",
    callbackUrl="https://t.me/ton_rocket",
    payload="some payload",
    expiredIn=10
)
```

### Получение счетов
[Документация](https://pay.ton-rocket.com/api/#/tg-invoices/InvoicesController_deleteInvoice)

Пример:
```python
await api.get_invoices()
```

### Получение счёта по ID
Все параметры как в [документации](https://pay.ton-rocket.com/api/#/tg-invoices/InvoicesController_getInvoice)

Пример:
```python
await api.get_invoice(1234)
```

### Удаление счёта
Все параметры как в [документации](https://pay.ton-rocket.com/api/#/tg-invoices/InvoicesController_deleteInvoice)

Пример:
```python
await api.delete_invoice(1234)
# ИЛИ ТАК
await invoice.delete() # в стиле ООП
```

### Доступные валюты
[Документация](https://pay.ton-rocket.com/api/#/currencies/CurrenciesController_getCoins)

Пример:
```python
await api.available_currencies()
```

## ⚠ Обработка ошибок

```python
try:
    api.get_invoice(1234) # вызов метода
except aiorocket.classes.RocketAPIError as err:
    print(err.errors)
```

Результат:
```json
{
    "property": "somePropertyName",
    "error": "somePropertyName should be less than X"
}
```