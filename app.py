"""Authenticated, owner-scoped IT service request API for API Gateway HTTP API v2."""
import json
import logging
import os
import uuid
from datetime import datetime, timezone

import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
_TABLE = None
ALLOWED_CATEGORIES = {'network', 'hardware', 'software', 'account', 'other'}
ALLOWED_PRIORITIES = {'low', 'medium', 'high'}
ALLOWED_STATUSES = {'open', 'in_progress', 'resolved'}


def table():
    global _TABLE
    if _TABLE is None:
        _TABLE = boto3.resource('dynamodb').Table(os.environ['TABLE_NAME'])
    return _TABLE


def response(status, data):
    return {'statusCode': status, 'headers': {'content-type': 'application/json',
            'cache-control': 'no-store'}, 'body': json.dumps(data)}


def parse_json(event):
    try:
        value = json.loads(event.get('body') or '{}')
        if not isinstance(value, dict):
            raise ValueError('JSON object required')
        return value
    except (ValueError, TypeError) as exc:
        raise ValueError('Body must be a valid JSON object') from exc


def validate_create(body):
    title = body.get('title')
    description = body.get('description')
    category = body.get('category', 'other')
    priority = body.get('priority', 'medium')
    if not isinstance(title, str) or not (3 <= len(title.strip()) <= 120):
        raise ValueError('title must be 3 to 120 characters')
    if not isinstance(description, str) or not (5 <= len(description.strip()) <= 2000):
        raise ValueError('description must be 5 to 2000 characters')
    if category not in ALLOWED_CATEGORIES:
        raise ValueError('invalid category')
    if priority not in ALLOWED_PRIORITIES:
        raise ValueError('invalid priority')
    return {'title': title.strip(), 'description': description.strip(),
            'category': category, 'priority': priority}


def handler(event, context):
    claims = (event.get('requestContext', {}).get('authorizer', {})
              .get('jwt', {}).get('claims', {}))
    owner = claims.get('sub')
    if not owner:
        return response(401, {'error': 'unauthorized'})

    method = event.get('requestContext', {}).get('http', {}).get('method', '')
    request_id = (event.get('pathParameters') or {}).get('requestId')
    try:
        if method == 'POST' and not request_id:
            fields = validate_create(parse_json(event))
            now = datetime.now(timezone.utc).isoformat()
            item = {'ownerId': owner, 'requestId': str(uuid.uuid4()), **fields,
                    'status': 'open', 'createdAt': now, 'updatedAt': now}
            table().put_item(Item=item)
            logger.info('request_created id=%s', item['requestId'])
            return response(201, item)

        if method == 'GET' and not request_id:
            result = table().query(KeyConditionExpression=Key('ownerId').eq(owner), Limit=50)
            return response(200, {'items': result.get('Items', []),
                                  'nextKey': result.get('LastEvaluatedKey')})

        if method == 'GET' and request_id:
            item = table().get_item(Key={'ownerId': owner, 'requestId': request_id}).get('Item')
            return response(200, item) if item else response(404, {'error': 'not found'})

        if method == 'PATCH' and request_id:
            body = parse_json(event)
            status = body.get('status')
            if set(body) != {'status'} or status not in ALLOWED_STATUSES:
                raise ValueError('only status=open|in_progress|resolved may be updated')
            result = table().update_item(
                Key={'ownerId': owner, 'requestId': request_id},
                UpdateExpression='SET #s=:s, updatedAt=:t',
                ConditionExpression='attribute_exists(ownerId) AND attribute_exists(requestId)',
                ExpressionAttributeNames={'#s': 'status'},
                ExpressionAttributeValues={':s': status, ':t': datetime.now(timezone.utc).isoformat()},
                ReturnValues='ALL_NEW')
            logger.info('request_updated id=%s', request_id)
            return response(200, result['Attributes'])

        return response(404, {'error': 'route not found'})
    except ValueError as exc:
        return response(400, {'error': str(exc)})
    except ClientError as exc:
        if exc.response.get('Error', {}).get('Code') == 'ConditionalCheckFailedException':
            return response(404, {'error': 'not found'})
        logger.exception('AWS service error')
        return response(500, {'error': 'internal server error'})
    except Exception:
        logger.exception('unexpected error')
        return response(500, {'error': 'internal server error'})
