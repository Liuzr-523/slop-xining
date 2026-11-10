"""第四轮：地图标注。位置全部取自 OpenStreetMap（海湖广场取 OSM“广场环路”的圆心）；分类显示在地图列表里。可重复运行。"""
import json,pathlib
R=pathlib.Path(__file__).resolve().parents[1]/'slop-xining'
p=R/'tools/build-runtime.py';s=p.read_text(encoding='utf-8');o=s
s=s.replace("'road':r['name'],'mode':t.get('mode','car')})\n        xn_core=","'road':r['name'],'mode':t.get('mode','car'),'category':t.get('category','地点')})\n        xn_core=")
s=s.replace("'category':'地点','summary':t['sub']","'category':t.get('category','地标'),'summary':t['sub']")
if s!=o:p.write_text(s,encoding='utf-8');print('patched build-runtime.py')
cfg=R/'config/xining-core.json';prof=json.loads(cfg.read_text(encoding='utf-8'))
prof['teleports']=[
 {'id':'xn-haihu-plaza','name':'海湖广场','sub':'海湖新区 · 广场环路','lon':101.713813,'lat':36.645219,'mode':'person','category':'广场','source':'OSM 广场环路 圆心拟合'},
 {'id':'xn-science-museum','name':'青海省科学技术馆','sub':'海湖新区 · 广场环路西北','lon':101.71181,'lat':36.64687,'mode':'person','category':'地标','source':'OSM n9177401404'},
 {'id':'xn-tangdao','name':'唐道637','sub':'海湖新区 · 商业街区','lon':101.71643,'lat':36.64242,'mode':'person','category':'商业','source':'OSM w1126145681'},
 {'id':'xn-wanda','name':'海湖万达广场','sub':'海湖新区','lon':101.714,'lat':36.64246,'category':'商业','source':'OSM w1126145677'},
 {'id':'xn-sports','name':'青海体育中心','sub':'海湖新区','lon':101.6973,'lat':36.6505,'category':'体育','source':'OSM'},
 {'id':'xn-wetland','name':'海湖湿地公园','sub':'湟水河畔','lon':101.6850,'lat':36.6534,'mode':'person','category':'公园','source':'OSM'},
 {'id':'xn-huangshui-forest','name':'湟水森林公园','sub':'湟水河畔','lon':101.6996,'lat':36.6383,'mode':'person','category':'公园','source':'OSM'},
 {'id':'xn-qilinwan','name':'麒麟湾公园','sub':'西关大街','lon':101.7690,'lat':36.6215,'mode':'person','category':'公园','source':'OSM'},
 {'id':'xn-kunlun-bridge','name':'昆仑桥','sub':'昆仑西路','lon':101.7677,'lat':36.6186,'category':'桥梁','source':'OSM'},
]
cfg.write_text(json.dumps(prof,ensure_ascii=False,indent=2),encoding='utf-8')
h=R/'index.html';t=h.read_text(encoding='utf-8');t2=t.replace('<summary>代表地标 <span>8处</span></summary>','<summary>代表地标 <span>10处</span></summary>')
if t2!=t:h.write_text(t2,encoding='utf-8');print('patched index.html')
print('teleports',len(prof['teleports']))

# 标签画在真实位置（OSM 坐标），传送到达点仍是最近车行道
s=p.read_text(encoding='utf-8');o=s
s=s.replace("'mode':t.get('mode','car'),'category':t.get('category','地点')})\n","'mode':t.get('mode','car'),'category':t.get('category','地点'),'tx':target.x,'tz':target.y})\n")
s=s.replace("'summary':t['sub'],'x':t['x'],'z':t['z'],","'summary':t['sub'],'x':t.get('tx',t['x']),'z':t.get('tz',t['z']),")
if s!=o:p.write_text(s,encoding='utf-8');print('patched label positions')
