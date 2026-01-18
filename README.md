# Public ST APIs - 时空信息服务API集合

## 项目概述

Public ST APIs 是一个专注于地理空间和时空信息服务的API集合项目，旨在为开发者提供一个全面、可扩展的地理空间API资源库。该项目受 public-apis 项目的启发，专门收集与地图服务、天气API、POI查询、空间智能等相关的免费API。

## 项目特点

- **专注时空领域**: 专门收集地理空间和时空信息服务API
- **分类清晰**: 按照功能将API分为不同类别，便于查找和使用
- **可扩展性强**: 模块化设计，易于添加新的API分类和服务
- **数据验证**: 提供工具验证API数据的格式和有效性
- **易于使用**: 提供搜索工具和清晰的文档

## 当前API集合

### 1. 地图服务 (Mapping Services)
提供基础地图瓦片、地图样式、矢量地图等服务，包括：
- OpenStreetMap Tiles
- Google Maps Platform
- Mapbox
- Stadia Maps
- Thunderforest

### 2. 天气API (Weather APIs)
提供天气数据、预报、气候信息等服务，包括：
- OpenWeatherMap
- WeatherAPI
- AccuWeather
- Tomorrow.io
- Visual Crossing Weather

### 3. POI查询 (Points of Interest)
提供地点搜索、POI数据、地址解析等服务，包括：
- Google Places API
- Foursquare Places API
- OpenStreetMap Nominatim
- Mapbox Geocoding
- HERE Geocoding & Search

### 4. 空间智能 (Spatial Intelligence)
提供空间分析、路径规划、地理围栏等智能服务，包括：
- Google Maps Distance Matrix API
- OpenRouteService
- Geoapify
- LocationIQ
- GraphHopper

## 使用方法

### 浏览API
您可以直接查看 `data/index.md` 文件来浏览所有可用的API。

### 搜索API
使用 `utils/search_apis.py` 脚本来搜索特定的API或按分类浏览：

```bash
python utils/search_apis.py
```

### 验证数据
使用 `utils/validate_apis.py` 脚本来验证API数据的格式：

```bash
python utils/validate_apis.py
```

## 使用示范

### 1. 在Web应用中使用地图API

以下是如何在网页中使用OpenStreetMap Tiles API的示例：

```html
<!DOCTYPE html>
<html>
<head>
    <title>使用OpenStreetMap示例</title>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.7.1/dist/leaflet.css" />
</head>
<body>
    <div id="map" style="height: 400px;"></div>

    <script src="https://unpkg.com/leaflet@1.7.1/dist/leaflet.js"></script>
    <script>
        var map = L.map('map').setView([39.9042, 116.4074], 13); // 北京坐标

        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        }).addTo(map);

        L.marker([39.9042, 116.4074]).addTo(map)
            .bindPopup('北京')
            .openPopup();
    </script>
</body>
</html>
```

### 2. 使用天气API获取实时天气

以下是如何使用OpenWeatherMap API获取实时天气数据的示例：

```javascript
// JavaScript示例
const apiKey = 'YOUR_API_KEY';
const city = 'Beijing';
const url = `https://api.openweathermap.org/data/2.5/weather?q=${city}&appid=${apiKey}&units=metric`;

fetch(url)
    .then(response => response.json())
    .then(data => {
        console.log(`温度: ${data.main.temp}°C`);
        console.log(`天气: ${data.weather[0].description}`);
        console.log(`湿度: ${data.main.humidity}%`);
    })
    .catch(error => console.error('Error:', error));
```

### 3. 使用POI查询API

以下是如何使用OpenStreetMap Nominatim API进行地理编码的示例：

```python
# Python示例
import requests

def geocode_address(address):
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        'q': address,
        'format': 'json',
        'limit': 1
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data:
            return {
                'lat': float(data[0]['lat']),
                'lon': float(data[0]['lon']),
                'display_name': data[0]['display_name']
            }
    return None

# 使用示例
location = geocode_address("北京市天安门广场")
print(location)
```

### 4. 使用空间智能API进行路径规划

以下是如何使用OpenRouteService API进行路径规划的示例：

```python
# Python示例
import requests

def get_route(start_lon, start_lat, end_lon, end_lat, api_key):
    url = "https://api.openrouteservice.org/v2/directions/driving-car"

    headers = {
        'Authorization': api_key,
        'Content-Type': 'application/json'
    }

    body = {
        "coordinates": [[start_lon, start_lat], [end_lon, end_lat]],
        "format": "geojson"
    }

    response = requests.post(url, headers=headers, json=body)
    if response.status_code == 200:
        return response.json()
    return None

# 使用示例（需要有效的API密钥）
# route = get_route(116.3972, 39.9075, 116.4074, 39.9042, 'YOUR_API_KEY')
```

### 5. 使用搜索工具查找API

您可以使用项目提供的搜索工具来查找特定类型的API：

```bash
# 启动交互式搜索
python utils/search_apis.py

# 或者在代码中使用API数据
import json

# 读取地图服务API
with open('api/mapping/mapping_apis.json', 'r', encoding='utf-8') as f:
    mapping_apis = json.load(f)

for api in mapping_apis:
    print(f"API名称: {api['name']}")
    print(f"描述: {api['description']}")
    print(f"文档: {api['url']}")
    print("---")
```

## 扩展项目

### 添加新的API
要添加新的API，请按照以下步骤操作：

1. 确定API所属的分类
2. 在相应的分类目录中编辑或创建JSON文件
3. 按照标准格式添加API信息
4. 运行验证脚本确保格式正确
5. 更新索引文件（如有必要）

### 创建新的分类
要创建新的API分类，请：

1. 在 `categories/categories.md` 中定义新分类
2. 在 `api/` 目录下创建新分类的子目录
3. 在新目录中添加API数据文件
4. 更新 `data/index.md` 索引文件

## 技术细节

### 数据格式
所有API数据均以JSON格式存储，每个API条目包含以下字段：
- `name`: API名称
- `description`: API描述
- `auth`: 认证方式（apiKey, oauth, 或 null）
- `https`: 是否支持HTTPS
- `cors`: CORS支持状态（yes/no/unknown）
- `category`: API分类
- `url`: API文档链接
- `comment`: 额外说明（可选）

### 项目结构
```
public-st-apis/
├── api/                    # API定义和分类
│   ├── mapping/           # 地图服务API
│   ├── weather/           # 天气API
│   ├── poi/               # POI查询API
│   └── spatial_intelligence/ # 空间智能API
├── categories/            # API分类定义
├── data/                  # 示例数据和索引
├── utils/                 # 工具脚本
│   ├── validate_apis.py   # API数据验证工具
│   └── search_apis.py     # API搜索工具
└── docs/                  # 扩展文档
```

## 贡献

我们欢迎任何形式的贡献！请参阅 `CONTRIBUTING.md` 获取更多信息。

## 许可证

MIT License