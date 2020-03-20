# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
from multiprocessing import Pool
f = open("codes.txt", 'r')
target = open("data.txt", 'w', 1)
target.write("종목	코드	현재가	시가총액	PER	E_PER	PBR	ROE	배당수익률\n\n")


def safe_list_get_text(element_list, index):
    try:
        return element_list[index].get_text()
    except IndexError:
        # print("error : " + code)
        return ""


def strip_exclude_number(str):
    return ''.join(i for i in str if i.isdigit())


def scrap(code):
    data = []
    print("code = " + code)
    resp = requests.get('https://finance.naver.com/item/main.nhn?code=' + code)
    soup = BeautifulSoup(resp.text, 'html.parser')
    title = safe_list_get_text(soup.select('#middle > div.h_company > div.wrap_company > h2 > a'), 0)
    price = strip_exclude_number(safe_list_get_text(
        soup.select("#content > div.section.invest_trend > div.sub_section.right > table > tbody  em"), 0).strip())
    tot = ''
    totstr = safe_list_get_text(soup.select("#_market_sum"), 0).strip().split("조")
    if len(totstr) > 1:
        tot = totstr[0].strip() + totstr[1].strip().zfill(4)
    else:
        tot = totstr[0].strip()
    per1 = safe_list_get_text(soup.select("#_per"), 0).strip()
    #per2 = safe_list_get_text(soup.select("#krx_per"), 0).strip()
    per3 = safe_list_get_text(soup.select("#_cns_per"), 0).strip()
    pbr = safe_list_get_text(soup.select("#_pbr"), 0).strip()
    try:
        roe = soup.select(".cop_analysis > .sub_section > table > tbody > tr")[5].select("td")[3].get_text().strip()
        if not roe:
            roe = soup.select(".cop_analysis > .sub_section > table > tbody > tr")[5].select("td")[2].get_text().strip()
    except IndexError:
        roe = ""
        print(f'{code} no roe')
    dvr = safe_list_get_text(soup.select("#_dvr"), 0).strip()
    data.append(title)
    data.append(code)
    data.append(price)
    data.append(tot)
    data.append(per1)
    #data.append(per2)
    data.append(per3)
    data.append(pbr)
    data.append(roe)
    data.append(dvr)
    target.write("\t".join(data) + "\n")


if __name__ == '__main__':
    pool = Pool(processes=16)

    codes = []
    for line in f:
        codes.append(line.strip())

    f.close()
    pool.map(scrap, codes)
    target.flush()
    target.close()
