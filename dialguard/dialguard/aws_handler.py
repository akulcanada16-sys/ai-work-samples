"""AWS performs the OpenCV workload and writes opt-in derived evidence to S3."""
import base64
import hmac
import json
import os
from .app import MAX_BODY, WEB, analyze, parse_request
from .fixtures import make_dial
import cv2


def response(code, data, mime='application/json', binary=False):
    body = base64.b64encode(data).decode() if binary else (
        data.decode() if isinstance(data,bytes) else json.dumps(data, allow_nan=False))
    return {'statusCode':code, 'headers':{'Content-Type':mime, 'Cache-Control':'no-store',
            'X-Content-Type-Options':'nosniff','Referrer-Policy':'no-referrer'},
            'body':body,'isBase64Encoded':binary}


def handler(event, context):
    method = event.get('requestContext',{}).get('http',{}).get('method','')
    path = event.get('rawPath','/')
    routes = {'/':('index.html','text/html; charset=utf-8'), '/app.js':('app.js','text/javascript'),
              '/style.css':('style.css','text/css')}
    if method == 'GET':
        if path in routes:
            name,mime = routes[path]
            return response(200,(WEB/name).read_bytes(),mime)
        if path == '/health':
            return response(200,{'ok':True,'opencv_version':cv2.__version__,'mode':'aws'})
        if path.startswith('/sample/'):
            condition=path.split('/')[-1]
            if condition in ('clean','blur','ambiguous','missing','dim','noise','high'):
                img=make_dial(90 if condition=='high' else 62,condition=condition)
                return response(200,cv2.imencode('.png',img)[1].tobytes(),'image/png',True)
        return response(404,{'error':'Not found'})
    if method != 'POST' or path != '/api/inspect':
        return response(404,{'error':'Not found'})
    headers = {k.lower():v for k,v in event.get('headers',{}).items()}
    token = os.environ.get('DIALGUARD_TOKEN','')
    if not token or not hmac.compare_digest(headers.get('x-dialguard-token',''),token):
        return response(401,{'error':'Invalid demo access code'})
    try:
        body=event.get('body','')
        if len(body) > MAX_BODY * 1.4:
            return response(413,{'error':'Request too large'})
        if event.get('isBase64Encoded'):
            body=base64.b64decode(body,validate=True)
        result=analyze(parse_request(body))
        # Persist derived evidence only if the operator configured retention.
        bucket=os.environ.get('EVIDENCE_BUCKET')
        if bucket:
            import boto3
            evidence={k:v for k,v in result.items() if k!='annotated_image'}
            boto3.client('s3').put_object(Bucket=bucket,
                Key=f"inspections/{result['inspection_id']}.json",
                Body=json.dumps(evidence,allow_nan=False).encode(),
                ContentType='application/json',ServerSideEncryption='AES256')
            result['evidence_retained_days']=7
        print(json.dumps({'inspection_id':result['inspection_id'],'status':result['status'],
                          'latency_ms':result['latency_ms'],'opencv_version':result['opencv_version']}))
        return response(200,result)
    except (ValueError,TypeError) as exc:
        return response(400,{'error':str(exc)})
    except Exception:
        print(json.dumps({'event':'inspection_failed'}))
        return response(500,{'error':'Inspection failed; no reading recorded'})
