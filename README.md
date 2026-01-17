# Public ST APIs (Space-Time APIs)

一个可扩展的地理空间API集合，专注于满足各类时空信息服务需求，如地图服务、天气API、POI查询、空间智能等。

## 项目概述

Public ST APIs 是一个受 public-apis 项目启发的地理空间和时空信息服务API集合。该项目致力于整理和提供免费的地理空间API，涵盖地图服务、天气数据、POI查询、空间智能等多个领域，以满足开发者在构建时空应用时的需求。

## 目录结构

```
public-st-apis/
├── api/                    # API定义和分类
│   ├── mapping/           # 地图服务API
│   ├── weather/           # 天气API
│   ├── poi/               # POI查询API
│   ├── spatial_intelligence/ # 空间智能API
│   └── other/             # 其他地理空间API
├── categories/            # API分类定义
├── data/                  # 示例数据和测试数据
├── utils/                 # 工具函数和验证脚本
├── docs/                  # 文档
├── CONTRIBUTING.md        # 贡献指南
└── README.md              # 项目说明
```

## API分类

### 地图服务 (Mapping Services)
- 提供基础地图瓦片服务
- 支持多种地图样式
- 支持矢量地图服务

### 天气API (Weather APIs)
- 实时天气数据
- 天气预报
- 历史天气数据
- 气候数据分析

### POI查询 (Points of Interest)
- 地点搜索
- 地址解析
- 兴趣点数据
- 地理编码服务

### 空间智能 (Spatial Intelligence)
- 路径规划
- 空间分析
- 地理围栏
- 空间关系计算

## 贡献指南

我们欢迎任何形式的贡献！请参阅 [CONTRIBUTING.md](CONTRIBUTING.md) 获取更多信息。

## API提交规范

要提交新的API，请遵循以下格式：

```json
{
  "name": "API名称",
  "description": "API描述",
  "auth": "认证方式 (apiKey, oauth, 或 null)",
  "https": true,
  "cors": "CORS支持状态",
  "category": "API分类",
  "url": "API文档链接",
  "comment": "额外说明"
}
```

## 许可证

MIT License