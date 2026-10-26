from cargar_csv import load_fixture
from app.domain import InvalidOrderTransition

# Cargar los datos en memoria
orders = load_fixture()
order = orders["O013"]

print(f"Estado inicial: {order.status}, Unidades: {order.units}, Total: {order.total.amount}")

# Primera confirmacion (Transicion valida)
order.confirm()
print(f"Estado tras confirmar: {order.status}, Eventos: {[e.name for e in order.events]}")

# Segunda confirmacion (Transicion invalida)
try:
    order.confirm()
except InvalidOrderTransition as exc:
    print(f"Excepcion capturada correctamente: {exc}")