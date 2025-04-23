from flask import Flask, render_template, request, redirect, url_for
from fpdf import FPDF
from datetime import datetime
import os

app = Flask(__name__)

# Make sure 'invoices' folder exists
if not os.path.exists("invoices"):
    os.makedirs("invoices")

# Function to generate invoice PDF
def generate_invoice(client_name, service, rate, hours, tax_rate=0, discount=0, logo_path=None):
    total = rate * hours
    tax_amount = (total * tax_rate) / 100
    discount_amount = (total * discount) / 100
    final_amount = total + tax_amount - discount_amount
    
    file_name = f"invoices/{client_name.replace(' ', '_')}_invoice.pdf"
    
    pdf = FPDF()
    pdf.add_page()

    # Add logo at the top if path is provided
    if logo_path:
        pdf.image(logo_path, 10, 8, 30)  # 10,8 are X,Y coordinates, 30 is size (width)

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
    pdf.cell(200, 10, txt=f"Subtotal: ${total:.2f}", ln=True)
    pdf.cell(200, 10, txt=f"Tax ({tax_rate}%): ${tax_amount:.2f}", ln=True)
    pdf.cell(200, 10, txt=f"Discount ({discount}%): -${discount_amount:.2f}", ln=True)
    pdf.cell(200, 10, txt=f"Total Amount: ${final_amount:.2f}", ln=True)

    pdf.output(file_name)
    return file_name

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    client = request.form['client']
    service = request.form['service']
    rate = float(request.form['rate'])
    hours = float(request.form['hours'])
    tax_rate = float(request.form['tax_rate'])
    discount = float(request.form['discount'])

    file_name = generate_invoice(client, service, rate, hours, tax_rate, discount, logo_path="logo.png")
    return redirect(url_for('download', file_name=file_name))

@app.route('/download/<file_name>')
def download(file_name):
    return send_from_directory('invoices', file_name)

if __name__ == "__main__":
    app.run(debug=True)

if __name__ == "__main__":
    app.run()
