"""
翻译相关配置
"""
#QUERY='apple'
S_DIR=r"C:\Users\Administrator\Desktop\1"#必须要加r，否则1会被转义对待
D_DIR=r"C:\Users\Administrator\Desktop\2"+'\\'#为了表示这是目录而不是文件，必须加两个反斜杠
FROM='en'
TO='zh'

"""
接口授权相关配置
"""
#APPID='20180406000143498'
#KEY='57lEkHjA_Ej8d3aQJsf6'
TRANS_URL='http://api.fanyi.baidu.com/api/trans/vip/translate'

"""
OCR相关配置
"""
#token相关
AUTH_URL='https://aip.baidubce.com/oauth/2.0/token'
#API_KEY="r6Y8xGL6YrWD2Gl7ZnL5EsK1"
#SECRET_KEY="5tHLpqG3AXHcQAonKCLxBSqCt8LZFNP1"#一个空格都不能多


#接口地址
OCR_URL='https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic'

#待识别的图片地址
PIC_URL='https://pic1.zhimg.com/v2-e6aca6ac19fe3dfc2733dfe211a6986b_r.jpg'
#图片保存名字
OCR_FILE='ocr.txt'


