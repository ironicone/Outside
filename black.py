import requests
import time
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import base64

def get_webpage_content(url):
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return response.text
        else:
            print(f"Failed to fetch the webpage. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
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
    # Define the list of URLs to access
    urls = [
        'https://www.hd327658.xyz:20000/api/evmess',
        'https://www.lt71126.xyz:20000/api/evmess'
    ]
    key = "ks9KUrbWJj46AftX"  # Replace with the correct key

    for url in urls:
        temp_content = ''  # Temporary variable to store content
        
        for _ in range(10):  # Read content from each website 10 times
            content = get_webpage_content(url)
            if content is None:
                break
            decrypted_content = decrypt(content, key)
            processed_content = custom_process(decrypted_content)
            
            # Store the content in the temporary variable
            temp_content += processed_content + ' '
            
            print(processed_content)
            time.sleep(1)  # You can adjust the sleep time as needed
        
        # Write the unencoded content, append instead of overwrite
        with open('heidong.txt', 'a') as file:
            file.write(temp_content)
        
        # Write the encoded content, append instead of overwrite
        encode_text_to_base64(temp_content, 'n0des.txt')

if __name__ == "__main__":
    main()
