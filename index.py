import boto3
import json

# Inicializar el cliente de DynamoDB
dynamodb = boto3.resource('dynamodb')
pedidos_table = dynamodb.Table('Pedidos')

def lambda_handler(event, context):
    try:
        # Registrar el evento para depuración
        print("Evento recibido:", json.dumps(event))

        # Verificar el método HTTP
        http_method = event.get('httpMethod')
        if http_method == 'GET':
            return obtener_pedidos()
        elif http_method == 'POST':
            return crear_pedido(event)
        elif http_method == 'PUT':
            return actualizar_pedido(event)
        elif http_method == 'DELETE':
            return eliminar_pedido(event)
        else:
            return {
                'statusCode': 405,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                },
                'body': json.dumps({'mensaje': f'Método {http_method} no permitido'})
            }
    except Exception as e:
        print(f"Error interno: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
            },
            'body': json.dumps({'mensaje': f'Error interno: {str(e)}'})
        }

# Obtener todos los pedidos
def obtener_pedidos():
    response = pedidos_table.scan()
    pedidos = response.get('Items', [])
    if not pedidos:
        return {
            'statusCode': 404,
            'headers': {
                'Access-Control-Allow-Origin': '*',
            },
            'body': json.dumps({'mensaje': 'No se encontraron pedidos'})
        }
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
        },
        'body': json.dumps({'pedidos': pedidos})
    }

# Crear un nuevo pedido
def crear_pedido(event):
    body = json.loads(event.get('body', '{}'))
    if 'Id' not in body or 'detalle' not in body:
        return {
            'statusCode': 400,
            'headers': {
                'Access-Control-Allow-Origin': '*',
            },
            'body': json.dumps({'mensaje': 'Faltan campos obligatorios: Id y detalle'})
        }
    pedido = {
        'Id': body['Id'],
        'detalle': body['detalle'],
        'estado': body.get('estado', 'Pendiente')  # Estado por defecto
    }
    pedidos_table.put_item(Item=pedido)
    return {
        'statusCode': 201,
        'headers': {
            'Access-Control-Allow-Origin': '*',
        },
        'body': json.dumps({'mensaje': 'Pedido creado exitosamente', 'pedido': pedido})
    }

# Actualizar un pedido
def actualizar_pedido(event):
    body = json.loads(event.get('body', '{}'))
    if 'Id' not in body or 'estado' not in body:
        return {
            'statusCode': 400,
            'headers': {
                'Access-Control-Allow-Origin': '*',
            },
            'body': json.dumps({'mensaje': 'Faltan campos obligatorios: Id y estado'})
        }
    pedido_id = body['Id']
    nuevo_estado = body['estado']
    pedidos_table.update_item(
        Key={'Id': pedido_id},
        UpdateExpression="SET estado = :estado",
        ExpressionAttributeValues={':estado': nuevo_estado}
    )
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
        },
        'body': json.dumps({'mensaje': 'Pedido actualizado exitosamente'})
    }

# Eliminar un pedido
def eliminar_pedido(event):
    body = json.loads(event.get('body', '{}'))
    if 'Id' not in body:
        return {
            'statusCode': 400,
            'headers': {
                'Access-Control-Allow-Origin': '*',
            },
            'body': json.dumps({'mensaje': 'Faltan campos obligatorios: Id'})
        }
    pedido_id = body['Id']
    pedidos_table.delete_item(Key={'Id': pedido_id})
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
        },
        'body': json.dumps({'mensaje': 'Pedido eliminado exitosamente'})
    }
