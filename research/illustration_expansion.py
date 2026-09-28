"""Attach only image-bound anatomy-approved teaching illustrations."""
import importlib.util
import json

def attach_illustrations(root, actions):
    manifest_path = root / 'research/illustration-manifest.json'
    plan_path = root / 'research/illustration-plan.json'
    plan = json.loads(plan_path.read_text()) if plan_path.exists() else {'items': []}
    records = json.loads(manifest_path.read_text())['records'] if manifest_path.exists() else []
    spec = importlib.util.spec_from_file_location('anatomy_gate', root / 'quality/hand-anatomy-reviewer/scripts/check_report.py')
    gate = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(gate)
    reports = {}
    for path in (root / 'quality/anatomy-reviews').glob('*.json'):
        report = json.loads(path.read_text())
        reports[report['asset']] = (report, path.relative_to(root).as_posix())
    by_id = {a['id']: a for a in actions}
    review_records = []
    for record in records:
        asset = root / record['path']
        report, report_path = reports.get(record['path'], ({}, None))
        errors = gate.validate_report(report, asset) if report else ['尚无逐帧形态检查报告']
        if report and (report.get('asset') != record['path'] or report.get('action_id') != record['action_id']):
            errors.append('图片或动作 ID 与检查报告不一致')
        if report.get('action_fidelity') and report['action_fidelity'].get('status') != 'pass':
            errors.append('关键姿态与动作匹配检查未通过或仍不确定')
        publish = record['status'] == 'approved' and report.get('decision') == 'approve' and not errors
        review_records.append(dict(action_id=record['action_id'], path=record['path'], anatomy=report.get('decision', 'pending'), action_review=record['status'], publishable=publish, report=report_path, errors=errors))
        if not publish:
            continue
        a = by_id[record['action_id']]
        a['illustration'] = dict(path=record['path'], label='AI 教学图', generator='built-in image_gen',
            caption=record.get('caption', '按本库动作描述生成的关键姿态示意；不是原研究图像或实际采集记录。'),
            review=record['review'], anatomy_report=report_path, anatomy_scope='已逐帧检查可见手形；单视图不能证明被遮挡几何或精确尺寸。',
            handedness=record.get('handedness', '见图'), sources=a['sources'], physics='unknown')
    audit = dict(version='1.0', candidates=len(plan['items']), approved=sum('illustration' in a for a in actions),
        generated=len({r['action_id'] for r in records}), records=review_records,
        scope='逐图、逐帧的可见手形检查；AI 示意不提高原动作的文献证据等级，未验证物理可行性。')
    audit['remaining'] = audit['candidates'] - audit['approved']
    (root / 'research/illustration-audit.json').write_text(json.dumps(audit, ensure_ascii=False, indent=2)+'\n')
    return audit
