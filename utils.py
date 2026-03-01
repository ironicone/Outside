"""
公共工具模块
提供代理节点抓取所需的通用功能
"""

import requests
import json
import time
import base64
from typing import Optional, List, Dict, Any
from urllib.parse import urljoin


class NodeFetcher:
    """代理节点获取器"""
    
    def __init__(self, timeout: int = 10, retry: int = 3):
        self.timeout = timeout
        self.retry = retry
        self.session = requests.Session()
    
    def get(self, url: str, verify: bool = False) -> Optional[requests.Response]:
        """发送 GET 请求，带重试机制"""
        for attempt in range(self.retry):
            try:
                response = self.session.get(
                    url, 
                    timeout=self.timeout, 
                    verify=verify
                )
                if response.status_code == 200:
                    return response
                else:
                    print(f"[警告] 请求失败: {url}, 状态码: {response.status_code}")
            except requests.exceptions.RequestException as e:
                print(f"[错误] 请求异常: {url}, 原因: {e}")
                if attempt < self.retry - 1:
                    time.sleep(1)
        return None
    
    def post(self, url: str, data: Dict = None, json: bool = True) -> Optional[requests.Response]:
        """发送 POST 请求"""
        try:
            if json:
                response = self.session.post(url, json=data, timeout=self.timeout)
            else:
                response = self.session.post(url, data=data, timeout=self.timeout)
            if response.status_code == 200:
                return response
        except requests.exceptions.RequestException as e:
            print(f"[错误] POST 请求异常: {url}, 原因: {e}")
        return None


class NodeConverter:
    """节点格式转换器"""
    
    @staticmethod
    def vless_to_link(uuid: str, address: str, port: int, 
                      network: str = "tcp", security: str = "reality",
                      **kwargs) -> str:
        """生成 VLESS 链接"""
        params = {
            "encryption": "none",
            "type": network,
            "security": security,
        }
        params.update(kwargs)
        
        param_str = "&".join([f"{k}={v}" for k, v in params.items() if v])
        return f"vless://{uuid}@{address}:{port}?{param_str}"
    
    @staticmethod
    def hy2_to_link(auth: str, server: str, sni: str, 
                    insecure: bool = False) -> str:
        """生成 hysteria2 链接"""
        return f"hysteria2://{auth}@{server}/?peer={sni}&insecure={int(insecure)}&obfs=none&fastopen=1"
    
    @staticmethod
    def hy2_to_original_link(auth: str, server: str, sni: str,
                             insecure: bool = False) -> str:
        """生成 hysteria2 原始格式链接"""
        return f"hy2://{auth}@{server}/?insecure={int(insecure)}&sni={sni}"


class FileManager:
    """文件管理器"""
    
    @staticmethod
    def save_lines(lines: List[str], filename: str):
        """保存多行文本到文件"""
        with open(filename, 'w', encoding='utf-8') as f:
            for line in lines:
                f.write(line + '\n')
    
    @staticmethod
    def append_line(line: str, filename: str):
        """追加一行到文件"""
        with open(filename, 'a', encoding='utf-8') as f:
            f.write(line + '\n')
    
    @staticmethod
    def read_lines(filename: str) -> List[str]:
        """读取文件所有行"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                return [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            return []
    
    @staticmethod
    def to_base64(text: str) -> str:
        """将文本转换为 base64"""
        return base64.b64encode(text.encode('utf-8')).decode('utf-8')
    
    @staticmethod
    def deduplicate(lines: List[str]) -> List[str]:
        """去重"""
        return list(dict.fromkeys(lines))
