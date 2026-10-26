from decimal import Decimal
from cargar_csv import load_fixture
from app.specifications import ten_percent, five_percent
from app.domain import OrderItem, Money

# Cargar los datos frescos en memoria
orders = load_fixture()

print("--- BITÁCORA DE ESCENARIOS (E01 - E15) ---\n")

# E01 a E02: Evaluaciones de descuentos
print(f"E01 (O001 - VIP 4 unidades): ¿Aplica 10%? -> {ten_percent.is_satisfied_by(orders['O001'])}")
print(f"E02 (O002 - No VIP): ¿Aplica 10%? -> {ten_percent.is_satisfied_by(orders['O002'])}")

# E03 a E04: Clientes inactivos
for eid, oid in [("E03", "O003"), ("E04", "O004")]:
    try:
        orders[oid].confirm()
    except Exception as e:
        print(f"{eid} ({oid} - Cliente inactivo): Bloqueado -> {type(e).__name__}: {e}")

# E05 a E06: Más descuentos
print(f"E05 (O005 - Promoción activa): ¿Aplica 10%? -> {ten_percent.is_satisfied_by(orders['O005'])}")
print(f"E06 (O006 - >5000 MXN sin promo): ¿Aplica 5%? -> {five_percent.is_satisfied_by(orders['O006'])}")

# E07: Pedido vacío
try:
    orders['O007'].confirm()
except Exception as e:
    print(f"E07 (O007 - Pedido vacío): Bloqueado -> {type(e).__name__}: {e}")

# E08: Frontera 20 unidades
try:
    orders['O008'].confirm()
    print(f"E08 (O008 - 20 unidades exactas): Éxito -> Estado cambiado a {orders['O008'].status.value}")
except Exception as e:
    print(f"E08 (O008): {e}")

# E09: Superar 20 unidades
try:
    item_extra = OrderItem(sku="TEST", quantity=2, unit_price=Money(Decimal("100")))
    orders['O009'].add_item(item_extra)
except Exception as e:
    print(f"E09 (O009 - Superar límite 20): Bloqueado -> {type(e).__name__}: {e}")

# E10 a E11: Fronteras de Specification
print(f"E10 (O010 - Total exactamente 500): ¿Aplica 10%? -> {ten_percent.is_satisfied_by(orders['O010'])}")
print(f"E11 (O011 - VIP solo 3 unidades): ¿Aplica 10%? -> {ten_percent.is_satisfied_by(orders['O011'])}")

# E12: Guía vacía
try:
    orders['O012'].confirm()
    orders['O012'].ship("")
except Exception as e:
    print(f"E12 (O012 - Enviar sin guía): Bloqueado -> {type(e).__name__}: {e}")

# E13: Confirmar doble
try:
    orders['O013'].confirm()
    orders['O013'].confirm()
except Exception as e:
    print(f"E13 (O013 - Confirmar dos veces): Bloqueado -> {type(e).__name__}: {e}")

# E14: Transición inválida (Cancelar después de enviar)
try:
    orders['O014'].confirm()
    orders['O014'].ship("TRACK123")
    orders['O014'].cancel("Motivo X")
except Exception as e:
    print(f"E14 (O014 - Cancelar desde SHIPPED): Bloqueado -> {type(e).__name__}: {e}")

# E15: Transición válida (Devolución)
try:
    orders['O015'].confirm()
    orders['O015'].ship("TRACK123")
    orders['O015'].return_order()
    print(f"E15 (O015 - Devolución desde SHIPPED): Éxito -> Estado final {orders['O015'].status.value}, Eventos: {[e.name for e in orders['O015'].events]}")
except Exception as e:
    print(f"E15 (O015): {e}")