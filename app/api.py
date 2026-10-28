from fastapi import FastAPI, HTTPException
from cargar_csv import load_fixture
from app.domain import InvalidOrderTransition, InvalidOrderData

app = FastAPI(title="TechStore U4")

# Cargar datos en memoria al iniciar
orders = load_fixture()

@app.get("/orders/{order_id}")
def get_order(order_id: str):
    order = orders.get(order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="No existe")
    return {
        "id": order.id,
        "status": order.status.value,
        "units": order.units,
        "total": float(order.total.amount)
    }

@app.post("/orders/{order_id}/confirm")
def confirm_order(order_id: str):
    order = orders.get(order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="El pedido no existe")
    try:
        order.confirm()
    except InvalidOrderTransition as exc:
        raise HTTPException(status_code=409, detail=str(exc))
    except InvalidOrderData as exc:
        raise HTTPException(status_code=422, detail=str(exc))
    return {"id": order.id, "status": order.status.value, "mensaje": "Pedido confirmado exitosamente"}

@app.post("/orders/{order_id}/ship")
def ship_order(order_id: str, tracking_number: str):
    order = orders.get(order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="No existe")
    try:
        order.ship(tracking_number)
    except InvalidOrderTransition as exc:
        raise HTTPException(status_code=409, detail=str(exc))
    except InvalidOrderData as exc:
        raise HTTPException(status_code=422, detail=str(exc))
    return {"id": order.id, "status": order.status.value}

@app.post("/orders/{order_id}/cancel")
def cancel_order(order_id: str, reason: str):
    order = orders.get(order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="No existe")
    try:
        order.cancel(reason)
    except InvalidOrderTransition as exc:
        raise HTTPException(status_code=409, detail=str(exc))
    except InvalidOrderData as exc:
        raise HTTPException(status_code=422, detail=str(exc))
    return {"id": order.id, "status": order.status.value}