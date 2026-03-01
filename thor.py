#!/usr/bin/env python3
"""
 Thor (雷場) 节点抓取脚本
 从 API 获取加密的 VMESS 配置并解密
"""

from utils import NodeFetcher, FileManager
from Crypto.Cipher import AES
import base64

# 配置
CONFIG = {
    "urls": [
        "https://www.lt71126.xyz:20000/api/evmess"
    ],
    "key": "ks9KUrbWJj46AftX",
    "path": "/path/1676233915122",  # 替换路径
    "output": "leiting.txt"
}


def decrypt(content: str, key: str) -> str:
    """AES 解密"""
    cipher = AES.new(key.encode('utf-8'), AES.MODE_CBC, key.encode('utf-8'))
    decoded_str = base64.b64decode(content)
    decrypted_data = cipher.decrypt(decoded_str)
    return decrypted_data.decode('utf-8')


def process_vmess(decrypted_content: str, replace_path: str) -> str:
    """处理 VMESS 配置"""
    # 移除 "vmess://" 前缀
    content = decrypted_content.replace('vmess://', '')
    
    # 再次 Base64 解码
    decoded = base64.b64decode(content).decode('utf-8')
    
    # 替换路径
    modified = decoded.replace('/footers', replace_path)
    
    # 重新编码并添加前缀
    return "vmess://" + base64.b64encode(modified.encode('utf-8')).decode('utf-8')


def main():
    fetcher = NodeFetcher()
    visited = set()
    
    print(f"开始抓取 {len(CONFIG['urls'])} 个 URL...")
    
    for url in CONFIG["urls"]:
        print(f"正在抓取: {url}")
        
        while True:
            response = fetcher.get(url)
            if not response:
                print("[错误] 请求失败，停止该 URL")
                break
            
            try:
                encrypted_content = response.text
                decrypted = decrypt(encrypted_content, CONFIG["key"])
                processed = process_vmess(decrypted, CONFIG["path"])
                
                if processed in visited:
                    print(f"[信息] 节点已存在，停止该 URL")
                    break
                
                visited.add(processed)
                FileManager.append_line(processed, CONFIG["output"])
                print(f"[成功] 新增节点")
                
            except Exception as e:
                print(f"[错误] 处理失败: {e}")
                break
    
    print(f"\n完成! 共获取 {len(visited)} 个节点")
    print(f"保存至: {CONFIG['output']}")


if __name__ == "__main__":
    main()
