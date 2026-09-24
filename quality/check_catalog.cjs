const fs=require('fs'),path=require('path'),root=path.resolve(__dirname,'..');
global.window={THREE:require(path.join(root,'vendor/three.min.js'))};
require(path.join(root,'hand.js'));
const data=JSON.parse(fs.readFileSync(path.join(root,'research/catalog.json'),'utf8'));
const failures=[];function check(ok,message){if(!ok)failures.push(message)}
const ids=new Set();for(const a of data.actions){check(!ids.has(a.id),'duplicate '+a.id);ids.add(a.id);check(a.sources.length>0,'missing source '+a.id);for(const s of a.sources)check(!!data.sources[s],'unknown source '+s);for(const p of a.primitives)check(data.primitives.some(x=>x.id===p),'unknown primitive '+p);for(const p of a.props)check(data.props.some(x=>x.id===p),'unknown prop '+p);check(!!data.media[a.media],'missing media '+a.id);check(!!a.locator&&!!a.mediaScope,'missing provenance '+a.id);if(a.id.startsWith('J'))check(fs.existsSync(path.join(root,'assets/joints',a.id+'.png')),'missing joint asset '+a.id);if(a.id.startsWith('G'))check(fs.existsSync(path.join(root,'assets/feix','grasp-'+a.id.slice(1)+'.png')),'missing grasp asset '+a.id)}
check(data.actions.filter(a=>a.category==='grasp').length===33,'GRASP coverage');
for(const f of data.families||[]){check(f.actions.length>0,'empty task family '+f.id);for(const id of f.actions)check(ids.has(id),'unknown family action '+id);check(!!f.gap,'missing coverage limit '+f.id)}
check(data.actions.find(a=>a.id==='I01').aliases.includes('持续旋转'),'continuous rotation search alias');
for(const id of ['catch_under','catch_over','catch_two','piano'])check(data.media[id].domain==='仿真','simulation disclosure '+id);
check(data.featured[0]==='I01','featured video task must be first');
const model=window.HandModel;let sampled=0,maxStep=0;
for(const a of data.actions.filter(a=>a.pose)){
 let prev=null;for(let i=0;i<=100;i++){
  const f=model.frame(a.pose,i/100);sampled++;check(f.f.length===4&&f.f.every(v=>v.length===3),'joint dimensions '+a.id);f.f.forEach(row=>row.forEach((q,j)=>{const lim=[model.LIMITS.mcp,model.LIMITS.pip,model.LIMITS.dip][j];check(Number.isFinite(q)&&q>=lim[0]&&q<=lim[1],'joint range '+a.id)}));
  check(f.spread.every(v=>v>=-15&&v<=15),'spread limits '+a.id);check(f.wrist.every(Number.isFinite),'finite wrist '+a.id);if(prev)f.f.flat().forEach((q,j)=>maxStep=Math.max(maxStep,Math.abs(q-prev.f.flat()[j])));prev=f;
 }
}
const report={checked_at:new Date().toISOString(),catalogue:{actions:data.actions.length,primitives:data.primitives.length,props:data.props.length,sources:Object.keys(data.sources).length,by_origin:Object.fromEntries(['direct','adapted','extension'].map(k=>[k,data.actions.filter(a=>a.origin===k).length]))},numeric_template_checks:{templates:data.actions.filter(a=>a.pose).length,sampled_frames:sampled,max_finger_angle_step_deg:maxStep,status:failures.length?'fail':'pass'},failures,scope:{reference_integrity:'IDs, source mappings and local assets checked; human source reading documented separately',visual_review:'Representative joint templates and cited source figures inspected. Not all action variants individually visually reviewed.',physics:'NOT VALIDATED: no collision/force/friction simulator or calibrated human model',template_limits:'Illustrative display bounds, not clinical ROM or a robot URDF'}};
fs.writeFileSync(path.join(__dirname,'validation-report.json'),JSON.stringify(report,null,2));console.log(JSON.stringify(report,null,2));process.exitCode=failures.length?1:0;
