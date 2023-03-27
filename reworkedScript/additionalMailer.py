import yagmail
import json
from flask import Flask, request

app = Flask(__name__)


@app.route('/send_mail', methods=['POST'])
def send_mail():
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']

    subject = "Заголовок письма"
    body = f"""
    <h2>Новое письмо</h2>
    <b>Имя:</b> {name}<br>
    <b>Почта:</b> {email}<br><br>
    <b>Сообщение:</b><br>{message}
    """

    try:
        yag = yagmail.SMTP(user='no-reply@infinitytechnologies.ch', password='password')
        yag.send(to=email, subject=subject, contents=body)
        return json.dumps({"result": "success", "status": "Message sent successfully"})
    except Exception as e:
        return json.dumps({"result": "error", "status": str(e)})


@app.route('/send_case_study', methods=['POST'])
def send_case_study():
    name = request.form['name']
    email = request.form['email']
    file = request.form['file']

    with open("mail.html", "r") as file:
        body = file.read()
    body = body.replace('$name', name)

    files = {
        "sosbooking": "SOSbooking.pdf",
        "vodafone": "VodafoneTV.pdf",
        "fitto": "fitto.pdf",
        "zimit": "Zimit.pdf",
        "basf": "BASF.pdf",
        "edms": "EDMS.pdf",
        "sw2": "EdTech.pdf",
        "E-commerce": "E-commerce.pdf",
        "OptimizedWarehouse": "OptimizedWarehouse.pdf"
    }
    file_name = files.get(file)

    try:
        yag = yagmail.SMTP(user='no-reply@infinitytechnologies.ch', password='password')
        yag.send(to=email, subject="Full Case Study", contents=body, attachments=file_name)
        yag.send(to='info@infinitytechnologies.ch', subject="Request of Full Case Study", contents=f"<p>Контактное лицо {name}, email {email}, Case Study {file}</p>")
        return json.dumps({"result": "success", "status": "Case study sent successfully"})
    except Exception as e:
        return json.dumps({"result": "error", "status": str(e)})


if __name__ == "__main__":
    app.run()
