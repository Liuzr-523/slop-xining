"""第三轮：加入 CMAB（清华，2023 影像，CC BY 4.0）作为第三个建筑来源，只补 OSM/Overture 都没有的楼。可重复运行。"""
import json,pathlib
R=pathlib.Path(__file__).resolve().parents[1]/'slop-xining'
p=R/'tools/build-wuhan.py';s=p.read_text(encoding='utf-8')
old="    parts_audit=apply_parts(buildings,raw.get('buildingParts',[]),evidence)\n"
new=("    if profile.get('cmabExtract'):\n"
"        have=STRtree([Polygon(b['rings'][0],b['rings'][1:]) for b in buildings]);have_polys=list(have.geometries)\n"
"        cmab=json.loads((ROOT/profile['cmabExtract']).read_text(encoding='utf-8'))\n"
"        for feature in cmab['features']:\n"
"            props=feature['properties']\n"
"            g=make_valid(transform(project,shape(feature['geometry']))).intersection(region)\n"
"            for i,poly in enumerate(parts(g)):\n"
"                if poly.area<40:continue\n"
"                if any(poly.intersection(have_polys[int(j)]).area>.2*min(poly.area,have_polys[int(j)].area) for j in have.query(poly)):\n"
"                    excluded['cmab_duplicate']+=1;continue\n"
"                item={'id':feature['id'],'h':props.get('height') or 0,'heightSource':'CMAB:model-estimate','name':'',\n"
"                      'tags':{'building':'yes'},'sourceDatasets':['CMAB (Zhang, Zhao & Long 2025, CC BY 4.0)']}\n"
"                add_building(item,poly,i,'CMAB:footprint')\n"
+old)
if "profile.get('cmabExtract')" not in s:
    assert old in s;s=s.replace(old,new,1);p.write_text(s,encoding='utf-8');print('patched build-wuhan.py')
else:print('unchanged build-wuhan.py')
cfg=R/'config/xining-core.json';prof=json.loads(cfg.read_text(encoding='utf-8'))
prof['cmabExtract']='data/source/cmab-xining-buildings.geojson'
cfg.write_text(json.dumps(prof,ensure_ascii=False,indent=2),encoding='utf-8');print('profile updated')
