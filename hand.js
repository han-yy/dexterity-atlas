/* Parametric right hand for joint-motion illustration. Units are schematic, not subject-calibrated. */
(() => {
 const T=window.THREE;if(!T)return;
 const rad=d=>d*Math.PI/180;
 const FINGERS=[{x:.60,y:.69,l:[.65,.43,.31],r:.115},{x:.20,y:.79,l:[.72,.46,.33],r:.12},{x:-.21,y:.74,l:[.67,.43,.31],r:.113},{x:-.57,y:.60,l:[.52,.34,.27],r:.10}];
 const LIMITS={mcp:[0,70],pip:[0,88],dip:[0,52],spread:[-15,15],wristFlex:[-40,40],wristDeviation:[-18,18],forearm:[-70,70]};
 function frame(pose,u){
  const k=pose?.kind||'rest',q=pose?.reverse?1-u:u;
  const f=FINGERS.map(()=>[6,8,4]),spread=[2,0,-2,-4];
  const state={f,spread,wrist:[0,0,0],thumb:[20,-38,10,12],kind:k};
  const curl=(i,v)=>{f[i]=[6+v*56,8+v*74,4+v*42]};
  if(k==='finger')curl(pose.finger-1,q);
  if(['fist','fist_wrist','thumb_up'].includes(k))for(let i=0;i<4;i++)curl(i,u);
  if(k==='point'){for(let i=1;i<4;i++)curl(i,u);state.thumb=[20+20*u,-38+18*u,10+30*u,12+20*u]}
  if(k==='victory'){curl(2,u);curl(3,u);spread[0]=8*u;spread[1]=-5*u;state.thumb=[20+20*u,-38+18*u,10+30*u,12+20*u]}
  if(k==='two_flex'){curl(2,u);curl(3,u)}
  if(k==='spread'||k==='adduct'){const v=k==='adduct'?1-u:u;[14,3,-7,-14].forEach((s,i)=>spread[i]=s*v)}
  if(k==='thumb_abduct')state.thumb=[20,-25-40*u,10,12];
  if(k==='thumb_adduct')state.thumb=[20,-65+40*u,10,12];
  if(k==='thumb_flex'||k==='thumb_extend'){const v=k==='thumb_extend'?1-u:u;state.thumb=[20+20*v,-38+10*v,10+35*v,12+25*v]}
  if(k==='thumb_up')state.thumb=[10,-40,0,0];
  if(k==='fist'||k==='fist_wrist')state.thumb=[20+25*u,-38+27*u,10+30*u,12+25*u];
  if(k==='wrist_flex')state.wrist[0]=40*u;
  if(k==='wrist_extend'||k==='fist_wrist')state.wrist[0]=-40*u;
  if(k==='radial')state.wrist[2]=-18*u;
  if(k==='ulnar')state.wrist[2]=18*u;
  if(k==='supinate')state.wrist[1]=-65*u;
  if(k==='pronate')state.wrist[1]=65*u;
  return state;
 }
 function material(color,extra={}){return new T.MeshStandardMaterial({color,roughness:.52,metalness:.12,...extra})}
 function ellipsoid(parent,scale,pos,mat){const o=new T.Mesh(new T.SphereGeometry(1,24,18),mat);o.scale.set(...scale);o.position.set(...pos);parent.add(o);return o}
 function link(parent,length,r,mat,jmat){
  const g=new T.Group();parent.add(g);ellipsoid(g,[r,r,r],[0,0,0],jmat);
  const mesh=new T.Mesh(new T.CylinderGeometry(r*.84,r,length,18,1),mat);mesh.position.y=length/2;g.add(mesh);
  ellipsoid(g,[r*.84,r*.84,r*.84],[0,length,0],mat);return g;
 }
 // CPU projection of the same 3D scene for browsers without a working WebGL context.
 class SoftwareRenderer{
  constructor(){this.domElement=document.createElement('canvas');this.ctx=this.domElement.getContext('2d');this.ratio=1;this.software=true}
  setPixelRatio(r){this.ratio=r}setClearColor(){}dispose(){}forceContextLoss(){}
  setSize(w,h){this.w=w;this.h=h;this.domElement.width=w*this.ratio;this.domElement.height=h*this.ratio}
  render(scene,camera){
   scene.updateMatrixWorld(true);camera.updateMatrixWorld(true);const ctx=this.ctx,w=this.w,h=this.h;ctx.setTransform(this.ratio,0,0,this.ratio,0,0);ctx.fillStyle='#142136';ctx.fillRect(0,0,w,h);
   const project=p=>{const v=p.clone().project(camera);return {x:(v.x+1)*w/2,y:(1-v.y)*h/2,z:v.z}};
   const origin=new T.Vector3(),meshes=[];scene.traverse(o=>{if(o.isMesh&&o.visible)meshes.push(o)});meshes.sort((a,b)=>{const ap=origin.clone().applyMatrix4(a.matrixWorld).applyMatrix4(camera.matrixWorldInverse),bp=origin.clone().applyMatrix4(b.matrixWorld).applyMatrix4(camera.matrixWorldInverse);return ap.z-bp.z});
   ctx.strokeStyle='#263d59';ctx.lineWidth=1;for(let i=-4;i<=4;i++){for(const pts of [[[i,-2.27,-4],[i,-2.27,4]],[[-4,-2.27,i],[4,-2.27,i]]]){const a=project(new T.Vector3(...pts[0])),b=project(new T.Vector3(...pts[1]));ctx.beginPath();ctx.moveTo(a.x,a.y);ctx.lineTo(b.x,b.y);ctx.stroke()}}
   for(const o of meshes){
    const g=o.geometry,p=g.parameters,m=o.matrixWorld,center=project(origin.clone().applyMatrix4(m)),color='#'+o.material.color.getHexString();
    if(g.type==='CylinderGeometry'){
     const a=project(new T.Vector3(0,-p.height/2,0).applyMatrix4(m)),b=project(new T.Vector3(0,p.height/2,0).applyMatrix4(m));const r0=project(new T.Vector3(p.radiusBottom,0,0).applyMatrix4(m)),r1=project(new T.Vector3(0,0,p.radiusBottom).applyMatrix4(m));const width=2*Math.max(Math.hypot(r0.x-center.x,r0.y-center.y),Math.hypot(r1.x-center.x,r1.y-center.y));ctx.strokeStyle=color;ctx.lineWidth=Math.max(2,width);ctx.lineCap='round';ctx.beginPath();ctx.moveTo(a.x,a.y);ctx.lineTo(b.x,b.y);ctx.stroke();ctx.strokeStyle='#ffffff18';ctx.lineWidth=Math.max(1,width*.25);ctx.beginPath();ctx.moveTo(a.x-width*.18,a.y);ctx.lineTo(b.x-width*.18,b.y);ctx.stroke();
    }else if(g.type==='SphereGeometry'){
     const axes=[[1,0,0],[0,1,0],[0,0,1]].map(v=>project(new T.Vector3(...v).applyMatrix4(m)));let xx=0,xy=0,yy=0;axes.forEach(a=>{const x=a.x-center.x,y=a.y-center.y;xx+=x*x;xy+=x*y;yy+=y*y});const delta=Math.sqrt((xx-yy)**2+4*xy*xy),rx=Math.sqrt(Math.max(.1,(xx+yy+delta)/2)),ry=Math.sqrt(Math.max(.1,(xx+yy-delta)/2)),angle=.5*Math.atan2(2*xy,xx-yy);ctx.save();ctx.translate(center.x,center.y);ctx.rotate(angle);const grad=ctx.createRadialGradient(-rx*.25,-ry*.3,1,0,0,rx);grad.addColorStop(0,color);grad.addColorStop(1,o.material.color.clone().multiplyScalar(.62).getStyle());ctx.fillStyle=grad;ctx.beginPath();ctx.ellipse(0,0,rx,ry,0,0,Math.PI*2);ctx.fill();ctx.strokeStyle='#0c1d3430';ctx.lineWidth=.6;ctx.stroke();ctx.restore();
    }
   }
   const o=project(new T.Vector3(-1.75,-1.7,0));[[.6,0,0,'#ed8b8b','X'],[0,.6,0,'#a2cf80','Y'],[0,0,.6,'#75abe0','Z']].forEach(([x,y,z,col,label])=>{const p=project(new T.Vector3(-1.75+x,-1.7+y,z));ctx.strokeStyle=col;ctx.lineWidth=2;ctx.beginPath();ctx.moveTo(o.x,o.y);ctx.lineTo(p.x,p.y);ctx.stroke();ctx.fillStyle=col;ctx.font='12px sans-serif';ctx.fillText(label,p.x+4,p.y)});
  }
 }
 function makeRenderer(options){const c=document.createElement('canvas');let gl;try{gl=c.getContext('webgl2',{antialias:true})||c.getContext('webgl',{antialias:true})}catch{}return gl?new T.WebGLRenderer({canvas:c,context:gl,antialias:true,alpha:false,preserveDrawingBuffer:!!options.thumbnail}):new SoftwareRenderer()}
 class HandView{
  constructor(container,pose={kind:'rest'},options={}){
   this.container=container;this.pose=pose;this.playing=!matchMedia('(prefers-reduced-motion: reduce)').matches;this.progress=.7;this.speed=1;this.time=0;this.disposed=false;this.materials=[];
   this.renderer=makeRenderer(options);this.renderer.setPixelRatio(Math.min(devicePixelRatio,2));this.renderer.setClearColor(0x142136);this.renderer.outputColorSpace=T.SRGBColorSpace;container.appendChild(this.renderer.domElement);if(this.renderer.software)container.dataset.renderer='software-3d';else container.dataset.renderer='webgl';
   this.scene=new T.Scene();this.camera=new T.PerspectiveCamera(34,1,.1,60);this.yaw=.3;this.pitch=.05;this.distance=8.2;
   this.scene.add(new T.HemisphereLight(0xdcebff,0x344660,2.5));const key=new T.DirectionalLight(0xffffff,3);key.position.set(3,5,7);this.scene.add(key);const fill=new T.DirectionalLight(0x80b3ff,1.8);fill.position.set(-4,1,2);this.scene.add(fill);
   const skin=material(0xc7d7e9),joints=material(0x45668d),active=material(0xc9ed77),palmMat=material(0x96aecb);this.materials.push(skin,joints,active,palmMat);
   this.arm=new T.Group();this.scene.add(this.arm);ellipsoid(this.arm,[.43,.68,.27],[0,-1.65,-.02],palmMat);
   this.wrist=new T.Group();this.wrist.position.y=-.93;this.scene.add(this.wrist);this.hand=new T.Group();this.hand.position.y=.93;this.wrist.add(this.hand);
   ellipsoid(this.hand,[.78,.93,.24],[0,-.07,0],palmMat);ellipsoid(this.hand,[.29,.47,.26],[.48,-.35,.10],skin);
   this.digits=FINGERS.map((d,i)=>{
    const base=new T.Group();base.position.set(d.x,d.y,0);this.hand.add(base);const arr=[];let parent=base;
    d.l.forEach((len,j)=>{const g=link(parent,len,d.r*(1-.12*j),skin,joints);if(j)g.position.y=d.l[j-1];arr.push(g);parent=g});return {base,joints:arr};
   });
   this.thumbBase=new T.Group();this.thumbBase.position.set(.62,-.38,.10);this.hand.add(this.thumbBase);this.thumb=[];let par=this.thumbBase;[.49,.40,.30].forEach((l,j)=>{const g=link(par,l,.145-j*.015,skin,joints);if(j)g.position.y=[.49,.40][j-1];this.thumb.push(g);par=g});
   this.axes=new T.AxesHelper(.65);this.axes.position.set(-1.75,-1.7,0);this.scene.add(this.axes);
   this.grid=new T.GridHelper(8,20,0x355274,0x233a57);this.grid.position.y=-2.27;this.scene.add(this.grid);
   this.skin=skin;this.active=active;this.resize=()=>{const r=container.getBoundingClientRect(),w=options.width||r.width||560,h=options.height||r.height||420;this.renderer.setSize(w,h,false);this.camera.aspect=w/h;this.camera.updateProjectionMatrix();this.render()};
   this.resizeObserver=new ResizeObserver(this.resize);this.resizeObserver.observe(container);this.resize();this.highlight();
   this.canvas=this.renderer.domElement;this.down=e=>{this.drag={x:e.clientX,y:e.clientY};this.canvas.setPointerCapture(e.pointerId)};this.move=e=>{if(!this.drag)return;this.yaw+=(e.clientX-this.drag.x)*.009;this.pitch=Math.max(-1.2,Math.min(1.2,this.pitch+(e.clientY-this.drag.y)*.008));this.drag={x:e.clientX,y:e.clientY};this.render()};this.up=()=>this.drag=null;
   this.canvas.addEventListener('pointerdown',this.down);this.canvas.addEventListener('pointermove',this.move);this.canvas.addEventListener('pointerup',this.up);this.canvas.addEventListener('pointercancel',this.up);
   this.wheel=e=>{e.preventDefault();this.distance=Math.max(5.4,Math.min(12,this.distance+e.deltaY*.008));this.render()};this.canvas.addEventListener('wheel',this.wheel,{passive:false});
   this.last=performance.now();if(!options.thumbnail)this.loop();
  }
  highlight(){const k=this.pose.kind;this.digits.forEach((d,i)=>{const on=k==='finger'?i===this.pose.finger-1:!k.startsWith('thumb')&&!k.startsWith('wrist')&&!['radial','ulnar','supinate','pronate','rest'].includes(k);d.joints.forEach(g=>g.children.forEach(m=>{if(m.isMesh&&m.material===this.skin&&on)m.material=this.active}))});if(k.startsWith('thumb'))this.thumb.forEach(g=>g.children.forEach(m=>{if(m.isMesh&&m.material===this.skin)m.material=this.active}))}
  setView(name){this.yaw=name==='side'?1.45:name==='back'?Math.PI:0;this.pitch=name==='oblique'?.25:0;if(name==='oblique')this.yaw=.6;this.render()}
  render(){if(this.disposed)return;const s=frame(this.pose,this.progress);this.digits.forEach((d,i)=>{d.base.rotation.z=rad(-s.spread[i]);d.joints.forEach((g,j)=>g.rotation.x=rad(s.f[i][j]))});this.thumbBase.rotation.set(rad(s.thumb[0]),rad(-22),rad(s.thumb[1]));this.thumb[0].rotation.x=0;this.thumb[1].rotation.x=rad(s.thumb[2]);this.thumb[2].rotation.x=rad(s.thumb[3]);this.wrist.rotation.set(...s.wrist.map(rad));const t=new T.Vector3(0,.25,0);this.camera.position.set(Math.sin(this.yaw)*this.distance,Math.sin(this.pitch)*this.distance+.55,Math.cos(this.yaw)*Math.cos(this.pitch)*this.distance);this.camera.lookAt(t);this.renderer.render(this.scene,this.camera)}
  loop(){if(this.disposed)return;this.raf=requestAnimationFrame(()=>this.loop());const now=performance.now(),dt=Math.min((now-this.last)/1000,.1);this.last=now;if(this.playing){this.time+=dt*this.speed;this.progress=(1-Math.cos(this.time*Math.PI/2))/2;this.onProgress?.(this.progress)}this.render()}
  dispose(){this.disposed=true;cancelAnimationFrame(this.raf);this.resizeObserver.disconnect();this.canvas.removeEventListener('pointerdown',this.down);this.canvas.removeEventListener('pointermove',this.move);this.canvas.removeEventListener('pointerup',this.up);this.canvas.removeEventListener('pointercancel',this.up);this.canvas.removeEventListener('wheel',this.wheel);this.scene.traverse(o=>{o.geometry?.dispose()});this.materials.forEach(m=>m.dispose());this.renderer.dispose();this.renderer.forceContextLoss();this.canvas.remove()}
 }
 window.HandModel={HandView,frame,LIMITS,FINGERS};
})();
