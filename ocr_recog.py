from config import AUTH_URL,OCR_URL
import json
import requests
def get_token(api_key,secret_key):
	params = {
		'grant_type' :'client_credentials',
		'client_id':api_key,
		'client_secret':secret_key
	}
	res = requests.post(AUTH_URL, params=params)
	# print('headers',res.request.headers)
	return res

def parse_token(res):
	a_dic=json.loads(res.text)
	token=a_dic['access_token']
	#print('token=',token)
	return token


def get_res_from_ocr(access_token,pic_url):
	headers={
		'Content-Type':'application/x-www-form-urlencoded'
	}
	params = {
		'access_token':access_token,
		'url':pic_url
	}
	res = requests.post(OCR_URL, headers=headers,params=params)
	res.raise_for_status()
	return res

def parse_query(res):
	a_dic=json.loads(res.text)
	words_result=a_dic['words_result']
	#print(words_result)
	query=''.join([item['words'] for item in words_result])
	#''.join(a_lst)=》list元素拼接成一个str
	return query


def ocr_recong(api_key,secret_key,pic_url):
	res=get_token(api_key,secret_key)
	access_token=parse_token(res)
	res=get_res_from_ocr(access_token,pic_url)
	query=parse_query(res)
	#print('query=',query)
	return query

if __name__=='__main__':
	api_key="r6Y8xGL6YrWD2Gl7ZnL5EsK1"
	secret_key="5tHLpqG3AXHcQAonKCLxBSqCt8LZFNP1"
	pic_url='https://pic1.zhimg.com/v2-e6aca6ac19fe3dfc2733dfe211a6986b_r.jpg'
	ocr_recong(api_key,secret_key,pic_url)


