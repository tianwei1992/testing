import requests
from config import *
import hashlib
import random
import json

def generate_sign(appid,q,salt,key):

	#print('salt=',salt)
	str1=appid+q+salt+key
	#print(str1)
	sign=hashlib.md5(str1.encode("utf-8")).hexdigest()
	#实例给的sign是16进制的字符串，注意hashlib.md5只是得到一个object，继续调用hexdiget()方法才能得到真正的值
	#print("sign=",sign)
	return sign
	
	
	"""
	签名生成方法如下：
1、将请求参数中的 APPID(appid), 翻译query(q, 注意为UTF-8编码), 随机数(salt), 以及平台分配的密钥(可在管理控制台查看)
按照 appid+q+salt+密钥 的顺序拼接得到字符串1。
2、对字符串1做md5，得到32位小写的sign。
	"""

def get_res_from_baidu():
	"""
	首先生成随机数salt，接着构造sign,接着构造请求参数params
	这里salt在文档里被描述成一个int类型的随机数，但没有规定大小。示例中salt=1435660288，于是这里我也随机random.random.int()
	"""

	salt = str(random.randint(1, 1000))
	QUERY = input(">>请输入英文：")
	sign=generate_sign(APPID, QUERY, salt, KEY)

	params = {
		'q': QUERY,
		'from': FROM,
		'to': TO,
		'appid': APPID,
		'salt': salt,
		'key': KEY,
		'sign':sign

	}
	res = requests.get(URL, params=params)
	# print('headers',res.request.headers)
	res.raise_for_status()
	return res

def parse_content(json_str):
	a_dic=json.loads(json_str)
	trans_result=a_dic['trans_result']
	dst=trans_result[0]['dst']
	return dst

def start():
	while True:
		try:
			res=get_res_from_baidu()
			content=parse_content(res.text)
			print("翻译结果是：",content)
		except:
			continue
if __name__=="__main__":
	start()