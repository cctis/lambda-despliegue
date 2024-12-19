Sistema de Gestión de Pedidos con AWS
Este proyecto es una solución serverless diseñada para gestionar pedidos de una manera eficiente y escalable. Aprovecha los servicios de AWS para integrar el backend, frontend y despliegues automatizados.

Descripción del Proyecto
El objetivo del proyecto es proporcionar una aplicación web funcional donde los clientes puedan:

Crear pedidos ingresando sus datos.
Visualizar el estado de sus pedidos en tiempo real.
El sistema también está diseñado para que el equipo logístico pueda gestionar y actualizar los estados de los pedidos.

Este sistema se construyó utilizando una arquitectura serverless, asegurando escalabilidad y costos bajos, y cuenta con un pipeline CI/CD para automatizar los despliegues.

Arquitectura del Proyecto
Backend
AWS Lambda: Gestiona la lógica del negocio para la creación, actualización y consulta de pedidos.
API Gateway: Expone los endpoints RESTful para que el frontend pueda interactuar con el backend.
DynamoDB: Almacena los datos de los pedidos, diseñado para consultas rápidas y eficiente escalabilidad.
Frontend
React: Diseñado para ser responsivo e intuitivo, incluye:
Formulario para crear pedidos.
Visualización en tiempo real del estado de los pedidos.
Pipeline CI/CD
GitHub Actions:
Automatiza el despliegue del código para funciones Lambda, configuración de API Gateway y el frontend.
Incluye notificaciones de fallos para garantizar tiempos de respuesta rápidos.
Requisitos Previos
Antes de ejecutar el proyecto, asegúrate de tener:

Cuenta de AWS: Configurada con los servicios necesarios (API Gateway, Lambda, DynamoDB, S3 para el frontend).
Node.js: Para ejecutar y construir el frontend.
AWS CLI: Configurado en tu máquina para gestionar los despliegues.
GitHub Actions: Para el pipeline CI/CD (o alternativa como AWS CodePipeline).
Instrucciones de Ejecución
1. Backend
a. Configuración de DynamoDB
Crea una tabla en DynamoDB con:
Clave de partición: pedidoId (tipo: String).
Configura las políticas de acceso necesarias para Lambda.
b. Implementación de Funciones Lambda
Implementa las funciones Lambda para:
Crear pedidos.
Consultar el estado de pedidos.
Actualizar el estado de pedidos.
Vincula las funciones a los endpoints en API Gateway.
2. Frontend
2. Frontend
Clona el repositorio:
bash
Copiar código
git clone <URL-del-repositorio>
cd <carpeta-del-repositorio>
Instala las dependencias:
bash
Copiar código
npm install
Configura las variables de entorno en un archivo .env con la URL de los endpoints de API Gateway.
Inicia la aplicación localmente:
bash
Copiar código
npm start
3. Pipeline CI/CD
Configura un archivo .yml para GitHub Actions que:
Construya el código.
Despliegue las funciones Lambda, API Gateway y el frontend.
Asegúrate de tener las credenciales de AWS configuradas en GitHub Secrets.
Diagrama de Arquitectura
plaintext
Copiar código
[Frontend (React)] <-> [API Gateway] <-> [Lambda Functions] <-> [DynamoDB]
                  |------------------------ AWS Cloud -----------------------|
Características Clave
Arquitectura Serverless: Aprovecha la escalabilidad automática de AWS Lambda y DynamoDB.
Actualización en Tiempo Real: Los pedidos se crean y actualizan de forma inmediata.
Automatización de Despliegues: Un pipeline CI/CD garantiza actualizaciones rápidas y sin interrupciones.
Monitoreo Activo: Métricas y alarmas configuradas en CloudWatch aseguran la continuidad del servicio.
Tecnologías Utilizadas
Frontend: React
Backend:
AWS Lambda
API Gateway
DynamoDB
CI/CD: GitHub Actions
Infraestructura: AWS CloudFormation (opcional para IaC)
