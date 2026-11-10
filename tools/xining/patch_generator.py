"""把武汉版生成器改成可按 profile 生成西宁数据（第一版：平地、桥梁落地）。可重复运行。"""
import json,pathlib,shutil,hashlib
R=pathlib.Path(__file__).resolve().parents[1]/'slop-xining'
def patch(rel,pairs):
    p=R/rel;s=p.read_text(encoding='utf-8');o=s
    for old,new in pairs:
        if new in s:continue
        if old not in s:raise SystemExit(f'patch target missing in {rel}: {old[:70]}')
        s=s.replace(old,new,1)
    if s!=o:p.write_text(s,encoding='utf-8')
    print('patched' if s!=o else 'unchanged',rel)
patch('tools/city_profile.py',[
 ("ROOT/'config/wuhan-core.json'","ROOT/'config/xining-core.json'"),
 ("if data['origin']!=[114.293,30.585] or data['tileSizeM']!=500:","if data['tileSizeM']!=500:")])
patch('tools/import-citywide.py',[
 ("path=ROOT/'data/hubei-latest.osm.pbf'","path=ROOT/PROFILE.get('pbf','data/hubei-latest.osm.pbf')"),
 ("'url':'https://download.geofabrik.de/asia/china/hubei-latest.osm.pbf'","'url':PROFILE.get('pbfUrl','https://download.geofabrik.de/asia/china/hubei-latest.osm.pbf')")])
patch('tools/build-wuhan.py',[
 ("os.environ['WUHAN_PROFILE']=profile['_file']\n","os.environ['WUHAN_PROFILE']=profile['_file'];SOURCE=ROOT/profile.get('pbf','data/hubei-latest.osm.pbf');ORIGIN=profile['origin'];XN=profile['id'].startswith('xining')\n"),
 ("        if r['tunnel'] or r['bridge'] or r['layer']!=0:\n",
  "        if XN and not r['tunnel'] and r['layer']>=0 and (r['bridge'] or r['layer']>0):\n            r={**r,'flatBridgeOriginal':{'bridge':r['bridge'],'layer':r['layer']},'bridge':False,'layer':0,'levelSource':'flattened-v1:bridge-or-viaduct-drawn-at-grade'}\n        if r['tunnel'] or r['bridge'] or r['layer']!=0:\n"),
 ("    asphalt=unary_union([line.buffer(r['width']/2,quad_segs=4)",
  "    if XN:\n        water=water.difference(unary_union([line.buffer(r['width']/2+1.5) for line,r in zip(road_lines,roads) if r.get('flatBridgeOriginal')])).buffer(0)\n    asphalt=unary_union([line.buffer(r['width']/2,quad_segs=4)"),
 ("    landmark_source=next((b for b in raw['buildings'] if b['name']=='江汉关大楼'),None)\n    if landmark_source is None:raise",
  "    landmark_source=next((b for b in raw['buildings'] if b['name']=='江汉关大楼'),None)\n    if XN:\n        spec=profile['primaryLandmark'];px,pz=project(spec['lon'],spec['lat']);near=[b for b in raw['buildings'] if geometry(b['polygons']).distance(Point(px,pz))<80]\n        landmark_source=max(near,key=lambda b:geometry(b['polygons']).area) if near else {'id':'synthetic-'+spec['id'],'polygons':polygons(Point(px,pz).buffer(38,quad_segs=6))}\n    if landmark_source is None:raise"),
 ("    landmarks=[landmark]\n",
  "    if XN:landmark.update({'id':spec['id'],'name':spec['name'],'type':spec['type'],'height':spec['height'],'modelSource':'footprint + placeholder massing','heightSource':spec.get('heightSource','visual-estimate'),'aliases':spec.get('aliases',[]),'district':profile.get('district','')})\n    landmarks=[landmark]\n"),
 ("    for name in ['江汉路','沿江大道','中山大道','北京路','南京路','洞庭街']:","    for name in profile.get('placeRoads',['江汉路','沿江大道','中山大道','北京路','南京路','洞庭街']):"),
 ("places.append({'id':'road-'+name,'name':name,'district':'汉口试验区'","places.append({'id':'road-'+name,'name':name,'district':profile.get('district','汉口试验区')"),
 ("    spawn=next((p for p in places if p['name']=='沿江大道'),None)","    SPAWN=profile.get('spawnRoad','沿江大道')\n    spawn=next((p for p in places if p['name']==SPAWN),None)"),
 ("if r['name']=='沿江大道' and r['mode']=='car']","if r['name']==SPAWN and r['mode']=='car']"),
 ("    walking=[(r,line) for r,line in zip(roads,road_lines) if r['name']=='江汉路']","    walking=[(r,line) for r,line in zip(roads,road_lines) if XN or r['name']=='江汉路']"),
 ("'landmarkId':'jianghanguan'}","'landmarkId':landmark['id']}"),
 ("(ROOT/'config/core-destinations.json')","(ROOT/profile.get('destinations','config/core-destinations.json'))")])
# 数据：Overture 与楼高裁剪
src=R.parent/'数据/原始';dst=R/'data/source'
shutil.copy(src/'overture_buildings.geojson',dst/'overture-xining-buildings.geojson');shutil.copy(src/'overture_buildings.geojson.state',dst/'overture-xining-buildings.geojson.state')
g=json.loads((src/'globfp_xining_clip.geojson').read_text())
feats=[{'type':'Feature','id':f['id'],'properties':{'height':round(f['properties']['Height'],3),'method':'remote-sensing-model-estimate','referenceYear':2020},'geometry':f['geometry']} for f in g['features'] if 2<=f['properties']['Height']<=650]
meta={'provider':'3D-GloBFP','article':'https://figshare.com/articles/dataset/28904453','download':'https://ndownloader.figshare.com/files/54098723','fileId':54098723,'block':'2163_100.0_35.0_102.5_37.5_gansuCN_qinghaiCN','archiveMd5':'3558157564736aee33083f0e351dfd5c','crs':'EPSG:4326','referenceYear':2020,'license':'CC BY 4.0',
 'citation':'Che et al., 2024, 3D-GloBFP: the first global three-dimensional building footprint dataset, ESSD 16, 5357-5374, https://doi.org/10.5194/essd-16-5357-2024','boundsWgs84':[101.690,36.612,101.778,36.658],'features':len(feats),'limitations':['Model heights are estimates, not surveyed','2020 reference year; tall towers are underestimated']}
(dst/'globfp-xining-buildings.geojson').write_text(json.dumps({'type':'FeatureCollection','source':meta,'features':feats},separators=(',',':')))
profile={'id':'xining-haihu-qilinwan','name':'西宁·海湖新区—麒麟湾','boundsWgs84':[101.690,36.612,101.778,36.658],'origin':[101.7165,36.6445],'tileSizeM':500,
 'pbf':'data/qinghai-latest.osm.pbf','pbfUrl':'https://download.geofabrik.de/asia/china/qinghai-latest.osm.pbf',
 'overtureExtract':'data/source/overture-xining-buildings.geojson','heightExtract':'data/source/globfp-xining-buildings.geojson',
 'district':'海湖新区','placeRoads':['五四西路','西关大街','昆仑西路','海湖路','文苑路','文景街','通海路','桃李路'],'spawnRoad':'五四西路',
 'primaryLandmark':{'id':'qinghai-grand-theatre','name':'青海大剧院','type':'grand-theatre','lon':101.7172,'lat':36.6458,'height':36,'heightSource':'visual-estimate','aliases':['大剧院']},
 'destinations':'config/xining-destinations.json',
 'description':'约7.9公里×5.1公里；WGS84真实位置与米制距离。第一版：平地，桥梁与高架落地绘制，无地形。'}
(R/'config/xining-core.json').write_text(json.dumps(profile,ensure_ascii=False,indent=2))
(R/'config/xining-destinations.json').write_text(json.dumps({'destinations':[]},ensure_ascii=False,indent=2))
print('profile + extracts written; height features',len(feats))
