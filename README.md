# Slop 西宁

西宁海湖新区到麒麟湾的浏览器城市漫游：步行、开车、骑行、坐直升机，逛青海大剧院、海湖广场、唐道637、新宁广场和力盟商业步行街一带。three.js · WebGPU · TSL。

**在线体验：** https://liuzr-523.github.io/slop-xining/

> 需要支持 WebGPU 的浏览器：电脑上用新版 Chrome / Edge；苹果设备需较新的系统与 Safari。首次进入要编译着色器，约半分钟。

## 来历
- 原作：[mrdoob/slop-newyork](https://github.com/mrdoob/slop-newyork)
- 运行系统沿用 [LightYearZh/slop-wuhan](https://github.com/LightYearZh/slop-wuhan)（其运行系统又源于 Slop Taipei），本仓库把城市数据、地名、机位和传送点换成了西宁。武汉版原说明保留在 `README-wuhan-upstream.md`。

## 范围与数据
- 经度 101.690–101.778，纬度 36.612–36.658，约 7.9 × 5.1 公里，真实位置、1:1 距离。
- 路网、水系、地名：OpenStreetMap；建筑轮廓：OSM、Overture Maps、CMAB；楼高：3D-GloBFP 与 CMAB 遥感估算。
- 楼高与外观大多为估算，环形路圈内等新建区域开放数据缺失，地标为占位体块，后续手工补建。

详细来源与许可见 [数据来源与许可.md](数据来源与许可.md)。

## 本地运行
任意静态服务器即可，不需要打包：

```sh
python3 -m http.server 8765
# 打开 http://localhost:8765
```

## 重新生成数据
需要 Python 3.10+、`shapely` `osmium` `pyshp` `numpy`，并把 Geofabrik 的 `qinghai-latest.osm.pbf` 放到 `data/`：

```sh
python tools/build-wuhan.py      # 读 config/xining-core.json，生成 public/data/city.json
python tools/build-runtime.py    # 生成 js/runtime/wuhan-geodata.*
```

`tools/xining/` 里是把武汉版改成西宁的补丁脚本，记录了每一处改动。

## 许可
代码：MIT（见 LICENSE）。地理数据：OSM 为 ODbL 1.0，3D-GloBFP 与 CMAB 为 CC BY 4.0，其余见各自条款。
