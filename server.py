from spyne import Application, rpc, ServiceBase, Iterable, Unicode, Decimal
from spyne.model.complex import ComplexModel
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from wsgiref.simple_server import make_server
from spyne.model.primitive import Integer, String
from spyne.model import XmlAttribute


# Определение объекта Shipto
class Shipto(ComplexModel):
    name = String(min_occurs=1, nillable=False)
    address = String(min_occurs=1, nillable=False)
    city = String(min_occurs=1, nillable=False)
    country = String(min_occurs=1, nillable=False)

# Определение объекта Item
class Item(ComplexModel):
    title = String(min_occurs=1, nillable=False)
    note = String(nillable=False)
    quantity = Integer(min_occurs=1, nillable=False)
    price = Decimal(min_occurs=1, nillable=False)

# Определение атрибутов объектов
Orderperson = String(min_occurs=1, nillable=False)
Shipto = Shipto.customize(min_occurs=1, nillable=False)
Item = Item.customize(min_occurs=1, nillable=False)
Items = Iterable(Item, min_occurs=1, nillable=False)
Orderid = XmlAttribute(Integer, use="required")

# Сервис
class OrderService(ServiceBase):
    @rpc(Orderid, Orderperson, Shipto, Items, _returns=Unicode(min_occurs=1, nillable=False))
    def Shiporder(ctx, orderid, orderperson, shipto, items):
        return f"Заказ успешно обработан. ID: {orderid}"

# Создание приложения
app = Application(
    [OrderService],
    'my.namespace',
    in_protocol=Soap11(validator='schema'),  
    out_protocol=Soap11()
)

wsgi_app = WsgiApplication(app)

# Запуск сервера
if __name__ == '__main__':
    server = make_server('0.0.0.0', 8000, wsgi_app)
    print('For WSDL type http://localhost:8000/?wsdl')
    server.serve_forever()