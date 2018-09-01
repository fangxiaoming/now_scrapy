#!/usr/bin/env python
# encoding: utf-8

"""
@version: 1.0
@license: Apache Licence
"""
import requests
from scrapy.selector import Selector
import pymysql
import random

conn = pymysql.connect(host="127.0.0.1", user="root", passwd="", db="article_spider", charset="utf8")
cursor = conn.cursor()

def get_random_ip():
    #爬取西刺的免费IP
    headers = {
        "User-Agent" : "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11"
    }
    rand = random.randint(1,10)
    re = requests.get("http://www.xicidaili.com/nt/{0}".format(rand), headers=headers)
    selector = Selector(text=re.text)
    all_trs = selector.css("#ip_list tr")
    ip_list = []
    # for tr in all_trs[1:]:
    rand1 = random.randint(1,len(all_trs)-1)
    tr = all_trs[rand1]
    speed_str = tr.css(".bar::attr(title)").extract()[0]
    if speed_str:
        speed = float(speed_str.split("秒")[0])

    all_texts = tr.css("td::text").extract()
    ip = all_texts[0]
    port = all_texts[1]
    proxy_type = all_texts[5]
    ip_list.append((ip,port,proxy_type,speed))
    ip_list = ip_list[0]
    print(ip_list)
    if ip_list[2] == "HTTPS":
        proxy_url ="https://{0}:{1}".format(ip_list[0], ip_list[1])
        print(proxy_url)
    elif ip_list[2] == "HTTP":
        proxy_url ="http://{0}:{1}".format(ip_list[0], ip_list[1])
        print(proxy_url)
    if judge_ip(ip_list,proxy_url):
        print("valid")
    else:
        print("invalid")
    return ip_list
        # for ip_info in ip_list:
        #     cursor.execute(
        #         "insert ip_list(ip,port,speed,proxy_type) VALUES('{0}','{1}',{2},'{3}')".format(
        #         ip_info[0],ip_info[1],ip_info[3],ip_info[2]
        #         )
        #     )
        #     conn.commit()

def judge_ip(ip_list,proxy_url):
    #判断ip是否可用
    http_url = "http://www.seu.edu.cn/"
    try:
        proxy_dict = {
            "http":proxy_url,
            "https":proxy_url

        }
        response = requests.get(http_url, proxies = proxy_dict)
        return True
    except Exception as e:
        print("invalid ip and port")
        print(e)
        return False
    else:
        code = response.status_code
        if code >= 200 and code < 300:
            print("effectiv ip")
            return True
        else:
            print("invalid")

if __name__ == "__main__":
    get_random_ip()