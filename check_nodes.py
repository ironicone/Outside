#!/usr/bin/env python3
"""
节点测速脚本
测试节点连通性，筛选可用节点
"""

import socket
import re
import asyncio
from concurrent.futures import ThreadPoolExecutor
from utils import FileManager

TIMEOUT = 5  # 超时秒数


def parse_node(node: str) -> dict:
    """解析节点 URL"""
    result = {
        "type": None,
        "address": None,
        "port": None,
        "raw": node
    }
    
    # VLESS
    if node.startswith("vless://"):
        match = re.search(r'vless://([^@]+)@([^:]+):(\d+)', node)
        if match:
            result["type"] = "vless"
            result["address"] = match.group(2)
            result["port"] = int(match.group(3))
    
    # Hysteria2
    elif node.startswith("hysteria2://") or node.startswith("hy2://"):
        match = re.search(r'hysteria2?://([^@]+)@([^:]+):(\d+)', node)
        if match:
            result["type"] = "hysteria2"
            result["address"] = match.group(2)
            result["port"] = int(match.group(3))
    
    # Trojan
    elif node.startswith("trojan://"):
        match = re.search(r'trojan://([^@]+)@([^:]+):(\d+)', node)
        if match:
            result["type"] = "trojan"
            result["address"] = match.group(2)
            result["port"] = int(match.group(3))
    
    # VMess
    elif node.startswith("vmess://"):
        # 解析 JSON 格式的 vmess
        try:
            import base64
            json_str = node[8:]
            data = base64.b64decode(json_str).decode()
            import json
            config = json.loads(data)
            result["type"] = "vmess"
            result["address"] = config.get("add", "")
            result["port"] = int(config.get("port", 0))
        except:
            pass
    
    return result


def check_port(host: str, port: int) -> bool:
    """检查端口是否开放"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(TIMEOUT)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except:
        return False


def test_node(node: str) -> tuple:
    """测试单个节点"""
    parsed = parse_node(node)
    
    if not parsed["address"] or not parsed["port"]:
        return node, False, "解析失败"
    
    is_available = check_port(parsed["address"], parsed["port"])
    return node, is_available, f"{parsed['address']}:{parsed['port']}"


def main():
    # 读取节点
    print("读取节点文件...")
    all_nodes = FileManager.read_lines("nodes.txt")
    print(f"共 {len(all_nodes)} 个节点\n")
    
    # 测速
    print("开始测速 (只检测端口开放)...")
    working_nodes = []
    
    with ThreadPoolExecutor(max_workers=100) as executor:
        results = list(executor.map(test_node, all_nodes[:500]))  # 限制前500个
    
    for node, is_available, info in results:
        if is_available:
            working_nodes.append(node)
            print(f"✓ 可用: {info}")
        else:
            print(f"✗ 不可用: {info}")
    
    # 保存可用节点
    FileManager.save_lines(working_nodes, "nodes_working.txt")
    
    print(f"\n=== 完成 ===")
    print(f"总节点: {len(all_nodes)}")
    print(f"可用节点: {len(working_nodes)}")
    print(f"保存到: nodes_working.txt")


if __name__ == "__main__":
    main()
