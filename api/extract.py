import json

def handler(request):
    return {
        "statusCode": 200,
        "body": json.dumps({"hello": "world"})
    }
