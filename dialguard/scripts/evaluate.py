"""Frozen procedural benchmark. No training, no field-validation claims."""
import hashlib
import json
import platform
from pathlib import Path
import sys
import time
ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT))
import cv2
import numpy as np
from dialguard.fixtures import make_dial
from dialguard.vision import Calibration, inspect, hough_baseline, angle_distance


def main():
    rows=[]
    # Seeded evaluation angles deliberately differ from interactive 62/90 samples.
    rng=np.random.default_rng(20260930)
    for condition,count in [('clean',40),('noise',40),('blur',12),('dim',12),('missing',12),('ambiguous',12)]:
        for i in range(count):
            value=float(rng.uniform(2,98))
            seed=int(rng.integers(10000,99999))
            frame=make_dial(value,seed,condition)
            result=inspect(frame,Calibration())
            baseline=hough_baseline(cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY),np.array([256,256]),.4*512)
            truth=(135+value/100*270)%360
            row={'condition':condition,'seed':seed,'truth':round(value,6),'status':result['status'],
                 'reading':result['reading'],'latency_ms':result['latency_ms'],
                 'input_sha256':hashlib.sha256(frame.tobytes()).hexdigest(),
                 'error':None if result['reading'] is None else abs(result['reading']-value),
                 'baseline_error_degrees':None if baseline is None else angle_distance(baseline,truth)}
            rows.append(row)
    readable=[r for r in rows if r['condition'] in ('clean','noise')]
    invalid=[r for r in rows if r['condition'] not in ('clean','noise')]
    accepted=[r for r in readable if r['reading'] is not None]
    errors=[r['error'] for r in accepted]
    by_condition={}
    for condition in sorted({r['condition'] for r in rows}):
        subset=[r for r in rows if r['condition']==condition]
        by_condition[condition]={'n':len(subset),'readings':sum(r['reading'] is not None for r in subset),
                                'retakes':sum(r['status']=='RETAKE' for r in subset)}
    source_files=sorted((ROOT/'dialguard').glob('*.py'))
    source_sha=hashlib.sha256(b''.join(p.name.encode()+p.read_bytes() for p in source_files)).hexdigest()
    report={'kind':'procedural_fixture_benchmark_not_field_validation','seed':20260930,
            'opencv_version':cv2.__version__,'numpy_version':np.__version__,'python_version':platform.python_version(),
            'machine':platform.machine(),'processor':platform.processor(),'source_sha256':source_sha,
            'n':len(rows),'readable_n':len(readable),'invalid_n':len(invalid),
            'accepted_readable_n':len(accepted),'coverage':len(accepted)/len(readable),
            'mae_scale_units':float(np.mean(errors)) if errors else None,
            'max_error_scale_units':max(errors) if errors else None,
            'invalid_false_accept_n':sum(r['reading'] is not None for r in invalid),
            'latency_ms_p50':float(np.median([r['latency_ms'] for r in rows])),
            'latency_ms_p95':float(np.percentile([r['latency_ms'] for r in rows],95)),
            'baseline_detected_readable_n':sum(r['baseline_error_degrees'] is not None for r in readable),
            'baseline_mae_degrees_detected':float(np.mean([r['baseline_error_degrees'] for r in readable if r['baseline_error_degrees'] is not None])),
            'baseline_mae_scale_units_detected':float(np.mean([r['baseline_error_degrees'] for r in readable if r['baseline_error_degrees'] is not None]))/270*100,
            'baseline_invalid_detections_n':sum(r['baseline_error_degrees'] is not None for r in invalid),
            'by_condition':by_condition,'cases':rows,
            'limitations':['Synthetic renderer and known calibration; no natural-image generalization demonstrated.',
                           'Noise/blur parameters and gates are development choices, not independently validated thresholds.',
                           'Timing is local warm-process timing, excludes transport, AWS cold starts and S3 writes.',
                           'Primary and baseline errors must be compared in the same units; 270 degrees = 100 scale units.']}
    (ROOT/'evidence'/'benchmark.json').write_text(json.dumps(report,indent=2)+'\n')
    for condition in ('clean','blur','ambiguous','high'):
        value=90 if condition=='high' else 62
        result=inspect(make_dial(value,condition=condition),Calibration(review_above=80))
        import base64
        (ROOT/'evidence'/f'{condition}.jpg').write_bytes(base64.b64decode(result['annotated_image']))
    print(json.dumps({k:v for k,v in report.items() if k!='cases'},indent=2))

if __name__=='__main__':main()
