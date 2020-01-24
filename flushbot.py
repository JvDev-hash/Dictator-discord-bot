import aiohttp
import json
import numpy as np
import subprocess as sb
import boto3

dynamodb = boto3.resource('dynamodb')

# Flush configurations to DynamoDB database on AWS
# Check if server name has spaces and if this server already have a record on DB
def flush_config(serverName, open_dict):

    if ' ' in serverName:
        serverName = serverName.replace(" ", "_")
    
    table = dynamodb.Table(serverName)
    try:
        table = dynamodb.create_table(
            TableName=serverName,
            KeySchema=[
                {
                    'AttributeName': 'channel', 
                    'KeyType': 'HASH'
                }
            ], 
            AttributeDefinitions=[
                {
                    'AttributeName': 'channel', 
                    'AttributeType': 'S'
                }, 
            ], 
            ProvisionedThroughput={
                'ReadCapacityUnits': 1, 
                'WriteCapacityUnits': 1
            }
        )

        table.meta.client.get_waiter('table_exists').wait(TableName=serverName)

        table = dynamodb.Table(serverName)

        print(open_dict)

        table.put_item(
            Item = open_dict
            )

    except dynamodb.meta.client.exceptions.ResourceInUseException:
        table = dynamodb.Table(serverName)

        print(open_dict)

        table.put_item(
            Item = open_dict
            )        