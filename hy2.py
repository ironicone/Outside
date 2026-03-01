import requests
import json

# URL列表
urls = [
    "https://www.gitlabip.xyz/Alvin9999/pac2/master/hysteria2/1/config.json",
    "https://www.githubip.xyz/Alvin9999/pac2/master/hysteria2/config.json",
    "https://www.gitlabip.xyz/Alvin9999/pac2/master/hysteria2/13/config.json",
    "https://www.githubip.xyz/Alvin9999/pac2/master/hysteria2/2/config.json"
]

# 创建三个空的列表，用于存储所有内容
all_content_original = []
all_content_new = []
all_json_data = []

for url in urls:
    response = requests.get(url, verify=False)
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

        # 将JSON数据按原始格式添加到列表
        json_str = json.dumps(config_data, indent=2)
        all_json_data.append(json_str)

print("所有内容已生成")

# 将原始JSON数据保存到txt文件
with open("hy2_json.txt", "w", encoding="utf-8") as f:
    for json_data in all_json_data:
        f.write(json_data + "\n")

# 将所有内容保存到一个单独的txt文件
with open("hy2.txt", "w", encoding="utf-8") as f:
    for content in all_content_original:
        f.write(content + "\n")

with open("hy2_rocket.txt", "w", encoding="utf-8") as f:
    for content in all_content_new:
        f.write(content + "\n")

print("所有内容已保存到文件")
