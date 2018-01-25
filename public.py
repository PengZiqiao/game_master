import subprocess
from io import BytesIO
from pathlib import Path

import requests
from PIL import Image
from aip import AipOcr
from selenium import webdriver

import config

ocr_client = AipOcr(config.APP_ID, config.API_KEY, config.SECRET_KEY)
chrome = webdriver.Chrome()


def screenshot():
    process = subprocess.Popen('adb shell screencap -p', stdout=subprocess.PIPE)
    binary_screenshot = process.stdout.read().replace(b'\r\n', b'\n')

    # 写入文件
    Path('test.png').write_bytes(binary_screenshot)

    # 写入内存
    fb = BytesIO()
    fb.write(binary_screenshot)

    print('[*] 截图成功！')
    return Image.open(fb)


def ocr(img, join=True):
    print('[*] 正在识别图片中文字...')

    # 将图片写入内存
    fb = BytesIO()
    img.save(fb, 'png')

    # 调用baidu api
    res = ocr_client.basicGeneral(fb.getvalue())

    if res['words_result_num']:
        words = [x['words'] for x in res['words_result']]

        if join:
            words = ''.join(words)

        print(f'[*] 识别结果：{words}')
        return words

    else:
        print('[*] 识别失败！')
        return None


def baidu_search(keyword):
    url = f'https://www.baidu.com/s?wd={keyword}'
    chrome.get(url)
    return chrome.page_source
