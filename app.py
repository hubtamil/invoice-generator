from flask import Flask, render_template, request, send_file
from fpdf import FPDF
from datetime import datetime
import os

app = Flask(__name__)

# Make sure 'invoices' folder exists
if not os.path.exists("invoices"):
    os.makedirs("invoices")

def generate_invoice_pdf(client_name, service, rate, hours):
    total = rate * hours
    file_name = f"invoices/{client_name.replace(' ', '_')}_invoice.pdf"

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="INVOICE", ln=True, align="C")
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Date: {datetime.now().strftime('%Y-%m-%d')}", ln=True, align="C")
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Bill To: {client_name}", ln=True)
    pdf.cell(200, 10, txt=f"Service: {service}", ln=True)
    pdf.cell(200, 10, txt=f"Rate: ${rate:.2f} per hour", ln=True)
    pdf.cell(200, 10, txt=f"Hours: {hours}", ln=True)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt=f"Total Amount: ${total:.2f}", ln=True)
    pdf.output(file_name)
    return file_name

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/generate', methods=["POST"])
def generate():
    client = request.form["client"]
    service = request.form["service"]
    rate = float(request.form["rate"])
    hours = float(request.form["hours"])
    file_path = generate_invoice_pdf(client, service, rate, hours)
    return send_file(file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, render_template, request
from flask_mail import Mail, Message
from fpdf import FPDF
from datetime import datetime
import os

app = Flask(__name__)

# Mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'your-email@gmail.com'  # Use environment variables for sensitive data
app.config['MAIL_PASSWORD'] = 'your-email-password'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

def generate_invoice(client_name, service, rate, hours):
    total = rate * hours
    file_name = f"invoices/{client_name.replace(' ', '_')}_invoice.pdf"
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="INVOICE", ln=True, align="C")
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Date: {datetime.now().strftime('%Y-%m-%d')}", ln=True, align="C")
    pdf.ln(10)

    pdf.cell(200, 10, txt=f"Bill To: {client_name}", ln=True)
    pdf.cell(200, 10, txt=f"Service: {service}", ln=True)
    pdf.cell(200, 10, txt=f"Rate: ${rate:.2f} per hour", ln=True)
    pdf.cell(200, 10, txt=f"Hours: {hours}", ln=True)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt=f"Total Amount: ${total:.2f}", ln=True)

    pdf.output(file_name)
    print(f"\n✅ Invoice generated: {file_name}")
    return file_name

@app.route('/generate_invoice', methods=['GET', 'POST'])
def generate_invoice_route():
    if request.method == 'POST':
        client_name = request.form['client_name']
        service = request.form['service']
        rate = float(request.form['rate'])
        hours = float(request.form['hours'])
        invoice_file = generate_invoice(client_name, service, rate, hours)

        msg = Message('Your Invoice', sender='your-email@gmail.com', recipients=[request.form['email']])
        msg.body = 'Here is your invoice.'
        with app.open_resource(invoice_file) as fp:
            msg.attach(invoice_file, 'application/pdf', fp.read())

        mail.send(msg)
        return f'Invoice sent to {request.form["email"]}'

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, render_template, request
from flask_mail import Mail, Message
from fpdf import FPDF
from datetime import datetime
import os

app = Flask(__name__)

# Mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'your-email@gmail.com'  # Use environment variables for sensitive data
app.config['MAIL_PASSWORD'] = 'your-email-password'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

# Ensure 'invoices' folder exists
if not os.path.exists("invoices"):
    os.makedirs("invoices")

def generate_invoice(client_name, service, rate, hours):
    total = rate * hours
    file_name = f"invoices/{client_name.replace(' ', '_')}_invoice.pdf"
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="INVOICE", ln=True, align="C")
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Date: {datetime.now().strftime('%Y-%m-%d')}", ln=True, align="C")
    pdf.ln(10)

    pdf.cell(200, 10, txt=f"Bill To: {client_name}", ln=True)
    pdf.cell(200, 10, txt=f"Service: {service}", ln=True)
    pdf.cell(200, 10, txt=f"Rate: ${rate:.2f} per hour", ln=True)
    pdf.cell(200, 10, txt=f"Hours: {hours}", ln=True)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt=f"Total Amount: ${total:.2f}", ln=True)

    pdf.output(file_name)
    return file_name

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate_invoice', methods=['GET', 'POST'])
def generate_invoice_route():
    if request.method == 'POST':
        client_name = request.form['client_name']
        service = request.form['service']
        rate = float(request.form['rate'])
        hours = float(request.form['hours'])
        email = request.form['email']
        
        # Generate the invoice
        invoice_file = generate_invoice(client_name, service, rate, hours)
        
        # Send the invoice via email
        msg = Message('Your Invoice', sender='your-email@gmail.com', recipients=[email])
        msg.body = 'Here is your invoice.'
        
        with app.open_resource(invoice_file) as fp:
            msg.attach(invoice_file, 'application/pdf', fp.read())
        
        mail.send(msg)
        return f'Invoice sent to {email}'
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, render_template
from flask_mail import Mail, Message

# Initialize Flask app
app = Flask(__name__)

# Configure Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Use Gmail's SMTP server
app.config['MAIL_PORT'] = 587  # TLS
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'your-email@gmail.com'  # Your email address
app.config['MAIL_PASSWORD'] = 'your-email-password'  # Your email password or app password for Gmail with 2FA
app.config['MAIL_DEFAULT_SENDER'] = 'your-email@gmail.com'

mail = Mail(app)

# Route to send email
@app.route('/')
def send_email():
    try:
        # Create a message object
        msg = Message("Hello from Flask-Mail", recipients=["recipient@example.com"])
        msg.body = "This is a test email sent from Flask using Flask-Mail!"
        
        # Send the email
        mail.send(msg)
        return 'Email sent successfully!'
    except Exception as e:
        return f"Error: {e}"

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello from Flask!"

if __name__ == '__main__':
    app.run(debug=True)

