import boto3
import json


# Inicializar el cliente de DynamoDB
dynamodb = boto3.resource('dynamodb')
pedidos_table = dynamodb.Table('Pedidos')

def lambda_handler(event, context):
    try:
        # Escanear todos los pedidos en la tabla
        response = pedidos_table.scan()
        
        # Obtener los pedidos de la respuesta
        pedidos = response.get('Items', [])
        
        # Si no hay pedidos, devolver un mensaje adecuado
        if not pedidos:
            return {
                'statusCode': 404,
                'headers': {
                    'Access-Control-Allow-Origin': '*',  # Habilitar CORS
                    'Access-Control-Allow-Methods': 'GET'
                },
                'body': json.dumps({'mensaje': 'No se encontraron pedidos'})
            }

        # Respuesta exitosa con todos los pedidos
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',  # Habilitar CORS
                'Access-Control-Allow-Methods': 'GET'
            },
            'body': json.dumps({
                'mensaje': 'Pedidos recuperados con éxito',
                'pedidos': pedidos
            })
        }

    except Exception as e:
        # Manejar errores generales
        print(f"Error al obtener los pedidos: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',  # Habilitar CORS
                'Access-Control-Allow-Methods': 'GET'
            },
            'body': json.dumps({'mensaje': f'Error al obtener los pedidos: {str(e)}'})
        }
