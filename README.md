# Outside

代理节点抓取工具集合，通过 GitHub Actions 自动运行。

## 目录结构

```
Outside/
├── utils.py              # 公共工具模块
├── hy2.py               # Hysteria2 节点抓取
├── vless.py             # VLESS 节点抓取
├── thor.py              # Thor (雷場) 节点抓取
├── times.py             # 时光节点抓取
├── yaml.py              # YAML 配置处理
├── config.yaml          # 配置文件
├── requirements.txt     # Python 依赖
└── .github/
    └── workflows/
        └── main.yml     # GitHub Actions 工作流
```

## 模块说明

### utils.py - 公共工具模块

提供三类工具类：

| 类名 | 功能 |
|------|------|
| `NodeFetcher` | HTTP 请求封装，带超时和重试 |
| `NodeConverter` | 节点格式转换 (VLESS, Hysteria2) |
| `FileManager` | 文件读写、去重、Base64 编码 |

### 节点脚本

| 脚本 | 协议 | 数据源 |
|------|------|--------|
| `hy2.py` | Hysteria2 | JSON 配置文件 |
| `vless.py` | VLESS (TCP/WS) | JSON 配置文件 |
| `thor.py` | VMESS | 加密 API |

## 核心逻辑

```
┌─────────────────┐
│  读取配置 URL   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  HTTP 请求获取  │ ◄── NodeFetcher.get()
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  解析 JSON/解密 │ ◄── JSON 解析 / AES 解密
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  转换为节点链接 │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  去重 & 保存    │ ◄── FileManager.deduplicate()
└─────────────────┘
```

## 依赖

```
requests
pycryptodome
```

## GitHub Actions

自动任务：

1. **定时执行**: 每天 UTC 0:00 运行
2. **手动触发**: push 时自动运行
3. **自动提交**: 结果推送到主分支
4. **镜像同步**: 同步到 GitLab

## 扩展开发

### 添加新协议

1. 在 `utils.py` 添加转换方法
2. 创建新的抓取脚本
3. 在 `.github/workflows/main.yml` 添加执行步骤

### 添加新数据源

```python
from utils import NodeFetcher, FileManager

fetcher = NodeFetcher()
response = fetcher.get("https://example.com/api/nodes")

if response:
    # 处理数据
    links = parse_nodes(response.json())
    FileManager.save_lines(links, "output.txt")
```
