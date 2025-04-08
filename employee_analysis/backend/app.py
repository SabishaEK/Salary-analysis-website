from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import matplotlib.pyplot as plt
import os

app = Flask(__name__, template_folder="templates", static_folder="static")

UPLOAD_FOLDER = 'static/'
CSV_FILE = os.path.join(UPLOAD_FOLDER, 'employees.csv')

# Ensure static folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def generate_analysis(csv_file):
    # Read CSV file
    df = pd.read_csv(csv_file)

    # Ensure required columns exist
    required_columns = ["Name", "Department", "Performance", "Salary", "Experience"]
    if not all(col in df.columns for col in required_columns):
        return "Invalid CSV format! Required columns: Name, Department, Performance, Salary, Experience"

    # Convert necessary columns to numeric
    df["Experience"] = pd.to_numeric(df["Experience"], errors='coerce')
    df["Salary"] = pd.to_numeric(df["Salary"], errors='coerce')
    df["Performance"] = pd.to_numeric(df["Performance"], errors='coerce')

    # Drop NaN values
    df = df.dropna()

    # Calculate Key Statistics
    avg_salary = df["Salary"].mean()
    highest_paid = df.loc[df["Salary"].idxmax(), "Name"]
    top_performer = df.loc[df["Performance"].idxmax(), "Name"]

    stats = {
        "Average Salary": f"${avg_salary:,.2f}",
        "Highest Paid Employee": highest_paid,
        "Top Performer": top_performer
    }

    # Generate Salary Trend Graph
    plt.figure(figsize=(8, 5))
    df.groupby("Experience")["Salary"].mean().plot(kind="line", marker="o", color="blue")
    plt.xlabel("Experience (Years)")
    plt.ylabel("Average Salary")
    plt.title("Salary Trend by Experience")
    plt.grid()

    # Save the chart
    chart_path = os.path.join(app.static_folder, "chart.png")
    plt.savefig(chart_path)
    plt.close()

    # Generate HTML tables
    summary_table = df.groupby("Experience")[["Salary"]].mean().to_html(classes="styled-table")
    employee_data = df.to_html(classes="styled-table")

    return stats, summary_table, employee_data, chart_path

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        if file and file.filename.endswith('.csv'):
            file.save(CSV_FILE)
            return redirect(url_for('dashboard'))

    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    if not os.path.exists(CSV_FILE):
        return "No data uploaded yet!"

    # Process data and generate visualization
    stats, summary_table, employee_data, chart_path = generate_analysis(CSV_FILE)

    return render_template('dashboard.html', 
                           stats=stats, 
                           summary_table=summary_table, 
                           employee=employee_data, 
                           chart_path=chart_path)

if __name__ == "_main_":
    app.run(debug=True)