# Outside

免费代理节点仓库 + QX 配置同步工具

## 功能

### QX 配置自动同步
- 每天自动从[墨鱼库](https://ddgksf2013.top/Profile/QuantumultX.conf)同步 Quantumult X 配置
- 节点订阅使用 **GitLab bendi.txt** (本地节点，非公共抓取)
- 生成 `QuantumultX.conf` 可直接导入 QX 使用

### GitHub → GitLab 自动同步
- 推送到 main 分支时自动同步到 GitLab
- 仓库地址: https://gitlab.com/ironicone/Outside

## 文件说明

| 文件 | 说明 |
|------|------|
| `bendi.txt` | 本地节点列表 (不抓取公共节点) |
| `QuantumultX.conf` | QX 配置文件 |
| `sync_qx.py` | QX 配置同步脚本 |

## 工作流

| 工作流 | 触发 | 说明 |
|--------|------|------|
| main.yml | 每天 00:00 (UTC) | 同步 QX 配置到 GitHub |
| sync-to-gitlab.yml | push 到 main | 同步到 GitLab |
