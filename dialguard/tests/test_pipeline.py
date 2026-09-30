import base64
import json
import math
from unittest.mock import patch, MagicMock
import cv2
import numpy as np
import pytest
from dialguard.app import analyze
from dialguard.aws_handler import handler
from dialguard.fixtures import make_dial
from dialguard.vision import Calibration, inspect


def payload(value=62,condition='clean'):
    frame=make_dial(value,condition=condition)
    return {'image':base64.b64encode(cv2.imencode('.png',frame)[1]).decode(),'calibration':{'review_above':80}}


@pytest.mark.parametrize('value',[3,15,30,50,62,79,90,97])
def test_reads_known_angles(value):
    result=analyze(payload(value))
    assert result['status']==('REVIEW' if value>=80 else 'READ')
    assert abs(result['reading']-value)<1.2
    assert result['opencv_version'].startswith('5.')
    assert result['trace'][-2]['tool']=='verify_candidate'
    assert result['annotated_image']


@pytest.mark.parametrize('condition',['blur','dim','missing','ambiguous'])
def test_bad_evidence_requests_recapture(condition):
    result=analyze(payload(condition=condition))
    assert result['status']=='RETAKE'
    assert result['reading'] is None
    assert result['action']=='request_new_photo'
    assert result['reasons']


def test_image_changes_subsequent_action():
    assert analyze(payload(62))['action']=='record_reading'
    assert analyze(payload(90))['action']=='request_human_review'
    assert analyze(payload(condition='blur'))['trace']==[
        analyze(payload(condition='blur'))['trace'][0],
        {'tool':'decision','status':'RETAKE','action':'request_new_photo'}]


@pytest.mark.parametrize('data',[{'radius':float('nan')},{'maximum':0},{'cx':True},{'sweep_deg':360},{'unit':'a'*25},{'unknown':1}])
def test_invalid_calibration(data):
    with pytest.raises(ValueError):Calibration.parse(data)


@pytest.mark.parametrize('image',['bad','',base64.b64encode(b'GIF89a').decode()])
def test_invalid_images(image):
    with pytest.raises(ValueError):analyze({'image':image})


def test_circle_must_fit_image():
    p=payload();p['calibration']['cx']=.1
    with pytest.raises(ValueError):analyze(p)


def test_out_of_scale_is_not_clamped_into_a_reading():
    p=payload(50);p['calibration'].update(start_deg=20,sweep_deg=40)
    assert analyze(p)['reading'] is None


def event(body=None, token='secret', path='/api/inspect',method='POST'):
    return {'rawPath':path,'requestContext':{'http':{'method':method}},
            'headers':{'X-DialGuard-Token':token},'body':json.dumps(payload() if body is None else body)}


def test_lambda_closed_without_access_code():
    with patch.dict('os.environ',{},clear=True):
        assert handler(event(),None)['statusCode']==401


def test_lambda_analysis_and_derived_s3_evidence():
    s3=MagicMock()
    with patch.dict('os.environ',{'DIALGUARD_TOKEN':'secret','EVIDENCE_BUCKET':'test-evidence'}),patch('boto3.client',return_value=s3):
        result=handler(event(),None)
    assert result['statusCode']==200
    response=json.loads(result['body'])
    assert abs(response['reading']-62)<1.2
    saved=json.loads(s3.put_object.call_args.kwargs['Body'])
    assert 'image' not in saved and 'annotated_image' not in saved
    assert saved['input_sha256']==response['input_sha256']
    assert s3.put_object.call_args.kwargs['ServerSideEncryption']=='AES256'


def test_lambda_denies_bad_code_and_does_not_store():
    with patch.dict('os.environ',{'DIALGUARD_TOKEN':'secret'}):
        assert handler(event(token='wrong'),None)['statusCode']==401
        assert handler(event(body={'image':'bad'}),None)['statusCode']==400


def test_lambda_health_and_static_ui():
    assert json.loads(handler(event(path='/health',method='GET'),None)['body'])['mode']=='aws'
    assert '<title>DialGuard' in handler(event(path='/',method='GET'),None)['body']


def test_storage_failure_does_not_claim_success():
    s3=MagicMock();s3.put_object.side_effect=RuntimeError('fake unavailable')
    with patch.dict('os.environ',{'DIALGUARD_TOKEN':'secret','EVIDENCE_BUCKET':'test'}),patch('boto3.client',return_value=s3):
        assert handler(event(),None)['statusCode']==500
