"""Validate a human/model visual review record, NOT anatomy from image pixels."""
import argparse
import hashlib
import json
from pathlib import Path

DIGITS = {'thumb', 'index', 'middle', 'ring', 'little'}
CHECKS = {'five_digits', 'connectivity', 'proportions', 'joint_structure', 'handedness', 'framing'}
STATES = {'pass', 'fail', 'unknown'}

def validate_report(report, asset):
    if not isinstance(report, dict):
        return ['report must be a JSON object']
    try:
        return _validate_report(report, asset)
    except (TypeError, AttributeError, KeyError, ValueError) as error:
        return ['malformed review structure: ' + str(error)]

def _validate_report(report, asset):
    errors, states = [], []
    def require(condition, message):
        if not condition:
            errors.append(message)
    def box(value, where):
        require(isinstance(value, list) and len(value) == 4 and
                all(isinstance(n, (int, float)) and not isinstance(n, bool) and 0 <= n <= 1 for n in value)
                and value[0] < value[2] and value[1] < value[3], where + ': invalid bbox')
    require(report.get('version') == '1.0', 'unsupported report version')
    require(asset.is_file(), 'asset missing')
    if asset.is_file():
        require(hashlib.sha256(asset.read_bytes()).hexdigest() == report.get('sha256'), 'image hash mismatch')
    for key in ('asset', 'action_id', 'reviewer', 'limitations'):
        require(isinstance(report.get(key), str) and bool(report[key].strip()), 'missing ' + key)
    n = report.get('expected_panels')
    panels = report.get('panels', [])
    require(isinstance(n, int) and not isinstance(n, bool) and n > 0, 'invalid panel count')
    require(isinstance(panels, list) and len(panels) == n, 'incomplete panel coverage')
    expected_hands = report.get('expected_hands_per_panel', [])
    require(isinstance(expected_hands, list) and len(expected_hands) == n and all(isinstance(v, int) and not isinstance(v, bool) and v > 0 for v in expected_hands), 'invalid hand coverage')
    if not isinstance(panels, list):
        return errors + ['panels must be a list']
    require([p.get('panel') for p in panels] == list(range(1, len(panels)+1)), 'panels must be unique and ordered')
    for i, p in enumerate(panels):
        prefix = f'panel {i+1}'
        box(p.get('bbox'), prefix)
        hands = p.get('hands', [])
        require(i < len(expected_hands) and len(hands) == expected_hands[i], prefix + ': incomplete hands')
        require(len({h.get('hand_id') for h in hands}) == len(hands), prefix + ': duplicated hand id')
        for h in hands:
            where = prefix + ' ' + str(h.get('hand_id'))
            box(h.get('bbox'), where)
            require(h.get('side') in {'left', 'right', 'unknown'}, where + ': invalid side')
            for key in ('hand_id', 'view', 'count_observation', 'length_observation', 'joint_observation'):
                require(isinstance(h.get(key), str) and len(h[key].strip()) >= 2, where + ': missing ' + key)
            digits = h.get('digits', {})
            require(set(digits) == DIGITS, where + ': five named digit traces required')
            for name, digit in digits.items():
                require(digit.get('visibility') in {'visible', 'traceable', 'unresolvable'}, where + ': invalid visibility ' + name)
                require(isinstance(digit.get('trace'), str) and len(digit['trace'].strip()) > 5, where + ': missing digit trace ' + name)
            checks = h.get('checks', {})
            require(set(checks) == CHECKS and set(checks.values()) <= STATES, where + ': incomplete checks')
            states.extend(checks.values())
            issues = h.get('issues', [])
            for key, status in checks.items():
                if status != 'pass':
                    require(any(issue.get('check') == key and all(issue.get(k) for k in ('code', 'evidence', 'correction')) for issue in issues), where + ': missing issue for ' + key)
            if any(d.get('visibility') == 'unresolvable' for d in digits.values()):
                require(checks.get('five_digits') != 'pass', where + ': unresolved digit cannot pass count')
            if h.get('side') == 'unknown':
                require(checks.get('handedness') != 'pass', where + ': unknown side cannot pass')
    sequence = report.get('sequence', {})
    require(sequence.get('status') in STATES and bool(sequence.get('observation')), 'missing sequence review')
    states.append(sequence.get('status'))
    if sequence.get('status') != 'pass':
        require(bool(sequence.get('issues')), 'sequence issue required')
    decision = 'reject' if 'fail' in states else 'needs_review' if 'unknown' in states else 'approve'
    require(report.get('decision') == decision, 'decision must agree with required checks: ' + decision)
    return errors

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('report', type=Path)
    parser.add_argument('--asset', type=Path, required=True)
    args = parser.parse_args()
    report = json.loads(args.report.read_text())
    errors = validate_report(report, args.asset)
    result = {'record_valid': not errors, 'decision': report.get('decision'),
              'publishable': not errors and report.get('decision') == 'approve', 'errors': errors,
              'scope': 'Report integrity only. Visual anatomy must be reviewed by an image-capable agent.'}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(1 if errors else 0)

if __name__ == '__main__':
    main()
