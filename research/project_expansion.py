"""Four user-supplied project pages: deduplicated tasks, conditions and objects.

Source names and section locators are evidence; capture criteria are authored.
Motion counts never include a shape, seed, control mode or training stage alone.
"""
def expand_projects(sources, media, primitives, props, actions, add, families, featured, gaps):
    before_actions={a['id'] for a in actions}
    before_props={p['id'] for p in props}
    rows=[
        ('PLAY2PERFECT','Play2Perfect','What Matters in Dexterous Play Pretraining for Precise Assembly?','Tyler Ga Wei Lum, Kushal Kedia, C. Karen Liu, Jeannette Bohg','https://play2perfect.github.io/','2606.26428','精密装配、螺纹桌腿、多部件装配与失败重试。浏览器中的充电器、餐叉任务是仿真；不能仅凭 real-size 字样标为实机。'),
        ('ADEPT','ADEPT','ADEPT: Accelerating Dexterity via Pre-Training and Post-Training using Reinforcement Learning','Jayjun Lee, Jessica Yin, Asif Rana, Nicholas Blauch, Sam Mady, Mohak Bhardwaj, Nima Fazeli, Nathan Ratliff, Karl Van Wyk, Ankur Handa','https://adept-dexterity.github.io/','2608.19182','FMB 插销、星形插销、盘子入架；16 primitives 指 16 个几何规格，而非 16 种元动作。预训练教师仿真和实机学生分开标注。'),
        ('WMCRAFT','WM-Craftnet','World Synesthesia Model for Generalizable and Robust Dexterous In-Hand Manipulation','Jie Yin, Zeyuan Zhao, Xiaojing Tan, Yang Liu, Chiyu Wang, Xinyang Gu','https://wmcraftnet.github.io/','2609.07002','跨物体连续旋转、不同轴、失稳恢复和工具平移。Multi-Object 表示轮流更换物体；工具使用是定性展示，不能据此推定全任务成功率。'),
        ('TELEDEXTER','TeleDexter','TeleDexter: Towards Human-level Dexterous Teleoperation','Puhao Li, Zeyuan Chen, Yingying Wu, Pengkun Wei, Yuyang Li, Tianyu Wang, Jiaxiao Shi, Mingrui Yu, Baoxiong Jia, Song-Chun Zhu, Tengyu Liu, Siyuan Huang','https://bigai-dex.github.io/blog/teledexter/','2607.11481','七项评估任务以及连续转笔、抓型转换。完整工具链是遥操作；锤击、装灯泡、刷扫另有自主策略演示。'),
    ]
    for sid,short,title,authors,url,paper,note in rows:
        sources[sid]=dict(short=short,title=title,authors=authors,year='2026',venue='项目页 / arXiv',url=url,doi='10.48550/arXiv.'+paper,note=note)
    def m(mid,sid,path,label,locator,domain='真实机器人',control='自主策略',typ='video'):
        from urllib.parse import urljoin
        media[mid]=dict(type=typ,url=urljoin(sources[sid]['url'],path),source=sid,label=label,match=locator,domain=domain,control=control)
        return mid
    p2='static/videos/'
    m('p2_tight','PLAY2PERFECT',p2+'slowmo_tight_insertion.mp4?v=2','Play2Perfect · 紧配插入','Watch Play2Perfect in Slow Speed / Tight Insertion；网站播放器可调速。')
    m('p2_screw','PLAY2PERFECT',p2+'slowmo_screwing.mp4?v=2','Play2Perfect · 螺纹桌腿旋入','Watch Play2Perfect in Slow Speed / Screwing。')
    m('p2_multi','PLAY2PERFECT',p2+'slowmo_multi_part.mp4','Play2Perfect · 多部件装配','Watch Play2Perfect in Slow Speed / Multi-Part Assembly。')
    m('p2_retry','PLAY2PERFECT',p2+'recovery_1.mp4?v=2','Play2Perfect · 装配失败后重试','Recovery Behavior / 第一段；包含失败和后续重试。')
    m('p2_retry2','PLAY2PERFECT',p2+'recovery_2.mp4?v=2','Play2Perfect · 第二段重试','Recovery Behavior / 第二段。')
    m('p2_interactive','PLAY2PERFECT','interactive/','Play2Perfect · 可交互装配仿真','Select Assembly Task：iPhone Charger into Socket / YCB Fork in Rack；选择任务后播放。','仿真','自主策略',typ='link')
    ad='assets/'
    m('ad_fmb','ADEPT',ad+'gallery/realfmb__kuka_1160.mp4','ADEPT · 双叉 FMB 插销','Rollout gallery / Real / FMB insertion / KUKA–Allegro / Vision-based insert。')
    m('ad_star','ADEPT',ad+'gallery/realfmb__kuka_star.mp4','ADEPT · 星形插销','Rollout gallery / Real / KUKA–Allegro / Star peg。')
    m('ad_touch','ADEPT',ad+'gallery/realfmb__rizon_5824.mp4','ADEPT · 视触觉 FMB 插入','Rollout gallery / Real / Flexiv–Sharpa / Visuo-tactile insert。')
    m('ad_dish','ADEPT',ad+'capabilities/dish-placement.mp4','ADEPT · 盘子翻转并放入架中','Capabilities / Dish-rack placement：Flip · regrasp · transport。')
    m('ad_repose','ADEPT',ad+'method/method-01-pretrain.mp4?v=8741b17','ADEPT · 臂手物体位姿调整','The ADEPT recipe / Reposing pre-training；并行仿真教师，多种几何体。','仿真')
    wm='static/videos/'
    for mid,path,label,loc,domain in [
        ('wm_z',wm+'real_z/consecutive.mp4','Z 轴连续旋转 · 顺序更换物体','Real-world rollout：0–24 s 鸭子，24–35 s 圆柱，35–50 s 十字块，50–73 s 馒头，73–94 s 双缺口块。','真实机器人'),
        ('wm_y',wm+'real_y/screwdriver_y_h264.mp4','Y 轴连续旋转 · 螺丝刀','Diverse Axis / Sim-to-Real / Screwdriver；绕较短方向，不是工具长轴快转。','真实机器人'),
        ('wm_x',wm+'x/3.mp4','X 轴连续旋转 · 阶梯块','Diverse Axis / Tests in Simulation / X-Axis Rotation / Stepped block。','仿真'),
        ('wm_perturb',wm+'real/corner_cube_robust_h264.mp4','扰动后恢复连续旋转','Real-world perturbation recovery：3–5 s、22–25 s 人为扰动。','真实机器人'),
        ('wm_ood',wm+'real_z/duck_recovery.mp4','更换物体后恢复可控抓握','OOD-to-duck recovery：换入鸭子后恢复；不意味着原 OOD 物体也已成功。','真实机器人'),
        ('wm_start',wm+'real/recovery/5_recovery.mp4','侧倒初态扶正后旋转','Challenging-start recovery：0 s switch 侧倒，调整为可旋转状态。','真实机器人'),
        ('wm_palm',wm+'real/recovery/1_recovery.mp4','桶形物滑入掌区后送回','Bucket palm-region recovery：约 6 s 滑入掌区后重新调整并续转。','真实机器人'),
        ('wm_cylinder',wm+'real/recovery/18_recovery.mp4','圆柱受接触扰动后恢复','Cylinder unexpected-contact recovery：约 6 s、15 s。','真实机器人'),
        ('wm_gravity','static/images/north1.mp4','改变掌向时持续旋转','Gravity-Invariant Rotation / Successful sim-to-real transfer。','真实机器人'),
        ('wm_cross',wm+'adjustment/crosscube_adjustment_z_h264.mp4','十字块掌到指转移后旋转','Challenging Initialization Pose / Cross block：0–7 s 掌到指，随后 Z 轴旋转。','仿真'),
        ('wm_bulb',wm+'adjustment/bulb_adjustment_z_h264.mp4','灯泡三指扶正后旋转','Challenging Initialization Pose / Bulb：0–5 s 拇指、食指、中指扶正。','仿真'),
        ('wm_move',wm+'tooluse/screwdriver_h264.mp4','螺丝刀目标位置平移','Application: Tool Use / Goal-conditioned translation；定性仿真，不演示拧螺丝。','仿真'),
        ('wm_axial',wm+'tooluse/screwdriverrot.mp4','螺丝刀长轴快速旋转','Application: Tool Use / Fast screwdriver rotation；定性仿真，不演示紧固。','仿真'),
    ]:m(mid,'WMCRAFT',path,'WM-Craftnet · '+label,loc,domain)
    td='../../assets/videos/teledexter/'
    for kind,label in [('hammer','锤子完整使用链'),('brush','刷子完整使用链'),('screwdriver','螺丝刀完整使用链'),('bulb','灯泡更换完整链')]:
        m('td_'+kind,'TELEDEXTER',td+f'teleop_demo/tele_{kind}-1.mp4','TeleDexter · '+label,'Full Task Teleoperation / '+label+' / 第 1 次演示。',control='遥操作')
    m('td_pen','TELEDEXTER',td+'any2any/penspin_long-1.mp4','TeleDexter · 连续转笔','In-Hand Manipulation / long-horizon pen spinning。',control='遥操作')
    m('td_penrecover','TELEDEXTER',td+'any2any/penspin_recover-1.mp4','TeleDexter · 转笔中恢复','In-Hand Manipulation / mid-spin recovery。',control='遥操作')
    for obj,label in [('cuboid','长方体'),('cylinder','圆柱')]:m('td_'+obj,'TELEDEXTER',td+f'any2any/a2a-leaphand_{obj}.mp4','TeleDexter · '+label+'抓型转换','Any-grasp-to-any-grasp / Leap Hand / '+obj+'；物体与手的目标同时变化。',control='遥操作')
    for kind,label in [('hammer','锤击'),('brush','刷扫'),('bulb','安装灯泡')]:m('td_policy_'+kind,'TELEDEXTER',td+f'policy/policy-{kind}-1.mp4','TeleDexter · 自主'+label,'Autonomous Policy Learning / '+label+'；这是单项策略，不是完整遥操作链。')
    # Posters extracted from explicit video attributes on the four source pages.
    from pathlib import Path
    import json
    index=Path(__file__).with_name('project-media-index.json')
    if index.exists():
        known=json.loads(index.read_text())
        for mm in media.values():
            if mm['url'] in known and known[mm['url']].get('poster'):
                mm['poster']=known[mm['url']]['poster']
    by={a['id']:a for a in actions}
    def evidence(aid,mid,label=None,scope=None,relation='对应任务 / 条件',objects=()):
        a=by[aid];mm=media[mid]
        if mm['source'] not in a['sources']:a['sources'].append(mm['source'])
        a.setdefault('evidence',[]).append(dict(source=mm['source'],media=mid,label=label or mm['label'],locator=mm['match'],scope=scope or mm['match'],relation=relation,props=list(objects)))
        a['props']=list(dict.fromkeys(a['props']+list(objects)))
    def task(aid,name,en,cat,ps,objects,mid,desc,success,origin='direct',level='完整任务',parent=None):
        mm=media[mid]
        add(aid,name,en,cat,ps,objects,mm['source'],mm['match'],desc,success,origin=origin,demo=mid,difficulty='高阶',variation='记录初态、目标、几何尺寸、摩擦、接触切换和失败原因；遥操作与自主策略、仿真与实机分别建条件。')
        a=actions[-1];a.update(mediaScope=mm['domain']+' · '+mm['control']+'；'+('完整任务中的子步骤，非独立子任务录像。' if origin=='adapted' else '对应范围以本段素材说明为准。'),granularity=level,aliases=[],added_in='1.2')
        if parent:a['parent']=parent
        by[aid]=a
        evidence(aid,mid,objects=objects.split(','),relation='任务子步骤' if origin=='adapted' else '直接来源任务')
    for pid,name,en,definition,observe,sids in [
        ('P36','对准并约束插入','Align and insert','将零件对准配合特征，在接触约束下沿插入方向推进。','轴线与孔型、配合间隙、插入深度、碰撞与卡滞',['PLAY2PERFECT','ADEPT']),
        ('P37','工具冲击','Tool impact','握持工具，通过短时冲击改变目标物状态。','接触前速度、冲击时刻、工具姿态、目标位移',['TELEDEXTER']),
    ]:primitives.append(dict(id=pid,name=name,en=en,definition=definition,observe=observe,source=sids))
    # New tasks use invariant goals and contact changes, not object names alone.
    task('I35','侧倒初态恢复后持续旋转','Upright a fallen initial grasp and resume rotation','inhand','P10,P18,P20','switch_object','wm_start','从侧倒、不利抓握初态调整物体，使其进入可持续旋转的接触构型。不同于执行中受到扰动。','记录初始侧倒方向、扶正时间、恢复后旋转进展和掉落。')
    task('I36','物体滑入掌区后送回并续转','Palm-region recovery during rotation','inhand','P10,P17,P20,P30','toy_bucket,cylinder','wm_palm','旋转中的物体进入掌区后，手指将其送回可控工作区并继续旋转；保留失稳到恢复的全过程。','分别记录掌区进入、返回工作区、恢复连续旋转三项事件；不能只截取成功终态。')
    evidence('I36','wm_cylinder')
    task('I37','改变手掌朝向时保持手内旋转','Continuous rotation under changing palm orientation','inhand','P07,P10,P18,P20','cylinder','wm_gravity','手掌相对重力方向变化时，保持物体相对手掌持续旋转。属于持续旋转的重力条件，单列为采集条件入口。','同时记录世界系掌姿和掌系物体姿态；腕部转动不能替代手内角进展。',level='条件协议')
    task('I38','手与物体联合目标下的抓型转换','Any-grasp-to-any-grasp hand-object tracking','inhand','P10,P18,P19,P20','cube,cylinder','td_cuboid','跟踪同时给定的手姿与物体姿态，从初始抓型切换到目标抓型。与只要求物体终点朝向的重定向区分。','分别记录手部目标误差、物体位姿误差、接触切换和滑落；不能仅以物体到达评价。')
    evidence('I38','td_cylinder')
    task('I39','螺丝刀在手内移到目标位置','Goal-conditioned in-hand tool translation','inhand','P10,P17,P20','screw','wm_move','维持工具接触，把螺丝刀在手内调整到目标位置。来源为定性仿真展示；不把位置目标夸大成完整 6D 跟踪。','在声明的坐标系中记录位置误差和接触；补充掌系位移用于排除腕臂搬运。')
    task('T21','翻转并重抓盘子后放入碗碟架','Dish flip, regrasp and rack placement','transfer','P08,P10,P18,P20,P16,P36,P15','plate,dish_rack','ad_dish','拾取盘子，翻转和改变抓握，搬运并放入碗碟架。终点受架槽约束，与普通圆盘持握或自由放置不同。','盘子进入目标槽并在释放后稳定；分别标记翻转、重抓、入架与释放。')
    task('T22','机械臂与手协同调整物体目标位姿','Arm-hand object reposing','transfer','P08,P09,P10,P16,P18,P19,P20','cube,sphere,capsule,cone','ad_repose','ADEPT 的预训练教师在臂手系统中完成物体位姿调整。目标涉及工作空间搬运与手内重定向，不将其直接等同于固定掌系的 I03。','同时报告工作空间目标误差和掌系相对运动；明确臂、腕、指各自贡献。')
    task('U39','手持螺纹桌腿对准并旋入底座','Threaded table-leg screwing','tool','P10,P18,P20,P25,P36','threaded_leg','p2_screw','抓住带螺纹的桌腿状构件，调整到螺纹座并旋入。被驱动的是整个零件，而非用螺丝刀驱动螺钉。','记录啮合、轴向进给、旋转量和卡扣 / 螺纹卡滞，按夹具终态判断完成。')
    task('U40','分阶段多部件精密装配','Multi-part sequential assembly','tool','P08,P10,P18,P20,P36,P15','multipart_kit','p2_multi','依次操纵不同部件完成两阶段装配；记录已装入部件如何改变后续配合约束。区别于双手拼合两个普通积木。','逐阶段记录取件、重定向、配合完成；所有部件均到位才记完整任务成功。')
    task('U41','单手调整充电器并插入插座模型','Charger insertion into socket','tool','P10,P18,P20,P36','plug','p2_interactive','在 Play2Perfect 浏览器仿真中选择 iPhone Charger into Socket；单只灵巧手调整刚性充电器并插入。原 B11 是双手扶线插接。','记录插头方向、对准误差与插入深度；若采集实物，使用无电配合模型。')
    task('U42','餐叉重定向后插入收纳架','YCB fork insertion into rack','tool','P10,P18,P20,P36,P15','fork,fork_rack','p2_interactive','在浏览器仿真中选择 YCB Fork in Rack。这里的 fork 是餐叉，与双叉异形插销不是同一个道具。','餐叉朝向、位置与收纳架匹配，进入指定位置；记录滑落、碰架和重抓。')
    task('U43','装配失败后重新对准并重试','Closed-loop assembly retry after failure','tool','P10,P17,P18,P20,P36','peg,multipart_kit,threaded_leg','p2_retry','在未完成配合或初次尝试失败后继续调整抓握与位姿，再次装配。是装配任务的恢复阶段，不是一个新的配合几何。','记录每次失败、重新对准与最终完成的时间；保留失败试次，避免只统计最后一段。',level='恢复子任务')
    evidence('U43','p2_retry2')
    task('U44','锤子换面：敲入、拔钉并放回','Hammer use with functional reorientation','tool','P08,P10,P18,P20,P26,P37,P24,P15','hammer,nail_board','td_hammer','拾取 → 锤面朝下 → 敲钉 → 转成羊角朝下 → 拔钉 → 重定向 → 放回。相同工具在不同阶段需要不同功能朝向。','分别标注 7 个阶段、锤面 / 羊角方向及钉子状态；全链完成才计任务成功。')
    task('U45','持锤敲入钉子','Hammer driving a nail','tool','P10,P26,P37','hammer,nail_board','td_policy_hammer','保持锤子功能朝向，通过冲击将钉子敲入板中；来源另有自主策略录像。','记录冲击时刻、接触位置和钉子推进量；区分挥动与有效敲击。',level='工具子任务',parent='U44')
    task('U46','转为羊角抓型并拔钉','Claw-hammer nail extraction','tool','P10,P18,P20,P24,P26','hammer,nail_board','td_hammer','完整 Hammer Use 中将羊角对准钉子并拔出；使用原完整录像作为子步骤参考。','记录羊角嵌合、工具支点及钉子拔出；单纯上提锤子不算成功。',origin='adapted',level='工具子任务',parent='U44')
    task('U47','刷子重定向并向不同方向刷扫','Brush use with directional reorientation','tool','P08,P10,P18,P20,P22,P26,P15','brush','td_brush','拾取 → 重定向 → 向前刷扫 → 刷毛转向右侧 → 向右刷扫 → 重定向 → 放回。方向是阶段目标，不再拆成多个新动作。','检查各阶段刷毛与表面的接触和方向；记录工具朝向切换是否在手内完成。')
    task('U48','保持刷毛接触并刷扫','Brush sweeping','tool','P10,P22,P26','brush','td_policy_brush','保持刷毛朝向目标表面并执行刷扫；来源有独立自主策略演示。','记录扫过区域、刷毛接触区和路径；视频不能单独证明接触力。',level='工具子任务',parent='U47')
    task('U49','螺丝刀拾取、换抓、拧紧并放回','Screwdriver use with functional reorientation','tool','P08,P10,P18,P20,P25,P26,P15','screw','td_screwdriver','拾取 → 转到可用抓型 → 拧紧螺丝 → 重定向 → 放回。已有 U07 对应其中紧固步骤，本条补入完整功能抓型切换链。','分别检查 5 个阶段；保留工具在手内的抓型变化与螺丝的实际推进。')
    task('U50','灯泡重定向、旋入、旋出并放回','Bulb replacement with functional reorientation','tool','P08,P10,P18,P20,P25,P36,P15','bulb,bulb_socket','td_bulb','拾取 → 重定向 → 旋入灯座 → 旋出 → 重定向 → 放回；原站为六阶段遥操作链。','分别记录 6 个阶段、灯泡相对灯座的转角与轴向位移。')
    task('U51','对准灯座并旋入灯泡','Bulb installation','tool','P10,P25,P36','bulb,bulb_socket','td_policy_bulb','将灯泡与灯座对准、螺纹啮合并旋入；来源包含独立自主策略演示。','确认啮合与轴向进给；按装配终态评估，不能仅看灯泡转动。',level='工具子任务',parent='U50')
    task('U52','旋出并取下灯泡','Bulb unscrewing and removal','tool','P10,P25,P24','bulb,bulb_socket','td_bulb','完整 Bulb Replace 中旋出灯泡并与灯座分离；原录像同时包含安装与移除。','记录反向旋转、退出螺纹及稳定取下三阶段。',origin='adapted',level='工具子任务',parent='U50')
    # Existing entries retain stable IDs and broaden only where the evidence matches.
    evidence('I01','wm_z',objects=['duck','cylinder','cross_block','bun','notched_block'])
    evidence('I01','wm_y',objects=['screw'])
    evidence('I01','wm_x',objects=['stepped_block'])
    evidence('I01','wm_axial',objects=['screw'])
    evidence('I32','td_pen',objects=['pen'])
    evidence('I32','td_penrecover',scope='连续转笔中失稳恢复，是该动作的恢复条件；不是新增转笔花式。')
    evidence('I02','td_cuboid',scope='对象重定向的相关证据；原演示还跟踪手部目标，完整联合目标动作见 I38。',relation='相关任务片段',objects=['cube','cylinder','bunny'])
    evidence('I05','wm_cross',scope='十字块掌到指转移子步骤（0–7 s），不是原硬币任务的逐项录像。',relation='不同道具的转移变体',objects=['cross_block'])
    evidence('I28','wm_perturb',scope='支持恢复可控抓握并续转；没有声明返回指定的完整 6D 目标。',objects=['corner_block'])
    evidence('I28','wm_ood',scope='更换为鸭子后恢复可控抓握；不代表扰动前后的物体一致。',objects=['duck'])
    evidence('U07','td_screwdriver',scope='完整遥操作链中的紧固阶段；原 NinaPro 动作图仍保留。',relation='完整录像中的子步骤')
    for mid,objs in [('p2_tight',['peg']),('ad_fmb',['fmb_double']),('ad_star',['fmb_star']),('ad_touch',['fmb_double'])]:evidence('U17',mid,objects=objs)
    a=by['U17'];a.update(origin='direct',sources=['PLAY2PERFECT','ADEPT','BULLOCK','NINA'],locator=media['p2_tight']['match'],media='p2_tight',mediaScope='紧配插入任务的实机演示；双叉 / 星形 FMB 插销在下方切换。',description='对准配合形状并推进插销。紧配插入、方圆双叉和星形插销作为几何条件；同一动作 ID 下保留各自演示。',primitives=['P10','P17','P18','P20','P36'])
    # All newly encountered object classes. Variants record object identities, not new skills.
    def prop(pid,name,group,spec,use,sid,loc,domain,variants=()):
        props.append(dict(id=pid,name=name,group=group,spec=spec,use=use,added_in='1.2',variants=list(variants),evidence=[dict(source=sid,locator=loc,domain=domain)]))
    for pid,name,group,spec,use,sid,loc,domain in [
        ('threaded_leg','螺纹桌腿与配合底座','装配','记录螺距、牙型、啮合长度和桌腿几何','整个构件旋入','PLAY2PERFECT','Screwing / interactive preview','真实机器人 + 仿真'),
        ('multipart_kit','多部件精密装配套件','装配','记录各部件编号、接口和阶段顺序','两阶段装配与重试','PLAY2PERFECT','Multi-Part Assembly / Step 1 / Step 2','真实机器人 + 仿真'),
        ('fmb_double','方形与圆形双叉 FMB 插销及孔座','装配','记录双叉间距、截面、孔位与间隙','多约束对准插入','ADEPT','Capabilities / FMB peg insertion','真实机器人 + 仿真'),
        ('fmb_star','星形 FMB 插销与孔座','装配','记录齿数、对称性和配合角度','异形插销定向插入','ADEPT','Capabilities / FMB star-peg insertion','真实机器人'),
        ('plate','盘子','日用品','记录厚度、直径、边缘形状与质量','翻转、重抓、入架','ADEPT','Dish-rack placement；teal / red plate','真实机器人 + 仿真'),
        ('dish_rack','碗碟架','装配','记录槽宽、间距、倾角与容差','盘子受限放置','ADEPT','Dish-rack placement','真实机器人 + 仿真'),
        ('fork','YCB 餐叉','餐具','记录叉头、柄长和接触几何；实物数采规格另行确认','细长餐具重定向','PLAY2PERFECT','Interactive / YCB Fork in Rack','仿真'),
        ('fork_rack','餐叉收纳架','装配','记录槽口与叉具配合特征','餐叉定向插入','PLAY2PERFECT','Interactive / YCB Fork in Rack','仿真'),
        ('hammer','羊角锤','工具','同时记录锤面、羊角与握柄的几何关系','敲击与拔钉功能切换','TELEDEXTER','Hammer Use / 7 stages','真实机器人'),
        ('nail_board','钉子与敲拔练习板','任务对象','记录钉径、露出长度、板材与固定方式','锤击推进及羊角拔取','TELEDEXTER','Hammer Use / drive nails / pull nails','真实机器人'),
        ('brush','长柄刷与刷扫表面','工具','记录刷毛长度、柔顺性及表面材料','朝向切换与接触刷扫','TELEDEXTER','Brush Sweep / 7 stages','真实机器人'),
        ('bulb','灯泡 / 灯泡形模型','日用品','旋转试件与螺纹装配件区分；记录重心、柄径和螺纹','灯泡旋转、扶正、安装与拆卸','TELEDEXTER','Bulb Replace / 6 stages','真实机器人'),
        ('bulb_socket','螺口灯座模型','装配','无电装配模型；记录螺纹和底座固定方式','灯泡旋入和旋出','TELEDEXTER','Bulb Replace / installation policy','真实机器人'),
        ('capsule','胶囊体 / 圆端长杆组','几何体','ADEPT 原规格，单位 mm：80×80×105、80×80×90、80×80×180、50×50×150、50×50×250、20×20×220；训练另有尺度随机化','重抓与目标位姿调整','ADEPT','Pre-training diet / primitives 09–14','仿真'),
        ('cone','圆锥体组','几何体','ADEPT 原规格，单位 mm：100×100×100、50×50×100','非均匀截面的位姿调整','ADEPT','Pre-training diet / primitives 15–16','仿真'),
        ('duck','鸭子模型','不规则形体','记录突出部位、重心与材质','旋转与扰动恢复','WMCRAFT','Real-World Z-Axis Rotation / Duck','真实机器人 + 仿真'),
        ('piggy','小猪储蓄罐模型','不规则形体','记录非轴对称外形、质量与填充情况','连续旋转与初态调整','WMCRAFT','Z-Axis Rotation / Piggy Bank','真实机器人 + 仿真'),
        ('apple','苹果模型','不规则形体','记录曲率、凹部与朝向标记','Z 轴旋转','WMCRAFT','Tests in Simulation / Z-Axis / Apple','仿真'),
        ('strawberry','草莓模型','不规则形体','记录锥状外形与表面纹理','连续旋转与接触变化','WMCRAFT','Real-World Z-Axis Rotation / Strawberry','真实机器人 + 仿真'),
        ('bun','馒头状模型','不规则形体','按原项目形体记录；不能因名称推定为柔性食物','跨物体连续旋转','WMCRAFT','Continuous real-world rollout / 50–73 s','真实机器人'),
        ('fire_hydrant','消防栓模型','不规则形体','记录侧向突出结构','突出部件旋转避碰','WMCRAFT','Real-World Z-Axis Rotation / Fire hydrant','真实机器人'),
        ('cross_block','十字块','几何体','记录各臂长度、粗细与交汇形状','持续旋转、掌指转移','WMCRAFT','Cross block / palm-to-finger transfer','真实机器人 + 仿真'),
        ('corner_block','拐角块','几何体','记录拐角尺寸和凸棱','连续旋转、扰动恢复','WMCRAFT','Corner block / perturbation recovery','真实机器人 + 仿真'),
        ('notched_block','缺口块 / 缺口圆柱组','几何体','记录单 / 双缺口、窄体版本；块状与柱状不混用几何模型','未见几何旋转','WMCRAFT','Zero-Shot Transfer / notched, narrow, double-notched；Z-axis double-notched cylinder','真实机器人 + 仿真'),
        ('stepped_block','阶梯块','几何体','记录台阶高差与截面','X 轴连续旋转','WMCRAFT','Tests in Simulation / X-Axis / Stepped block','仿真'),
        ('lego_brick','凸点积木','几何体','记录凸点、凹槽、长宽高','X 轴连续旋转','WMCRAFT','Tests in Simulation / X-Axis / Lego Brick','仿真'),
        ('can','易拉罐模型','日用品','记录半径、长度、质量与是否为空罐','初态扶正和轴向旋转','WMCRAFT','Coca Can / Z, Y axes / initialization','仿真'),
        ('toothpaste','牙膏管状物','日用品','记录扁平尾部、盖端及是否可变形','短轴连续旋转','WMCRAFT','Real Y-Axis Rotation / Toothpaste','真实机器人 + 仿真'),
        ('flashlight','手电筒模型','日用品','记录头部与柄部直径、重心','Y 轴连续旋转','WMCRAFT','Tests in Simulation / Y-Axis / Flashlight','仿真'),
        ('toy_bucket','玩具桶 / 垃圾桶形模型','日用品','保留桶形结构，标记开口、凸缘与底部','掌区失稳恢复及旋转','WMCRAFT','Bucket palm-region recovery / Toy Trashcan','真实机器人 + 仿真'),
        ('switch_object','开关形旋转试件','不规则形体','独立试件，不等同于固定按钮板；记录侧倒初态','初态恢复后续转','WMCRAFT','Challenging-start recovery / switch','真实机器人'),
        ('bunny','兔子模型','不规则形体','记录耳部突出几何和物体身份','BunnyReorient 物体朝向调整','TELEDEXTER','Seven-task evaluation / BunnyReorient；无单独直链','真实机器人'),
    ]:prop(pid,name,group,spec,use,sid,loc,domain)
    pb={p['id']:p for p in props}
    def pe(pid,sid,locator,domain,variants=()):
        pb[pid].setdefault('evidence',[]).append(dict(source=sid,locator=locator,domain=domain))
        pb[pid].setdefault('variants',[]).extend(variants)
    pe('cube','ADEPT','Pre-training diet / primitives 01–06','仿真',['长方体 mm：50×100×100、50×50×100、25×100×100、25×50×100、25×25×100、10×100×100'])
    pb['cube']['name']='方块 / 长方体组'
    pe('sphere','ADEPT','Pre-training diet / primitives 07–08','仿真',['原始球体直径 100 mm、50 mm；尺度随机化另记'])
    pe('cylinder','WMCRAFT','Z-Axis / Cylinder；Y-Axis / Corner Cylinder','真实机器人 + 仿真',['常规圆柱','拐角圆柱（Y 轴仿真）'])
    pe('bottle','WMCRAFT','Y-Axis / Bottle；Challenging Initialization Pose','仿真',['瓶体重心与柄口结构'])
    pe('plug','PLAY2PERFECT','Interactive / iPhone Charger into Socket','仿真',['刚性 iPhone 充电器与插座配合；区别于带线双手插接'])
    pe('peg','PLAY2PERFECT','Tight Insertion','真实机器人 + 仿真',['紧配插入件与孔座，记录配合几何'])
    pe('pen','TELEDEXTER','Pen spinning / long take / recovery','真实机器人')
    pe('screw','TELEDEXTER','Screwdriver Use / 5 stages','真实机器人')
    pe('screw','WMCRAFT','Tool Use translation / axial rotation；real Y-axis','仿真平移 / 长轴；实机 Y 轴')
    pe('bulb','WMCRAFT','Bulb / Z-axis / initialization','真实机器人 + 仿真',['灯泡形旋转试件；不推定具备可装配螺纹'])
    # Source-specific object conditions for rotation, without manufacturing new action IDs.
    extra=['piggy','apple','strawberry','fire_hydrant','bulb','corner_block','lego_brick','can','toothpaste','flashlight','toy_bucket','bottle']
    by['I01']['props']=list(dict.fromkeys(by['I01']['props']+extra))
    evidence('I01','wm_z',label='跨物体集合与演示范围',scope='本视频只展示鸭子、圆柱、十字块、馒头、双缺口块；其余道具见原站同章节及 X/Y 轴小节。不能把一个视频当成全部道具录像。',relation='道具集合 / 分项定位见道具库',objects=extra)
    # Individual clips preserve all named rotation objects without duplicate tasks.
    for pid,path,label,domain in [
        ('duck','color/duck.mp4','鸭子 · Z 轴','真实机器人'),
        ('corner_block','real/comparison/ours.mp4','拐角块 · Z 轴','真实机器人'),
        ('cross_block','real_z/crosscube.mp4','十字块 · Z 轴','真实机器人'),
        ('cylinder','color/cylinder1.mp4','圆柱 · Z 轴','真实机器人'),
        ('piggy','color/piggybank2.mp4','储蓄罐 · Z 轴','真实机器人'),
        ('strawberry','color/strawberry.mp4','草莓 · Z 轴','真实机器人'),
        ('fire_hydrant','color/firehydrant_red2.mp4','消防栓 · Z 轴','真实机器人'),
        ('cube','color/block_blue.mp4','蓝色方块 · Z 轴','真实机器人'),
        ('bulb','color/bulb_yellow.mp4','灯泡 · Z 轴','真实机器人'),
        ('apple','z/2.mp4','苹果 · Z 轴','仿真'),
        ('notched_block','z/8.mp4','双缺口圆柱 · Z 轴','仿真'),
        ('notched_block','unseen/unseen_h264.mp4','单缺口 / 窄体 / 双缺口块 · 未见物体','仿真'),
        ('toothpaste','real_y/toothpaste_y_h264.mp4','牙膏管 · Y 轴短轴','真实机器人'),
        ('corner_block','real_y/cornerblock_y_h264.mp4','拐角块 · Y 轴','真实机器人'),
        ('toy_bucket','y/0.mp4','玩具垃圾桶 · Y 轴','仿真'),
        ('cylinder','y/3.mp4','拐角圆柱 · Y 轴','仿真'),
        ('can','y/5.mp4','易拉罐 · Y 轴','仿真'),
        ('flashlight','y/7.mp4','手电筒 · Y 轴','仿真'),
        ('bottle','y/8.mp4','瓶子 · Y 轴','仿真'),
        ('lego_brick','x/4.mp4','凸点积木 · X 轴','仿真'),
    ]:
        mid='wm_object_'+pid+'_'+str(len(media))
        m(mid,'WMCRAFT',wm+path,'WM-Craftnet · '+label,'One Policy for Multi-Object Rotation / Diverse Axis / '+label,domain)
        evidence('I01',mid,objects=[pid],relation='物体 / 轴条件，非新增动作')
    evidence('I35','wm_bulb',objects=['bulb'])
    for aid,pid,path,label,loc in [
        ('I36','bottle','bottle_adjustment_y_h264.mp4','拇指引导瓶体回到工作区','0–10 s 拇指调整瓶子靠近手指，随后 Y 轴旋转'),
        ('I35','can','cokecan_adjustment_z_h264.mp4','五指扶正易拉罐','0–5 s 五指扶正，随后 Z 轴旋转'),
        ('I36','corner_block','cornercube_adjustment_z_h264.mp4','拇指与小指调整拐角块','0–4 s 引导至掌指交界，随后 Z 轴旋转'),
        ('I35','piggy','piggy_bank_adjust_z_h264.mp4','五指调整储蓄罐初态','0–5 s 五指调整至可控区域，随后 Z 轴旋转'),
    ]:
        mid='wm_init_'+pid;m(mid,'WMCRAFT',wm+'adjustment/'+path,'WM-Craftnet · '+label,'Challenging Initialization Pose / '+loc,'仿真')
        evidence(aid,mid,scope='初态调整的仿真变体；'+loc+'。不表示该物体具有主要实机录像中的同一初始状态。',relation='相关恢复变体',objects=[pid])
    for pid,n in [('cube','01'),('sphere','07'),('capsule','09'),('cone','15')]:
        pb[pid]['image']='https://adept-dexterity.github.io/assets/primitives/'+n+'.png'
        pb[pid]['imageLabel']='ADEPT 几何示意 · 原规格之一'
    by['I02'].setdefault('objectEvidence',[]).append(dict(source='TELEDEXTER',prop='bunny',locator='Seven-task evaluation / BunnyReorient',scope='任务名称与物体明确列出；所选 cuboid 视频不展示兔子。'))
    by['I01']['aliases']+=['X轴旋转','Y轴旋转','Z轴旋转','短轴旋转','长轴旋转','跨物体','WM-Craftnet']
    for aid in ['I35','I36','I37','I38','I39','T21','T22','U39','U40','U41','U42','U43','U44','U45','U46','U47','U48','U49','U50','U51','U52']:
        by[aid]['aliases'] += [sources[s]['short'] for s in by[aid]['sources']]
    # Coverage map explicitly states overlapping task / subtask / condition granularity.
    fm={f['id']:f for f in families}
    for fid,ids,gap in [
        ('spin',['I37'],'新增 X / Y / Z 轴及变掌向演示；轴的坐标定义需按原项目记录，跨物体不等于同时多物体。'),
        ('pose',['I39','T22'],'已有工具目标平移和臂手重定向的仿真；固定掌系 I03 的完整 6D 仍需独立逐项演示。'),
        ('gait',['I38','T21','U44','U47','U49','U50'],'新增联合手物目标和功能工具换抓。完整工具链为实机遥操作，不能当成自主策略全链。'),
        ('palm',['I35','I36'],'新增实机失稳恢复；十字块掌到指子步骤为仿真参考，不是硬币转移录像。'),
        ('tool',['U44','U45','U46','U47','U48','U49','U50','U51','U52'],'锤击、刷扫、装灯泡有单项自主策略；完整七 / 五 / 六阶段工具链是遥操作。'),
        ('force',['I35','I36','U43'],'增加实机扰动恢复、初态扶正与装配重试；视频不证明接触力或全局成功率。'),
    ]:
        fm[fid]['actions']=list(dict.fromkeys(fm[fid]['actions']+ids));fm[fid]['gap']=gap
    families.append(dict(id='assembly',name='精密装配与受限放置',actions=['U17','U39','U40','U41','U42','U43','T21','U51'],definition='对准配合特征、进入约束并完成装配；区分插入、螺纹啮合、分阶段装配和失败重试。',gap='Play2Perfect / ADEPT 提供实机装配；充电器和餐叉来自浏览器仿真。配合间隙未在页面统一披露，不能臆造。'))
    featured[:]=['I01','U39','U40','T21','U44','I38','I35','I36','I37','U17','U47','U50','I32','I33','U41','U42','I39','T22','I02','I03']
    gaps[1]='变掌向旋转已加入 WM-Craftnet 实机证据；触觉闭环完全盲操作仍需独立核对，传感条件不能直接当作新任务。'
    audit=[]
    notes={
        'PLAY2PERFECT':'紧配插入并入 U17；新增螺纹桌腿、多部件装配、刚性充电器插接、餐叉入架和重试。仿真菜单确认 charger / fork，未把叉子误记为叉形插销。',
        'ADEPT':'FMB 方圆双叉、星形插销和视触觉版本并入 U17；盘子入架、臂手协同 reposing 新建。16 个几何规格归入已有方块 / 球及新增胶囊 / 圆锥道具。',
        'WMCRAFT':'轴向、形状、控制策略不重复计为动作。新建恢复、重力条件入口与工具平移；未见物体测试归为条件，失败案例不冒充成功演示。',
        'TELEDEXTER':'连续转笔并入 I32、重定向并入 I02；新建联合抓型转换和完整工具链。工具链与可独立采集子步骤有父子关联，不能把条目数当独立能力数。',
    }
    for sid,*_ in rows:
        related=[a['id'] for a in actions if sid in a['sources']]
        audit.append(dict(source=sid,new_actions=[x for x in related if x not in before_actions],enriched_actions=[x for x in related if x in before_actions],new_props=[p['id'] for p in props if p['id'] not in before_props and any(e['source']==sid for e in p.get('evidence',[]))],existing_props=[p['id'] for p in props if p['id'] in before_props and any(e['source']==sid for e in p.get('evidence',[]))],note=notes[sid]))
    return dict(version='1.2',date='2026-09-24',projects=audit,new_action_count=len(actions)-len(before_actions),new_prop_count=len(props)-len(before_props),enriched_action_count=len({a for p in audit for a in p['enriched_actions']}),granularity_note='条目包含完整任务、工具子任务、恢复子任务与条件协议；父子任务与条件不应相加解释为独立技能数量。')
