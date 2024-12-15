import React, { useState } from "react";
import PedidoList from "./components/PedidoList";
import SavePedido from "./components/SavePedido";
import UpdatePedido from "./components/UpdatePedido";
import DeletePedido from "./components/DeletePedido";
import './App.css';

function App() {
  const [currentView, setCurrentView] = useState("list");

  const renderView = () => {
    switch (currentView) {
      case "list":
        return <PedidoList />;
      case "save":
        return <SavePedido />;
      case "update":
        return <UpdatePedido />;
      case "delete":
        return <DeletePedido />;
      default:
        return <PedidoList />;
    }
  };

  return (
    <div className="App">
      <h1>Gestión de Pedidos</h1>
      <nav>
        <button onClick={() => setCurrentView("list")}>Ver Pedidos</button>
        <button onClick={() => setCurrentView("save")}>Crear Pedido</button>
        <button onClick={() => setCurrentView("update")}>Actualizar Pedido</button>
        <button onClick={() => setCurrentView("delete")}>Eliminar Pedido</button>
      </nav>

      {renderView()}
    </div>
  );
}

export default App;
