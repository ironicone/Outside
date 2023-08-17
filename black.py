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

def encode_text_to_base64(input_file, output_file):
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            text = f.read()
        
        encoded_text = base64.b64encode(text.encode('utf-8')).decode('utf-8')
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(encoded_text)
        
        print(f"文本已编码并写入到 {output_file}")
    except Exception as e:
        print(f"发生错误：{e}")


def main():
    urls = [
        'https://www.hd327658.xyz:20000/api/evmess',
        'https://www.lt71126.xyz:20000/api/evmess'
    ]
    key = "ks9KUrbWJj46AftX"  # Replace with the correct key
    file_path = 'heidong.txt'
    visited_contents = set()

    for url in urls:
        while True:
            content = get_webpage_content(url)
            if content is None:
                break
            
            decrypted_content = decrypt(content, key)

            # Custom processing of decrypted content
            processed_content = custom_process(decrypted_content)

            if processed_content in visited_contents:
                print(f"Duplicate content found on {url}. Switching to the next website.")
                break

            visited_contents.add(processed_content)
            with open(file_path, 'a') as file:
                file.write(processed_content + '\n')  # Add a newline after each content
            print(processed_content)
            time.sleep(1)

    input_file = "heidong.txt"  # 输入文本文件名
    output_file = "n0des.txt"  # 输出编码后文本文件名
    
    encode_text_to_base64(input_file, output_file)

if __name__ == "__main__":
    main()
