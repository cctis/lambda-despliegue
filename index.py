import boto3
import json

# Inicializar el cliente de DynamoDB
dynamodb = boto3.resource('dynamodb')
pedidos_table = dynamodb.Table('Pedidos')

def lambda_handler(event, context):
    # Imprimir el evento completo para ver qué contiene
    print("Evento completo recibido:", json.dumps(event))  # Muestra todo el evento
    
    # Obtener la clave de la ruta de la solicitud (routeKey)
    route_key = event.get('routeKey', '')
    print("RouteKey de la solicitud:", route_key)

    # Verificamos el valor de routeKey para determinar qué acción tomar
    if route_key == "GET /GestionPedidos/getbyid/{id}":
        return obtener_pedido_por_id(event)
    elif route_key == "GET /GestionPedidos/GetAll":
        return obtener_todos_pedidos()
    elif route_key == "POST /GestionPedidos/Save":
        return guardar_pedido(event)
    elif route_key == "PUT /GestionPedidos/{id}":
        return actualizar_pedido(event)
    elif route_key == "DELETE /GestionPedidos/{id}":
        return eliminar_pedido(event)
    else:
        # Ruta no soportada
        return {
            'statusCode': 404,
            'body': json.dumps({'mensaje': 'Ruta no soportada', 'routeKey': route_key})
        }

def obtener_todos_pedidos():
    try:
        # Recuperar todos los pedidos
        response = pedidos_table.scan()
        pedidos = response.get('Items', [])
        
        if not pedidos:
            return {
                'statusCode': 404,
                'body': json.dumps({'mensaje': 'No se encontraron pedidos'})
            }

        return {
            'statusCode': 200,
            'body': json.dumps({'mensaje': 'Pedidos recuperados con éxito', 'pedidos': pedidos})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'mensaje': f'Error al obtener pedidos: {str(e)}'})
        }

def guardar_pedido(event):
    try:
        body = json.loads(event['body'])
        Id = body.get('Id')
        detalle = body.get('detalle')
        estado = 'En preparación'  # Estado por defecto al guardar el pedido
        
        # Crear el pedido
        pedido = {
            'Id': Id,
            'detalle': detalle,
            'estado': estado
        }
        
        # Guardar en DynamoDB
        pedidos_table.put_item(Item=pedido)
        
        return {
            'statusCode': 200,
            'body': json.dumps({'mensaje': 'Pedido guardado con éxito', 'pedido': pedido})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'mensaje': f'Error al guardar el pedido: {str(e)}'})
        }

def obtener_pedido_por_id(event):
    try:
        # Obtener el ID de la ruta
        path_parameters = event.get('pathParameters', {})
        pedido_id = path_parameters.get('id')
        
        if not pedido_id:
            return {
                'statusCode': 400,
                'body': json.dumps({'mensaje': 'ID del pedido no proporcionado'})
            }
        
        # Buscar el pedido en DynamoDB por ID
        response = pedidos_table.get_item(Key={'Id': pedido_id})
        pedido = response.get('Item', None)
        
        if not pedido:
            return {
                'statusCode': 404,
                'body': json.dumps({'mensaje': 'Pedido no encontrado'})
            }

        return {
            'statusCode': 200,
            'body': json.dumps({'mensaje': 'Pedido recuperado con éxito', 'pedido': pedido})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'mensaje': f'Error al obtener el pedido: {str(e)}'})
        }

def actualizar_pedido(event):
    try:
        # Obtener el ID del pedido a actualizar de la ruta
        path_parameters = event.get('pathParameters', {})
        pedido_id = path_parameters.get('id')
        
        if not pedido_id:
            return {
                'statusCode': 400,
                'body': json.dumps({'mensaje': 'ID del pedido no proporcionado'})
            }
        
        # Obtener los datos del pedido a actualizar
        body = json.loads(event['body'])
        detalle = body.get('detalle')
        estado = body.get('estado')

        # Actualizar el pedido en DynamoDB
        update_expression = "SET detalle = :detalle, estado = :estado"
        expression_values = {
            ":detalle": detalle,
            ":estado": estado
        }

        response = pedidos_table.update_item(
            Key={'Id': pedido_id},
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_values,
            ReturnValues="UPDATED_NEW"
        )

        return {
            'statusCode': 200,
            'body': json.dumps({'mensaje': 'Pedido actualizado con éxito', 'pedido': response['Attributes']})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'mensaje': f'Error al actualizar el pedido: {str(e)}'})
        }

def eliminar_pedido(event):
    try:
        # Obtener el ID del pedido a eliminar de la ruta
        path_parameters = event.get('pathParameters', {})
        pedido_id = path_parameters.get('id')
        
        if not pedido_id:
            return {
                'statusCode': 400,
                'body': json.dumps({'mensaje': 'ID del pedido no proporcionado'})
            }

        # Eliminar el pedido de DynamoDB
        response = pedidos_table.delete_item(Key={'Id': pedido_id})
        
        return {
            'statusCode': 200,
            'body': json.dumps({'mensaje': 'Pedido eliminado con éxito'})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'mensaje': f'Error al eliminar el pedido: {str(e)}'})
        }
