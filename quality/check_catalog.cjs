const fs=require('fs'),path=require('path'),root=path.resolve(__dirname,'..');
global.window={THREE:require(path.join(root,'vendor/three.min.js'))};
require(path.join(root,'hand.js'));
const data=JSON.parse(fs.readFileSync(path.join(root,'research/catalog.json'),'utf8'));
const failures=[];function check(ok,message){if(!ok)failures.push(message)}
const ids=new Set();for(const a of data.actions){check(!ids.has(a.id),'duplicate '+a.id);ids.add(a.id);check(a.sources.length>0,'missing source '+a.id);for(const s of a.sources)check(!!data.sources[s],'unknown source '+s);for(const p of a.primitives)check(data.primitives.some(x=>x.id===p),'unknown primitive '+p);for(const p of a.props)check(data.props.some(x=>x.id===p),'unknown prop '+p);check(!!data.media[a.media],'missing media '+a.id);check(!!a.locator&&!!a.mediaScope,'missing provenance '+a.id);if(a.id.startsWith('J'))check(fs.existsSync(path.join(root,'assets/joints',a.id+'.png')),'missing joint asset '+a.id);if(a.id.startsWith('G'))check(fs.existsSync(path.join(root,'assets/feix','grasp-'+a.id.slice(1)+'.png')),'missing grasp asset '+a.id)}
// Generated illustrations must retain the exact image-bound visual approval.
const crypto=require('crypto');
for(const a of data.actions.filter(a=>a.illustration)){
 const i=a.illustration,asset=path.join(root,i.path),reportPath=path.join(root,i.anatomy_report);
 check(fs.existsSync(asset)&&fs.existsSync(reportPath),'missing illustration/review '+a.id);
 if(!fs.existsSync(asset)||!fs.existsSync(reportPath))continue;
 const r=JSON.parse(fs.readFileSync(reportPath,'utf8'));
 check(r.decision==='approve'&&r.action_id===a.id&&r.asset===i.path,'unapproved illustration '+a.id);
 check(r.sha256===crypto.createHash('sha256').update(fs.readFileSync(asset)).digest('hex'),'stale anatomy approval '+a.id);
 check(r.panels.length===r.expected_panels&&r.panels.every((p,index)=>p.hands.length===r.expected_hands_per_panel[index]&&p.hands.every(h=>Object.values(h.checks).every(s=>s==='pass'))),'incomplete hand checks '+a.id);
 check(i.physics==='unknown'&&i.sources.join('|')===a.sources.join('|'),'generated image claim/source mismatch '+a.id);
}
check(data.actions.filter(a=>a.illustration).length===data.illustration_audit.approved,'illustration coverage count');
check(data.actions.filter(a=>a.category==='grasp').length===33,'GRASP coverage');
for(const f of data.families||[]){check(f.actions.length>0,'empty task family '+f.id);for(const id of f.actions)check(ids.has(id),'unknown family action '+id);check(!!f.gap,'missing coverage limit '+f.id)}
check(data.actions.find(a=>a.id==='I01').aliases.includes('持续旋转'),'continuous rotation search alias');
for(const id of ['catch_under','catch_over','catch_two','piano'])check(data.media[id].domain==='仿真','simulation disclosure '+id);
check(data.featured[0]==='I01','featured video task must be first');
// Imported tasks, object conditions, and evidence must survive exports / regeneration.
const propIds=new Set();for(const p of data.props){check(!propIds.has(p.id),'duplicate prop '+p.id);propIds.add(p.id);for(const e of p.evidence||[])check(!!data.sources[e.source]&&!!e.locator&&!!e.domain,'prop provenance '+p.id);if(p.added_in==='1.2')check(data.actions.some(a=>a.props.includes(p.id)),'orphan imported prop '+p.id)}
for(const a of data.actions){if(a.parent)check(ids.has(a.parent),'unknown parent '+a.id);for(const e of a.evidence||[]){check(!!data.media[e.media],'missing evidence media '+a.id);check(a.sources.includes(e.source),'evidence source not indexed '+a.id);check(data.media[e.media]?.source===e.source,'evidence source mismatch '+a.id);check(!!e.scope&&!!e.locator,'missing evidence scope '+a.id);for(const p of e.props||[])check(a.props.includes(p),'evidence object not indexed '+a.id)}}
for(const audit of [...(data.import_history||[]),data.project_audit]){
 check(audit.new_action_count===data.actions.filter(a=>a.added_in===audit.version).length,'new action count '+audit.version);
 check(audit.new_prop_count===data.props.filter(p=>p.added_in===audit.version).length,'new prop count '+audit.version);
}
// ActionSense raw labels remain distinct even when mapped to the same skill.
const as=data.actionsense;
check(as.activities.length===20&&new Set(as.activities.map(r=>r.id)).size===20,'ActionSense 20-label coverage');
check(new Set(as.activities.map(r=>r.label)).size===20,'ActionSense duplicate raw label');
check(new Set(as.activities.map(r=>r.action)).size===13,'ActionSense deduplicated activity mapping');
for(const r of as.activities){
 const a=data.actions.find(a=>a.id===r.action);
 check(!!a&&a.sources.includes('ACTIONSENSE'),'unmapped source activity '+r.id);
 check(a.conditions?.some(c=>c.label_id===r.id),'lost source condition '+r.id);
 for(const pid of r.props)check(a.props.includes(pid),'source condition prop not indexed '+r.id+' '+pid);
 for(const aid of r.subactions)check(ids.has(aid),'unknown source subaction '+r.id);
 check(!!r.url&&!!r.protocol_url,'missing raw label provenance '+r.id);
}
for(const a of data.actions){
 for(const pid of a.equipment||[])check(propIds.has(pid),'unknown equipment '+a.id+' '+pid);
 for(const p of a.phases||[]){
  for(const id of p.actions)check(ids.has(id),'unknown phase action '+a.id+' '+id);
  for(const id of p.primitives)check(data.primitives.some(x=>x.id===id),'unknown phase primitive '+a.id+' '+id);
 }
 if(a.added_in==='1.3')check(a.sources.includes('ACTIONSENSE')&&!a.pose,'unverified AS hand animation '+a.id);
}
for(const p of data.props.filter(p=>p.added_in==='1.3'))check(data.actions.some(a=>[...a.props,...(a.equipment||[])].includes(p.id)),'orphan AS prop/equipment '+p.id);
for(const mid of ['as_grid','as_session','as_calibration'])check(data.media[mid].scope==='reference'&&data.media[mid].domain==='人类采集','ActionSense media scope '+mid);
for(const id of ['B14','C09'])check(data.actions.find(a=>a.id===id).origin==='direct','existing ID merge '+id);
check(as.calibration_actions.every(id=>!as.activity_tasks.includes(id)),'calibration counted as kitchen activity');
check(as.license==='CC BY-NC-SA 4.0','ActionSense license');
check(data.media.p2_interactive.domain==='仿真','browser demo must be simulation');
check(data.media.wm_move.domain==='仿真','tool translation is simulation');
check(data.media.td_hammer.control==='遥操作'&&data.media.td_policy_hammer.control==='自主策略','control mode separation');
check(data.actions.find(a=>a.id==='U17').sources.includes('ADEPT'),'merge insertion into existing ID');
const model=window.HandModel;let sampled=0,maxStep=0;
for(const a of data.actions.filter(a=>a.pose)){
 let prev=null;for(let i=0;i<=100;i++){
  const f=model.frame(a.pose,i/100);sampled++;check(f.f.length===4&&f.f.every(v=>v.length===3),'joint dimensions '+a.id);f.f.forEach(row=>row.forEach((q,j)=>{const lim=[model.LIMITS.mcp,model.LIMITS.pip,model.LIMITS.dip][j];check(Number.isFinite(q)&&q>=lim[0]&&q<=lim[1],'joint range '+a.id)}));
  check(f.spread.every(v=>v>=-15&&v<=15),'spread limits '+a.id);check(f.wrist.every(Number.isFinite),'finite wrist '+a.id);if(prev)f.f.flat().forEach((q,j)=>maxStep=Math.max(maxStep,Math.abs(q-prev.f.flat()[j])));prev=f;
 }
}
const report={checked_at:new Date().toISOString(),catalogue:{actions:data.actions.length,primitives:data.primitives.length,props:data.props.length,sources:Object.keys(data.sources).length,by_origin:Object.fromEntries(['direct','adapted','extension'].map(k=>[k,data.actions.filter(a=>a.origin===k).length]))},generated_illustrations:{published:data.illustration_audit.approved,candidates:data.illustration_audit.candidates,remaining:data.illustration_audit.remaining,gate:'action approval + complete visual anatomy report + exact image hash'},numeric_template_checks:{templates:data.actions.filter(a=>a.pose).length,sampled_frames:sampled,max_finger_angle_step_deg:maxStep,status:failures.length?'fail':'pass'},failures,scope:{reference_integrity:'IDs, source mappings and local assets checked; human source reading documented separately',visual_review:'Representative joint templates and cited source figures inspected. Not all action variants individually visually reviewed.',physics:'NOT VALIDATED: no collision/force/friction simulator or calibrated human model',template_limits:'Illustrative display bounds, not clinical ROM or a robot URDF'}};
fs.writeFileSync(path.join(__dirname,'validation-report.json'),JSON.stringify(report,null,2));console.log(JSON.stringify(report,null,2));process.exitCode=failures.length?1:0;
