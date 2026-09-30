"""One exploratory real-photo failure case; deliberately not a benchmark."""
import base64
import hashlib
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT))
import cv2
from dialguard.vision import Calibration,inspect

photo=ROOT/'evidence'/'air-pressure-gauge-tokino.jpg'
raw=photo.read_bytes()
assert hashlib.sha1(raw).hexdigest()=='5c7ee0b63603f387170fbb7a25142ee6d3fd14ae'
c=Calibration(cx=417/640,cy=254/480,radius=105/480,minimum=0,maximum=400,start_deg=90,sweep_deg=270,unit='kPa')
r=inspect(cv2.imread(str(photo)),c)
image=r.pop('annotated_image')
r.update({'kind':'exploratory_photo_not_ground_truth_validation','calibration':c.__dict__,
          'truth':None,'source':'https://commons.wikimedia.org/wiki/File:Air_pressure_gauge.jpg',
          'author':'Tokino','license':'Public domain (PD-self)','input_sha256':hashlib.sha256(raw).hexdigest(),
          'limitations':['Manually estimated exploratory calibration, not verified instrument calibration.',
                         'Tilted photo outside supported frontal-image scope.',
                         'Rejected because estimate falls outside this configured scale, not because perspective was automatically detected.',
                         'No reference reading or numeric accuracy claim.']})
(ROOT/'evidence'/'exploratory-photo.json').write_text(json.dumps(r,indent=2)+'\n')
(ROOT/'evidence'/'exploratory-photo-annotated.jpg').write_bytes(base64.b64decode(image))
print('Exploratory photo:',r['status'],r['reasons'])
