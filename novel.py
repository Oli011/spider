import re
import os
import requests
from multiprocessing.dummy import Pool

# 从https://www.kanunu8.com/book3/6879/爬取所有章节网址


# 获取每一章链接，贮存到一个列表中并返回
# 函数返回值的应用
def get_toc(html):
    chapters_list = []
    chapter_block = re.findall("正文(.*?)</tbody>", html, re.S)[0]
    chapter_block_url = re.findall('href="(.*?)">', chapter_block, re.S)
    for url in chapter_block_url:
        chapters_list.append(url_0 + url)
    return chapters_list

# # 定义单个页面内容爬取函数,获取每一章的正文并返回章节名和正文
def get_article(html):
    html = requests.get(html).content.decode('GBK')
    # 标题
    chapter_name = re.search('size="4">(.*?)<', html, re.S).group(1)
    # 正文
    text_block = re.search('<p>(.*?)</p>', html, re.S).group(1)
    text_block = text_block.replace('<br />', '')
    return chapter_name, text_block

# 本地创建文件夹，每一章分别保存到这个文件夹中，每章保存为一个文件
def save(chapter, article):
    os.makedirs('动物农场', exist_ok=True)
    with open(os.path.join('动物农场', chapter+'.txt'), 'w', encoding='utf-8') as f:
        f.write(article)


if __name__=='__main__':
    global url_0
    url_0 = "https://www.kanunu8.com/book3/6879/"
    html = requests.get(url_0).content.decode('GBK')
    # # 设定多线程
    pool = Pool(2)
    result = pool.map(get_article, get_toc(html))
    #多线程处理后的result是多个元组所组成的列表
    for item in result:
        save(item[0], item[1])


# #post 方式练习
# data = {'name': 'k', 'password': '123'}
# html = requests.post('http://exercise.kingname.info/exercise_requests_post', data=data)
# print(html.content.decode())
