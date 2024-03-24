import requests

def download_file(url, output_file):
    try:
        response = requests.get(url, verify=False)
        if response.status_code == 200:
            with open(output_file, 'wb') as f:
                f.write(response.content)
            print("文件下载成功:", output_file)
        else:
            print("无法下载文件，HTTP 状态码:", response.status_code)
    except Exception as e:
        print("下载文件时出错:", str(e))

if __name__ == "__main__":
    url = "https://www.gitlabip.xyz/Alvin9999/pac2/master/clash.meta2/1/config.yaml"
    output_file = "config.yaml"
    download_file(url, output_file)
