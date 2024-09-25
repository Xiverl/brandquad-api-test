import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse


def get_direct_link(url):
    domain = urlparse(url).netloc

    if 'drive.google.com' in domain:
        return get_google_drive_link(url)
    elif 'dropbox.com' in domain:
        return get_dropbox_link(url)
    elif 'disk.yandex' in domain:
        return get_yandex_disk_link(url)
    else:
        return get_generic_link(url)


def get_google_drive_link(url):
    file_id = re.findall(r'/d/([^/]+)', url)[0]
    return f'https://drive.google.com/uc?export=download&id={file_id}'


def get_dropbox_link(url):
    return url.replace('www.dropbox.com', 'dl.dropboxusercontent.com')


def get_yandex_disk_link(url):
    base_url = "https://cloud-api.yandex.net/v1/disk/public/resources/download"
    params = {"public_key": url}
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        return response.json()['href']
    return None


def get_generic_link(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Пытаемся найти ссылку на скачивание
    download_link = soup.find('a', text=re.compile(r'download', re.I))
    if download_link:
        return download_link.get('href')

    # Ищем любую ссылку, которая может быть ссылкой на файл
    file_extensions = r'\.(txt|pdf|doc|docx|xls|xlsx|zip|rar)$'
    file_link = soup.find('a', href=re.compile(file_extensions, re.I))
    if file_link:
        return file_link.get('href')

    return None


def download_file(url):
    direct_link = get_direct_link(url)
    if direct_link:
        return direct_link
    return None
