#!/usr/bin/env python3
"""
 hysteria2 节点抓取脚本
 从多个 URL 获取 hysteria2 配置并转换为节点链接
"""

from utils import NodeFetcher, NodeConverter, FileManager
import json

# 配置
CONFIG = {
    "urls": [
        "https://www.gitlabip.xyz/Alvin9999/pac2/master/hysteria2/1/config.json",
        "https://www.githubip.xyz/Alvin9999/pac2/master/hysteria2/config.json",
        "https://www.gitlabip.xyz/Alvin9999/pac2/master/hysteria2/13/config.json",
        "https://www.githubip.xyz/Alvin9999/pac2/master/hysteria2/2/config.json"
    ],
    "output": {
        "original": "hy2_original.txt",
        "new": "hy2_rocket.txt",
        "json": "hy2_json.txt"
    }
}


def parse_hy2_config(config_data: dict) -> dict:
    """解析 hysteria2 配置"""
    auth = config_data.get("auth", "")
    server = config_data.get("server", "")
    tls = config_data.get("tls", {})
    insecure = tls.get("insecure", False)
    sni = tls.get("sni", "")
    
    return {
        "auth": auth,
        "server": server,
        "sni": sni,
        "insecure": insecure
    }


def main():
    fetcher = NodeFetcher()
    converter = NodeConverter()
    
    original_links = []
    new_links = []
    json_data = []
    
    print(f"开始抓取 {len(CONFIG['urls'])} 个 URL...")
    
    for url in CONFIG["urls"]:
        response = fetcher.get(url)
        if not response:
            continue
            
        try:
            config_data = response.json()
            parsed = parse_hy2_config(config_data)
            
            # 生成原始格式
            original = converter.hy2_to_original_link(
                parsed["auth"],
                parsed["server"],
                parsed["sni"],
                parsed["insecure"]
            )
            original_links.append(original)
            
            # 生成新格式
            new = converter.hy2_to_link(
                parsed["auth"],
                parsed["server"],
                parsed["sni"],
                parsed["insecure"]
            )
            new_links.append(new)
            
            # 保存原始 JSON
            json_data.append(json.dumps(config_data, indent=2))
            
            print(f"[成功] {url}")
            
        except json.JSONDecodeError as e:
            print(f"[错误] JSON 解析失败: {url}, {e}")
        except Exception as e:
            print(f"[错误] 处理失败: {url}, {e}")
    
    # 去重
    original_links = FileManager.deduplicate(original_links)
    new_links = FileManager.deduplicate(new_links)
    
    # 保存文件
    FileManager.save_lines(original_links, CONFIG["output"]["original"])
    FileManager.save_lines(new_links, CONFIG["output"]["new"])
    FileManager.save_lines(json_data, CONFIG["output"]["json"])
    
    print(f"\n完成! 共获取 {len(original_links)} 个节点")
    print(f"原始格式: {CONFIG['output']['original']}")
    print(f"新格式: {CONFIG['output']['new']}")


if __name__ == "__main__":
    main()
