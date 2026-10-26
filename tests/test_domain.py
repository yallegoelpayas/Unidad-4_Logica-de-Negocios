import pytest
from decimal import Decimal
from app.domain import Money, InvalidOrderData, InvalidOrderTransition, OrderItemLimitExceeded, OrderItem
from app.specifications import ten_percent
from cargar_csv import load_fixture

def test_money_negativo():
    with pytest.raises(InvalidOrderData):
        Money(Decimal("-1"))

def test_pedido_0001_inicia_draft():
    orders = load_fixture()
    assert orders["O001"].status.value == "DRAFT"
    assert orders["O001"].units == 4
    assert orders["O001"].total.amount == Decimal("2100.00")

def test_limite_21_unidades_bloqueado():
    orders = load_fixture()
    order = orders["O009"] # Ya tiene 19 unidades
    item_extra = OrderItem(sku="SKUTEST", quantity=2, unit_price=Money(Decimal("100")))
    with pytest.raises(OrderItemLimitExceeded):
        order.add_item(item_extra)

def test_cliente_inactivo_no_puede_confirmar():
    orders = load_fixture()
    with pytest.raises(InvalidOrderData):
        orders["O003"].confirm()

def test_pedido_vacio_no_puede_confirmar():
    orders = load_fixture()
    with pytest.raises(InvalidOrderData):
        orders["O007"].confirm()

def test_descuento_vip_aplicado():
    orders = load_fixture()
    assert ten_percent.is_satisfied_by(orders["O001"]) == True

def test_promocion_activa_excluye_descuento():
    orders = load_fixture()
    assert ten_percent.is_satisfied_by(orders["O005"]) == False

def test_envio_sin_guia_rechazado():
    orders = load_fixture()
    order = orders["O012"]
    order.confirm()
    with pytest.raises(InvalidOrderData):
        order.ship("")

def test_confirmacion_doble_rechazada():
    orders = load_fixture()
    order = orders["O013"]
    order.confirm()
    with pytest.raises(InvalidOrderTransition):
        order.confirm()

def test_cancelacion_desde_shipped_rechazada():
    orders = load_fixture()
    order = orders["O014"]
    order.confirm()
    order.ship("TRACK123")
    with pytest.raises(InvalidOrderTransition):
        order.cancel("Motivo de prueba")