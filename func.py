import io
import json
import os
import requests
import fdk
from fdk import response

AWS_URL = os.environ.get("AWS_ORDERS_URL", "https://vdwa84epn1.execute-api.us-east-1.amazonaws.com/dev/pedidos")

def handler(ctx, data: io.BytesIO = None):

    try:
        body = json.loads(data.getvalue())
    except Exception:
        return response.Response(
            ctx,
            response_data=json.dumps({"status": 400, "mensaje": "Body inválido"}),
            headers={"Content-Type": "application/json"}
        )

    cliente     = body.get("cliente", {})
    items       = body.get("items", [])
    monto_total = body.get("monto_total", 0.0)

    if not items:
        return response.Response(
            ctx,
            response_data=json.dumps({"status": 400, "mensaje": "Faltan items del pedido"}),
            headers={"Content-Type": "application/json"}
        )

    if not cliente.get("nombre"):
        return response.Response(
            ctx,
            response_data=json.dumps({"status": 400, "mensaje": "Falta nombre del cliente"}),
            headers={"Content-Type": "application/json"}
        )

    payload = {
        "tenant_id":   "madam-tusan",  
        "origen":      "RAPPI",        
        "cliente": {
            "nombre":    cliente.get("nombre"),
            "direccion": cliente.get("direccion", "Sin dirección"),
            "telefono":  cliente.get("telefono", "")
        },
        "items":       items,          
        "monto_total": monto_total
    }

    try:
        res = requests.post(
            f"{AWS_URL}",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=10
        )

        data_aws = res.json()

        return response.Response(
            ctx,
            response_data=json.dumps({
                "status":    200,
                "mensaje":   "Pedido enviado al restaurante correctamente",
                "pedido_id": data_aws.get("pedido_id"),
                "tenant_id": data_aws.get("tenant_id")
            }),
            headers={"Content-Type": "application/json"}
        )

    except Exception as e:
        return response.Response(
            ctx,
            response_data=json.dumps({
                "status":  500,
                "mensaje": "Error al conectar con AWS",
                "detalle": str(e)
            }),
            headers={"Content-Type": "application/json"}
        )


if __name__ == "__main__":
    fdk.handle(handler)
