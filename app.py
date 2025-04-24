from flask import Flask, render_template, request, send_file
from fpdf import FPDF
import os
from datetime import datetime

app = Flask(__name__)

if not os.path.exists("invoices"):
    os.makedirs("invoices")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        client_name = request.form['client_name']
        service = request.form.get('service')
        rate = float(request.form['rate'])
        hours = float(request.form['hours'])
        email = request.form['email']  # Get the email address
        
        total = rate * hours
        file_name = f"invoices/{client_name.replace(' ', '_')}_invoice.pdf"

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(200, 10, "INVOICE", ln=True, align="C")

        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, f"Date: {datetime.now().strftime('%Y-%m-%d')}", ln=True, align="C")
        pdf.ln(10)

        pdf.cell(200, 10, f"Bill To: {client_name}", ln=True)
        pdf.cell(200, 10, f"Service: {service}", ln=True)
        pdf.cell(200, 10, f"Rate: ${rate:.2f} per hour", ln=True)
        pdf.cell(200, 10, f"Hours: {hours}", ln=True)
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(200, 10, f"Total Amount: ${total:.2f}", ln=True)

        pdf.output(file_name)

        # Optional: Send the email (if you want to implement email functionality)
        # You can use Flask-Mail to send the generated invoice via email to the provided email address.

        return send_file(file_name, as_attachment=True)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

