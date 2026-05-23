import logging
from zeep import Client
from zeep.plugins import HistoryPlugin
from lxml import etree

# Логгирование
logging.basicConfig(level=logging.INFO)
logging.getLogger('zeep.transports').setLevel(logging.DEBUG)

# История сообщений
history = HistoryPlugin()

# URL WSDL
wsdl_url = "http://localhost:8000/?wsdl"

# Клиент с плагином
client = Client(wsdl=wsdl_url, plugins=[history])

# Данные запроса
shiporder_data = {
    "orderid": "12345",
    "orderperson": "Иван Петров",
    "shipto": {
        "name": "Петр Иванов",
        "address": "ул. Ленина",
        "city": "Москва",
        "country": "Россия"
    },
    "items": {
        "Item": [
            {
                "title": "Ручка гелевая",
                "note": "Цвет: черный",
                "quantity": 10,
                "price": 25.00
            },
            {
                "title": "Калькулятор",
                "quantity": 5,
                "price": 350.00
            }
        ]
    }
}

# Вызов метода
response = client.service.Shiporder(**shiporder_data)

# Печать сырого SOAP-запроса и ответа
print("SOAP Request:")
print(etree.tostring(history.last_sent["envelope"], pretty_print=True, encoding="unicode"))

# Печать полученного SOAP-ответа
print("\nSOAP Response:")
print(etree.tostring(history.last_received["envelope"], pretty_print=True, encoding="unicode"))

# Результат
print("\nParsed Response:")
print(response)