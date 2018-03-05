from urllib import request

url = "http://www.baidu.com"
resp = request.urlopen(url)
html = resp.read().decode("utf-8")
# print(html)

# 携带User-Agent头
req = request.Request(url)
req.add_header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; WOW64)', 'Mozilla/5.0 (Windows NT 6.3; WOW64)")
resp = request.urlopen(req)
html = resp.read().decode("utf-8")
# print(html)

# 发送post请求
from urllib import parse

post_data = parse.urlencode([
    ("m", "QueryData"),
    ("dbcode", "hgyd"),
    ("rowcode", "zb"),
    ("colcode", "sj"),
    ("wds", "[]"),
    ("dfwds", "[{\"wdcode\":\"zb\",\"valuecode\":\"A1501\"}]"),
    ("k1", 1503554448051)
])
url = "http://data.stats.gov.cn/easyquery.htm?cn=A01"
req = request.Request(url)
req.add_header("Origin", "http://data.stats.gov.cn")
req.add_header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; WOW64)', 'Mozilla/5.0 (Windows NT 6.3; WOW64)")
post_resp = request.urlopen(req, data=post_data.encode("utf-8"))
print(post_resp.status, post_resp.reason)
print(post_resp.read().decode("utf-8"))

"""
("id","A15"),
("dbcode","hgyd"),
("wdcode","zb"),
("m","getTree")
"""
