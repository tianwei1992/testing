#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
先引入系统库
"""
import requests
import hashlib
import random
import json
import glob, os
import logging
import sys
import getopt

"""
再引入自己的
"""
from config import S_DIR,D_DIR,FROM,TO,TRANS_URL,OCR_FILE
from ocr_recog import ocr_recong



"""
复制知乎multiple1902的建议：

0. 不要用 import * 这种写法，永远详细地写清楚到底 import 了哪些符号。
1. start() 里面，遇到了不明确的 exception 时候把异常的内容打出来，之后方便单独处理。最终不要写单独的 except，而是具体给出会遇到哪些 exception，比如 except KeyError 这样。
2. import 顺序：先 import 系统级别的库 (json 和 requests)，再 import 来自自己项目的内容 (config)。
3. 代码的格式：使用现有的某种代码风格，大部分风格应该都是规定了用 n 个空格代替 tab 的。也有别的规定，比如赋值号两边要有空格之类。
4. 单元测试：单元测试应该尽量没有外部依赖，那么怎么把现在的测试改成没有外部依赖的形式？至于检查和外部 API 的集成，可以写个集成测试。
5. 检查拼写。
6. 代码里面定义了一些常量，比如文件路径、API key 之类，把它改成更灵活的形式。比如文件路径每次调用可能不一样，那就换成命令行参数 (推荐使用 fire 库)；API key 不同人用起来可能不一样，但不应该放在命令行参数里面 (为什么?)，那就改成读取环境变量。


"""

"""
为保密，APPID,KEY,API_KEY,SECRET_KEY全部从命令行参数当场传入，而不放在配置信息里
usage: start.py -a <appid> -k <key> -i <api_key> -s <secret_key> -p <pic_url>
"""
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

def get_trans_from_baidu(query,appid,key):
	"""
	首先生成随机数salt，接着构造sign,接着构造请求参数params
	这里salt在文档里被描述成一个int类型的随机数，但没有规定大小。示例中salt=1435660288，于是这里我也随机random.random.int()
	"""
	salt = str(random.randint(1, 1000))
	sign=generate_sign(appid, query, salt, key)

	params = {
		'q': query,
		'from': FROM,
		'to': TO,
		'appid':appid,
		'salt': salt,
		'key': key,
		'sign':sign

	}
	res = requests.get(TRANS_URL, params=params)
	# print('headers',res.request.headers)
	res.raise_for_status()
	return res

def parse_content(json_str):
	a_dic=json.loads(json_str)
	trans_result=a_dic['trans_result']
	dst=trans_result[0]['dst']
	return dst

def get_query(file):
	with open(file, "r") as fd:
		query = fd.read()
		#print('query=', query)
		return query


def save_result(file,content,D_DIR):
	file_name=file.split('.')[0]+'_trans'+'.txt'
	#print(file_name)
	file_path=D_DIR+file_name
	if  not os.path.exists(D_DIR):
		os.mkdir(D_DIR)

	with open(file_path,'w+') as fd:
		fd.write(content)

def get_opt():
	try:
		argv=sys.argv[1:]
		opts, args = getopt.getopt(argv, "ha:k:i:s:p:")
	except getopt.GetoptError:
		print('usage: start.py -a <appid> -k <key> -i <api_key> -s <secret_key> -p <pic_url>')
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print('usage: start.py -a <appid> -k <key> -i <api_key> -s <secret_key> -p <pic_url>')
			sys.exit()
		elif opt == '-a':
			appid = arg
		elif opt == '-k':
			key = arg
		elif opt == '-i':
			api_key = arg
		elif opt == '-s':
			secret_key = arg
		elif opt == '-p':
			pic_url = arg
	return (appid,key,api_key,secret_key,pic_url)

def start():
	try:
		print("获取输入中……")
		appid, key, api_key, secret_key,pic_url=get_opt()
		print("正在识别图片 ……")
		query = ocr_recong(api_key,secret_key,pic_url)
		print("正在翻译……")
		res = get_trans_from_baidu(query,appid,key)
		content = parse_content(res.text)
		print("翻译结果是：", content)
		save_result(OCR_FILE, content, D_DIR)
		print("保存成功")
	except ConnectionError as e:
		logging.exception(e)
		print("ConnectionError")
	except OSError as e:
		logging.exception(e)
		print("OSError")
	except NameError as e:
		logging.exception(e)
		print("NameError")
	except SyntaxError as e:
		logging.exception(e)
		print("SyntaxError")
	except Exception as e:
		logging.exception(e)
		print("OtherError")

		"""
		os.chdir(S_DIR)
		for file in glob.glob("*.txt"):
			#print(file)
			query=get_query(file)
			try:
				print("正在翻译文档 "+file+"……")
				res=get_trans_from_baidu(query)
				content=parse_content(res.text)
				print("翻译结果是：",content)
				save_result(file,content,D_DIR)
				print("保存成功\n")
			except:
				print("翻译失败")
				continue
	"""

if __name__=="__main__":
	start()