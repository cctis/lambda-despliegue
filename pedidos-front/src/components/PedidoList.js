import React, { useState, useEffect } from "react";
import axios from "axios";

function PedidoList() {
  const [pedidos, setPedidos] = useState([]);
  const [mensaje, setMensaje] = useState("");

  useEffect(() => {
    const obtenerPedidos = async () => {
      try {
        const response = await axios.get("https://w7y87cphve.execute-api.us-east-1.amazonaws.com/develop/GestionPedidos/GetAll");
        if (response.data.pedidos) {
          setPedidos(response.data.pedidos);
        } else {
          setMensaje("No se encontraron pedidos.");
        }
      } catch (error) {
        setMensaje("Hubo un error al obtener los pedidos.");
        console.error(error);
      }
    };

    obtenerPedidos();
  }, []);

  return (
    <div className="pedido-list">
      <h2>Lista de Pedidos 1111</h2>
      {mensaje && <p>{mensaje}</p>}
      {pedidos.length > 0 && (
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Estado</th>
              <th>Detalles</th>
            </tr>
          </thead>
          <tbody>
            {pedidos.map((pedido) => (
              <tr key={pedido.Id}>
                <td>{pedido.Id}</td>
                <td>{pedido.estado}</td>
                <td>{pedido.detalle}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

export default PedidoList;
