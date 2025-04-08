# Salary-analysis-website

A web-based application built using *Flask, **Pandas, and **Matplotlib* to analyze and visualize employee performance and salary data.

## Features

- Upload and analyze employee data in CSV format
- Display uploaded data in a structured table
- Show key statistics:
  - Average salary
  - Highest paid employee
  - Top performing employee
- Generate and display a salary trend chart based on experience
- User-friendly and responsive interface

## Setup

Follow these steps to run the project locally:

```bash
 Step 1: Install required packages (make sure Python is installed)
     pip install flask pandas matplotlib

 Step 2: Run the application
python app.py

 Step 3: Open your browser and go to
http://localhost:5000

 Step 4: Upload your employees.csv file in the following format:
 Name,Department,Performance,Salary,Experience
 John Doe,IT,4.5,60000,5
 Jane Smith,HR,4.2,55000,4
 Mike Johnson,Finance,4.8,70000,6
 Emily Davis,Marketing,4.1,50000,3
