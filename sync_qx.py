#!/usr/bin/env python3
"""
QX 配置同步脚本
每周一自动从墨鱼库同步规则，并替换节点订阅链接
"""

import requests
from utils import FileManager
import re

# 配置
墨鱼QX配置 = "https://ddgksf2013.top/Profile/QuantumultX.conf"

# 节点订阅链接
节点订阅链接列表 = [
    "https://gitlab.com/ironicone/Outside/-/raw/main/bendi.txt",
    "http://43.139.168.201/link/u0KNHoqk9Ilqb0nU",
]


def fetch_remote_config(url: str) -> str:
    """获取远程配置"""
    print(f"获取墨鱼配置: {url}")
    resp = requests.get(url, timeout=30)
    if resp.status_code == 200:
        print("✓ 配置获取成功")
        return resp.text
    else:
        raise Exception(f"获取失败: {resp.status_code}")


def replace_server_remote(config: str, sub_urls: list, tag: str = "本地节点") -> str:
    """替换 server_remote 部分"""
    print("\n替换节点订阅...")
    
    # 移除原有的 [server_local] 和 [server_remote] 部分
    config = re.sub(r'\[server_local\].*?(?=\n\[|$)', '\n', config, flags=re.DOTALL)
    config = re.sub(r'\[server_remote\].*?(?=\n\[|$)', '\n', config, flags=re.DOTALL)
    
    # 找到 [dns] 前插入
    match = re.search(r'\[dns\]', config)
    
    if not match:
        print("  ✗ 未找到 [dns] 位置")
        return config
    
    # 生成新的 section
    new_section = """[server_local]


[server_remote]

"""
    for i, url in enumerate(sub_urls):
        tag_name = tag if i == 0 else f"节点{i+1}"
        new_section += f"# > {tag_name}\n{url}, tag={tag_name}, update-interval=86400, opt-parser=false, enabled=true\n\n"
    
    # 在 [dns] 前插入
    result = config[:match.start()] + new_section + config[match.start():]
    print(f"  ✓ 节点订阅已替换")
    
    return result


def save_config(content: str, filename: str):
    """保存配置"""
    print(f"\n保存配置到: {filename}")
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    print("  ✓ 完成")


def main():
    print("=== QX 配置同步工具 ===\n")
    
    # 1. 获取墨鱼配置
    config = fetch_remote_config(墨鱼QX配置)
    
    # 2. 替换节点订阅链接
    new_config = replace_server_remote(config, 节点订阅链接列表)
    
    # 3. 保存
    save_config(new_config, "QuantumultX.conf")
    
    print("\n=== 完成 ===")
    print("配置文件: QuantumultX.conf")
    print("可导入 QuantumultX 使用")


if __name__ == "__main__":
    main()
