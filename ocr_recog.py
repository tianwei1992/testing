from config import *
import json
import requests
def get_token():
	params = {
		'grant_type' :'client_credentials',
		'client_id':API_KEY,
		'client_secret':SECRET_KEY
	}
	res = requests.post(AUTH_URL, params=params)
	# print('headers',res.request.headers)
	return res

def parse_token(res):
	a_dic=json.loads(res.text)
	token=a_dic['access_token']
	#print('token=',token)
	return token


def get_res_from_ocr(access_token):
	headers={
		'Content-Type':
	'application/x-www-form-urlencoded'
	}
	params = {
		'access_token':access_token,
		'url':PIC_URL
	}

	res = requests.post(OCR_URL, headers=headers,params=params)
	print(res.request.headers)
	print(res.request.url)
	res.raise_for_status()
	return res

def parse_query(res):
	a_dic=json.loads(res.text)
	words_result=a_dic['words_result']
	#print(words_result)
	query=''.join([item['words'] for item in words_result])
	#''.join(a_lst)=》list元素拼接成一个str
	return query


def ocr_recong():
	res=get_token()
	access_token=parse_token(res)
	res=get_res_from_ocr(access_token)
	query=parse_query(res)
	print(query)
	return query

if __name__=='__main__':
	ocr_recong()


