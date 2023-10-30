import requests
import time
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import base64

def get_webpage_content(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Failed to fetch the webpage. Status code: {response.status_code}")
        return None

def decrypt(content, key):
    cipher = AES.new(key.encode('utf-8'), AES.MODE_CBC, key.encode('utf-8'))
    decoded_str = base64.b64decode(content)
    decrypted_data = cipher.decrypt(decoded_str)
    return decrypted_data.decode('utf-8')

def custom_process(decrypted_content):
    # Remove "vmess://" from the content
    decrypted_content = decrypted_content.replace('vmess://', '')
    # Base64 decode the content again after removing "vmess://"
    decoded_content = base64.b64decode(decrypted_content).decode('utf-8')
    # Replace "/footers" with "/path/1676233915122"
    modified_content = decoded_content.replace('/footers', '/path/1676233915122')
    # Base64 encode the modified content and add "vmess://" at the beginning
    encoded_content = "vmess://" + base64.b64encode(modified_content.encode('utf-8')).decode('utf-8')
    return encoded_content

def encode_text_to_base64(input_text, output_file):
    encoded_text = base64.b64encode(input_text.encode('utf-8')).decode('utf-8')
    with open(output_file, 'w') as f:
        f.write(encoded_text + ' ')

def main():
    # 定义要访问的URL列表
    urls = [
        'https://www.hd327658.xyz:20000/api/evmess',
        'https://www.lt71126.xyz:20000/api/evmess'
    ]
    key = "ks9KUrbWJj46AftX"  # 替换为正确的密钥

    for url in urls:
        temp_content = ''  # 临时保存内容的变量
        
        for _ in range(10):  # 读取每个网站的内容10次
            content = get_webpage_content(url)
            if content is None:
                break
            decrypted_content = decrypt(content, key)
            processed_content = custom_process(decrypted_content)
            
            # 将内容存储在临时变量中
            temp_content += processed_content + ' '
            
            print(processed_content)
            time.sleep(1)  # 可以适当调整休眠时间
        
        # 写入未编码的内容，追加而不覆盖
        with open('heidong.txt', 'w') as file:
            file.write(temp_content)
        
        # 写入编码后的内容，追加而不覆盖
        encode_text_to_base64(temp_content, 'n0des.txt')

if __name__ == "__main__":
    main()
