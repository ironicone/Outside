#!/usr/bin/env python3
"""
节点测速脚本
测试节点延迟，筛选延迟最低的节点
"""

import socket
import time
import re
from concurrent.futures import ThreadPoolExecutor
from utils import FileManager

TIMEOUT = 3  # 超时秒数


def parse_node(node: str) -> dict:
    """解析节点 URL"""
    result = {"address": None, "port": None, "raw": node}
    
    # VLESS
    match = re.search(r'vless://[^@]+@([^:]+):(\d+)', node)
    if match:
        result["address"] = match.group(1)
        result["port"] = int(match.group(2))
        return result
    
    # Hysteria2
    match = re.search(r'hysteria2?://[^@]+@([^:]+):(\d+)', node)
    if match:
        result["address"] = match.group(1)
        result["port"] = int(match.group(2))
        return result
    
    # Trojan
    match = re.search(r'trojan://[^@]+@([^:]+):(\d+)', node)
    if match:
        result["address"] = match.group(1)
        result["port"] = int(match.group(2))
        return result
    
    return result


def test_latency(node: str) -> tuple:
    """测试单个节点延迟"""
    parsed = parse_node(node)
    
    if not parsed["address"] or not parsed["port"]:
        return node, 9999
    
    start = time.time()
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(TIMEOUT)
        result = sock.connect_ex((parsed["address"], parsed["port"]))
        sock.close()
        
        if result == 0:
            latency = int((time.time() - start) * 1000)  # 毫秒
            return node, latency
    except:
        pass
    
    return node, 9999


def main():
    # 读取节点
    print("读取节点...")
    all_nodes = FileManager.read_lines("nodes.txt")
    print(f"共 {len(all_nodes)} 个节点\n")
    
    # 随机取500个测试
    import random
    test_nodes = random.sample(all_nodes, min(500, len(all_nodes)))
    print(f"测速中 (前 {len(test_nodes)} 个)...\n")
    
    # 测速
    results = []
    with ThreadPoolExecutor(max_workers=100) as executor:
        results = list(executor.map(test_latency, test_nodes))
    
    # 按延迟排序
    results.sort(key=lambda x: x[1])
    
    # 取前50个
    top_50 = [node for node, latency in results if latency < 9999][:50]
    
    # 保存
    FileManager.save_lines(top_50, "nodes_top50.txt")
    
    # 输出结果
    print("=== 延迟最低的 50 个节点 ===\n")
    parsed_test = parse_node("")
    for i, (node, latency) in enumerate(results[:50], 1):
        if latency < 9999:
            parsed_test = parse_node(node)
            addr = parsed_test.get('address', node[:30])
            print(f"{i:2}. {addr:30} - {latency}ms")
    
    print(f"\n=== 完成 ===")
    print(f"可用: {len(top_50)} 个")
    print(f"保存到: nodes_top50.txt")


if __name__ == "__main__":
    main()
