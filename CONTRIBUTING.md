# 贡献指南

感谢您有兴趣为 Public ST APIs 做出贡献！我们的目标是创建一个全面的地理空间和时空信息服务API集合。

## 提交API

要提交新的API，请遵循以下步骤：

1. Fork 仓库
2. 在相应的分类目录中添加API信息
3. 确保API符合以下标准：
   - 提供地理空间或时空数据服务
   - 有公开可用的文档
   - 对开发者免费或提供免费层级
   - 稳定可靠
4. 提交Pull Request

## API格式

请使用以下JSON格式提交API信息：

```json
{
  "name": "API名称",
  "description": "API描述",
  "auth": "认证方式 (apiKey, oauth, 或 null)",
  "https": true,
  "cors": "CORS支持状态 (yes/no/unknown)",
  "category": "API分类",
  "url": "API文档链接",
  "comment": "额外说明 (可选)"
}
```

## API分类

目前支持的分类包括：
- Mapping Services (地图服务)
- Weather APIs (天气API)
- POI Queries (兴趣点查询)
- Spatial Intelligence (空间智能)
- Geocoding (地理编码)
- Routing (路径规划)
- Satellite Imagery (卫星影像)
- Transportation (交通)
- Environment (环境)
- Demographics (人口统计)

## 贡献流程

1. 搜索现有的API，避免重复提交
2. 检查API是否仍然可用
3. 验证API文档的有效性
4. 按照上述格式提交API信息
5. 提交Pull Request并等待审核

## 代码风格

- 使用标准的JSON格式
- 确保URL是HTTPS（如果可用）
- 描述简洁明了
- 遵循现有文件的结构

## 社区

如果您有任何问题或建议，请通过Issues与我们联系。