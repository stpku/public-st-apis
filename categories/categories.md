# API 分类定义

此文件定义了 Public ST APIs 项目中使用的API分类体系。

## 分类列表

### Mapping Services (地图服务)
- **描述**: 提供基础地图瓦片、地图样式、矢量地图等服务
- **示例用途**: 显示地图、切换地图样式、获取地图瓦片
- **关键词**: map tiles, basemap, vector tiles, map style

### Weather APIs (天气API)
- **描述**: 提供天气数据、预报、气候信息等服务
- **示例用途**: 获取实时天气、天气预报、历史天气数据
- **关键词**: weather, forecast, climate, meteorological

### POI Queries (兴趣点查询)
- **描述**: 提供地点搜索、POI数据、地址解析等服务
- **示例用途**: 搜索地点、获取POI详情、地址转坐标
- **关键词**: poi, places, geocoding, address lookup

### Spatial Intelligence (空间智能)
- **描述**: 提供空间分析、路径规划、地理围栏等智能服务
- **示例用途**: 路径规划、空间关系分析、地理围栏
- **关键词**: spatial analysis, routing, geofencing, spatial intelligence

### Geocoding (地理编码)
- **描述**: 提供地址与坐标相互转换的服务
- **示例用途**: 地址转坐标、坐标转地址、批量地理编码
- **关键词**: geocoding, reverse geocoding, coordinates, addresses

### Routing (路径规划)
- **描述**: 提供路线规划、导航、交通状况等服务
- **示例用途**: 最短路径、最快路径、多点路径规划
- **关键词**: routing, navigation, directions, traffic

### Satellite Imagery (卫星影像)
- **描述**: 提供卫星图像、遥感数据等服务
- **示例用途**: 获取卫星图像、遥感分析、影像处理
- **关键词**: satellite imagery, remote sensing, earth observation

### Transportation (交通)
- **描述**: 提供公共交通、交通状况、出行规划等服务
- **示例用途**: 公交查询、交通状况、出行规划
- **关键词**: transportation, transit, traffic, mobility

### Environment (环境)
- **描述**: 提供环境监测、污染数据、生态保护等服务
- **示例用途**: 空气质量、水质监测、生态数据
- **关键词**: environment, pollution, air quality, ecology

### Demographics (人口统计)
- **描述**: 提供人口统计、社会经济数据等服务
- **示例用途**: 人口分布、经济数据、社会指标
- **关键词**: demographics, population, census, socioeconomic

## 分类管理

- 每个API只能属于一个主要分类
- 分类名称应简洁明了
- 新分类的添加需要经过社区讨论
- 分类定义应保持稳定，避免频繁变更