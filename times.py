import requests
import datetime

def download_clashnode_file(date, output_filename):
    url = f"https://clashnode.com/wp-content/uploads/{date[:4]}/{date[4:6]}/{date}.yaml"
    
    try:
        response = requests.get(url)
        
        if response.status_code == 200:
            with open(output_filename, 'wb') as f:
                f.write(response.content)
            print(f"文件已下载并保存为 {output_filename}")
        else:
            print(f"请求失败，状态码：{response.status_code}")
    except Exception as e:
        print(f"发生错误：{e}")

if __name__ == "__main__":
    date = datetime.datetime.now().strftime('%Y%m%d')
    output_filename = "n0des.yaml"
    download_clashnode_file(date, output_filename)
