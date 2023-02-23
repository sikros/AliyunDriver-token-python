from flask import Flask, render_template, request,send_file,session
import qrcode,base64,io,os
from cli import *
from PIL import Image

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

@app.route('/')
def index():
    text,t,ck=get_qrcode()
    session['t']=t
    session['ck']=ck
    # 生成二维码
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(text)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    # 将图像转换为字节流
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='PNG')

    image_stream = img_bytes.getvalue()
    heximage = base64.b64encode(image_stream)
    return render_template('show_qrcode.html',img_data=heximage.decode())

@app.route('/querystatus')
def querystatus():
    print('query')
    t=session.get('t')
    ck=session.get('ck')
    resp=query_status(t,ck)
    print(resp)
    return resp

@app.route('/bizext')
def decodebizext():
    _bizext = request.args.get('code')
    bizext = decode_bizext(_bizext)
    return bizext


@app.route('/generate_qrcode', methods=['POST'])
def generate_qrcode():
    data = request.form.get('data')
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color='black', back_color='white')
    img.save('qrcode.png')
    return render_template('show_qrcode.html')

@app.route('/scan_qrcode')
def scan_qrcode():
    return render_template('scan_qrcode.html')

@app.route('/scan_qrcode_result', methods=['POST'])
def scan_qrcode_result():
    file = request.files['file']
    img = Image.open(file)
    result = pyzbar.decode(img)
    if len(result) > 0:
        data = result[0].data.decode('utf-8')
        return render_template('scan_qrcode_result.html', data=data)
    else:
        return render_template('scan_qrcode_result.html', data='未能扫描到二维码')

if __name__ == '__main__':
    app.run(debug=True)
