import requests,qrcode,time,flask,base64,json

def getqrcode():
    params=["appName=aliyun_drive","fromSite=52","appName=aliyun_drive","appEntrance=web","isMobile=false",
    "lang=zh_CN","returnUrl=","bizParams=","&_bx-v=2.0.31"]
    endpoint="https://passport.aliyundrive.com/newlogin/qrcode/generate.do?"
    url=endpoint+"&".join(params)
    resp=requests.get(url).json()
    print(resp)
    t=resp['content']['data']['t']
    ck=resp['content']['data']['ck']
    qr=qrcode.make(resp['content']['data']['codeContent'])
    return qr,t,ck

def querystatus(t,ck):
    url="https://passport.aliyundrive.com"+"/newlogin/qrcode/query.do?appName=aliyun_drive&fromSite=52&_bx-v=2.0.31"
    headers={"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}
    body={"t":t,"ck":ck,
        "appName": "aliyun_drive",
        "appEntrance": "web",
        "isMobile": "false",
        "lang": "zh_CN",
        "returnUrl": "",
        "fromSite": "52",
        "bizParams": "",
        "navlanguage": "zh-CN",
        "navPlatform": "MacIntel"}
    resp=requests.post(url,data=body,headers=headers).json()
    print(resp)
    return resp['content']

if __name__=="__main__":
    qr,t,ck=getqrcode()
    qr.show()
    statsmap={}
    qrCodeStatus='NEW'
    while (qrCodeStatus=='NEW' or qrCodeStatus=='SCANED'):
        status=querystatus(t, ck)
        qrCodeStatus=status['data']['qrCodeStatus']

        time.sleep(1)
    if qrCodeStatus=='CONFIRMED':
        encoded_text=status['data']['bizExt']
        decoded_text = base64.b64decode(encoded_text).decode('gbk')
        print(decoded_text)
        bizExt=json.loads(decoded_text)
        print(bizExt['pds_login_result']['refreshToken'])
    else:
        print(qrCodeStatus)