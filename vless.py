#!/usr/bin/env python3
"""
 VLESS 节点抓取脚本
 从多个 URL 获取 VLESS 配置并转换为节点链接
 支持 TCP 和 WebSocket 协议
"""

from utils import NodeFetcher, NodeConverter, FileManager
import json

# 配置
CONFIG = {
    "urls": [
        "https://raw.githubusercontent.com/Alvin9999/pac2/master/xray/1/config.json",
        "https://raw.githubusercontent.com/Alvin9999/pac2/master/xray/config.json",
        "https://raw.githubusercontent.com/Alvin9999/pac2/master/xray/3/config.json"
    ],
    "output": {
        "links": "vless.txt",
        "base64": "vless_base64.txt"
    }
}


def parse_vless_config(config_data: dict) -> list:
    """解析 VLESS 配置"""
    links = []
    outbounds = config_data.get('outbounds', [])
    
    for vless_info in outbounds:
        if vless_info.get('protocol', '') != 'vless':
            continue
            
        try:
            settings = vless_info.get('settings', {})
            vnext = settings.get('vnext', [])
            if not vnext:
                continue
                
            user = vnext[0].get('users', [])[0]
            uuid = user.get('id', '')
            address = vnext[0].get('address', '')
            port = vnext[0].get('port', '')
            
            stream = vless_info.get('streamSettings', {})
            network = stream.get('network', '')
            
            if network == 'tcp':
                link = _parse_tcp(uuid, address, port, stream)
            elif network == 'ws':
                link = _parse_ws(uuid, address, port, stream)
            
            if link:
                links.append(link)
                
        except (KeyError, IndexError) as e:
            print(f"[警告] 解析配置失败: {e}")
            continue
    
    return links


def _parse_tcp(uuid: str, address: str, port: int, stream: dict) -> str:
    """解析 TCP + REALITY 配置"""
    reality = stream.get('realitySettings', {})
    
    params = {
        "encryption": "none",
        "flow": "xtls-rprx-vision",
        "security": "reality",
        "sni": reality.get('serverName', ''),
        "fp": reality.get('fingerprint', ''),
        "pbk": reality.get('publicKey', ''),
        "sid": reality.get('shortId', ''),
        "type": "tcp",
        "headerType": "none"
    }
    
    param_str = "&".join([f"{k}={v}" for k, v in params.items()])
    return f"vless://{uuid}@{address}:{port}?{param_str}"


def _parse_ws(uuid: str, address: str, port: int, stream: dict) -> str:
    """解析 WebSocket + TLS 配置"""
    tls_settings = stream.get('tlsSettings', {})
    ws_settings = stream.get('wsSettings', {})
    
    params = {
        "encryption": "none",
        "security": "tls",
        "sni": tls_settings.get('serverName', ''),
        "fp": tls_settings.get('fingerprint', ''),
        "type": "ws",
        "host": ws_settings.get('headers', {}).get('Host', ''),
        "path": ws_settings.get('path', '')
    }
    
    param_str = "&".join([f"{k}={v}" for k, v in params.items() if v])
    return f"vless://{uuid}@{address}:{port}?{param_str}"


def main():
    fetcher = NodeFetcher()
    
    all_links = []
    
    print(f"开始抓取 {len(CONFIG['urls'])} 个 URL...")
    
    for url in CONFIG["urls"]:
        response = fetcher.get(url)
        if not response:
            continue
            
        try:
            config_data = response.json()
            links = parse_vless_config(config_data)
            all_links.extend(links)
            print(f"[成功] {url}, 获取 {len(links)} 个节点")
            
        except json.JSONDecodeError as e:
            print(f"[错误] JSON 解析失败: {url}, {e}")
        except Exception as e:
            print(f"[错误] 处理失败: {url}, {e}")
    
    # 去重
    all_links = FileManager.deduplicate(all_links)
    
    # 保存链接
    FileManager.save_lines(all_links, CONFIG["output"]["links"])
    
    # 生成 base64
    text_content = "\n".join(all_links)
    base64_content = FileManager.to_base64(text_content)
    FileManager.append_line(base64_content, CONFIG["output"]["base64"])
    
    print(f"\n完成! 共获取 {len(all_links)} 个节点")
    print(f"链接文件: {CONFIG['output']['links']}")
    print(f"Base64: {CONFIG['output']['base64']}")


if __name__ == "__main__":
    main()
