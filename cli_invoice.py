from datetime import datetime
from fpdf import FPDF
import os

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

    if not os.path.exists("invoices"):
        os.makedirs("invoices")

    pdf.output(file_name)
    print(f"\n✅ Invoice generated: {file_name}")

if __name__ == "__main__":
    print("=== Invoice Generator ===")
    client = input("Client Name: ")
    service = input("Service Description: ")
    rate = float(input("Rate per Hour ($): "))
    hours = float(input("Hours Worked: "))

    generate_invoice(client, service, rate, hours)
