#!/usr/bin/env python3
"""Numerical screening with explicit unknowns. This does not certify physical feasibility."""
import argparse,json,math,sys

def review(data):
    issues=[];unknown=[]
    def fail(check,frame,detail):issues.append({'check':check,'frame':frame,'detail':detail})
    def num(v):return isinstance(v,(int,float)) and not isinstance(v,bool) and math.isfinite(v)
    frames=data.get('frames',[])
    if not isinstance(frames,list) or not frames:
        return {'status':'fail','issues':[{'check':'schema','frame':None,'detail':'frames must be a nonempty array'}],'unknown':['physical_feasibility']}
    for k in ['angle_unit','handedness','frame_convention']:
        if not data.get(k):unknown.append(k)
    if data.get('angle_unit') not in (None,'deg','rad'):fail('schema',None,'angle_unit must be deg or rad')
    limits=data.get('joint_limits',{});speeds=data.get('max_joint_speed',{})
    if not limits:unknown.append('joint_limits')
    valid_limits={}
    for joint,bounds in limits.items():
        if not isinstance(bounds,list) or len(bounds)!=2 or not all(num(v) for v in bounds) or bounds[0]>bounds[1]:fail('schema',None,f'invalid joint limit: {joint}')
        else:valid_limits[joint]=bounds
    valid_speeds={}
    for joint,s in speeds.items():
        if not num(s) or s<=0:fail('schema',None,f'invalid speed limit: {joint}')
        else:valid_speeds[joint]=s
    if not speeds:unknown.append('joint_speed_limits')
    tol=data.get('bone_length_tolerance',.02)
    if not num(tol) or tol<0:fail('schema',None,'invalid bone_length_tolerance');tol=.02
    bone_ref={};prev=None;seen_bones=0;seen_quats=0;unlimited=set();max_speed={}
    for i,f in enumerate(frames):
        if not isinstance(f,dict):fail('schema',i,'frame must be an object');continue
        t=f.get('t');joints=f.get('joints',{})
        if not num(t):fail('timestamp',i,'time must be finite');prev=None;continue
        if not isinstance(joints,dict):fail('schema',i,'joints must be an object');joints={}
        for j,b in valid_limits.items():
            if j not in joints:fail('missing_joint',i,j)
        for j,v in joints.items():
            if not num(v):fail('finite',i,j);continue
            if j in valid_limits and not valid_limits[j][0]<=v<=valid_limits[j][1]:fail('joint_limit',i,f'{j}: {v}, expected {valid_limits[j]}')
            if j not in valid_limits:unlimited.add(j)
        if prev:
            dt=t-prev['t']
            if dt<=0:fail('timestamp',i,'timestamps must increase strictly')
            else:
                for j,v in joints.items():
                    pv=prev.get('joints',{}).get(j)
                    if num(v) and num(pv):
                        speed=abs(v-pv)/dt;max_speed[j]=max(speed,max_speed.get(j,0))
                        if j in valid_speeds and speed>valid_speeds[j]:fail('joint_speed',i,f'{j}: {speed} > {valid_speeds[j]}')
        bones=f.get('bone_lengths')
        if isinstance(bones,dict) and bones:
            seen_bones+=1
            if not bone_ref:bone_ref=bones.copy()
            for b,ref in bone_ref.items():
                v=bones.get(b)
                if not num(v) or v<=0 or not num(ref) or ref<=0:fail('bone_length',i,f'{b}: invalid or missing length')
                elif abs(v/ref-1)>tol:fail('bone_length',i,f'{b}: relative drift {abs(v/ref-1):.5f}')
        q=f.get('object_quaternion_wxyz')
        if q is not None:
            seen_quats+=1
            if not isinstance(q,list) or len(q)!=4 or not all(num(v) for v in q):fail('quaternion',i,'expected four finite values, wxyz')
            elif abs(math.sqrt(sum(v*v for v in q))-1)>1e-3:fail('quaternion',i,'quaternion not normalized')
        prev={'t':t,'joints':joints}
    if len(frames)<2:unknown.append('temporal_checks')
    if seen_bones<len(frames):unknown.append('bone_lengths_on_all_frames')
    if seen_quats<len(frames):unknown.append('object_quaternions_on_all_frames')
    if unlimited:unknown.append('limits_missing_for:'+','.join(sorted(unlimited)))
    unknown.extend(['action_fidelity','collision_geometry','contact_plausibility','physical_feasibility','between_sample_motion'])
    return {'status':'fail' if issues else 'pass_supplied_numerical_checks_only','frames':len(frames),'issues':issues,'unknown':unknown,'max_observed_joint_speed':max_speed}

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('input');args=parser.parse_args()
    try:
        with open(args.input,encoding='utf-8') as f:data=json.load(f)
        result=review(data)
    except (OSError,ValueError,TypeError,AttributeError) as e:result={'status':'fail','issues':[{'check':'input','detail':str(e)}],'unknown':['physical_feasibility']}
    print(json.dumps(result,ensure_ascii=False,indent=2));sys.exit(1 if result['status']=='fail' else 0)
