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
api = aiorocket.Rocket('токен', True)
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
    tgUserId=87209764,
    currency="TONCOIN",
    amount=1.23,
    description="Hello, Owls!"
)
```

### Вывод

Все параметры как в [документации](https://pay.ton-rocket.com/api/#/app/AppsController_withdrawal)

Пример:
```python
await api.withdraw(
    address="EQAJkw0RC9s_FAEmKr4GftJsNbA0IK0o4cfEH3bNoSbKJHAy",
    currency="TONCOIN",
    amount=1.23,
    comment="Hello, Owls!"
)
```

### Создание чека
Все параметры как в [документации](https://pay.ton-rocket.com/api/#/multi-cheques/ChequesController_createCheque)

Пример:
```python
api.create_cheque({
    chequePerUser=0.005,
    usersNumber=100,
    refProgram=50,
    password="pwd",
    description="This cheque is the best",
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

### Получение чека
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
```

### Создание счёта
Все параметры как в [документации](https://pay.ton-rocket.com/api/#/tg-invoices/InvoicesController_createInvoice)

Пример:
```python
await api.createInvoice(
    amount=1.23,
    description="best thing in the world, 1 item",
    hiddenMessage="thank you",
    callbackUrl="https://t.me/ton_rocket",
    payload="some custom payload I want to see in webhook or when I request invoice",
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
```

### Доступные валюты
[Документация](https://pay.ton-rocket.com/api/#/currencies/CurrenciesController_getCoins)

Пример:
```python
await api.available_currencies()
```