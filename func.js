const fdk = require("@fnproject/fdk");
const axios = require("axios");

// CAMBIAR: poner la URL del API Gateway de AWS del microservicio de pedidos
// Ejemplo: https://abc123.execute-api.us-east-1.amazonaws.com/dev
const AWS_URL = process.env.AWS_ORDERS_URL;

fdk.handle(async function(input) {

  const { clientName, address, items, phone } = input;

  if (!clientName) {
    return { status: 400, message: "Falta el nombre del cliente (clientName)" };
  }

  if (!items || items.length === 0) {
    return { status: 400, message: "El pedido no tiene productos (items)" };
  }

  const orderPayload = {
    clientName,
    address: address || "Recojo en tienda",
    phone: phone || "",
    items,
    source: "rappi",
    // CAMBIAR: poner el tenantId del restaurante que corresponda al grupo
    tenantId: "madam-tusan"
  };

  try {
    const response = await axios.post(`${AWS_URL}/orders`, orderPayload, {
      headers: { "Content-Type": "application/json" },
      timeout: 10000
    });

    return {
      status: 200,
      message: "Pedido enviado al restaurante correctamente",
      // AWS debe responder con el orderId generado
      orderId: response.data.orderId,
      estimatedTime: "30-45 minutos"
    };

  } catch (error) {
    return {
      status: 500,
      message: "No se pudo enviar el pedido al restaurante",
      detail: error.message
    };
  }

});