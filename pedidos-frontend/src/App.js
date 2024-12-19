import React, { useState, useEffect } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [pedidos, setPedidos] = useState([]);
  const [detalle, setDetalle] = useState("");
  const [estado, setEstado] = useState("");
  const [idEdicion, setIdEdicion] = useState(null);
  const [mensaje, setMensaje] = useState("");

  // Obtener lista de pedidos
  const obtenerPedidos = async () => {
    try {
      const response = await axios.get(
        "https://w7y87cphve.execute-api.us-east-1.amazonaws.com/develop/GestionPedidos/GetAll"
      );
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

  useEffect(() => {
    obtenerPedidos();
  }, []);

  // Mostrar mensaje temporal
  const mostrarMensajeTemporal = (mensaje) => {
    setMensaje(mensaje);
    setTimeout(() => {
      setMensaje("");
    }, 3000); // Mensaje visible durante 3 segundos
  };

  // Guardar o actualizar pedido
  const handleSubmit = async (e) => {
    e.preventDefault();

    if (idEdicion) {
      // Actualizar pedido
      try {
        const pedidoActualizado = { detalle, estado };
        const response = await axios.put(
          `https://w7y87cphve.execute-api.us-east-1.amazonaws.com/develop/GestionPedidos/${idEdicion}`,
          pedidoActualizado
        );
        mostrarMensajeTemporal(response.data.mensaje);
        obtenerPedidos();
        limpiarFormulario();
      } catch (error) {
        mostrarMensajeTemporal("Error al actualizar el pedido.");
        console.error(error);
      }
    } else {
      // Crear nuevo pedido
      try {
        const nuevoPedido = { detalle, estado };
        const response = await axios.post(
          "https://w7y87cphve.execute-api.us-east-1.amazonaws.com/develop/GestionPedidos/Save",
          nuevoPedido
        );
        mostrarMensajeTemporal(response.data.mensaje);
        obtenerPedidos();
        limpiarFormulario();
      } catch (error) {
        mostrarMensajeTemporal("Error al guardar el pedido.");
        console.error(error);
      }
    }
  };

  // Eliminar pedido
  const handleDelete = async (id) => {
    try {
      const response = await axios.delete(
        `https://w7y87cphve.execute-api.us-east-1.amazonaws.com/develop/GestionPedidos/${id}`
      );
      mostrarMensajeTemporal(response.data.mensaje);
      obtenerPedidos();
    } catch (error) {
      mostrarMensajeTemporal("Error al eliminar el pedido.");
      console.error(error);
    }
  };

  // Preparar formulario para edición
  const handleEdit = (pedido) => {
    setIdEdicion(pedido.Id);
    setDetalle(pedido.detalle);
    setEstado(pedido.estado);
  };

  // Limpiar formulario
  const limpiarFormulario = () => {
    setIdEdicion(null);
    setDetalle("");
    setEstado("");
  };

  return (
    <div className="App">
      <h1>Gestión de Pedidos</h1>
      {mensaje && <div className="mensaje">{mensaje}</div>}

      <form onSubmit={handleSubmit}>
        <h2>{idEdicion ? "Editar Pedido" : "Crear Pedido"}</h2>
        <div>
          <label>Detalles:</label>
          <input
            type="text"
            value={detalle}
            onChange={(e) => setDetalle(e.target.value)}
            required
          />
        </div>
        <div>
          <label>Estado:</label>
          <input
            type="text"
            value={estado}
            onChange={(e) => setEstado(e.target.value)}
            required
          />
        </div>
        <div className="form-buttons">
          <button type="submit">{idEdicion ? "Actualizar" : "Guardar"}</button>
          {idEdicion && <button type="button" onClick={limpiarFormulario}>Cancelar</button>}
        </div>
      </form>

      <h2>Lista de Pedidos</h2>
      {pedidos.length > 0 ? (
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Detalles</th>
              <th>Estado</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            {pedidos.map((pedido) => (
              <tr key={pedido.Id}>
                <td>{pedido.Id}</td>
                <td>{pedido.detalle}</td>
                <td>{pedido.estado}</td>
                <td>
                  <button onClick={() => handleEdit(pedido)}>Editar</button>
                  <button onClick={() => handleDelete(pedido.Id)}>
                    Eliminar
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      ) : (
        <p>No hay pedidos disponibles.</p>
      )}
    </div>
  );
}

export default App;
