import boto3
import json
import uuid

# Inicializar el cliente de DynamoDB
dynamodb = boto3.resource('dynamodb')
pedidos_table = dynamodb.Table('Pedidos')

def lambda_handler(event, context):
    try:
        # Obtener el método HTTP
        method = event['httpMethod']

        # Rutas según el método
        if method == 'GET':
            pedido_id = event.get('pathParameters', {}).get('id')
            if pedido_id:
                # Obtener un pedido específico
                response = pedidos_table.get_item(Key={'Id': pedido_id})
                pedido = response.get('Item')
                if not pedido:
                    return {
                        'statusCode': 404,
                        'headers': {'Access-Control-Allow-Origin': '*'},
                        'body': json.dumps({'mensaje': f'Pedido con ID {pedido_id} no encontrado'})
                    }
                return {
                    'statusCode': 200,
                    'headers': {'Access-Control-Allow-Origin': '*'},
                    'body': json.dumps({'mensaje': 'Pedido recuperado', 'pedido': pedido})
                }
            else:
                # Obtener todos los pedidos
                response = pedidos_table.scan()
                pedidos = response.get('Items', [])
                return {
                    'statusCode': 200,
                    'headers': {'Access-Control-Allow-Origin': '*'},
                    'body': json.dumps({'mensaje': 'Pedidos recuperados', 'pedidos': pedidos})
                }

        elif method == 'POST':
            # Crear un nuevo pedido
            body = json.loads(event['body'])
            nuevo_pedido = {
                'Id': str(uuid.uuid4()),  # ID único
                'estado': body['estado'],
                'detalle': body['detalle']
            }
            pedidos_table.put_item(Item=nuevo_pedido)
            return {
                'statusCode': 201,
                'headers': {'Access-Control-Allow-Origin': '*'},
                'body': json.dumps({'mensaje': 'Pedido creado', 'pedido': nuevo_pedido})
            }

        elif method == 'PUT':
            # Actualizar un pedido existente
            pedido_id = event.get('pathParameters', {}).get('id')
            if not pedido_id:
                return {
                    'statusCode': 400,
                    'headers': {'Access-Control-Allow-Origin': '*'},
                    'body': json.dumps({'mensaje': 'Se requiere un ID para actualizar el pedido'})
                }
            body = json.loads(event['body'])
            pedidos_table.update_item(
                Key={'Id': pedido_id},
                UpdateExpression="set #e = :e, #d = :d",
                ExpressionAttributeNames={'#e': 'estado', '#d': 'detalle'},
                ExpressionAttributeValues={':e': body['estado'], ':d': body['detalle']}
            )
            return {
                'statusCode': 200,
                'headers': {'Access-Control-Allow-Origin': '*'},
                'body': json.dumps({'mensaje': f'Pedido con ID {pedido_id} actualizado'})
            }

        elif method == 'DELETE':
            # Eliminar un pedido
            pedido_id = event.get('pathParameters', {}).get('id')
            if not pedido_id:
                return {
                    'statusCode': 400,
                    'headers': {'Access-Control-Allow-Origin': '*'},
                    'body': json.dumps({'mensaje': 'Se requiere un ID para eliminar el pedido'})
                }
            pedidos_table.delete_item(Key={'Id': pedido_id})
            return {
                'statusCode': 200,
                'headers': {'Access-Control-Allow-Origin': '*'},
                'body': json.dumps({'mensaje': f'Pedido con ID {pedido_id} eliminado'})
            }

        else:
            return {
                'statusCode': 405,
                'headers': {'Access-Control-Allow-Origin': '*'},
                'body': json.dumps({'mensaje': 'Método no permitido'})
            }

    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'mensaje': f'Error interno: {str(e)}'})
        }
