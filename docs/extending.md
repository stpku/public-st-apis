# 扩展 Public ST APIs 项目

本文档介绍如何扩展和定制 Public ST APIs 项目以满足特定的时空信息服务需求。

## 项目架构

Public ST APIs 采用模块化设计，便于扩展：

```
public-st-apis/
├── api/                    # API定义和分类
│   ├── mapping/           # 地图服务API
│   ├── weather/           # 天气API
│   ├── poi/               # POI查询API
│   ├── spatial_intelligence/ # 空间智能API
│   └── [新分类]/          # 新增的分类
├── categories/            # API分类定义
├── data/                  # 示例数据和索引
├── utils/                 # 工具脚本
└── docs/                  # 扩展文档
```

## 添加新的API分类

要添加新的API分类，请执行以下步骤：

### 1. 更新分类定义
修改 `categories/categories.md` 文件，添加新的分类定义。

### 2. 创建分类目录
在 `api/` 目录下创建新的分类子目录：

```bash
mkdir api/[新分类名称]
```

### 3. 添加API数据
在新创建的目录中添加JSON文件，包含该分类下的API定义：

```json
[
  {
    "name": "API名称",
    "description": "API描述",
    "auth": "apiKey",
    "https": true,
    "cors": "yes",
    "category": "新分类名称",
    "url": "https://api-documentation-url.com",
    "comment": "额外说明"
  }
]
```

### 4. 更新索引
更新 `data/index.md` 文件，将新分类和API添加到索引中。

## 扩展功能

### 数据验证
使用 `utils/validate_apis.py` 脚本来验证新增的API数据格式：

```bash
python utils/validate_apis.py
```

### API搜索
使用 `utils/search_apis.py` 脚本来搜索和浏览API：

```bash
python utils/search_apis.py
```

## 集成到应用程序

### 1. 直接使用JSON数据
您可以直接读取 `api/` 目录下的JSON文件，在您的应用程序中使用这些API信息。

### 2. 构建API客户端
基于API定义构建客户端库，自动处理认证、请求格式等。

### 3. 创建API网关
使用API定义创建统一的API网关，提供标准化的接口。

## 自定义需求

### 地图服务扩展
如果您需要特定的地图服务，可以在 `api/mapping/` 目录下添加：

- 本国地图服务（如百度地图、高德地图）
- 特定行业地图（如海洋地图、航空地图）
- 专业地图服务（如地质地图、气象地图）

### 天气API扩展
扩展天气API以包含：

- 本地天气服务
- 特定用途天气数据（农业、航空、海洋）
- 历史天气数据服务

### POI查询扩展
添加特定类型的POI查询：

- 本地POI数据源
- 特定行业POI（医疗、教育、零售）
- 实时POI数据

### 空间智能扩展
增加高级空间分析API：

- 空间统计分析
- 时空模式分析
- 预测模型API

## 最佳实践

### 1. 数据质量
- 确保API文档链接有效
- 定期验证API可用性
- 提供准确的认证和使用限制信息

### 2. 分类一致性
- 保持分类定义的一致性
- 避免API分类冲突
- 定期审查和整理分类

### 3. 扩展性考虑
- 设计灵活的数据结构
- 保留扩展字段
- 考虑国际化需求

## 贡献指南

要为项目贡献新的API或分类，请遵循以下步骤：

1. Fork 仓库
2. 创建新分支
3. 添加API数据或分类
4. 运行验证脚本
5. 更新相关文档
6. 提交Pull Request

## 许可证

本项目采用MIT许可证，您可以自由使用、修改和分发。