# AI Travel Pack List Tool

一个可离线运行的 AI 风格旅行打包清单工具（规则引擎 + 智能建议）。

## 功能

- 根据旅行天数自动估算衣物数量。
- 根据气候（cold/temperate/hot/rainy）推荐天气相关物品。
- 根据出行类型（business/leisure/adventure）补充专属清单。
- 支持活动维度（beach/hiking/formal_dinner/gym/photography）个性化推荐。
- 支持 Markdown 和 JSON 输出。

## 快速开始

```bash
python3 travel_pack_tool.py \
  --destination "Kyoto" \
  --days 6 \
  --climate rainy \
  --trip-type leisure \
  --activities hiking,photography \
  --format markdown
```

JSON 输出：

```bash
python3 travel_pack_tool.py \
  --destination "Bangkok" \
  --days 4 \
  --climate hot \
  --trip-type leisure \
  --activities beach \
  --format json
```

## 测试

```bash
python3 -m pytest -q
```
