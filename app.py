from flask import Flask, render_template, request, send_file
from fpdf import FPDF
from datetime import datetime
import os

app = Flask(__name__)

# Create invoices folder if not exists
if not os.path.exists('invoices'):
    os.makedirs('invoices')

# Industry invoice templates (can be extended)
industry_templates = {
    "College": ["Admission Fees", "Hostel Fees", "Exam Fees"],
    "Hospital": ["Consultation", "Lab Test", "Surgery"],
    "Cosmetic Shop": ["Facial", "Makeup", "Hair Spa"],
    "Social Media Services": ["Instagram Ads", "YouTube Editing", "Influencer Promo"],
    "Job Seeker": ["Resume Service", "Mock Interview", "Career Counseling"]
}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        client_name = request.form['client_name']
        industry = request.form['industry']
        selected_services = request.form.getlist('services')
        rate = float(request.form['rate'])
        hours = float(request.form['hours'])

        total = rate * hours
        file_name = f"invoices/{client_name.replace(' ', '_')}_invoice.pdf"

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(200, 10, "INVOICE", ln=True, align='C')

        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, f"Date: {datetime.now().strftime('%Y-%m-%d')}", ln=True, align='C')
        pdf.ln(10)
        pdf.cell(200, 10, f"Client: {client_name}", ln=True)
        pdf.cell(200, 10, f"Industry: {industry}", ln=True)

        pdf.ln(5)
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(200, 10, "Selected Services:", ln=True)
        pdf.set_font("Arial", size=12)

        for service in selected_services:
            pdf.cell(200, 10, f"- {service}", ln=True)

        pdf.ln(5)
        pdf.cell(200, 10, f"Rate: ${rate:.2f} / hour", ln=True)
        pdf.cell(200, 10, f"Hours: {hours}", ln=True)

        pdf.set_font("Arial", 'B', 12)
        pdf.cell(200, 10, f"Total Amount: ${total:.2f}", ln=True)

        pdf.output(file_name)
        return send_file(file_name, as_attachment=True)

    return render_template('index.html', templates=industry_templates)

if __name__ == '__main__':
    app.run(debug=True)

