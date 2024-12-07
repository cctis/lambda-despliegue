import boto3
import json

# Inicializar el cliente de DynamoDB
dynamodb = boto3.resource('dynamodb')
pedidos_table = dynamodb.Table('Pedidos')

def lambda_handler(event, context):
    try:
        # Obtener la ruta del evento
        path = event['path']
        
        # Gestionar rutas de acuerdo a la estructura
        if path == "/GestionPedidos":
            if event.get('body'):  # Si hay cuerpo, es un POST
                return crear_pedido(event)
            else:  # Si no hay cuerpo, es un GET
                return obtener_pedidos()
        
        elif path.startswith("/GestionPedidos/"):
            id_pedido = path.split("/")[-1]  # Obtener el ID desde la URL
            if event.get('body'):  # Si hay cuerpo, es un PUT
                return actualizar_pedido(event, id_pedido)
            else:  # Si no hay cuerpo, es un DELETE
                return eliminar_pedido(id_pedido)

        else:
            return {
                'statusCode': 404,
                'body': json.dumps({'mensaje': 'Ruta no encontrada'})
            }

    except Exception as e:
        print(f"Error interno: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'mensaje': f'Error interno: {str(e)}'})
        }

# Función para obtener todos los pedidos (GET)
def obtener_pedidos():
    try:
        response = pedidos_table.scan()
        pedidos = response.get('Items', [])

        if not pedidos:
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'mensaje': 'No se encontraron pedidos.',
                    'pedidos': []
                })
            }

        return {
            'statusCode': 200,
            'body': json.dumps({
                'mensaje': 'Pedidos obtenidos con éxito.',
                'pedidos': pedidos
            })
        }

    except Exception as e:
        print(f"Error al obtener los pedidos: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'mensaje': f'Error interno: {str(e)}'})
        }

# Función para crear un nuevo pedido (POST)
def crear_pedido(event):
    body = json.loads(event['body'])
    Id = body.get('Id')
    detalle = body.get('detalle')

    try:
        pedido = {
            'Id': Id,
            'estado': 'En preparación',  # Estado inicial
            'detalle': detalle
        }

        pedidos_table.put_item(Item=pedido)

        return {
            'statusCode': 200,
            'body': json.dumps({
                'mensaje': 'Pedido guardado con éxito.',
                'pedido': pedido
            })
        }

    except Exception as e:
        print(f"Error al crear el pedido: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'mensaje': f'Error interno: {str(e)}'})
        }

# Función para actualizar un pedido (PUT)
def actualizar_pedido(event, id_pedido):
    body = json.loads(event['body'])
    nuevo_estado = body.get('estado')

    try:
        pedidos_table.update_item(
            Key={'Id': id_pedido},
            UpdateExpression="SET estado = :estado",
            ExpressionAttributeValues={':estado': nuevo_estado}
        )

        return {
            'statusCode': 200,
            'body': json.dumps({'mensaje': 'Pedido actualizado con éxito.'})
        }

    except Exception as e:
        print(f"Error al actualizar el pedido: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'mensaje': f'Error interno: {str(e)}'})
        }

# Función para eliminar un pedido (DELETE)
def eliminar_pedido(id_pedido):
    try:
        pedidos_table.delete_item(Key={'Id': id_pedido})

        return {
            'statusCode': 200,
            'body': json.dumps({'mensaje': f'Pedido con ID {id_pedido} eliminado con éxito.'})
        }

    except Exception as e:
        print(f"Error al eliminar el pedido: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'mensaje': f'Error interno: {str(e)}'})
        }
