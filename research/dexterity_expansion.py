"""Source-backed additions and an explicit, non-exhaustive dexterity coverage map."""
def expand(sources, media, primitives, props, actions, add):
    source_rows = [
        ('PENSPIN','PenSpin · CoRL 2024','Lessons from Learning to Spin “Pens”','Jun Wang, Ying Yuan, Haichuan Che, Haozhi Qi, Yi Ma, Jitendra Malik, Xiaolong Wang','2024','CoRL','https://penspin.github.io/','10.48550/arXiv.2407.18902','细长物体连续转笔；有实机视频及失败案例，不能用普通块状物旋转代替。'),
        ('DACTYL','Dactyl · 2018','Learning Dexterous In-Hand Manipulation','OpenAI, Marcin Andrychowicz et al.','2018','arXiv','https://arxiv.org/abs/1808.00177','10.48550/arXiv.1808.00177','实机重定向，报告自发换指、多指协调和受控利用重力。重力辅助在本库被拆成观察子任务。'),
        ('CUBE','Dactyl Rubik · 2019','Solving Rubik’s Cube with a Robot Hand','OpenAI, Ilge Akkaya et al.','2019','arXiv / official project','https://openai.com/index/solving-rubiks-cube/','10.48550/arXiv.1910.07113','区分整体翻转 cube flip 与顶层面转 face rotation；魔方有内部自由度。'),
        ('DEXGYM','Dexterous Gym · ICML 2021','Solving Challenging Dexterous Manipulation Tasks With Trajectory Optimisation and Reinforcement Learning','Henry Charlesworth, Giovanni Montana','2021','ICML','https://dexterous-manipulation.github.io/','10.48550/arXiv.2009.05104','双手交接、抛接及转笔任务。本站采用的视频为仿真，不代表实机成功。'),
        ('DIFFHAND','Visuomotor Diffusion · 2025','Learning Dexterous In-Hand Manipulation with Multifingered Hands via Visuomotor Diffusion','Piotr Koczy, Michael C. Welle, Danica Kragic','2025','arXiv','https://dex-manip.github.io/','10.48550/arXiv.2503.02587','四指 Allegro 单手拧盖；同时保持瓶体和驱动瓶盖，区别于另一手或夹具固定瓶身。'),
        ('PDDM','PDDM · CoRL 2019','Deep Dynamics Models for Learning Dexterous Manipulation','Anusha Nagabandi, Kurt Konolige, Sergey Levine, Vikash Kumar','2019 / proceedings 2020','CoRL · PMLR 100','https://bair.berkeley.edu/blog/2019/09/30/deep-dynamics/','10.48550/arXiv.1909.11652','掌内双球协调有实机结果；任意笔尖轨迹等另有仿真展示，证据需逐项区分。'),
        ('PIANO','RoboPianist · CoRL 2023','RoboPianist: Dexterous Piano Playing with Deep Reinforcement Learning','Kevin Zakka, Philipp Wu, Laura Smith et al.','2023','CoRL','https://kzakka.com/robopianist/','10.48550/arXiv.2304.04150','双手多指精确时序击键的仿真基准；音乐曲目不在本库逐首计为新动作。'),
    ]
    for id,short,title,authors,year,venue,url,doi,note in source_rows:
        sources[id]=dict(short=short,title=title,authors=authors,year=year,venue=venue,url=url,doi=doi,note=note)
    media_rows = [
        ('hora_multi','video','https://haozhi.io/hora/results/multi_tennis.mp4','HORA','HORA · 多轴旋转','Multi-Axis Rotation Policy 小节；轴向切换，不等同于任意终点朝向。','真实机器人'),
        ('penspin','video','https://penspin.github.io/videos/teaser_web.mp4','PENSPIN','PenSpin · 连续转笔','官方 teaser；细长物体和换指过程。','真实机器人'),
        ('dactyl','youtube','https://www.youtube.com/embed/jwSbzNHGflM','DACTYL','Dactyl · 重定向与自发操作策略','论文摘要链接的总览；未逐帧定位重力辅助片段。','真实机器人'),
        ('rubik','link','https://openai.com/index/solving-rubiks-cube/','CUBE','Dactyl · 魔方完整求解','原站包含完整求解及扰动演示；请在原站播放，未取得稳定直链。','真实机器人'),
        ('onehand_lid','video','https://dex-manip.github.io/videos/policy_demo.mp4','DIFFHAND','Allegro · 单手拧开瓶盖','Experiments / Best policy evaluation。','真实机器人'),
        ('baoding','gif','https://bair.berkeley.edu/static/blog/deep-dynamics/image12.gif','PDDM','PDDM · 掌内双球轮转','Figure 4 最右：约 2 小时训练后的实机展示。','真实机器人'),
        ('pencil_path','gif','https://bair.berkeley.edu/static/blog/deep-dynamics/image14.gif','PDDM','PDDM · 笔尖轨迹','Figure 7 仿真手写展示；允许手指和手腕共同运动。','仿真'),
        ('catch_under','video','https://dexterous-manipulation.github.io/videos/eggcatchunderarm_topdm.webm','DEXGYM','Dexterous Gym · 下手抛接','Results / EggCatchUnderarm / TOPDM。','仿真'),
        ('catch_over','video','https://dexterous-manipulation.github.io/videos/eggcatchoverarm_topdm.webm','DEXGYM','Dexterous Gym · 上手抛接','Results / EggCatchOverarm / TOPDM。','仿真'),
        ('catch_two','video','https://dexterous-manipulation.github.io/videos/twoeggcatch_topdm.webm','DEXGYM','Dexterous Gym · 双物体抛接','Results / TwoEggCatchUnderarm / TOPDM。','仿真'),
        ('piano','video','https://kzakka.com/robopianist/assets/videos/simple/twinkle_twinkle.mp4','PIANO','RoboPianist · 多指时序弹奏','Simple pieces / Twinkle Twinkle Little Star。','仿真'),
    ]
    for id,typ,url,source,label,match,domain in media_rows:
        media[id]=dict(type=typ,url=url,source=source,label=label,match=match,domain=domain)
    for id in ['hora','viser','tea','cube','kitchen','egg']:
        media[id]['domain']='真实机器人'
    media['dexmachina']['domain']='仿真'
    media['arctic']['domain']='人手数据集'
    for id,name,en,definition,observe,source in [
        ('P33','抛出与动态接获','Throw / dynamic catch','在接触释放、自由飞行与重新接触之间切换。','释放速度、飞行轨迹、首次接触、接获后保持','DEXGYM'),
        ('P34','多物体协调','Multi-object coordination','同时控制两个或多个独立物体的相对位置与接触。','每个物体的独立轨迹、相位、物间碰撞、掉落','PDDM'),
        ('P35','多指时序触发','Timed multi-digit actuation','按时间目标协调不同手指建立和释放接触。','目标事件、实际起止、误触、时序偏差','PIANO'),
    ]:
        primitives.append(dict(id=id,name=name,en=en,definition=definition,observe=observe,source=[source]))
    for id,name,group,spec,use in [
        ('baoding','双球 / 保定球组','多物体','两枚可区分颜色的轻质球，记录各自尺寸与质量','掌内轮转、多物体跟踪'),
        ('rubik','三阶魔方 / 单层转动模型','机关','记录面转阻力；整体姿态和各层转角分别标记','整体翻转与面转组合'),
        ('keyboard','电子琴键盘 / 带事件记录的琴键板','时序工具','记录键距、键程及 MIDI 或开关时间戳','多指时序、和弦及双手协作'),
        ('ellipsoid','轻质椭球模型与接落垫','动态任务','对应仿真 egg 形状；真实采集从软质轻量模型开始','双手抛接与双物体抛接'),
    ]:
        props.append(dict(id=id,name=name,group=group,spec=spec,use=use))
    def task(id,name,en,cat,ps,obj,source,locator,desc,success,demo,origin='direct',hands='单手'):
        add(id,name,en,cat,ps,obj,source,locator,desc,success,origin=origin,demo=demo,difficulty='高阶',hands=hands,variation='记录物体几何、接触模式、初始状态和目标；先独立改变一个因素，不把参数条件当作新任务族。')
        actions[-1]['mediaScope']=('子策略的总览参考；不是独立动作录像' if origin=='adapted' else media[demo]['domain']+'任务演示；对应关系见素材说明。')
    task('I31','按指令切换旋转轴','Commanded multi-axis continuous rotation','inhand','P10,P18,P20','sphere','HORA','项目页 Multi-Axis Rotation Policy','在持续手内转动中根据输入切换旋转轴；分别记录轴指令与实际角速度方向。','考察轴向跟踪、旋转进展、切换延迟与掉落；不使用目标四元数到达替代。','hora_multi')
    task('I32','指间连续转笔','Continuous pen spinning','inhand','P10,P18,P20','pen','PENSPIN','项目页 teaser / Emergent Fingergaiting / Continuous Spinning','细长笔状物在指间连续旋转，协调换指、物体倾斜与位置漂移。','记录有效旋转周期、笔轴方向、物体中心漂移、卡滞与掉落。','penspin')
    task('I33','掌内双球协调轮转','Baoding balls rotation','inhand','P18,P20,P21,P34','baoding','PDDM','作者研究说明 Figure 1 / Figure 4；论文 Baoding Balls task','同一只手同时协调两枚自由物体绕掌内循环移动，跟踪各球身份和相位。','两球按目标方向完成循环且不掉落；记录轨迹误差和球间接触。','baoding')
    task('I34','利用重力辅助重定向','Gravity-assisted reorientation','inhand','P10,P18,P20,P22','cube','DACTYL','摘要：controlled use of gravity；拆解为观察子任务','记录松开局部接触、物体受重力运动和重新抓稳的过程；同时记录手腕倾斜，避免混淆运动来源。','比较掌系物体姿态与接触时序；视频仅能支持可见的运动，不能独立确定接触力。','dactyl',origin='adapted')
    task('U35','持稳魔方并转动顶层 90°','Rubik face rotation','tool','P10,P20,P25','rubik','CUBE','Analysis / Emergent meta-learning：top face 90 degrees clockwise or counterclockwise','部分手指稳定魔方本体，其他手指使顶层相对本体转动 90°。','同时评估顶层转角和本体漂移；整体转动魔方不算面转。','rubik')
    task('U36','魔方整体翻转与面转序列','Rubik cube flips and face-turn sequence','tool','P10,P18,P20,P25','rubik','CUBE','A full solve；Footnote A：face rotations and cube flips','交替执行整块重定向和内部层转动；动作序列由外部给定，单独记录规划与执行。','逐步比较本体朝向、每层转角和指令序列，记录错误层转、卡滞和掉落。','rubik')
    task('U37','单手稳瓶并拧开瓶盖','Single-hand lid unscrewing','tool','P10,P20,P25','bottle','DIFFHAND','Experiments / Best policy evaluation','同一只手承担瓶体稳定与瓶盖拧转，通过不同手指的功能分工完成开盖。','瓶盖相对瓶体产生旋转与轴向分离；明确是否使用桌面辅助，不能混记为双手或夹具固定。','onehand_lid')
    task('U38','手指与手腕协同跟踪笔尖轨迹','Dexterous pencil trajectory tracking','tool','P05,P10,P17,P18,P26','pen,paper','PDDM','Flexibility in Task Execution / Figure 7','固定手的基座，协调手指和手腕，让笔尖跟踪给定轨迹。原研究展示为仿真。','记录笔尖路径与时间误差；明确目标是轨迹，不能仅以笔的最终朝向评价。','pencil_path')
    task('B22','双手下手抛接物体','EggCatchUnderarm','bimanual','P09,P15,P33','ellipsoid','DEXGYM','Results / EggCatchUnderarm / TOPDM','抛出手释放物体，接收手在自由飞行后建立接触并保持；来源展示为仿真。','区分释放、自由飞行、首次接触与稳定接获；未离手的转交不计为抛接。','catch_under',hands='双手')
    task('B23','双手上手抛接物体','EggCatchOverarm','bimanual','P09,P15,P33','ellipsoid','DEXGYM','Results / EggCatchOverarm / TOPDM','按照原环境的上手抛接构型完成飞行与接获；具体初始构型以原演示为准。','记录两手起始位姿和飞行轨迹，检查接获后保持；这是抛接族的构型变体。','catch_over',hands='双手')
    task('B24','双手双物体抛接','TwoEggCatchUnderarm','bimanual','P09,P15,P33,P34','ellipsoid','DEXGYM','Results / TwoEggCatchUnderarm / TOPDM','同时追踪两枚物体的释放与接获，防止把一枚成功接住当成完整成功。','分别记录两个物体的轨迹、接触事件和终态；两物体都满足目标才计成功。','catch_two',hands='双手')
    task('B25','双手多指按节奏弹奏','Bimanual timed piano playing','bimanual','P09,P15,P23,P35','keyboard','PIANO','项目页 Simple pieces / Twinkle Twinkle Little Star','按音符与时间目标协调多个手指击键和松键，包含双手分工；此处为仿真研究演示。','比较目标/实际音符、起止时间、误触和漏触；不同曲目作为条件，不重复计为动作族。','piano',hands='双手')
    by_id={a['id']:a for a in actions}
    by_id['I01']['aliases']=['持续旋转','连续旋转','无限旋转','转圈','continuous rotation','spinning','HORA','标题视频','首页视频']
    by_id['I01']['mediaScope']='首页同一段 HORA 官方实机视频；主任务为持续绕轴旋转。'
    by_id['I02']['sources'].append('DACTYL')
    by_id['I02']['aliases']=['目标朝向','重定向','定向旋转','reorientation','Dactyl']
    by_id['I03']['aliases']=['六维位姿','6D','SE(3)','位置加朝向']
    by_id['I21']['aliases']=['支点旋转','pivoting']
    by_id['I22']['aliases']=['换指','指步态','finger gaiting','重新抓握']
    by_id['I32']['aliases']=['转笔','笔旋转','penspin','pen spinning']
    by_id['I33']['aliases']=['保定球','健身球','双球旋转','多物体','baoding']
    by_id['U35']['aliases']=['魔方','面转','rubik']
    by_id['U36']['aliases']=['魔方','解魔方','翻块','cube flip']
    by_id['U37']['aliases']=['单手拧盖','拧瓶盖','开瓶盖']
    for a in actions:
        a.setdefault('aliases',[])
    # Family memberships overlap: this map is a collection design aid, not a completeness claim.
    rows=[
        ('spin','持续旋转与轴切换','I01,I16,I30,I31','保持旋转进展；区别于转到某个终点。','已有任务演示；速度/质量等细分条件并非均有对应录像。'),
        ('orientation','目标朝向重定向','I02,I13,I14,I15,I17,I29','使物体相对手掌到达 SO(3) 目标。','已有任务族演示；对称物体的等价朝向需协议规定。'),
        ('pose','完整 6D 位姿与平移','I03,I10,I11,I12,I18','位置与朝向均为目标，而非只旋转。','有来源定义；当前仍缺完整 6D 的逐项视频，现有媒体仅作朝向对比。'),
        ('gait','换指、重抓与抓型转换','I22,I23,I24,I34','支撑指与移动指交替；区分手内运动和腕臂代偿。','转换条目多数仍为扩展；已有 HORA / Dactyl 子策略参考。'),
        ('contact_motion','滚动、滑移与支点旋转','I19,I20,I21,C10','通过不同接触运动实现局部调整。','当前主要为原语与扩展，缺逐项接触特写和接触力。'),
        ('palm','指掌转移与掌内暂存','I04,I05,I06,I07,I27','指端工作区与掌内储存区之间交换。','有分类依据；当前未定位各条目的独立录像。'),
        ('pen_spin','细长物体动态转笔','I32','细长物体的中心、倾斜和换指同步控制。','已补入 PenSpin 实机视频；不等同于所有花式转笔技巧。'),
        ('multiobject','单手多物体协调','I33','两个独立物体同时受控，而非只拿住多个物体。','已补入双球实机演示；三物体及不同形状组合待补。'),
        ('articulated','物体内部自由度操作','U35,U36,U37','稳定本体，同时改变层、盖或其他内部关节。','已补入魔方面转与单手拧盖；魔方视频在原站播放。'),
        ('tool','功能工具与笔尖轨迹','U01,U02,U38','持握结构和功能驱动分离，任务输出为工具端状态。','有真实工具视频与仿真笔尖轨迹；证据逐项标明。'),
        ('ballistic','离手抛接与再接触','B22,B23,B24','必须包含自由飞行，不能用手递手替代。','已补入原作者仿真视频；尚无对应实机验证。'),
        ('timing','多指时空精确操作','B25','多个接触事件满足各自位置与时间目标。','已补入 RoboPianist 仿真演示；不按曲目扩充动作计数。'),
        ('bimanual','双手交接、稳定与角色交换','B01,B02,B04,B05,B07,B16','接触重叠、稳定手和操作手的角色变化。','已有双手任务来源；部分细分动作仍是采集扩展。'),
        ('force','力调节、滑移与扰动恢复','C01,C05,C11,I28','维持或恢复接触稳定，而非只到达姿态。','多数仍为扩展；需要标定力/触觉记录，视频不能证实力控制。'),
    ]
    families=[dict(id=id,name=name,actions=ids.split(','),definition=definition,gap=gap) for id,name,ids,definition,gap in rows]
    featured=['I01','I02','I03','I31','I32','I33','U35','U37','B22','B25','I22','I34']
    gaps=[
        '目前的任务族是面向数采的工作划分，不是领域完整分类；条目数量不代表覆盖率。',
        '触觉闭环盲操作、掌面朝下/任意重力方向等还需要独立核对。它们常是已有动作的感知或姿态条件，应单独记录。',
        '环境辅助重抓、桌面滚推、指尖步行/爬行，以及更复杂的柔性物体手内操作仍待专题补充。',
        '现有 3D 模板只支持基础关节运动；复杂灵巧操作使用原始媒体，尚无统一的物理有效重放。',
    ]
    return families,featured,gaps
