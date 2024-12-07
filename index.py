import boto3
import json
import uuid

# Inicializar el cliente de DynamoDB
dynamodb = boto3.resource('dynamodb')
pedidos_table = dynamodb.Table('Pedidos')

def lambda_handler(event, context):
    try:
        http_method = event['httpMethod']
        
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
                'body': json.dumps({'mensaje': 'Método no permitido'})
            }
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'mensaje': f'Error interno del servidor: {str(e)}'})
        }

def obtener_pedidos():
    response = pedidos_table.scan()
    pedidos = response.get('Items', [])
    return {
        'statusCode': 200,
        'body': json.dumps({'mensaje': 'Pedidos recuperados', 'pedidos': pedidos}),
        'headers': {'Access-Control-Allow-Origin': '*'}
    }

def crear_pedido(event):
    data = json.loads(event['body'])
    pedido_id = str(uuid.uuid4())
    nuevo_pedido = {
        'Id': pedido_id,
        'estado': data.get('estado', 'pendiente'),
        'detalle': data.get('detalle', 'Sin detalles')
    }
    pedidos_table.put_item(Item=nuevo_pedido)
    return {
        'statusCode': 201,
        'body': json.dumps({'mensaje': 'Pedido creado', 'pedido': nuevo_pedido}),
        'headers': {'Access-Control-Allow-Origin': '*'}
    }

def actualizar_pedido(event):
    data = json.loads(event['body'])
    pedido_id = data.get('Id')
    if not pedido_id:
        return {
            'statusCode': 400,
            'body': json.dumps({'mensaje': 'ID del pedido es requerido'}),
            'headers': {'Access-Control-Allow-Origin': '*'}
        }
    update_expression = "SET estado = :estado, detalle = :detalle"
    expression_values = {
        ':estado': data.get('estado', 'pendiente'),
        ':detalle': data.get('detalle', 'Sin detalles')
    }
    pedidos_table.update_item(
        Key={'Id': pedido_id},
        UpdateExpression=update_expression,
        ExpressionAttributeValues=expression_values
    )
    return {
        'statusCode': 200,
        'body': json.dumps({'mensaje': 'Pedido actualizado'}),
        'headers': {'Access-Control-Allow-Origin': '*'}
    }

def eliminar_pedido(event):
    data = json.loads(event['body'])
    pedido_id = data.get('Id')
    if not pedido_id:
        return {
            'statusCode': 400,
            'body': json.dumps({'mensaje': 'ID del pedido es requerido'}),
            'headers': {'Access-Control-Allow-Origin': '*'}
        }
    pedidos_table.delete_item(Key={'Id': pedido_id})
    return {
        'statusCode': 200,
        'body': json.dumps({'mensaje': 'Pedido eliminado'}),
        'headers': {'Access-Control-Allow-Origin': '*'}
    }
