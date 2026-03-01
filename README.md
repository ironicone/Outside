# Outside

免费代理节点抓取工具。

## 目录结构

```
Outside/
├── utils.py           # 公共工具模块
├── fastnodes.py      # 从 FastNodes 抓取免费节点
├── check_nodes.py    # 节点测速脚本
├── nodes.txt         # 所有抓取的节点
├── nodes_working.txt  # 测速通过的节点
├── requirements.txt   # Python 依赖
└── .github/
    └── workflows/
        └── main.yml   # GitHub Actions
```

## 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
```

### 抓取节点

```bash
python fastnodes.py
```

### 测速筛选

```bash
python check_nodes.py
```

## 模块说明

### fastnodes.py

从 [FastNodes](https://github.com/rtwo2/FastNodes) 抓取免费节点：
- VLESS
- Hysteria2
- Trojan

### check_nodes.py

对节点进行端口测速，筛选可用节点。

## 数据源

- [FastNodes](https://github.com/rtwo2/FastNodes) - 每 6 小时更新

## 输出文件

| 文件 | 说明 |
|------|------|
| `nodes.txt` | 所有抓取的节点 |
| `nodes_working.txt` | 测速通过的节点 |

## GitHub Actions

自动任务：
1. 每天 UTC 0:00 抓取节点
2. 自动提交到仓库

## License

MIT
