import React, { useState } from "react";
import axios from "axios";

function DeletePedido() {
  const [id, setId] = useState("");
  const [mensaje, setMensaje] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.delete(`https://w7y87cphve.execute-api.us-east-1.amazonaws.com/develop/GestionPedidos/${id}`);
      setMensaje(response.data.mensaje);
    } catch (error) {
      setMensaje("Error al eliminar el pedido.");
      console.error(error);
    }
  };

  return (
    <div className="delete-pedido">
      <h2>Eliminar Pedido</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label>ID:</label>
          <input type="text" value={id} onChange={(e) => setId(e.target.value)} required />
        </div>
        <button type="submit">Eliminar Pedido</button>
      </form>
      {mensaje && <p>{mensaje}</p>}
    </div>
  );
}

export default DeletePedido;
