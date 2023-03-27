from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
import datetime
import yagmail

# Load environment variables from .env file
load_dotenv()

# Create a new Flask instance
app = Flask(__name__)

# Get SMTP server configurations from environment variables
smtp_server = os.environ.get('SMTP_SERVER')
smtp_port = os.environ.get('SMTP_PORT')
smtp_username = os.environ.get('SMTP_USERNAME')
smtp_password = os.environ.get('SMTP_PASSWORD')

# Example CURL commands for testing
'''
CURL examples

curl --location 'http://localhost:5000/'
curl --location 'http://localhost:5000/get-all-logs?date=2023-03-27'
curl --location 'http://localhost:5000/send-email' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'email=osa.9735@gmail.com' \
--data-urlencode 'attachment=aa'
'''


# Define root URL route
@app.route('/', methods=['GET'])
def get():
    return "hello world"


# Define send-email URL route
@app.route('/send-email', methods=['POST'])
def send_email():
    # Get email and attachment parameters from the request form data
    email = request.form.get('email')
    attachment = request.form.get('attachment')

    # Simple error handling
    if not email:
        error_msg = 'Error: Email is empty'
        log_request(email, attachment, error_msg)
        return error_msg
    if attachment not in ['aa', 'bb']:
        error_msg = 'Error: Invalid attachment type'
        log_request(email, attachment, error_msg)
        return error_msg

    # Send the email
    try:
        yag = yagmail.SMTP(smtp_username, smtp_password, host=smtp_server, port=smtp_port, smtp_ssl=True)
        yag.send(to=email, subject='Attachment', contents='See attachment', attachments=[f'files/{attachment}.pdf'])
        success_msg = 'Email sent successfully!'
        log_request(email, attachment, success_msg)
        return success_msg
    except Exception as e:
        error_msg = f'Error sending email: {str(e)}'
        log_request(email, attachment, error_msg)
        return error_msg


# Define get-all-logs URL route
@app.route('/get-all-logs', methods=['GET'])
def get_all_logs():
    # Get the date parameter from the request arguments
    date_str = request.args.get('date')

    # Convert the date string to a datetime object
    try:
        date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': 'Invalid date format'}), 400

    # Get the log file path based on the date parameter
    log_file_name = os.path.join('logs', f'{date_str}-log').replace('\\', '/')
    if not os.path.exists(log_file_name):
        return jsonify({'error': 'No logs for the specified date'}), 404

    # Read the log file and return its content in HTML format
    with open(log_file_name, 'r') as f:
        logs = f.read().replace('\n', '<br>')

    return jsonify({'html': logs}), 200


# Helper function to write log messages to a file
def log_request(email, attachment, result=None):
    log_file_name = os.path.join('logs', datetime.datetime.now().strftime('%Y-%m-%d') + '-log').replace('\\', '/')
    log_message = f'{datetime.datetime.now()} | Email: {email} | Attachment: {attachment}'
    if result:
        log_message += f' | Result: {result}'
    log_message += '\n'
    with open(log_file_name, 'a') as f:
        f.write(log_message)


if __name__ == '__main__':
    app.run()
