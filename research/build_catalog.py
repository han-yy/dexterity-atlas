"""Build the authored action catalogue. Dimensions/repetitions are proposed protocols, not paper claims."""
import json,csv
from dexterity_expansion import expand
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sources={
'FEIX':dict(short='GRASP · Feix 2016',title='The GRASP Taxonomy of Human Grasp Types',authors='Thomas Feix, Javier Romero, Heinz-Bodo Schmiedmayer, Aaron M. Dollar, Danica Kragic',year='2016',venue='IEEE Transactions on Human-Machine Systems 46(1), 66–77',url='https://www.eng.yale.edu/grablab/pubs/Feix_THMS2016.pdf',doi='10.1109/THMS.2015.2470657',note='33 种静态单手抓握。不是动态操作任务全集；本库保留原始编号。'),
'NINA':dict(short='NinaPro · 2014',title='Electromyography data for non-invasive naturally-controlled robotic hand prostheses',authors='Manfredo Atzori et al.',year='2014',venue='Scientific Data 1, 140053',url='https://ninapro.hevs.ch/instructions/DB1.html',doi='10.1038/sdata.2014.53',note='DB1 包含 52 个动作和静息。依据官网动作图 A/B/C 标号，重叠抓握合并映射到 GRASP。D 组不归入 DB1 的 52 动作。'),
'BULLOCK':dict(short='Bullock & Dollar · 2011',title='Classifying Human Manipulation Behavior',authors='Ian M. Bullock, Aaron M. Dollar',year='2011',venue='IEEE ICORR',url='https://www.eng.yale.edu/grablab/pubs/bullock_icorr2011.pdf',doi='10.1109/ICORR.2011.5975408',note='按接触、手内运动、接触点相对运动与手坐标系中的平移/旋转分解。用于元动作依据，不代表所有扩展任务在论文中逐项出现。'),
'HORA':dict(short='HORA · CoRL 2022',title='In-Hand Object Rotation via Rapid Motor Adaptation',authors='Haozhi Qi, Ashish Kumar, Roberto Calandra, Yi Ma, Jitendra Malik',year='2022 / proceedings 2023',venue='CoRL · PMLR 205',url='https://haozhi.io/hora/',doi='10.48550/arXiv.2210.04887',note='主要任务为指尖持续绕轴旋转；项目页另有多轴控制展示，不能直接等同于完整目标位姿任务。'),
'VISER':dict(short='ViserDex · RSS 2026',title='ViserDex: Visual Sim-to-Real for Robust Dexterous In-hand Reorientation',authors='Arjun Bhardwaj, Maximum Wilder-Smith, Mayank Mittal, Vaishakh Patil, Marco Hutter',year='2026',venue='RSS 2026',url='https://rffr.leggedrobotics.com/works/viserdex/',doi='10.48550/arXiv.2604.11138',note='目标条件手内重定向；项目页有方块、橡皮鸭、地球仪等真实展示。'),
'POISE':dict(short='POISE · 2026',title='Learning In-Hand Object Reaching to General 6D Poses',authors='Junxiao Lin et al.',year='2026',venue='arXiv preprint',url='https://arxiv.org/abs/2609.13761',doi='10.48550/arXiv.2609.13761',note='掌心相对坐标系中的完整位置和朝向目标。本文仅引用已核实摘要；更细的轴向测试是本库的扩展方案。'),
'DEXYCB':dict(short='DexYCB · CVPR 2021',title='DexYCB: A Benchmark for Capturing Hand Grasping of Objects',authors='Yu-Wei Chao et al.',year='2021',venue='CVPR',url='https://dex-ycb.github.io/',doi='',note='桌面物体拾取及持物；物体类型和采集过程来自原项目与论文，不把所有日常操作都归给该数据集。'),
'DEXUMI':dict(short='DexUMI · CoRL 2025',title='DexUMI: Using Human Hand as the Universal Manipulation Interface for Dexterous Manipulation',authors='Mengda Xu et al.',year='2025',venue='CoRL · PMLR 305',url='https://dex-umi.github.io/',doi='',note='官方逐任务视频：茶叶夹取、方块放杯、厨房操作、鸡蛋盒。厨房四个子动作在本库单独标为任务拆解。'),
'ARCTIC':dict(short='ARCTIC · CVPR 2023',title='ARCTIC: A Dataset for Dexterous Bimanual Hand-Object Manipulation',authors='Zicong Fan et al.',year='2023',venue='CVPR',url='https://arctic.is.tue.mpg.de/',doi='',note='双手操作带关节物体；原项目明确展示剪刀、笔记本等。类似物体的扩展没有冒充原始任务。'),
'DEXMACHINA':dict(short='DexMachina · 2025/26',title='DexMachina: Functional Retargeting for Bimanual Dexterous Manipulation',authors='Mandi Zhao et al.',year='2025 preprint / ICML 2026',venue='ICML 2026',url='https://project-dexmachina.github.io/',doi='10.48550/arXiv.2505.24853',note='双手关节物体操作。强调接触与功能复现；运动学相似并不保证物理可执行。'),
'OAKINK':dict(short='OakInk2 · CVPR 2024',title='OakInk 2: A Dataset of Bimanual Hands-Object Manipulation in Complex Task Completion',authors='Xinyu Zhan et al.',year='2024',venue='CVPR',url='https://oakink.net/v2/',doi='10.48550/arXiv.2403.19417',note='复杂任务、动作原语与依赖图的设计参考；本库扩展的双手动作不声称是原数据逐项标签。'),
'GRAB':dict(short='GRAB · ECCV 2020',title='GRAB: A Dataset of Whole-Body Human Grasping of Objects',authors='Omid Taheri, Nima Ghorbani, Michael J. Black, Dimitrios Tzionas',year='2020',venue='ECCV',url='https://grab.is.tue.mpg.de/',doi='',note='全身—手—物体接触的真实动作与三维标注；数据下载需遵循原站许可。'),
'IHM':dict(short='IHM classification · 2009',title='Conceptualising a modified system for classification of in-hand manipulation',authors='Karina Pont, Margaret Wallen, Anita Bundy',year='2009',venue='Australian Occupational Therapy Journal',url='https://pubmed.ncbi.nlm.nih.gov/20854484/',doi='10.1111/j.1440-1630.2008.00774.x',note='指到掌、掌到指、移位、简单与复杂旋转的分类依据。仅用于动作分析，不作临床训练建议。')}
# Verified on 2026-09-24. Media retain source attribution and are not re-licensed by this project.
media={
'hora':dict(type='video',url='https://haozhi.io/hora/results/teaser.mp4',source='HORA',label='官方演示 · 持续手内旋转',match='原项目同类演示；不承诺覆盖每个扩展条件'),
'viser':dict(type='video',url='https://rffr.leggedrobotics.com/works/viserdex/videos/teaser_reorientation.mp4',source='VISER',label='官方演示 · 目标朝向重定向',match='任务族演示；具体物体以视频实际内容为准'),
'tea':dict(type='video',url='https://dex-umi.github.io/static/videos/xhand_tea.mp4',source='DEXUMI',label='官方演示 · 镊子夹茶叶',match='对应 Tea Picking with Tool'),
'cube':dict(type='video',url='https://dex-umi.github.io/static/videos/inspire/pickNplace/pickNplace_demo.mp4',source='DEXUMI',label='官方演示 · 方块放入杯中',match='对应 Cube Picking'),
'kitchen':dict(type='video',url='https://dex-umi.github.io/static/videos/xhand/kitchen/kitchen_demo.mp4',source='DEXUMI',label='官方演示 · 厨房四步操作',match='完整四步视频，未裁切为各子动作'),
'egg':dict(type='video',url='https://dex-umi.github.io/static/videos/inspire/egg/egg_demo.mp4',source='DEXUMI',label='官方演示 · 鸡蛋盒开扣',match='对应 Egg Carton'),
'nina':dict(type='image',url='assets/ninapro-movements.png',source='NINA',label='官方动作图 · 按详情中的 A/B/C 编号查找',match='原图含 A/B/C/D；本库明确指出对应分组与编号'),
'feix':dict(type='image',url='assets/feix-taxonomy.png',source='FEIX',label='GRASP 原文分类图',match='按 GRASP # 编号定位；静态姿态参考，不是视频'),
'grab':dict(type='youtube',url='https://www.youtube.com/embed/s5syYMxmNHA',source='GRAB',label='官方项目总览 · GRAB',match='仅为相关任务与接触记录参考，未逐动作定位'),
}
categories=[('joint','01','关节与无物体'),('grasp','02','静态抓握'),('inhand','03','手内位姿操作'),('transfer','04','拾取与搬运'),('tool','05','工具与机关'),('bimanual','06','双手协作'),('deform','07','柔性物体'),('contact','08','接触与力控制')]
primitives=[]
def primitive(i,n,en,definition,obs,source):primitives.append(dict(id=i,name=n,en=en,definition=definition,observe=obs,source=source.split(',')))
for row in [
('P01','手指屈曲','Finger flexion','缩小指骨之间的夹角，区分 MCP、PIP、DIP。','关节角、邻指联动','NINA'),('P02','手指伸展','Finger extension','由屈曲状态回到伸展状态。','伸展终点、速度','NINA'),('P03','展指与并指','Abduction / adduction','在掌平面改变指间夹角。','指间距、MCP 外展','NINA'),('P04','拇指对掌','Thumb opposition','拇指指腹转向其他指腹或掌面。','CMC 旋转、拇指指腹朝向','NINA'),('P05','腕屈伸','Wrist flexion / extension','手相对前臂作掌屈或背伸。','腕角、前臂固定情况','NINA'),('P06','腕偏移','Radial / ulnar deviation','手向桡侧或尺侧偏移。','腕偏移角','NINA'),('P07','前臂旋转','Pronation / supination','前臂旋前或旋后，带动手掌转向。','前臂姿态；不能当成指内旋转','NINA'),('P08','接近与预成形','Reach / preshape','接触前将手移动并形成合适开度。','首次接触时间、开度','DEXYCB'),('P09','建立接触','Contact acquisition','指定指腹、侧面或手掌首次接触物体。','接触点、法向力','BULLOCK'),('P10','稳定持握','Stable hold','保持物体相对手的位姿。','滑移、位姿漂移、力','FEIX'),('P11','指腹对捏','Pad pinch','拇指指腹与对侧手指形成对向约束。','接触指、夹持距离','FEIX'),('P12','指尖对捏','Tip pinch','接触集中在拇指和另一指的末端。','指尖接触位置','FEIX'),('P13','侧向夹持','Lateral pinch','拇指与食指侧面夹持薄物体。','接触面、拇指位置','FEIX'),('P14','包络握持','Power enclosure','多个手指与掌面包围物体。','掌面接触、包覆程度','FEIX'),('P15','释放接触','Release','减小约束，按时序退出接触。','最后接触时间、释放次序','BULLOCK'),('P16','整体搬运','Transport','物体相对手大体固定，整体移动。','世界系位姿与手系位姿','BULLOCK,DEXYCB'),('P17','手内平移','In-hand translation','物体相对手掌产生位移。','掌系位置变化','BULLOCK,POISE'),('P18','手内旋转','In-hand rotation','物体相对手掌改变朝向。','掌系四元数与旋转轴','BULLOCK,HORA'),('P19','目标位姿到达','Goal pose reaching','到达给定朝向或位置—朝向目标。','位置误差、SO(3) 误差、保持时间','VISER,POISE'),('P20','换指与重建接触','Finger gait / recontact','交替释放和建立手指接触，同时由其余接触支撑。','接触图随时间变化','HORA'),('P21','滚动接触','Rolling','接触点在手与物表面随运动变化。','接触点轨迹、相对切向速度','BULLOCK'),('P22','滑动接触','Sliding','维持接触同时产生切向相对位移。','滑移量、接触法向','BULLOCK'),('P23','推与按压','Push / press','施力推动物体或压下机构。','位移、力—位移关系','BULLOCK,DEXUMI'),('P24','钩拉与牵引','Pull','通过约束施加朝向手的位移。','拉力、机构行程','BULLOCK'),('P25','拧转机构','Twist / articulate','改变对象的转动关节或螺纹状态。','关节角、扭矩、底座运动','NINA,ARCTIC'),('P26','工具驱动','Tool actuation','持稳工具并由活动手指驱动功能部分。','握持接触和驱动接触分离','DEXUMI'),('P27','双手稳定—操作','Stabilize / manipulate','一手稳定对象，另一手改变对象状态。','双手角色、对象关节','ARCTIC,DEXMACHINA'),('P28','双手转交','Handover','接收手建立支撑后，交出手解除接触。','交接重叠期、掉落','BULLOCK,OAKINK'),('P29','变形与张力','Deform / tension','通过多接触改变柔性物体形状或张力。','形状关键点、载荷','BULLOCK,OAKINK'),('P30','指到掌 / 掌到指','Finger–palm translation','在指端工作区与掌内储存区之间移动小物件。','储存数量、滑移、终点','IHM'),('P31','力级调节','Force modulation','在既定接触中改变作用力并尽量保持位姿。','力或触觉传感器；仅视频不能确证','DEXUMI'),('P32','接触探索','Tactile exploration','滑扫或按压表面以探查物体属性。','接触轨迹、触觉信号','BULLOCK')]:primitive(*row)
props=[]
def prop(i,n,group,spec,use):props.append(dict(id=i,name=n,group=group,spec=spec,use=use))
for r in [
('knife','训练刀 / 钝片','工具','钝头训练工具；固定软材料','食指伸展抓与切割模拟'),('none','无道具','基础','前臂支撑垫、同步提示屏可选','关节校准与无物体动作'),('cylinder','圆柱组','几何体','建议直径 20 / 40 / 60 mm；轻质、圆边','直径变化、绕轴旋转'),('sphere','球体组','几何体','建议直径 30 / 50 / 70 mm','球抓、重定向'),('cube','方块组','几何体','建议边长 25 / 40 / 60 mm；表面加朝向标记','角点接触与 goal pose'),('prism','棱柱','几何体','六棱或八棱，注明尺寸','非圆截面重定向'),('disk','圆盘','几何体','不同厚度、直径，边缘圆滑','盘抓与翻转'),('coin','代币 / 硬币','小物件','建议直径 25–35 mm 的代币','精细捏取、掌指转移'),('peg','插销与孔板','装配','配合间隙分两级，记录毫米值','对准与插入'),('pen','笔与笔帽','工具','粗细两级，钝端；有盖与无盖','笔姿调整、书写、拔帽'),('card','卡片','平薄物','塑料卡、硬纸卡，记录厚度','侧捏、翻面、插卡'),('key','钥匙与练习锁','机关','独立练习锁，注明旋转行程','插入、转动、拔出'),('bottle','瓶与螺纹盖','机关','空塑料瓶；盖子直径及螺距记录','包络抓、拧盖'),('cup','杯','日用品','有柄与无柄；先用空杯','搬运、放杯、倒出'),('bowl','碗与托盘','日用品','轻质防碎；记录边缘形状','边缘抓、双手搬运'),('tweezers','镊子 / 茶夹','工具','钝头、弹性夹臂','持握同时驱动夹口'),('tea','茶叶 / 仿真颗粒','耗材','先用大尺寸仿真颗粒','工具夹取与撒落'),('knob','旋钮板','机关','刻度盘；可调阻尼','目标角与保持'),('pan','轻质锅具','日用品','冷态、空载、侧把手','非指尖接触与转移'),('salt','颗粒与小容器','耗材','粗粒和细粒分开，记录粒径','捏取、撒落'),('carton','鸡蛋盒','机关','空纸盒；卡扣完整','按压与抬扣协同'),('scissors','安全剪刀','工具','钝头；空剪及薄纸分阶段','开合与切割'),('paper','纸张','柔性','纸型、克重、初始折痕记录','翻页、折叠、撕开'),('screw','螺丝刀与螺母板','装配','低阻力练习板','驱动工具、拧紧与松开'),('book','书 / 铰链板','机关','开合角可观测','双手稳定与翻页'),('laptop','笔记本模型','机关','优先无电子功能的铰链模型','上盖开合'),('box','盒与盖','机关','翻盖、滑盖、分离盖','拉、推、开盖'),('button','按钮 / 开关板','机关','不同键程与触感，低电压或无电','按压、切换'),('zip','拉链板','柔性','大拉环；分离式底布','双手稳定与拉动'),('cloth','布片 / 毛巾','柔性','固定尺寸、材质与标记角点','展平、折叠、拧转'),('rope','粗绳 / 鞋带','柔性','长度与粗细分级','牵引、穿孔、结绳'),('sponge','海绵 / 软球','柔性','不同压缩硬度','挤压与回弹'),('bag','软袋','柔性','空袋；密封条与提手分别记录','开口、捏封、搬运'),('elastic','低张力弹性圈','柔性','低阻力、限定形变','拉伸与套环'),('clay','软黏土','柔性','质量和初始形状固定','揉、搓、压扁'),('plug','无电插头模型','装配','完全断电的插接件','拔插与线缆稳定'),('drawer','抽屉模型','机关','有止挡，低负载','钩拉、推回'),('handle','门把手模型','机关','桌面夹具、有限转角','压柄与旋转'),('ring','环与短杆','装配','不同间隙的圆环','套环与环形抓'),('phone','手机模型','日用品','轻质模型，屏幕可贴标记','持握与拇指操作'),('weight','轻质配重','控制变量','先做低负荷预试；记录克数','同姿态不同负载'),('surface','纹理与摩擦板','控制变量','光滑、粗糙、软面，记录材质','滑扫、摩擦对比'),('sensor','力 / 触觉传感器','记录设备','记录标定、单位、量程与同步','力控制动作的有效验证')]:prop(*r)
actions=[]
def add(id,name,en,cat,ps,objects,src,locator,desc,success,origin='direct',demo=None,pose=None,difficulty='基础',hands='单手',variation=None):
    actions.append(dict(id=id,name=name,en=en,category=cat,primitives=ps.split(','),props=objects.split(','),sources=src.split(','),locator=locator,description=desc,success=success,origin=origin,media=demo,pose=pose,difficulty=difficulty,hands=hands,variation=variation or '速度（慢 / 自选）× 幅度（小 / 大）× 左右手；先独立改变一个因素。'))
# The first 29 follow NinaPro A/B, plus rest. Supination around two axes remains two task variants, not two anatomical DOFs.
finger_names=[('食指','Index',1),('中指','Middle',2),('无名指','Ring',3),('小指','Little',4)]
for j,(cn,en,f) in enumerate(finger_names):
 for k,(verb,ev) in enumerate([('屈曲','flexion'),('伸展','extension')]):
  i=j*2+k+1
  add(f'J{i:02}',cn+verb,f'{en} {ev}','joint','P01' if k==0 else 'P02','none','NINA',f'官方动作图 Exercise A{i}',f'前臂保持支撑，{cn}缓慢{verb}，其余手指尽量保持自然。','目标指完成可见运动；记录相邻手指伴随运动，不强行约束自然联动。',demo='nina',pose={'kind':'finger','finger':f,'reverse':bool(k)})
for i,n,en,kind,ps in [(9,'拇指内收','Thumb adduction','thumb_adduct','P03'),(10,'拇指外展','Thumb abduction','thumb_abduct','P03'),(11,'拇指屈曲','Thumb flexion','thumb_flex','P01'),(12,'拇指伸展','Thumb extension','thumb_extend','P02')]:
 add(f'J{i:02}',n,en,'joint',ps,'none','NINA',f'官方动作图 Exercise A{i}',f'以自然张开的手开始，执行{n}；掌面与腕姿态保持可观测。','目标方向明确；无明显腕部代偿。',demo='nina',pose={'kind':kind})
b=[('竖拇指','Thumb up','thumb_up','P01,P02'),('食中指伸展，其余屈曲','Index and middle extension','victory','P01,P02'),('无名指与小指屈曲','Ring and little flexion','two_flex','P01,P02'),('拇指对向小指根部','Thumb opposing little-finger base',None,'P04'),('五指张开','Abduction of all fingers','spread','P03'),('握拳','Fingers flexed together in fist','fist','P01,P04'),('食指指向','Pointing index','point','P01,P02'),('伸直手指并拢','Adduction of extended fingers','adduct','P03'),('前臂旋后：中指轴提示','Supination, middle-finger axis','supinate','P07'),('前臂旋前：中指轴提示','Pronation, middle-finger axis','pronate','P07'),('前臂旋后：小指轴提示','Supination, little-finger axis',None,'P07'),('前臂旋前：小指轴提示','Pronation, little-finger axis',None,'P07'),('腕掌屈','Wrist flexion','wrist_flex','P05'),('腕背伸','Wrist extension','wrist_extend','P05'),('腕桡偏','Wrist radial deviation','radial','P06'),('腕尺偏','Wrist ulnar deviation','ulnar','P06'),('握拳位腕背伸','Wrist extension with closed hand','fist_wrist','P01,P05')]
for i,(n,en,kind,ps) in enumerate(b,1):
 add(f'J{i+12:02}',n,en,'joint',ps,'none','NINA',f'官方动作图 Exercise B{i}',f'按原图 B{i} 的起始姿态完成{n}，以舒适范围执行。','记录目标运动及可能代偿；B9–B12 是原数据任务提示差异，旋前 / 旋后主要发生在前臂。',demo='nina',pose={'kind':kind} if kind else None)
add('J30','自然静息','Rest','joint','P02','none','NINA','DB1: rest position','手自然放松，记录静息片段。','稳定记录背景信号；不把低幅噪声直接标为动作。',demo='nina',pose={'kind':'rest'})
grasps='''大直径包络抓|Large Diameter|cylinder|P14
小直径包络抓|Small Diameter|cylinder|P14
中等包络抓|Medium Wrap|bottle|P14
拇指内收抓|Adducted Thumb|cylinder|P14
轻工具抓|Light Tool|pen|P10
四指棱柱抓|Prismatic 4 Finger|prism|P11
三指棱柱抓|Prismatic 3 Finger|prism|P11
二指棱柱抓|Prismatic 2 Finger|prism|P11
掌侧指腹捏|Palmar Pinch|coin|P11
力量圆盘抓|Power Disk|disk|P14
力量球抓|Power Sphere|sphere|P14
精密圆盘抓|Precision Disk|disk|P11
精密球抓|Precision Sphere|sphere|P11
三脚架抓|Tripod|sphere|P11
固定钩抓|Fixed Hook|handle|P10
侧向抓|Lateral|card|P13
食指伸展抓|Index Finger Extension|knife|P10
伸展型抓|Extension Type|disk|P10
远端型抓|Distal Type|scissors|P10
书写三脚架抓|Writing Tripod|pen|P11
三脚架变式|Tripod Variation|pen|P11
平行伸展抓|Parallel Extension|card|P11
指间内收夹|Adduction Grip|card|P03
指尖捏|Tip Pinch|coin|P12
侧向三脚架抓|Lateral Tripod|pen|P13
四指球抓|Sphere 4 Finger|sphere|P11
四脚架抓|Quadpod|sphere|P11
三指球抓|Sphere 3 Finger|sphere|P11
杆状抓|Stick|screw|P14
掌面抓|Palmar|disk|P14
环形抓|Ring|cylinder|P10
腹侧抓|Ventral|pen|P11
下位钳捏|Inferior Pincer|coin|P12'''
for i,line in enumerate(grasps.splitlines(),1):
 n,en,obj,ps=line.split('|')
 add(f'G{i:02}',n,en,'grasp',ps+',P10',obj,'FEIX',f'GRASP #{i} · Figure 4, p.70',f'依据 GRASP #{i} 的接触部位与拇指位置摆放物体，保持稳定。中文为本库工作译名；判别以英文名和原图为准。','接触手指、指腹 / 侧面 / 掌面以及拇指位置与原图一致；持握阶段物体相对手保持稳定。',demo='feix',variation='改变物体尺寸、表面与轻负载；不要把尺寸变体重复计为新的抓握类型。')
add('I01','指尖持续绕轴旋转','Continuous in-hand rotation','inhand','P10,P18,P20','cylinder','HORA','项目页：Rotate Different Objects using the Fingertips','在已有稳定抓握中交替换指，让物体持续绕轴转动。','统计有效旋转角 / 时间与掉落率；不使用单一目标姿态作为主要指标。',demo='hora',difficulty='进阶')
add('I02','旋转到指定朝向','Goal-conditioned reorientation','inhand','P10,P18,P19,P20','cube','VISER','项目页：Real-World Deployment / Cube','稳定持物，给定目标朝向，通过手指调整到目标并保持。','记录最小 SO(3) 朝向误差与保持时间；必须同时检查没有掉落。',demo='viser',difficulty='进阶')
add('I03','掌系完整 6D 位姿到达','Palm-relative 6D pose reaching','inhand','P10,P17,P18,P19','cube','POISE','摘要：palm-relative target pose','在手掌相对坐标系内同时指定物体的位置和朝向。','位置误差与旋转误差分别达标，并维持抓握；阈值由采集协议设定。',demo='viser',difficulty='高阶')
ihm=[('指尖到掌心转移','Finger-to-palm translation','P30','coin'),('掌心到指尖转移','Palm-to-finger translation','P30','coin'),('笔沿指腹小幅移位','Simple shift','P17','pen'),('多指配合复杂移位','Complex shift','P17,P20','pen'),('指间简单旋转','Simple rotation','P18','coin'),('指间复杂旋转','Complex rotation','P18,P20','pen')]
for i,(n,en,ps,obj) in enumerate(ihm,4):add(f'I{i:02}',n,en,'inhand',ps+',P10',obj,'IHM,BULLOCK','IHM 摘要分类；道具与执行方式为采集设计',f'用{next(p["name"] for p in props if p["id"]==obj)}执行该类手内位移，保持前臂稳定。','依据掌系物体轨迹判断，单纯移动腕或手臂不算手内操作。',origin='adapted',demo='grab',difficulty='进阶')
extensions=[('掌系 X 方向平移','Translation X','P17','cube','POISE'),('掌系 Y 方向平移','Translation Y','P17','cube','POISE'),('掌系 Z 方向平移','Translation Z','P17','cube','POISE'),('绕掌系 X 轴定向旋转','Rotation X','P18,P19','cube','VISER'),('绕掌系 Y 轴定向旋转','Rotation Y','P18,P19','cube','VISER'),('绕掌系 Z 轴定向旋转','Rotation Z','P18,P19','cube','VISER'),('顺转—停住—逆转','Rotate-stop-reverse','P18,P19','cylinder','HORA'),('连续目标朝向序列','Sequential orientation targets','P18,P19','cube','VISER'),('连续位置与朝向目标','Sequential 6D targets','P17,P18,P19','prism','POISE'),('指尖滚球','Fingertip rolling','P21,P18','sphere','BULLOCK'),('指腹滑移调整','Sliding regrasp','P22,P17','pen','BULLOCK'),('支点旋转','Pivot around contact','P18,P21','prism','BULLOCK'),('交替换食指与中指','Alternating finger gait','P20','cylinder','HORA'),('三指抓转为二指捏','Tripod-to-pinch transition','P20,P11','coin','FEIX'),('掌握转为指尖抓','Power-to-precision transition','P20,P14,P12','sphere','FEIX'),('硬币翻面 180°','Coin flip in hand','P18,P20','coin','BULLOCK'),('笔调至书写姿态','Pen reorientation','P18,P20','pen','BULLOCK'),('掌内暂存后逐枚取出','Sequential coin storage','P30,P12','coin','IHM'),('小扰动后的位姿恢复','Disturbance recovery','P19,P31','sphere','POISE'),('可见纹理改变下重定向','Reorientation with appearance variation','P18,P19','cube','VISER'),('不同质量下持续旋转','Rotation across masses','P18,P31','cylinder,weight','HORA')]
for i,(n,en,ps,obj,src) in enumerate(extensions,10):add(f'I{i:02}',n,en,'inhand','P10,'+ps,obj,src+',BULLOCK','本库扩展；原文支持任务族 / 元动作，未声称为原论文独立任务',f'{n}。固定手掌参考系，显式记录初始物体位姿和目标 / 路径。','运动主要来自手指；记录接触切换、轨迹误差与掉落。建议目标保持 1 s；这是本库默认值。',origin='extension',demo='hora' if src=='HORA' else 'viser' if src in ['VISER','POISE'] else 'grab',difficulty='高阶' if 'P20' in ps else '进阶')
# Functional tasks observed on the original source pages.
for r in [
('T01','方块拾取并放入杯中','Cube picking','transfer','P08,P09,P11,P16,P15','cube,cup','DEXUMI','Cube Picking','拾取桌上 2.5 cm 方块并放到杯中。','方块进入杯中，释放后保持；记录途中掉落。','direct','cube'),
('T02','桌面物体拾取并举起','Tabletop pick-up','transfer','P08,P09,P10,P16','bottle','DEXYCB','Data Collection and Annotation','从自然手姿开始，拾取桌面目标并举起。','目标离开桌面且保持稳定；标记接触和离桌帧。','direct','grab'),
('U01','镊子夹取茶叶','Tea picking with tool','tool','P10,P26,P16,P15','tweezers,tea,cup','DEXUMI','Tea Picking with Tool','拿起镊子，将茶叶从茶壶转移到杯中。','夹住目标并放入指定容器；区分工具握持失败与夹口驱动失败。','direct','tea'),
('U02','旋转炉具旋钮','Turn off stove knob','tool','P11,P25','knob','DEXUMI','Kitchen Manipulation · step 1','以无热源旋钮板复现拧到目标角的子动作。','旋钮到目标角，底座保持固定。','adapted','kitchen'),
('T03','锅具从台面转移','Transfer a pan','transfer','P10,P16,P15','pan','DEXUMI','Kitchen Manipulation · step 2','以侧面接触抓起冷态轻质锅具并转移。','锅具到目标区域，过程中不倾覆或滑落。','adapted','kitchen'),
('U03','捏取颗粒','Pinch seasoning','tool','P09,P12,P31','salt','DEXUMI','Kitchen Manipulation · step 3','手指接触颗粒后闭合，捏起一小撮。','可见颗粒被稳定带离容器；触觉记录用于验证接触。','adapted','kitchen'),
('U04','控制颗粒撒落','Sprinkle seasoning','tool','P15,P31','salt,pan','DEXUMI','Kitchen Manipulation · step 4','在目标区域上方逐步释放颗粒。','释放时机与落点被记录，区分均匀撒落和一次掉落。','adapted','kitchen'),
('U05','鸡蛋盒按压与抬扣','Open egg carton','tool','P23,P24,P26','carton','DEXUMI','Egg Carton','四指压住上盖，拇指抬起前部卡扣。','卡扣分离且上盖可打开；标记稳定手指和活动拇指。','direct','egg'),
('U06','三脚架抓开瓶盖','Open bottle with tripod grasp','tool','P11,P25','bottle','NINA','官方动作图 Exercise C21','按原图形成三脚架抓，旋转瓶盖。','瓶盖发生相对瓶身旋转；底座固定方式单独记录。','direct','nina'),
('U07','杆状抓使用螺丝刀','Turn a screw','tool','P14,P25,P26','screw','NINA','官方动作图 Exercise C22','抓住螺丝刀并转动练习螺丝。','工具与螺丝有效啮合并产生转角。','direct','nina'),
('U08','食指伸展抓切割','Cut with index-extension grasp','tool','P10,P23,P26','paper','NINA','官方动作图 Exercise C23','原任务是持刀切割。本库建议用钝头训练工具及软材料先做采集预试。','目标材料状态改变，工具握持姿态可辨。','direct','nina'),
('B01','双手剪刀开合','Bimanual scissors articulation','bimanual','P27,P26,P25','scissors','ARCTIC','项目摘要：scissors','一手稳定物体或手柄，另一手驱动剪刀开合。','剪刀关节角变化与手指接触同步。','direct','arctic'),
('B02','双手笔记本开合','Bimanual laptop articulation','bimanual','P27,P25','laptop','ARCTIC','项目摘要：laptops','一手稳定底座，另一手操作上盖。','底座稳定、上盖达到指定角度；记录换手。','direct','arctic'),
('B03','双手书本合盖','Notebook closing','bimanual','P27,P25','book','DEXMACHINA','项目页：Notebook task','分配稳定和合盖角色，允许手型改变操作策略。','书本合盖且无悬空驱动物体的现象。','direct','dexmachina')]:
 id,n,en,cat,ps,obj,src,loc,d,s,o,m=r
 add(id,n,en,cat,ps,obj,src,loc,d,s,o,m,difficulty='进阶' if cat!='transfer' else '基础',hands='双手' if cat=='bimanual' else '单手')
def batch(prefix,start,category,rows,source,ps,default_demo,hands='单手',difficulty='进阶'):
 for i,line in enumerate(rows.strip().splitlines(),start):
  parts=line.split('|');n,en,obj=parts[:3];p=parts[3] if len(parts)>3 else ps
  add(f'{prefix}{i:02}',n,en,category,p,obj,source,'本库采集方案扩展；来源提供分解框架或相近任务',f'{n}。在固定工作区内记录接近、接触、执行和结束四个阶段。','按任务目标记录物体终态与接触时序；具体容差在预试后设定并写入 trial 元数据。',origin='extension',demo=default_demo,difficulty=difficulty,hands=hands)
batch('T',4,'transfer','''平薄卡片从桌面捏起|Flat card pickup|card|P08,P12,P16
硬币从桌面捏起|Coin pickup|coin|P08,P12,P16
球体拾取并放置|Sphere pick and place|sphere|P08,P11,P16,P15
圆柱拾取并放置|Cylinder pick and place|cylinder|P08,P14,P16,P15
杯柄钩取|Cup handle pickup|cup|P08,P10,P16
杯沿精密夹取|Cup rim pickup|cup|P08,P11,P16
薄片边缘夹取|Edge pickup|card|P08,P13,P16
物体垂直堆叠|Block stacking|cube|P10,P16,P15
受限空间拾取|Constrained pickup|cube,box|P08,P09,P11
有遮挡目标拾取|Occluded target pickup|cube,bottle|P08,P09,P11
横放笔拾取|Horizontal pen pickup|pen|P08,P11,P16
物体移到标记区域|Object relocation|cube|P10,P16,P15
持物改变腕方向|Transport with wrist rotation|bottle|P10,P07,P16
细长物水平搬运|Horizontal rod transport|pen|P10,P16
抓取后精准回放|Pick and return|prism|P08,P10,P16,P15
放置后脱离接触|Controlled release|cube|P15,P16
预成形开度适配|Aperture preshaping|sphere,cylinder|P08,P03''','DEXYCB,BULLOCK','P08,P10,P16,P15','grab')
batch('U',9,'tool','''按下按钮|Button press|button|P23
拨动开关|Toggle switch|button|P23,P24
食指驱动扳机|Index trigger pull|button|P10,P26
拇指按压顶部泵头|Thumb pump press|bottle|P10,P23
旋钮转到刻度|Knob target angle|knob|P11,P25
钥匙插入练习锁|Key insertion|key|P13,P17
钥匙转动|Key turning|key|P13,P25
钥匙拔出|Key extraction|key|P13,P24
插销对孔并插入|Peg insertion|peg|P11,P17,P23
插销拔出|Peg extraction|peg|P11,P24
卡片插槽|Card insertion|card,box|P13,P17
卡片抽出|Card extraction|card,box|P13,P24
圆环套杆|Ring placement|ring|P11,P17
旋紧瓶盖|Screw cap tightening|bottle|P11,P25
旋松瓶盖|Screw cap loosening|bottle|P11,P25
书写短线|Writing strokes|pen,paper|P11,P17,P23
笔帽拔开|Pen uncapping|pen|P10,P24
笔帽扣合|Pen capping|pen|P10,P23
夹子夹持纸张|Clip actuation|tweezers,paper|P10,P26
抽屉钩拉|Drawer pull|drawer|P10,P24
抽屉推回|Drawer push|drawer|P23
门柄压下|Handle depression|handle|P14,P25
持手机模型并拇指滑动|Thumb swipe while holding|phone|P10,P22
空杯倾倒到目标角|Cup tilt|cup|P10,P07
剪刀空载开合|Scissor actuation|scissors|P10,P26
旋转螺母|Nut rotation|screw|P11,P25''','BULLOCK,NINA','P10,P26','nina')
batch('B',4,'bimanual','''左手向右手转交|Left-to-right handover|cube|P10,P28,P15
右手向左手转交|Right-to-left handover|cube|P10,P28,P15
双手共同搬运托盘|Two-hand tray transport|bowl|P10,P16,P27
一手扶瓶一手拧盖|Stabilized bottle opening|bottle|P27,P25
一手扶盒一手开盖|Stabilized box opening|box|P27,P24
一手扶纸一手翻页|Page turning|book,paper|P27,P12,P18
一手扶物一手插销|Stabilized peg insertion|peg|P27,P17,P23
一手扶线一手插接|Unpowered connector insertion|plug|P27,P23
一手固定一手拉链|Zipper operation|zip|P27,P24
双手拉开袋口|Bag opening|bag|P27,P29
双手扶杯与倒入|Pour-and-receive|cup|P27,P07
双手改变长杆方向|Two-hand rod reorientation|cylinder|P27,P18
稳定手与操作手换角色|Role switching|box|P27,P20
双手拉开套筒|Telescoping pull|cylinder|P27,P24
双手贴合两块物体|Object alignment|cube|P27,P17
一手持笔一手拔帽|Bimanual pen uncapping|pen|P27,P24
双手拆开插接块|Block separation|cube|P27,P24
双手组合插接块|Block assembly|cube|P27,P23''','OAKINK,ARCTIC,BULLOCK','P27','arctic',hands='双手')
batch('D',1,'deform','''布片对角拉平|Cloth spreading|cloth|P29,P24
布片对折|Cloth folding|cloth|P29,P16
毛巾卷起|Towel rolling|cloth|P29,P21
布片角点拾取|Cloth corner pickup|cloth|P12,P29
绳索牵引|Rope pulling|rope|P24,P29
绳索穿孔|Rope threading|rope,peg|P17,P29
粗绳简单打结|Simple knot tying|rope|P27,P29
粗绳解结|Knot untying|rope|P27,P29
海绵挤压释放|Sponge squeeze-release|sponge|P14,P29,P31
软球局部按压|Local soft-ball press|sponge|P23,P29
弹性圈小幅拉伸|Elastic ring stretch|elastic|P24,P29
弹性圈套杆|Elastic ring placement|elastic,ring|P17,P29
纸张折痕按压|Paper creasing|paper|P23,P29
纸张受控撕开|Paper tearing|paper|P24,P29
密封袋逐段捏封|Bag sealing|bag|P11,P23
黏土搓条|Clay rolling|clay|P21,P29
黏土压扁|Clay flattening|clay|P23,P29
薄膜边缘分离|Film separation|bag|P12,P24''','BULLOCK,OAKINK','P29','grab',hands='双手',difficulty='高阶')
batch('C',1,'contact','''恒定姿态轻握—较紧握|Force level change|sphere,sensor|P10,P31
法向力缓慢增加|Normal-force ramp|sensor|P23,P31
保持接触的切向滑动|Tangential surface slide|surface,sensor|P22,P32
指腹扫描粗糙表面|Texture scanning|surface,sensor|P22,P32
静态握持抗小扰动|Hold under small disturbance|sphere,sensor|P10,P31
不同摩擦表面持握|Friction-conditioned holding|cylinder,surface|P10,P31
低质量与高质量持握|Load-conditioned holding|bottle,weight,sensor|P10,P31
先接触后闭合|Contact-before-close|salt,sensor|P09,P11
只用活动指按压|Active-digit isolation|button,sensor|P10,P23
指腹滚动接触追踪|Contact-patch rolling|sphere,sensor|P21,P32
短时滑移后重新夹紧|Slip-and-recover|cylinder,sensor|P22,P31
受控缓慢卸载|Controlled unloading|sensor|P15,P31''','DEXUMI,BULLOCK','P31','kitchen',difficulty='高阶')
media['arctic']=dict(type='video',url='https://download.is.tue.mpg.de/arctic/static/videos/dexterous.mp4',source='ARCTIC',label='官方演示 · 双手关节物体操作',match='多任务合集，未逐项定位剪刀或笔记本片段')
media['dexmachina']=dict(type='video',url='https://project-dexmachina.github.io/compressed-dexmachina-deanon-teaser.mp4',source='DEXMACHINA',label='官方演示 · 双手功能重定向',match='仿真任务合集；不是每个动作的独立录像')
# All extensions explicitly use reference media rather than falsely claiming per-action demonstrations.
for a in actions:
 if a['origin']=='extension':a['mediaScope']='同类参考；尚无该扩展动作的逐项演示'
 elif a['media']=='grab':a['mediaScope']='项目总览参考，未定位该动作片段'
 elif a['id']=='I03':a['mediaScope']='对比参考：视频仅示朝向重定向，不演示完整 6D 目标'
 else:a['mediaScope']='对应原图或官方任务族演示；详见素材说明'
 if a['category']=='deform':a['success']='记录变形前后关键点、目标形状、接触次序；不得仅用刚体位姿判定成功。'
 if a['category']=='contact':a['success']='力级任务必须有经标定的力 / 触觉记录；视频和 EMG 本身不能直接证明接触力达标。'
 if a['id']=='U08':a['props']=['knife','paper']
 # The 'props' are collection suggestions, not assertions about the source's apparatus.
# Visual QA: thumb opposition/contact is not yet faithful enough in these templates.
for a in actions:
 if a['id'] in {'J09','J10','J11','J12','J13','J14','J18','J19','J29'}:
  a['pose']=None
  a['template_status']='unsupported: thumb coordination requires further geometry/contact review; use official illustration'
families,featured,coverage_gaps=expand(sources,media,primitives,props,actions,add)
data=dict(version='1.1',verified='2026-09-24',sources=sources,media=media,categories=[dict(id=x,label=z,index=y) for x,y,z in categories],primitives=primitives,props=props,actions=actions,families=families,featured=featured,coverage_gaps=coverage_gaps)
ROOT.joinpath('data.js').write_text('window.ATLAS = '+json.dumps(data,ensure_ascii=False,separators=(',',':'))+';\n')
ROOT.joinpath('research/catalog.json').write_text(json.dumps(data,ensure_ascii=False,indent=2))
with ROOT.joinpath('research/actions.csv').open('w',encoding='utf-8-sig',newline='') as f:
 writer=csv.writer(f)
 writer.writerow(['ID','中文动作','英文动作','类别','来源关系','元动作ID','道具ID','定位','来源','链接','演示范围','说明','成功判据建议'])
 for a in actions:
  writer.writerow([a['id'],a['name'],a['en'],a['category'],a['origin'],';'.join(a['primitives']),';'.join(a['props']),a['locator'],';'.join(sources[s]['title'] for s in a['sources']),';'.join(sources[s]['url'] for s in a['sources']),a['mediaScope'],a['description'],a['success']])
ROOT.joinpath('research/coverage-audit.json').write_text(json.dumps(dict(version=data['version'],families=families,gaps=coverage_gaps,counts={k:sum(a['origin']==k for a in actions) for k in ['direct','adapted','extension']}),ensure_ascii=False,indent=2))
provenance_path=ROOT/'research/media-provenance.json'
provenance=json.loads(provenance_path.read_text())
provenance=[p for p in provenance if not p.get('catalog_media_id')]
provenance.extend(dict(catalog_media_id=k,type=m['type'],url=m['url'],source=sources[m['source']]['url'],scope=m['match'],domain=m.get('domain','参考素材'),verified='2026-09-24') for k,m in media.items())
provenance_path.write_text(json.dumps(provenance,ensure_ascii=False,indent=2))
print(f'{len(actions)} actions, {len(primitives)} primitives, {len(props)} props, {len(sources)} sources')
