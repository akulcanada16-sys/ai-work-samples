"""Exercise a running local or AWS endpoint; access code comes from the environment."""
import argparse
import base64
import json
import os
import urllib.error
import urllib.request


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('url',nargs='?',default='http://127.0.0.1:8080')
    args=parser.parse_args()
    url=args.url.rstrip('/')
    def get(path):return urllib.request.urlopen(url+path,timeout=30).read()
    health=json.loads(get('/health'))
    assert health['opencv_version'].startswith('5.')
    assert b'DialGuard' in get('/') and b'Inspect this dial' in get('/')
    for name,expected in [('clean','READ'),('high','REVIEW'),('blur','RETAKE'),('ambiguous','RETAKE'),('missing','RETAKE'),('dim','RETAKE')]:
        payload={'image':base64.b64encode(get('/sample/'+name)).decode(),'calibration':{'review_above':80}}
        req=urllib.request.Request(url+'/api/inspect',data=json.dumps(payload).encode(),
             headers={'Content-Type':'application/json','X-DialGuard-Token':os.getenv('DIALGUARD_TOKEN','')})
        result=json.loads(urllib.request.urlopen(req,timeout=30).read())
        assert result['status']==expected,(name,result['status'])
        assert result['annotated_image'] and result['trace'][-1]['status']==expected
        if expected=='RETAKE':assert result['reading'] is None
        else:assert abs(result['reading']-(90 if name=='high' else 62))<1.2
        print(json.dumps({'sample':name,'status':result['status'],'reading':result['reading'],
                          'mode':health['mode'],'opencv_version':result['opencv_version']}))
    print('HTTP end-to-end smoke passed')

if __name__=='__main__':main()
