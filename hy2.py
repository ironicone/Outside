import requests
import json

# 下载JSON配置文件
url = "https://gitlab.com/free9999/ipupdate/-/raw/master/hysteria2/config.json"
response = requests.get(url)
if response.status_code == 200:
    config_data = json.loads(response.text)
    
    # 生成新的内容
    auth = config_data.get("auth", "")
    server = config_data.get("server", "")
    tls = config_data.get("tls", {})
    insecure = tls.get("insecure", False)
    sni = tls.get("sni", "")
    
    new_content = f"hy2://{auth}@{server}/?insecure={int(insecure)}&sni={sni}"

    # 将新内容保存到txt文件
    with open("hy2.txt", "w", encoding="utf-8") as f:
        f.write(new_content)

    print("新内容已保存到hy2.txt")
else:
    print(f"请求失败，状态码：{response.status_code}")
