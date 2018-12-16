import random

import requests
from bs4 import BeautifulSoup

data = []

def Comments(url):
    response = requests.get(url)
    tree = BeautifulSoup(response.text, 'lxml')
    commentSet = tree.find_all('span', attrs={'class': 'a-size-base review-text'})
    for i in commentSet:
        data.append(i.get_text())
        print(i.get_text())

def getComments(pn):
    url = 'https://www.amazon.cn/The-Adventures-of-Sherlock-Holmes-Doyle-Arthur-Conan/product-reviews/B00A72VZFU/ref' \
          '=cm_cr_arp_d_viewopt_sr?showViewpoints=1&filterByStar=%s&pageNumber=1'% pn
    response = requests.get(url)
    tree = BeautifulSoup(response.text, 'lxml')

    pageNums = tree.find_all('li',attrs={'class':'page-button' })
    if not pageNums:
        return
    index = pageNums[-1].get_text()
    for i in range(1, int(index)):
        url = 'https://www.amazon.cn/The-Adventures-of-Sherlock-Holmes-Doyle-Arthur-Conan/product-reviews/B00A72VZFU' \
              '/ref=cm_cr_getr_d_paging_btm_%s?showViewpoints=1&pageNumber=%s&filterByStar=%s' % ( i, i, pn)
        Comments(url)





if __name__ == "__main__":
    getComments('critical')
    print(len(data))
    with open('critical.txt', 'w+', encoding='utf-8') as f:  # 把评论放入txt,好评改为pos.txt
        for k in data:
            f.write(k)
            f.write('\n')

    # getComments('positive')
    # print(len(data))
    # with open('positive.txt', 'w+', encoding='utf-8') as f:  # 把评论放入txt,好评改为pos.txt
    #     for k in data:
    #         f.write(k)
    #         f.write('\n')