from fpdf import FPDF
from datetime import datetime
import os

# Make sure 'invoices' folder exists
if not os.path.exists("invoices"):
    os.makedirs("invoices")

# Function to generate invoice PDF
def generate_invoice(client_name, service, rate, hours, logo_path=None):
    total = rate * hours
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
    pdf.cell(200, 10, txt=f"Total Amount: ${total:.2f}", ln=True)

    pdf.output(file_name)
    print(f"\n✅ Invoice generated: {file_name}")

# --- Main Program ---
if __name__ == "__main__":
    print("=== Invoice Generator ===")
    client = input("Client Name: ")
    service = input("Service Description: ")
    rate = float(input("Rate per Hour ($): "))
    hours = float(input("Hours Worked: "))
    
    logo_path = "logo.png"  # Adjust this if your logo filename/path is different

    generate_invoice(client, service, rate, hours, logo_path)

from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello from Flask app deployed on Render! 🎉'

if __name__ == '__main__':
    app.run()
