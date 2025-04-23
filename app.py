from flask import Flask, render_template, request, send_file
from fpdf import FPDF
from datetime import datetime
import os

app = Flask(__name__)

# Make sure 'invoices' folder exists
if not os.path.exists("invoices"):
    os.makedirs("invoices")

def generate_invoice(client_name, selected_services, rate, hours):
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
    pdf.cell(200, 10, txt="Services:", ln=True)
    for service in selected_services:
        pdf.cell(200, 10, txt=f"- {service}", ln=True)

    pdf.cell(200, 10, txt=f"Rate: ${rate:.2f} per hour", ln=True)
    pdf.cell(200, 10, txt=f"Hours: {hours}", ln=True)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt=f"Total Amount: ${total:.2f}", ln=True)

    pdf.output(file_name)
    return file_name

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        client = request.form['client']
        rate = float(request.form['rate'])
        hours = float(request.form['hours'])
        selected_services = request.form.getlist('services')
        
        invoice_path = generate_invoice(client, selected_services, rate, hours)
        return send_file(invoice_path, as_attachment=True)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

