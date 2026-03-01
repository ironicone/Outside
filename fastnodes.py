#!/usr/bin/env python3
"""
免费节点订阅抓取脚本
从 FastNodes 获取免费代理节点
"""

from utils import NodeFetcher, FileManager

# FastNodes 订阅链接
SUBSCRIPTIONS = {
    "all": "https://raw.githubusercontent.com/rtwo2/FastNodes/main/sub/everything.txt",
    "top500": "https://raw.githubusercontent.com/rtwo2/FastNodes/main/sub/Best-Results/top500.txt",
    "vless": "https://raw.githubusercontent.com/rtwo2/FastNodes/main/sub/protocols/vless.txt",
    "hysteria2": "https://raw.githubusercontent.com/rtwo2/FastNodes/main/sub/protocols/hysteria2.txt",
    "trojan": "https://raw.githubusercontent.com/rtwo2/FastNodes/main/sub/protocols/trojan.txt",
}


def fetch_subscription(name: str, url: str, fetcher: NodeFetcher) -> list:
    """获取订阅内容"""
    print(f"正在获取: {name}...")
    response = fetcher.get(url)
    if not response:
        print(f"[失败] {name}")
        return []
    
    lines = [line.strip() for line in response.text.split('\n') if line.strip()]
    print(f"[成功] {name}: {len(lines)} 个节点")
    return lines


def main():
    fetcher = NodeFetcher()
    all_nodes = []
    
    print("=== FastNodes 节点抓取 ===\n")
    
    for name, url in SUBSCRIPTIONS.items():
        nodes = fetch_subscription(name, url, fetcher)
        if name in ["vless", "hysteria2", "trojan"]:
            all_nodes.extend(nodes)
    
    # 去重
    all_nodes = FileManager.deduplicate(all_nodes)
    
    # 保存
    FileManager.save_lines(all_nodes, "nodes.txt")
    
    # 生成 base64
    text = "\n".join(all_nodes)
    base64 = FileManager.to_base64(text)
    FileManager.append_line(base64, "nodes_base64.txt")
    
    print(f"\n=== 完成 ===")
    print(f"共获取 {len(all_nodes)} 个节点")
    print(f"保存到: nodes.txt")


if __name__ == "__main__":
    main()
