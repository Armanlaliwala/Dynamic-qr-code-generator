from flask import Flask, render_template, request, send_file
import qrcode
from io import BytesIO

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def generate_qr():
    if request.method == 'POST':
        name = request.form.get('name')
        company = request.form.get('company')
        email = request.form.get('email')
        mobile = request.form.get('mobile')
        extra_keys = request.form.getlist('extra_keys[]')
        extra_values = request.form.getlist('extra_values[]')

        # Structure QR code data
        qr_data = f"Name: {name}\nCompany: {company}\nEmail: {email}\nMobile: {mobile}"
        for key, value in zip(extra_keys, extra_values):
            qr_data += f"\n{key}: {value}"

        # Generate QR code
        qr = qrcode.make(qr_data)
        img_io = BytesIO()
        qr.save(img_io, 'PNG')
        img_io.seek(0)

        return send_file(img_io, mimetype='image/png', as_attachment=True, download_name="qr_code.png")

    return render_template('index.html')

if __name__ == '__main__':
    from waitress import serve
    serve(app, host="0.0.0.0", port=10000)
