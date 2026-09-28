"""ActionSense: preserve all 20 source labels; author an explicit capture decomposition.

The labels are activity-level annotations. Phases and success criteria below are
atlas-authored proposals, not released frame-level labels or robot demonstrations.
"""

HOME = 'https://action-sense.csail.mit.edu/'
PAPER_ROOT = 'https://proceedings.neurips.cc/paper_files/paper/2022/file/5985e81d65605827ac35401999aea22a-'
SUPP = PAPER_ROOT + 'Supplemental-Datasets_and_Benchmarks.pdf'
LICENSE = 'https://creativecommons.org/licenses/by-nc-sa/4.0/'
DATE = '2026-09-28'


def expand_actionsense(sources, media, primitives, props, actions, add, families):
    before_actions = {a['id'] for a in actions}
    before_props = {p['id'] for p in props}
    source = 'ACTIONSENSE'
    sources[source] = dict(
        short='ActionSense',
        title='ActionSense: A Multimodal Dataset and Recording Framework for Human Activities Using Wearable Sensors in a Kitchen Environment',
        authors='Joseph DelPreto, Chao Liu, Yiyue Luo, Michael Foshey, Yunzhu Li, Antonio Torralba, Wojciech Matusik, Daniela Rus',
        year='2022', venue='NeurIPS · Datasets and Benchmarks', url=HOME,
        doi='10.52202/068431-1003',
        note='20 项人类厨房活动标签。按完整活动记录，单次削皮、切片和擦拭需要另行分段；本库另列手部校准协议。不是机器人执行或完整可靠的手部 3D 真值。',
        license='CC BY-NC-SA 4.0', license_url=LICENSE,
        supporting_links=[
            dict(label='论文', url=PAPER_ROOT + 'Paper-Datasets_and_Benchmarks.pdf'),
            dict(label='补充材料 C.3–C.4 · 采集指令', url=SUPP + '#page=8'),
            dict(label='官方活动标签表', url=HOME + 'dataset_info.html#activities'),
            dict(label='数据与各参与者视频', url=HOME + 'data.html'),
        ])
    for mid,typ,url,label,match in [
        ('as_grid','video',HOME+'images/activities_grid_slide_compressed_cropped.mp4','ActionSense · 厨房活动合集','首页 Activities 拼接视频；覆盖多类活动，没有为本库子动作逐项裁剪或标定时间边界。'),
        ('as_session','youtube','https://www.youtube.com/embed/u3sUbmwJcrQ','ActionSense · 带活动章节的多模态演示','首页原始 YouTube 演示；章节对应活动标签。本库未核定各子动作时间戳。'),
        ('as_calibration','link',SUPP+'#page=8','ActionSense · 手部校准原始协议','Supplement C.3.1，印刷页 8；以文字协议为证据，尚未定位独立校准视频。'),
    ]:
        media[mid] = dict(type=typ,url=url,source=source,label=label,match=match,
                          domain='人类采集',control='真人执行',scope='reference',
                          license='CC BY-NC-SA 4.0',license_url=LICENSE,verified=DATE)
    # Deliberately no unrelated grasp poster for these kitchen task entries.
    media['as_grid']['poster'] = HOME+'images/kitchen_items.jpg'
    media['as_grid']['poster_label'] = '原项目道具总览 · 非动作帧'
    media['as_calibration']['poster'] = HOME+'images/wearable_sensors_v0.jpg'
    media['as_calibration']['poster_label'] = '原项目传感器总览'

    for pid,name,en,definition,observe in [
        ('P38','切分与表层剥离','Cut and peel material','用刃口使材料分离，或沿表面移除薄层；削皮与切片共享材料分离，但目标几何不同。','工具—材料相对路径、支撑接触、分离事件和材料形变'),
        ('P39','涂布与铺展','Spread a coating','保持工具与基底接触，将可变形材料铺展到目标区域。','覆盖区域、材料转移量、工具倾角、基底变形与破损'),
        ('P40','倾倒与流量终止','Pour and stop flow','改变容器姿态，将液体转移到接收容器，并恢复姿态以停止流动。','两容器相对位置、倾角、流动起止、接收量和洒漏'),
    ]:
        primitives.append(dict(id=pid,name=name,en=en,definition=definition,observe=observe,source=[source]))

    inventory = [
        ('cucumber','黄瓜','食材','原流程每轮取 3 根；记录长度、直径、表皮与已去皮状态。','去皮、切片',['整根带皮','已去皮','黄瓜片']),
        ('potato','土豆','食材','原流程取 3 个；记录尺寸、形状与表皮状态。','去皮、切片',['带皮','已去皮','土豆片']),
        ('bread','面包','食材','区分袋装小餐包与预切片；记录厚度、软硬和切前状态。','切片与涂抹',['sandwich bread rolls','预切面包片']),
        ('peeler','蔬菜削皮器','工具','记录刀口方向、握柄几何与刀片类型；来源未规定统一尺寸。','去黄瓜皮、土豆皮',[]),
        ('chef_knife','厨师刀','工具','来源为真实厨刀；训练刀可作预试替代，材料切分效果需另行验证。','切蔬菜；清理砧板时可辅助刮取',[]),
        ('bread_knife','面包刀','工具','与厨师刀、餐刀分开建道具条件；记录刀刃形态和柄长。','切小餐包',[]),
        ('table_knife','餐刀 / 涂抹刀','餐具','原文 dinner knife；作为餐具摆放或用于涂抹，勿等同厨师刀。','涂杏仁酱、果冻酱；摆台、装卸',[]),
        ('cutting_board','砧板','厨房用具','记录板面尺寸、摩擦与是否搬起；原流程允许将板移近容器。','去皮、切片与刮清',[]),
        ('almond_butter','杏仁酱','耗材','记录温度与稠度；来源为 almond butter，非花生酱。','面包涂抹与开关罐',['带螺纹盖包装']),
        ('jelly','果冻酱 / 果酱','耗材','保留来源 jelly 名称；原流程涂在已涂杏仁酱的面包上。','面包涂抹',[]),
        ('jar','广口罐与螺纹盖','机关','与窄口瓶分开记录；记录口径、盖型、初始紧度。','开关罐、酱料盛装、校准持握',['杏仁酱罐','果冻酱罐']),
        ('pitcher','带柄水壶 / 水罐','厨房用具','原文 pitcher；用于倒水，不是烧水壶。记录壶嘴与初始水量。','向杯中倒水',[]),
        ('water','水','耗材','记录初始量与最终接收量；原协议不固定精确体积。','倒水与洒漏记录',[]),
        ('spoon','餐勺','餐具','原流程餐具组每套一把；记录柄长、勺部形状。','摆台、洗碗机装卸',[]),
        ('pot','深锅 / 食材收集锅','厨房用具','原文 pot；与用于擦拭及收面包的 pan 分开。','收集蔬菜皮和蔬菜片',[]),
        ('dishwasher','洗碗机与内部搁架','环境设备','记录上下层、摆放槽与餐具容纳位置；只采装入和取出。','餐具装载、卸载',['上层杯架','下层盘架','餐具放置区']),
        ('cabinet','厨房储物柜','环境设备','记录柜门、层板和物体初始存放位置；不将步行另计手部动作。','取物、归位',[]),
        ('refrigerator','冰箱','环境设备','来源食材与酱料的取放位置；记录门与内部抽屉状态。','食材取放',[]),
        ('sink','水槽','环境设备','原流程清场时部分物体放入水槽；不据此增加流水洗涤任务。','物体归置',[]),
        ('scale','USB 数字秤','校准设备','来源 Dymo M25；记录同步读数与归零，作为触觉校准参考。','平掌与单指按压',[]),
        ('textured_calibration','3D 打印纹理校准块','校准设备','置于秤上，改变掌部局部受力；形状参数需从实物另记。','局部触觉响应校准',[]),
        ('emg_armband','Myo 前臂肌电臂环','记录设备','来源每前臂 8 对差分干电极；记录左右手、通道方位及同步。','肌电与前臂运动记录',[]),
        ('finger_glove','Manus 手指追踪手套','记录设备','来源 Manus Prime II Xsens；当前数据的指侧展与跟踪可靠性有限。','手部姿态及校准',['弯曲传感器','IMU 校准程序']),
        ('body_imu','Xsens 身体惯性传感器组','记录设备','来源 17 个 IMU；世界位置会漂移，不能替代接触真值。','腕臂与全身运动背景',[]),
        ('eye_tracker','Pupil Core 眼动与第一视角相机','记录设备','记录视线置信度、相机标定和同步；不是动作成功判据。','注意力和第一视角视频',[]),
        ('rgb_camera','多视角 RGB 相机','记录设备','来源 5 台 FLIR；记录视角、帧时间戳与外参。','动作与接触人工核对',[]),
        ('depth_camera','RealSense 深度相机','记录设备','来源 D415；校准手姿和持物姿态在相机前执行。','深度与手物几何参照',[]),
        ('microphone','环境麦克风','记录设备','来源全向与指向麦克风；切割声音可辅助拟定分段，未提供单刀真值。','音频及动作事件辅助定位',[]),
    ]
    equipment = ['emg_armband','finger_glove','body_imu','eye_tracker','rgb_camera','depth_camera','microphone','sensor']
    for pid,name,group,spec,use,variants in inventory:
        loc = 'Supplement C.3.1 / 传感与校准' if group in ('记录设备','校准设备') else 'Supplement C.4 / Kitchen environment and items'
        props.append(dict(id=pid,name=name,group=group,spec=spec,use=use,variants=variants,added_in='1.3',
                          evidence=[dict(source=source,locator=loc,domain='人类采集')]))
    reused = dict(
        cup=['水杯 glass：倒水时 5 个','马克杯 mug：餐具任务每套 1 个'],
        bowl=['餐碗：餐具任务每套 1 个'], plate=['大盘','小盘'],
        pan=['带柄平底锅：干擦拭','收集面包片的 pan'],
        sponge=['擦盘与擦锅的海绵'], cloth=['擦盘与擦锅的毛巾'],
        fork=['ActionSense 普通餐叉，非指定 YCB 型号'],
        bag=['装小餐包的袋子'], drawer=['真实厨房餐具抽屉'],
        sensor=['ActionSense 自制掌部与指部触觉阵列；未覆盖指尖'])
    for p in props:
        if p['id'] in reused:
            p['variants'] = list(dict.fromkeys(p.get('variants',[])+reused[p['id']]))
            p.setdefault('evidence',[]).append(dict(source=source,locator='Supplement C.3.1' if p['id']=='sensor' else 'Supplement C.4 / 取放、擦拭与餐具流程',domain='人类采集'))
    next(p for p in props if p['id']=='fork')['name'] = '餐叉 / YCB 餐叉'

    by = {a['id']:a for a in actions}
    enriched = set()
    def task(aid,name,en,cat,ps,objects,desc,success,origin='direct',parent=None,calibration=False,hands='双手'):
        mid = 'as_calibration' if calibration else 'as_grid'
        locator = 'Supplement C.3.1, p.8 · 手部校准' if calibration else '官方 Activity Stats 标签表；Supplement C.4, pp.9–11'
        add(aid,name,en,cat,ps,objects,source,locator,desc,success,origin=origin,demo=mid,hands=hands,difficulty='进阶',
            variation='记录左右手、设备状态、校准开始 / 结束时段及同步参考；保持来源要求与本库可选变化因素分开。' if calibration else '记录工具 / 物体身份、初态、稳定手与操作手、接触阶段及失败原因。条件分别采集；细分阶段需人工复核时间边界。')
        a=actions[-1]
        a.update(added_in='1.3',granularity='校准协议' if calibration else '本库拆解子动作' if origin=='adapted' else '完整活动 / 条件族',
                 aliases=['ActionSense'],mediaScope=media[mid]['match'],phases_author='本库建议分段；不是官方逐帧标签',
                 equipment=['depth_camera','finger_glove','sensor'] if calibration else equipment)
        if parent:a['parent']=parent
        by[aid]=a
        a['evidence']=[dict(source=source,media=mid,label=media[mid]['label'],locator=locator,
            url=SUPP+('#page=8' if calibration else '#page=9'),scope=a['mediaScope'],relation='校准协议' if calibration else '任务拆解' if origin=='adapted' else '直接活动来源',props=objects.split(','))]
        if not calibration:
            a['evidence'].append(dict(source=source,media='as_session',label=media['as_session']['label'],locator='首页多模态演示 / 活动章节',
                                      scope=media['as_session']['match'],relation='原始连续演示',props=[]))
        return a

    task('U53','蔬菜去皮','Peel vegetables','tool','P10,P26,P27,P38','cucumber,potato,peeler,cutting_board',
         '使用削皮器去除黄瓜或土豆表皮。两个官方活动合为一个技能入口，物体条件分别保留；抓法和削皮行程由参与者选择。',
         '记录去除表皮区域、每次工具接触和蔬菜的支撑方式；以目标表皮去除情况评估。')
    task('U54','蔬菜与面包切片','Slice vegetables and bread','tool','P10,P23,P26,P27,P38','cucumber,potato,bread,chef_knife,bread_knife,cutting_board',
         '黄瓜、土豆使用厨师刀，小餐包使用面包刀。三项官方活动合并为切片技能的三个条件；单刀过程需另行分段。U08 仍保留特定食指伸展抓型，不强行等同。',
         '记录实际材料分离、片数与厚度；区分工具运动、未切断与完整切片。')
    task('U55','刮清砧板并转移食材','Clear a cutting board','tool','P10,P16,P22,P26,P27','cutting_board,chef_knife,cucumber,potato,bread,pot,pan',
         '把蔬菜皮或切片从砧板移入锅中；面包片移入平底锅。来源允许借助刀，也允许移动砧板或收集容器，不能把某一种策略当成唯一标签。',
         '记录目标食材进入容器的比例、板面残留、散落与板 / 容器的相对运动。')
    task('U56','在面包上涂抹酱料','Spread almond butter or jelly on bread','tool','P10,P26,P27,P39','bread,table_knife,almond_butter,jelly,jar',
         '用餐刀铺展杏仁酱或果冻酱。原流程先杏仁酱、再果冻酱；面包可放桌上或手持，涂抹量和技术不固定。两种材料作为独立条件。',
         '记录覆盖范围、面包完整性与材料转移；工具悬空划动不计有效涂抹。')
    task('B26','扶罐并重复开合螺纹盖','Open and close a jar','bimanual','P10,P24,P25,P27','jar,almond_butter',
         '打开并盖回杏仁酱罐，原流程重复 3 次，允许罐体放桌上或持握。完整开合循环与已有 B07、U22、U23 单侧步骤关联。',
         '分开记录开盖、盖体分离、重新啮合和关盖；每次循环均有可辨识罐盖状态。')
    task('B27','持盘并用海绵或毛巾擦拭','Clean a plate with sponge or towel','bimanual','P10,P22,P27,P29','plate,sponge,cloth',
         '一手拿盘，一手以海绵或毛巾模拟擦洗。来源为假装有污渍的干擦拭，不包含流水、洗涤剂或实际去污效果验证。',
         '记录盘面接触覆盖与持盘稳定性；在干擦任务中不以去污率判定。')
    task('B28','持锅柄并擦拭锅面','Clean a pan with sponge or towel','bimanual','P10,P22,P27,P29','pan,sponge,cloth',
         '稳定手握住锅柄，另一手用海绵或毛巾模拟擦拭锅面。与持盘的边缘支撑不同，保留为单独接触与负载条件。',
         '记录锅柄抓握、锅面接触区域与锅体晃动；原流程未验证实际去污。')
    tableware = 'plate,bowl,cup,table_knife,spoon,fork'
    task('T23','从储物区取物并归位','Fetch and return kitchen items','transfer','P08,P09,P10,P16,P19,P15','cabinet,refrigerator,drawer,sink,cutting_board,cucumber,potato,bread,peeler,chef_knife,bread_knife,table_knife,almond_butter,jelly,jar,pitcher,cup,pan,pot,plate,bowl,spoon,fork,sponge,cloth,bag',
         '覆盖通用取放与批量取餐具两个官方标签。记录储物位置、物体集合与搬运次序；开门、开抽屉属于可能出现的上下文步骤，应按实际录像标注。',
         '目标物体从正确储位到达工作区，或归回指定位置；分别记录漏取、错放、碰撞和滑落。',hands='单手 / 双手')
    task('T24','布置三套餐具','Set a table with three place settings','transfer','P08,P10,P16,P19,P15',tableware,
         '每套含大盘、小盘、碗、马克杯、水杯、餐刀、餐勺和餐叉，共三套。原流程规定三个用餐位置，但具体餐具排布和中间暂存策略可自由选择。',
         '各用餐位置的物品集合完整且稳定；用目标集合而非唯一排列样式判断。',hands='单手 / 双手')
    task('T25','将盘碗分类叠放','Stack plates and bowls on a table','transfer','P08,P10,P16,P19,P15','plate,bowl',
         '分别叠放大盘、小盘和碗，每类 3 件。杯、刀叉勺不属于该官方堆叠标签；与盘子翻转入碗碟架 T21 区分。',
         '同类物体形成稳定叠组；标注落位、释放、倾斜与意外碰倒。',hands='单手 / 双手')
    task('T26','将餐具装入洗碗机','Load tableware into a dishwasher','transfer','P08,P10,P16,P19,P15',tableware+',dishwasher',
         '把三套餐具放进洗碗机，顺序、暂存位置和一次搬运数量允许变化。是受环境约束的长任务链，不包含开启洗涤程序。',
         '记录各件物品最终所在层架与稳定状态，检查遗漏和碰撞；整套装完才计活动完成。',hands='单手 / 双手')
    task('T27','从洗碗机取出餐具并归位','Unload a dishwasher and return items','transfer','P08,P09,P10,P16,P19,P15',tableware+',dishwasher,cabinet,drawer',
         '从洗碗机取出三套餐具并放回原存储位置。与装入任务分开，涉及从密集约束中取出和跨区域归位。',
         '目标餐具全部取出且归入正确储位；保留取出次序、批量搬运和失败事件。',hands='单手 / 双手')

    task('U57','单次削皮接触行程','One peeling contact stroke','tool','P10,P26,P27,P38','cucumber,potato,peeler',
         '从蔬菜去皮活动提议切出的最小接触片段：刃口接触、沿表皮运动、表层分离、脱离。原数据未提供本条逐次起止。',
         '一次连续接触产生可辨表层移除；标注行程边界及支撑手状态。',origin='adapted',parent='U53')
    task('U58','单片切下与刀具复位','One slice separation and tool reset','tool','P10,P23,P26,P27,P38','cucumber,potato,bread,chef_knife,bread_knife,cutting_board',
         '从整段切片提议分出切入、材料分离和刀具退离。面包可能需要多次往复才能分离一片，不能把一次往复自动当一片。',
         '以材料分离事件界定一片，刀具离开后标记结束；保留未切断片段。',origin='adapted',parent='U54')
    task('U59','一次接触涂布行程','One contact spreading stroke','tool','P10,P26,P27,P39','bread,table_knife,almond_butter,jelly',
         '从涂抹活动提议分出工具接触基底、推动材料并脱离的一次行程。取酱与换手只有在录像中出现时才额外标注。',
         '记录行程前后覆盖区域变化及面包破损；时长阈值由预试确定。',origin='adapted',parent='U56')
    task('B29','稳定餐具并完成一次擦拭行程','One supported wiping stroke','bimanual','P10,P22,P27,P29','plate,pan,sponge,cloth',
         '从盘面或锅面干擦中提议分出一次连续接触行程。路径可以直线或曲线，方向变化作为条件，非四个新技能。',
         '稳定手持续支撑目标物，擦拭材料接触表面；分开标记换向和离面。',origin='adapted',parent='B27')
    by['B29']['related_actions']=['B28']

    task('C13','平掌按秤的触觉校准','Flat-palm scale calibration','contact','P09,P23,P31,P15','scale,sensor',
         '按官方校准程序，以平掌向数字秤按压，每只手 3 次。重复次数是来源协议；不要求线性力斜坡，故不与 C02 等同。',
         '每次包含接触、加载和卸载；同步触觉与数字秤读数，并记录左右手及归零。',calibration=True,hands='单手')
    task('C14','掌部纹理块按压校准','Textured-object palm calibration','contact','P09,P23,P31,P15','scale,textured_calibration,sensor',
         '将 3D 打印纹理块放在秤上，重复平掌按压，以局部接触激发掌区触觉。这是 C13 的接触几何条件，单列校准入口。',
         '保留纹理块位置、掌部接触区域与参考秤读数；不从视频估计真实接触压力。',calibration=True,hands='单手')
    task('C15','五类物体静态持握校准','Static holding of five calibration objects','contact','P09,P10,P15','cup,pan,plate,chef_knife,jar,depth_camera,sensor',
         '原协议让每只手依次持握 mug、pan、plate、knife、jar，每个至少 5 秒，并在深度相机前记录。刀型未在校准段限定；本库用厨师刀作为可配置道具实例。',
         '记录对象、左右手、保持段与深度遮挡；原文未命名 GRASP 抓型，不自动赋予抓型真值。',calibration=True,hands='单手')
    task('C16','手套姿态与八字运动校准','Glove poses and figure-eight calibration','contact','P01,P02,P04,P05,P06,P07','finger_glove,depth_camera',
         'Manus 校准包含双手八字运动后平稳保持，以及握拳、四指伸直而拇指横屈掌前、拇食指伸出的手枪形。是校准动作串，不属于 20 个厨房标签。',
         '按设备软件确认各姿态与稳定段，保留深度视频；校准完成不等同所有关节追踪准确。',calibration=True,hands='单手 / 双手')

    def enrich(aid,objects,locator,scope,relation='关联子步骤',mid='as_grid'):
        a=by[aid];enriched.add(aid)
        if source not in a['sources']:a['sources'].append(source)
        a['props']=list(dict.fromkeys(a['props']+objects.split(',')))
        a.setdefault('evidence',[]).append(dict(source=source,media=mid,label='ActionSense · '+relation,locator=locator,
                                               url=SUPP+('#page=8' if mid=='as_calibration' else '#page=9'),scope=scope,relation=relation,props=objects.split(',')))
        return a
    pour=enrich('B14','pitcher,cup,water','Activity Stats / Pour water from a pitcher into a glass; C.4, p.10',
                '原流程要求一手拿接收杯，另一手持水壶；官方完整活动；演示为合集。','直接活动来源')
    pour.update(origin='direct',sources=[source]+[s for s in pour['sources'] if s!=source],
                name='双手扶杯与倒水',en='Pour water while holding the receiving glass',media='as_grid',
                locator='ActionSense: Pour water from a pitcher into a glass · Supplement C.4, p.10',
                description='一手持水杯，另一手持水壶倒入，原流程依次向 5 个杯子倒水。接收杯不得只是独自放在桌上；原协议不固定倒入体积。',
                success='记录液流开始与终止、接收量及洒漏，杯与壶在两手中保持稳定。',
                primitives=['P10','P27','P40'],mediaScope=media['as_grid']['match'],granularity='完整活动',equipment=equipment)
    pour.setdefault('aliases',[]).append('ActionSense')
    enrich('B07','jar','C.4 / Open and close a jar','开合罐任务中的开盖阶段；原 B07 的瓶也保留为本库可选条件。','本库子步骤映射')
    enrich('U22','jar','C.4 / Open and close a jar','重新盖合与拧紧阶段，完整任务见 B26。','本库子步骤映射')
    enrich('U23','jar','C.4 / Open and close a jar','旋松阶段，完整任务见 B26。','本库子步骤映射')
    for aid,description in [
        ('B07','一手稳定罐体，一手旋松并移开盖子；从 ActionSense 开合罐任务拆出。瓶类道具保留为本库变化条件。'),
        ('U22','盖子对准并啮合后旋紧；从 ActionSense 开合罐任务拆出。窄口瓶与广口罐分别记录。'),
        ('U23','旋松罐盖至解除螺纹约束；从 ActionSense 开合罐任务拆出。与完整开合循环 B26 区分。'),
    ]:
        a=by[aid]
        a.update(origin='adapted',description=description,media='as_grid',mediaScope=media['as_grid']['match'],
                 locator='ActionSense · Supplement C.4 / Open and close a jar 的本库子步骤',
                 sources=[source]+[s for s in a['sources'] if s!=source],parent='B26',granularity='本库拆解子动作')
    by['B07']['name']='一手扶瓶 / 罐，一手开盖'
    finger=enrich('C09','scale','Supplement C.3.1, p.8 / sequential finger pressing',
                  '官方触觉校准要求每根手指依次按压两次；没有独立校准演示片段。','直接校准协议',mid='as_calibration')
    finger.update(origin='direct',sources=[source]+[s for s in finger['sources'] if s!=source],media='as_calibration',
                  locator='ActionSense · Supplement C.3.1, p.8 / 每根手指依次按压两次',
                  description='每根手指依次单独按压，原触觉校准流程每指 2 次。数字秤为来源参考设备；原按钮道具保留为本库采集变体。',
                  mediaScope=media['as_calibration']['match'],granularity='校准协议',equipment=['finger_glove','sensor'])

    # Phases are authored event boundaries; reuse existing primitives and actions.
    def phases(aid,rows):
        by[aid]['phases_author']='本库建议分段；不是官方逐帧标签'
        by[aid]['phases']=[dict(name=n,primitives=p.split(','),observe=o,actions=a.split(',') if a else []) for n,p,o,a in rows]
    phases('U53',[
        ('持菜与持削皮器','P10,P27','记录两手分工及是否借助桌面。',''),
        ('连续去皮行程','P26,P38','按接触—分离—离面分段。','U57'),
        ('调整目标表面与结束','P19,P15','重抓、转动物体仅在录像中出现时标记。','')])
    phases('U54',[
        ('稳定食材与工具','P10,P27','记录食材—板面与稳定手接触。',''),
        ('切入并分离一片','P26,P38','将往复次数与实际片数分开记录。','U58'),
        ('下一片定位或结束','P19,P15','保留材料位置变化与刀具退离。','')])
    phases('U55',[
        ('定位板与收集容器','P16,P19','谁移动、谁固定；板与容器的相对位姿。',''),
        ('把食材移出板面','P22,P26','刀辅助刮取为可选策略；记录实际接触。',''),
        ('检查残留并放回','P19,P15','区分进入容器与散落。','')])
    phases('U56',[
        ('稳定面包与涂抹刀','P10,P27','面包手持 / 桌面支撑分别标注。',''),
        ('接触并铺展酱料','P26,P39','记录每次有效涂布与材料条件。','U59'),
        ('工具离面与检查覆盖','P15','接触结束、面包状态和覆盖范围。','')])
    phases('B26',[
        ('固定罐体、旋松罐盖','P10,P25,P27','盖子相对罐体的转角与解除啮合。','B07,U23'),
        ('分离与重新对准','P24,P19','盖体分离事件与重新啮合位置。',''),
        ('拧紧并重复循环','P25','原协议开关 3 次；不把次数当新技能。','U22')])
    phases('B14',[
        ('分别持壶和杯','P10,P27','接收杯在手中。',''),
        ('倾壶使水流入杯','P40','液流起点、两容器相对位置与洒漏。',''),
        ('回正止流与换杯','P19,P40','液流终点与杯内量，不强加原文没有的容量。','')])
    for aid in ['B27','B28']:
        phases(aid,[('稳定目标与清洁材料','P10,P27','盘面边缘或锅柄支撑，材料为海绵 / 毛巾。',''),
                    ('保持接触并擦拭','P22,P29','重复行程与接触覆盖；原任务是干擦。','B29'),
                    ('离面与结束','P15','来源建议每轮约 5–10 秒并重复，具体时长服从原标签。','')])
    phases('T23',[
        ('定位目标与取得接近空间','P08','开抽屉只在出现时使用现有动作；柜门开启不冒充手内运动。','U28'),
        ('抓取并搬到目标区','P09,P10,P16','每件 / 每批物品、储位与手数。',''),
        ('稳定放置、归位或关抽屉','P19,P15','关抽屉是可选上下文；按实际视频分段。','U29')])
    for aid,ending in [('T24','餐具齐全且各就各位'),('T25','同类稳定叠放'),('T26','目标餐具在洗碗机内稳定落位'),('T27','餐具回到原储位')]:
        phases(aid,[('选择目标并抓取','P08,P09,P10','记录物体身份、先后次序与一次搬运件数。',''),
                    ('搬运与外部对位','P16,P19','运动归因于腕臂搬运，不能直接称作手内平移。',''),
                    ('释放并检查终态','P15','完成条件：'+ending+'；继续下一件或结束。','')])

    # Every raw label remains visible, even when several map to one invariant goal.
    labels=[
        ('Get/replace items from refrigerator/cabinets/drawers','从冰箱、柜子、抽屉取放物品','T23','通用取物 / 归位','cabinet,refrigerator,drawer,sink',[]),
        ('Clear cutting board','清理砧板','U55','蔬菜皮、蔬菜片、面包片','cutting_board,chef_knife,pot,pan,cucumber,potato,bread',[]),
        ('Peel a cucumber','给黄瓜去皮','U53','黄瓜','cucumber,peeler,cutting_board',['U57']),
        ('Slice a cucumber','黄瓜切片','U54','已去皮黄瓜 + 厨师刀','cucumber,chef_knife,cutting_board',['U58']),
        ('Peel a potato','给土豆去皮','U53','土豆','potato,peeler,cutting_board',['U57']),
        ('Slice a potato','土豆切片','U54','已去皮土豆 + 厨师刀','potato,chef_knife,cutting_board',['U58']),
        ('Slice bread','面包切片','U54','小餐包 + 面包刀','bread,bread_knife,cutting_board',['U58']),
        ('Spread almond butter on a bread slice','在面包片上涂杏仁酱','U56','杏仁酱；面包手持或桌面支撑','bread,table_knife,almond_butter,jar',['U59']),
        ('Spread jelly on a bread slice','在面包片上涂果冻酱','U56','原流程在杏仁酱层上涂果冻酱','bread,table_knife,jelly,jar',['U59']),
        ('Open/close a jar of almond butter','开合杏仁酱罐','B26','开合循环 3 次；可桌面支撑','jar,almond_butter',['B07','U22','U23']),
        ('Pour water from a pitcher into a glass','把水壶中的水倒进杯子','B14','手持接收杯；依次向 5 杯倒入','pitcher,cup,water',[]),
        ('Clean a plate with a sponge','用海绵擦盘子','B27','持盘 + 海绵；模拟干擦','plate,sponge',['B29']),
        ('Clean a plate with a towel','用毛巾擦盘子','B27','持盘 + 毛巾；模拟干擦','plate,cloth',['B29']),
        ('Clean a pan with a sponge','用海绵擦锅','B28','握锅柄 + 海绵；模拟干擦','pan,sponge',['B29']),
        ('Clean a pan with a towel','用毛巾擦锅','B28','握锅柄 + 毛巾；模拟干擦','pan,cloth',['B29']),
        ('Get items from cabinets: 3 each large/small plates, bowls, mugs, glasses, sets of utensils','取出三套餐具','T23','每类 3 件；大盘 / 小盘分开，刀勺叉各 3','cabinet,drawer,'+tableware,[]),
        ('Set table: 3 each large/small plates, bowls, mugs, glasses, sets of utensils','布置三套餐具','T24','三处用餐位置；每处八种餐具',''+tableware,[]),
        ('Stack on table: 3 each large/small plates, bowls','在桌上叠放三组盘碗','T25','大盘 / 小盘 / 碗，各 3 件','plate,bowl',[]),
        ('Load dishwasher: 3 each large/small plates, bowls, mugs, glasses, sets of utensils','将三套餐具装入洗碗机','T26','三套完整餐具；摆放策略可变',tableware+',dishwasher',[]),
        ('Unload dishwasher: 3 each large/small plates, bowls, mugs, glasses, sets of utensils','卸下三套餐具并归位','T27','三套完整餐具；返回原储位',tableware+',dishwasher,cabinet,drawer',[]),
    ]
    activity_rows=[]
    for n,(label,name,aid,condition,objects,subactions) in enumerate(labels,1):
        entry=dict(id=f'AS{n:02}',label=label,name=name,action=aid,condition=condition,props=objects.split(','),subactions=subactions,
                   source=source,url=HOME+'dataset_info.html#activities',protocol_url=SUPP+'#page=9')
        activity_rows.append(entry)
        by[aid].setdefault('source_labels',[]).append(entry['id'])
        by[aid].setdefault('conditions',[]).append(dict(label_id=entry['id'],name=name,detail=condition,props=entry['props']))
        by[aid].setdefault('aliases',[]).extend([label,name,condition])

    task_ids=list(dict.fromkeys(r['action'] for r in activity_rows))
    calibration_ids=['C13','C14','C09','C15','C16']
    families.append(dict(id='kitchen_process',name='食材加工、涂布与液体转移',definition='手持工具与材料状态变化；包含多次接触行程及双手支撑。',
                         actions=['U53','U54','U55','U56','U57','U58','U59','B14'],gap='ActionSense 为人类活动采集；本库拆解缺少逐次行程标签，不能据此声称机器人策略已成功。'))
    families.append(dict(id='household_sequence',name='餐具擦拭、收纳与长程任务链',definition='目标集合、存放环境与多物体次序共同决定任务完成。',
                         actions=['B26','B27','B28','B29','T23','T24','T25','T26','T27'],gap='完整活动与子步骤数量不可相加当独立能力数；擦拭为模拟干擦，洗碗机只装卸。'))
    families.append(dict(id='hand_calibration',name='手部传感与接触校准',definition='动作、参考负载和同步传感互相对照；校准流程单列。',
                         actions=calibration_ids,gap='不属于 20 项厨房活动。缺失指侧展、指尖触觉及部分参与者的手套数据，不能推定全关节 3D 真值。'))
    new_ids=[a['id'] for a in actions if a['id'] not in before_actions]
    new_prop_ids=[p['id'] for p in props if p['id'] not in before_props]
    dataset=dict(source=source,label_count=len(labels),activity_tasks=task_ids,activities=activity_rows,
                 license='CC BY-NC-SA 4.0',license_url=LICENSE,
                 attribution='DelPreto et al., ActionSense, NeurIPS 2022 / MIT. 中文译名、归并映射与采集拆解由 Dexterity Atlas 编写。',
                 calibration_actions=calibration_ids,equipment=equipment,props=new_prop_ids+list(reused),
                 new_actions=new_ids,enriched_actions=sorted(enriched),
                 scope='完整活动 → 本库任务链 → 建议采集子动作。原始材料没有提供本库这些细分步骤的逐帧标签。',
                 images=[dict(url=HOME+'images/kitchen_items.jpg',label='官方厨房道具总览'),dict(url=HOME+'images/activity_stats.jpg',label='官方 20 项活动标签表')],
                 dataset_notes=[
                     '真实人类厨房活动。20 个原标签映射为 13 个完整活动入口，材料与工具差异保留为条件；另有子动作和校准入口。',
                     '官网 Data 提醒早期 Manus 手指追踪不可靠；S06–S09 无手指追踪与触觉。逐 session 核查模态，不能以项目概览推定每次录制都有完整传感。',
                     '传感说明中手套只记录指屈曲而没有侧展，触觉未覆盖指尖；身体 IMU 的全局位置也可能漂移。',
                     '细粒度分段、阶段判据与中文任务拆解是本库编写；校准协议来自 C.3.1，厨房流程来自 C.4。',
                 ])
    audit=dict(version='1.3',date=DATE,title='ActionSense · 活动与道具逐项拆解',
               new_action_count=len(new_ids),new_prop_count=len(new_prop_ids),enriched_action_count=len(enriched),
               projects=[dict(source=source,new_actions=new_ids,enriched_actions=sorted(enriched),new_props=new_prop_ids,
                              existing_props=list(reused),note='20 个标签均有映射；同技能材料条件合并，倒水复用 B14，单指校准复用 C09，开盖子步骤关联既有动作。')],
               granularity_note='新增条目包括完整活动、本库拆解子动作与校准协议。它们不是相互独立的技能；器材也不计作操纵道具或动作。')
    return audit,dataset
