"""第五轮：西关大街一带的地图标注。坐标均取自 OpenStreetMap；力盟商业步行街取 OSM 中力盟101大厦与力盟商业巷和熙楼的中点。可重复运行。"""
import json,pathlib
R=pathlib.Path(__file__).resolve().parents[1]/'slop-xining'
cfg=R/'config/xining-core.json';prof=json.loads(cfg.read_text(encoding='utf-8'))
add=[
 {'id':'xn-xinning-square','name':'新宁广场','sub':'西关大街 · 五四大街','lon':101.7529,'lat':36.63141,'mode':'person','category':'广场','source':'OSM w612003901'},
 {'id':'xn-qh-museum','name':'青海省博物馆','sub':'新宁广场东南','lon':101.75405,'lat':36.63028,'mode':'person','category':'地标','source':'OSM w55574906'},
 {'id':'xn-qh-library','name':'青海省图书馆','sub':'新宁广场西南','lon':101.75081,'lat':36.62997,'mode':'person','category':'地标','source':'OSM w878427314'},
 {'id':'xn-limeng','name':'力盟商业步行街','sub':'西关大街北侧','lon':101.75619,'lat':36.62843,'mode':'person','category':'商业','source':'OSM 力盟101大厦 n13968361597 与 力盟商业巷和熙楼 n13968361596 中点'},
 {'id':'xn-jiahao','name':'佳豪国际广场','sub':'西关大街','lon':101.75881,'lat':36.62876,'category':'商业','source':'OSM n13968361574'},
 {'id':'xn-wanfang','name':'万方城','sub':'五四大街','lon':101.76329,'lat':36.63108,'category':'商业','source':'OSM n13968361628'},
 {'id':'xn-hutai','name':'南凉虎台遗址公园','sub':'虎台','lon':101.74593,'lat':36.63286,'mode':'person','category':'公园','source':'OSM w371987572'},
 {'id':'xn-xinninglu-station','name':'新宁路客运站','sub':'新宁路','lon':101.75307,'lat':36.63413,'category':'交通','source':'OSM n13968361645'},
 {'id':'xn-no12-school','name':'西宁市第十二中学','sub':'古城台','lon':101.75436,'lat':36.62594,'mode':'person','category':'学校','source':'OSM w1478745143'},
 {'id':'xn-culture-park','name':'文化公园','sub':'五四西路','lon':101.74235,'lat':36.64405,'mode':'person','category':'公园','source':'OSM w371882591'},
 {'id':'xn-people-park','name':'西宁人民公园','sub':'湟水河畔','lon':101.76356,'lat':36.63667,'mode':'person','category':'公园','source':'OSM w689565079'},
 {'id':'xn-central-square','name':'中心广场','sub':'西关大街东端','lon':101.77252,'lat':36.62292,'mode':'person','category':'广场','source':'OSM w155424390'},
]
have={t['id'] for t in prof['teleports']}
prof['teleports']+= [t for t in add if t['id'] not in have]
cfg.write_text(json.dumps(prof,ensure_ascii=False,indent=2),encoding='utf-8')
n=len(prof['teleports'])+1
h=R/'index.html';s=h.read_text(encoding='utf-8')
import re;s2=re.sub(r'<summary>代表地标 <span>\d+处</span></summary>',f'<summary>代表地标 <span>{n}处</span></summary>',s)
if s2!=s:h.write_text(s2,encoding='utf-8')
print('teleports',len(prof['teleports']),'list',n)
