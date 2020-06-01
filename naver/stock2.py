# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup

target = open("data2.txt", 'w', 1)


def safe_list_get_text(element_list, index):
    try:
        return element_list[index].get_text()
    except IndexError:
        # print("error : " + code)
        return ""


def strip_exclude_number(s):
    return ''.join(i for i in s if i.isdigit())


def scrap(t, s):
    cookies = {"field_list": "12|0000811B"}
    for page in range(1, s):
        resp = requests.get('https://finance.naver.com/sise/sise_market_sum.nhn?sosok=' + str(t) + '&page=' + str(page),
                            cookies=cookies)
        soup = BeautifulSoup(resp.text, 'html.parser')
        tags = soup.select("div.box_type_l > table.type_2 > tbody > tr")

        for i in range(1, len(tags)):
            tds = []
            if not tags[i].select('td')[0].get_text().strip():
                continue
            for td in tags[i].select('td'):
                tds.append(td.get_text().strip())
            try:
                tds[12] = str(int(strip_exclude_number(tds[7])) / int(strip_exclude_number(tds[2])))
            except :
                print("\t".join(tds) + " N/A")
            target.write("\t".join(tds) + "\n")


if __name__ == '__main__':
    titles = ["no", "종목명", "현재가", "전일비", "등락률", "액면가", "시가총액", "배당금", "PER", "ROE", "PBR", "유보율", "배당율"]
    target.write("\t".join(titles) + "\n")
    scrap(0, 32)
    scrap(1, 29)
    target.flush()
    target.close()
