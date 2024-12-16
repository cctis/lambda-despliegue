import React, { useState } from "react";
import axios from "axios";

function UpdatePedido() {
  const [id, setId] = useState("");
  const [detalle, setDetalle] = useState("");
  const [estado, setEstado] = useState("");
  const [mensaje, setMensaje] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    const pedidoActualizado = { detalle, estado };
    try {
      const response = await axios.put(`https://w7y87cphve.execute-api.us-east-1.amazonaws.com/develop/GestionPedidos/${id}`, pedidoActualizado);
      setMensaje(response.data.mensaje);
    } catch (error) {
      setMensaje("Error al actualizar el pedido.");
      console.error(error);
    }
  };

  return (
    <div className="update-pedido">
      <h2>Actualizar Pedido</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label>ID:</label>
          <input type="text" value={id} onChange={(e) => setId(e.target.value)} required />
        </div>
        <div>
          <label>Detalles:</label>
          <input type="text" value={detalle} onChange={(e) => setDetalle(e.target.value)} />
        </div>
        <div>
          <label>Estado:</label>
          <input type="text" value={estado} onChange={(e) => setEstado(e.target.value)} />
        </div>
        <button type="submit">Actualizar Pedido</button>
      </form>
      {mensaje && <p>{mensaje}</p>}
    </div>
  );
}

export default UpdatePedido;
