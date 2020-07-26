from collections import deque
import requests
import sys
import os
from bs4 import BeautifulSoup
from colorama import init, Fore
init()


def get_page(url):
    if not url.startswith('https://'):
        url = 'https://' + url
    return requests.get(url)


def get_from_list(tag, list):
    if tag:
        for i in tag:
            list.append(' '.join(i.get_text().split()))


def get_url_content(page):
    content_list = list()
    beauty_page = BeautifulSoup(page.content, 'html.parser')
    header_tag = beauty_page.find_all('header')
    get_from_list(header_tag, content_list)
    p_tag = beauty_page.find_all('p')
    get_from_list(p_tag, content_list)
    a_tag = beauty_page.find_all('a')
    if a_tag:
        for i in a_tag:
            content_list.append(Fore.BLUE + i.get_text())
    ul_tag = beauty_page.find_all('ul')
    get_from_list(ul_tag, content_list)
    li_tag = beauty_page.find_all('li')
    get_from_list(li_tag, content_list)
    ol_tag = beauty_page.find_all('ol')
    get_from_list(ol_tag, content_list)
    return content_list


def save_file(path, name=''):
    with open(path, 'w') as file:
        file.write(name)


def make_favorite(user_url):
    if "www." in user_url:
        user_url = ''.join(user_url.split('www.'))
    if '.com' in user_url:
        user_url = ''.join(user_url.split('.com'))
    if '.org' in user_url:
        user_url = ''.join(user_url.split('.org'))
    favorite_list.append(user_url)
    return user_url


arg = sys.argv
if len(arg) == 2:
    try:
        os.mkdir(arg[1])
    except:
        pass

exit_ = True
favorite_list = list()
back_list = deque()
while exit_:
    user_url = input()
    if user_url == 'exit':
        exit_ = False
        continue
    if not('.com' in user_url or '.org' in user_url) and user_url != 'back' and user_url not in favorite_list:
        print('Error: Incorrect URL')
        continue
    if user_url == 'back':
        if len(back_list) > 1:
            back_list.pop()
            print('\n'.join(get_url_content(get_page(user_url))))
        else:
            print('')
        continue

    if user_url in favorite_list:
        user_url = user_url + '.com'
        print('\n'.join(get_url_content(get_page(user_url))))
        back_list.append(user_url)
        continue
    else:
        print('\n'.join(get_url_content(get_page(user_url))))
        favorite_url = make_favorite(user_url)
        back_list.append(user_url)
        save_file(path=f'{arg[1]}\{favorite_url}.txt', name='\n'.join(get_url_content(get_page(user_url))))

