"""第二轮：清除运行时里的武汉痕迹（城区名、传送点、相机、大剧院占位模型）。可重复运行。"""
import json,pathlib,math
R=pathlib.Path(__file__).resolve().parents[1]/'slop-xining'
def patch(rel,pairs):
    p=R/rel;s=p.read_text(encoding='utf-8');o=s
    for old,new in pairs:
        if new in s:continue
        if old not in s:raise SystemExit(f'patch target missing in {rel}: {old[:80]}')
        s=s.replace(old,new,1)
    if s!=o:p.write_text(s,encoding='utf-8')
    print('patched' if s!=o else 'unchanged',rel)

# 1) 运行包：出生点名称、城区标签、西宁传送点
patch('tools/build-runtime.py',[
 ("    teleports=[{'id':'jianghanguan','name':'江汉关博物馆','sub':'沿江大道 · 钟楼','x':spawn['x'],'z':spawn['z'],'heading':spawn['heading'],'road':'沿江大道'}]\n",
  "    XN=city['region']['id'].startswith('xining')\n"
  "    teleports=[{'id':'jianghanguan','name':'青海大剧院 · 五四西路' if XN else '江汉关博物馆','sub':'海湖新区 · 出生点' if XN else '沿江大道 · 钟楼','x':spawn['x'],'z':spawn['z'],'heading':spawn['heading'],'road':spawn.get('road','沿江大道')}]\n"
  "    if XN:\n"
  "        profile=json.loads((ROOT/'config/xining-core.json').read_text(encoding='utf-8'))\n"
  "        lon0,lat0=city['origin'];rad=math.pi/180;e2=6.69437999014e-3;s0=math.sin(lat0*rad)\n"
  "        sx=rad*6378137/math.sqrt(1-e2*s0*s0)*math.cos(lat0*rad);sz=rad*6378137*(1-e2)/(1-e2*s0*s0)**1.5\n"
  "        car=[(r,LineString([(q[0],q[2]) for q in r['points']])) for r in city['roads'] if r['mode']=='car' and r.get('class') in ('major','minor','local')]\n"
  "        for t in profile.get('teleports',[]):\n"
  "            target=Point((t['lon']-lon0)*sx,-(t['lat']-lat0)*sz)\n"
  "            r,line=min(car,key=lambda row:row[1].distance(target));d=line.project(target);p=line.interpolate(d);q=line.interpolate(min(line.length,d+3))\n"
  "            teleports.append({'id':t['id'],'name':t['name'],'sub':t.get('sub','西宁'),'x':p.x,'z':p.y,'heading':math.atan2(q.x-p.x,q.y-p.y),'road':r['name'],'mode':t.get('mode','car')})\n"),
 ("            teleports.append({'id':p['id'],'name':p['name'],'sub':'汉口核心区',","            teleports.append({'id':p['id'],'name':p['name'],'sub':p.get('district','汉口核心区'),"),
 ("    anchors=[('汉口',Point(-200,0)),('汉阳',Point(-2400,3200)),('武昌',Point(1700,4000))]\n",
  "    anchors=[('汉口',Point(-200,0)),('汉阳',Point(-2400,3200)),('武昌',Point(1700,4000))]\n    if city['region']['id'].startswith('xining'):anchors=[('城西区',Point(spawn['x'],spawn['z']))]\n"),
])
# 传送点清单（WGS84，取最近的车行道作为到达点）
cfg=R/'config/xining-core.json';prof=json.loads(cfg.read_text(encoding='utf-8'))
prof['teleports']=[
 {'id':'xn-tangdao','name':'唐道637','sub':'海湖新区 · 商业街区','lon':101.7164,'lat':36.6425,'mode':'person'},
 {'id':'xn-wanda','name':'海湖万达广场','sub':'海湖新区','lon':101.7139,'lat':36.6427},
 {'id':'xn-sports','name':'青海体育中心','sub':'海湖新区','lon':101.6973,'lat':36.6505},
 {'id':'xn-wetland','name':'海湖湿地公园','sub':'湟水河畔','lon':101.6850,'lat':36.6534,'mode':'person'},
 {'id':'xn-huangshui-forest','name':'湟水森林公园','sub':'湟水河畔','lon':101.6996,'lat':36.6383,'mode':'person'},
 {'id':'xn-qilinwan','name':'麒麟湾公园','sub':'西关大街','lon':101.7690,'lat':36.6215,'mode':'person'},
 {'id':'xn-kunlun-bridge','name':'昆仑桥','sub':'昆仑西路','lon':101.7677,'lat':36.6186},
]
cfg.write_text(json.dumps(prof,ensure_ascii=False,indent=2),encoding='utf-8');print('teleports',len(prof['teleports']))

# 2) 相机：换成西宁机位（坐标为本地米制，原点 101.7165E 36.6445N，x 向东，z 向南）
O=prof['origin'];rad=math.pi/180;e2=6.69437999014e-3;s0=math.sin(O[1]*rad)
SX=rad*6378137/math.sqrt(1-e2*s0*s0)*math.cos(O[1]*rad);SZ=rad*6378137*(1-e2)/(1-e2*s0*s0)**1.5
P=lambda lon,lat:[round((lon-O[0])*SX),round(-(lat-O[1])*SZ)]
th=P(101.7172,36.6458);td=P(101.7164,36.6425);wd=P(101.7139,36.6427);sp=P(101.6973,36.6505);wl=P(101.6850,36.6534);ql=P(101.7690,36.6215);rv=P(101.7250,36.6500)
views={'grand-theatre':{'position':[th[0]+260,70,th[1]+260],'target':[th[0],18,th[1]]},
 'tangdao':{'position':[td[0]+120,14,td[1]+160],'target':[td[0],10,td[1]]},
 'haihu-skyline':{'position':[wd[0]-700,180,wd[1]+650],'target':[wd[0]+150,40,wd[1]-80]},
 'sports':{'position':[sp[0]+350,120,sp[1]+300],'target':[sp[0],10,sp[1]]},
 'wetland':{'position':[wl[0]+500,90,wl[1]+400],'target':[wl[0],0,wl[1]]},
 'huangshui':{'position':[rv[0]-600,110,rv[1]+250],'target':[rv[0]+400,0,rv[1]-150]},
 'qilinwan':{'position':[ql[0]-350,120,ql[1]-300],'target':[ql[0],0,ql[1]]},
 'overview':{'position':[1500,3200,7200],'target':[1500,0,600]}}
presets=("  {id:'chase',name:'第三人称跟随',short:'跟随',category:'follow',fov:56},\n"
 "  {id:'action',name:'低角度视角',short:'低角度',category:'follow',fov:60},\n"
 "  {id:'pov',name:'第一人称 / 驾驶座',short:'第一人称',category:'follow',fov:68},\n"
 "  {id:'grand-theatre',name:'青海大剧院与环形路',short:'大剧院',category:'scenic',fov:50},\n"
 "  {id:'tangdao',name:'唐道637街区',short:'唐道637',category:'scenic',fov:58},\n"
 "  {id:'haihu-skyline',name:'海湖新区天际线',short:'海湖新区',category:'scenic',fov:50},\n"
 "  {id:'sports',name:'青海体育中心',short:'体育中心',category:'scenic',fov:50},\n"
 "  {id:'wetland',name:'海湖湿地公园',short:'湿地公园',category:'scenic',fov:50},\n"
 "  {id:'huangshui',name:'湟水河',short:'湟水河',category:'scenic',fov:48},\n"
 "  {id:'qilinwan',name:'麒麟湾公园',short:'麒麟湾',category:'scenic',fov:50},\n"
 "  {id:'overview',name:'海湖新区—麒麟湾全景',short:'全景',category:'scenic',fov:50},\n"
 "  {id:'drone',name:'海湖新区空中环游',short:'环游',category:'scenic',fov:50}\n")
p=R/'js/runtime/cameras.js';s=p.read_text(encoding='utf-8')
a=s.index('const CAMERA_PRESETS = [\n')+len('const CAMERA_PRESETS = [\n');b=s.index('];\nconst WUHAN_VIEWS')
s=s[:a]+presets+s[b:]
a=s.index('const WUHAN_VIEWS = {\n')+len('const WUHAN_VIEWS = {\n');b=s.index('};\n',a)
s=s[:a]+',\n'.join(f" '{k}':{{position:{v['position']},target:{v['target']}}}" for k,v in views.items())+'\n'+s[b:]
s=s.replace('scenic Wuhan vantage points','scenic Xining vantage points')
p.write_text(s,encoding='utf-8');print('cameras',len(views))

# 3) 大剧院占位体块：真实轮廓拉伸 + 屋顶檐口（待第 3 步换成专门模型）
patch('js/wuhan-landmarks.js',[
 ("  if(l.type!=='jianghanguan')continue;\n",
  "  if(l.type==='grand-theatre'){\n"
  "   const root=new THREE.Group();root.name=l.name;scene.add(root);groups.push(root);\n"
  "   const wall=new THREE.Mesh(createFootprintGeometry({rings:l.footprint,h:l.height-4}),stone);wall.castShadow=wall.receiveShadow=true;root.add(wall);\n"
  "   const band=new THREE.Mesh(createFootprintGeometry({rings:l.footprint,h:3,baseY:l.height-4}),dark);band.castShadow=true;root.add(band);\n"
  "   const cap=new THREE.Mesh(createFootprintGeometry({rings:l.footprint,h:1,baseY:l.height-1}),trim);cap.castShadow=true;root.add(cap);\n"
  "   continue;\n"
  "  }\n"
  "  if(l.type!=='jianghanguan')continue;\n")])

# 4) 地图里的“代表地标”列表和搜索提示：改成西宁地点
patch('tools/build-runtime.py',[
 ("            teleports.append({'id':t['id'],'name':t['name'],'sub':t.get('sub','西宁'),'x':p.x,'z':p.y,'heading':math.atan2(q.x-p.x,q.y-p.y),'road':r['name'],'mode':t.get('mode','car')})\n",
  "            teleports.append({'id':t['id'],'name':t['name'],'sub':t.get('sub','西宁'),'x':p.x,'z':p.y,'heading':math.atan2(q.x-p.x,q.y-p.y),'road':r['name'],'mode':t.get('mode','car')})\n"
  "        xn_core=[{'id':t['id'],'name':t['name'].split(' · ')[0],'district':t['sub'].split(' · ')[0],'category':'地点','summary':t['sub'],'x':t['x'],'z':t['z'],'mode':t.get('mode','car'),\n"
  "                  'arrival':{'x':t['x'],'z':t['z'],'heading':t['heading'],'road':t['road']}} for t in teleports]\n"),
 ("'coreDestinations':city.get('coreDestinations',[]),","'coreDestinations':xn_core if city['region']['id'].startswith('xining') else city.get('coreDestinations',[]),"),
])
p=R/'index.html';s=p.read_text(encoding='utf-8');o=s
s=s.replace('搜索路名与地标：黄鹤楼、龟山电视塔、江汉关…','搜索路名与地标：五四西路、海湖路、大剧院…').replace('<summary>代表地标 <span>10处</span></summary>','<summary>代表地标 <span>8处</span></summary>')
if s!=o:p.write_text(s,encoding='utf-8');print('patched index.html')
