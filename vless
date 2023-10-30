import json
import requests

# 定义JSON文件的URL列表
json_urls = [
	"https://raw.githubusercontent.com/Alvin9999/pac2/master/xray/config.json",
  "https://raw.githubusercontent.com/Alvin9999/pac2/master/xray/1/config.json",
  "https://raw.githubusercontent.com/Alvin9999/pac2/master/xray/3/config.json"
]

# 初始化一个空列表来存储所有的VLESS链接
vless_links = []

# 循环处理每个JSON文件的URL
for json_url in json_urls:
    # 发送GET请求以获取JSON数据
    response = requests.get(json_url)

    # 检查请求是否成功
    if response.status_code == 200:
        config_data = response.json()
        outbounds = config_data.get('outbounds', [])

        for vless_info in outbounds:
            if vless_info.get('protocol', '') == 'vless':
                users = vless_info.get('settings', {}).get('vnext', [])[0].get('users', [])
                if users:
                    uuid = users[0].get('id', '')
                    server_address = vless_info.get('settings', {}).get('vnext', [])[0].get('address', '')
                    server_port = vless_info.get('settings', {}).get('vnext', [])[0].get('port', '')

                    stream_settings = vless_info.get('streamSettings', {})
                    network = stream_settings.get('network', '')

                    if network == 'tcp':
                        security = 'none'
                        reality_settings = stream_settings.get('realitySettings', {})
                        sni = reality_settings.get('serverName', '')
                        fingerprint = reality_settings.get('fingerprint', '')
                        publicKey = reality_settings.get('publicKey', '')
                        shortId = reality_settings.get('shortId', '')
                        sid = reality_settings.get('spiderX', '')

                        vless_link = f'vless://{uuid}@{server_address}:{server_port}?encryption={security}&flow=xtls-rprx-vision&security=reality&sni={sni}&fp={fingerprint}&pbk={publicKey}&sid={shortId}&type=tcp&headerType=none#xray'
                        vless_links.append(vless_link)
                    elif network == 'ws':
                        security = 'tls'
                        tls_settings = stream_settings.get('tlsSettings', {})
                        sni = tls_settings.get('serverName', '')
                        fingerprint = tls_settings.get('fingerprint', '')

                        ws_settings = stream_settings.get('wsSettings', {})
                        path = ws_settings.get('path', '')
                        host = ws_settings.get('headers', {}).get('Host', '')

                        vless_link = f'vless://{uuid}@{server_address}:{server_port}?encryption=none&security={security}&sni={sni}&fp={fingerprint}&type=ws&host={host}&path={path}#xray'
                        vless_links.append(vless_link)

    else:
        print(f'无法获取JSON数据，HTTP状态码：{response.status_code}，URL: {json_url}')

# 保存所有的VLESS链接到txt文件
with open('vless.txt', 'w') as txt_file:
    for vless_link in vless_links:
        txt_file.write(vless_link + '\n')

print(f'所有的VLESS链接已保存到vless.txt文件')
