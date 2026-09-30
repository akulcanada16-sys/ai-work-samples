"""The same transport-independent request contract runs locally and in Lambda."""
import hashlib
import json
import uuid
from pathlib import Path
from .vision import Calibration, decode_image, inspect

WEB = Path(__file__).resolve().parent.parent / 'web'
MAX_BODY = 2_200_000


def analyze(payload):
    if not isinstance(payload, dict) or set(payload) - {'image', 'calibration'}:
        raise ValueError('Provide image and calibration only')
    calibration = Calibration.parse(payload.get('calibration', {}))
    frame, raw = decode_image(payload.get('image'))
    result = inspect(frame, calibration)
    result['inspection_id'] = uuid.uuid4().hex
    result['input_sha256'] = hashlib.sha256(raw).hexdigest()
    result['calibration'] = calibration.__dict__
    return result


def parse_request(body):
    if len(body) > MAX_BODY:
        raise ValueError('Request too large')
    try:
        return json.loads(body)
    except (ValueError, UnicodeDecodeError) as exc:
        raise ValueError('Request must contain JSON') from exc
