import requests
import json
import base64

# URL列表
urls = [
    "https://www.gitlabip.xyz/Alvin9999/pac2/master/hysteria2/1/config.json",
    "https://www.githubip.xyz/Alvin9999/pac2/master/hysteria2/config.json",
    "https://www.gitlabip.xyz/Alvin9999/pac2/master/hysteria2/13/config.json",
    "https://www.githubip.xyz/Alvin9999/pac2/master/hysteria2/2/config.json"
]

# 创建一个空的列表，用于存储所有内容
all_content_original = []
all_content_new = []

for url in urls:
    response = requests.get(url)
    if response.status_code == 200:
        config_data = json.loads(response.text)

        # 生成原有格式内容
        auth = config_data.get("auth", "")
        server = config_data.get("server", "")
        tls = config_data.get("tls", {})
        insecure = tls.get("insecure", False)
        sni = tls.get("sni", "")
        original_content = f"hy2://{auth}@{server}/?insecure={int(insecure)}&sni={sni}"
        all_content_original.append(original_content)

        # 生成新格式内容
        new_content = f"hysteria2://{auth}@{server}/?peer={sni}&insecure={int(insecure)}&obfs=none&fastopen=1"
        all_content_new.append(new_content)

print("所有内容已生成")

# 将所有内容保存到两个不同的txt文件并进行base64编码
with open("hy2.txt", "w", encoding="utf-8") as f:
    for content in all_content_original:
        f.write(content + "\n")

with open("hy2_base64.txt", "w", encoding="utf-8") as f:
    for content in all_content_new:
        content_base64 = base64.b64encode(content.encode('utf-8')).decode('utf-8')
        f.write(content_base64 + "\n")

print("所有内容已保存到文件")
