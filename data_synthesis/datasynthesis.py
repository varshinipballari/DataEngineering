# -*- coding: utf-8 -*-
"""Datasynthesis.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1pPmYXPFwdQ9vjJ4b5vYKAtQoL7iz6-v9
"""

pip install faker

import pandas as pd
import numpy as np
import random
from faker import Faker
from datetime import datetime, timedelta


random.seed(42)
np.random.seed(42)


employee_origins = {
    "India": 313944,
    "China": 49917,
    "Mexico": 2444,
    "Canada": 4006,
    "Philippines": 2736,
    "Taiwan": 2676,
    "South Korea": 3928
}


international_total = sum(employee_origins.values())


origin_countries = ["USA"]
origin_probabilities = [0.60]


for nation, employee_count in employee_origins.items():
    origin_countries.append(nation)
    probability = 0.40 * (employee_count / international_total)
    origin_probabilities.append(probability)


gender_options = ["female", "male", "nonbinary"]
gender_distribution = [0.49, 0.49, 0.02]


org_units = {
    "Engineering": 0.30,
    "Product Management": 0.10,
    "Sales": 0.20,
    "Marketing": 0.10,
    "Customer Support": 0.10,
    "IT": 0.06,
    "Human Resources": 0.05,
    "Finance": 0.02,
    "Legal": 0.02,
    "Administrative": 0.04,
    "Executive Leadership": 0.01
}

# Map countries to localization settings
country_localization = {
    "USA": "en_US",
    "India": "en_IN",
    "China": "zh_CN",
    "Mexico": "es_MX",
    "Canada": "en_CA",
    "Philippines": "en_PH",
    "Taiwan": "zh_TW",
    "South Korea": "ko_KR"
}

fake_generators = {locale: Faker(locale) for locale in set(country_localization.values())}
us_faker = Faker("en_US")


department_positions = {
    "Engineering": [
        ("Software Engineer", (100000, 150000)),
        ("Senior Software Engineer", (170000, 220000))
    ],
    "Product Management": [
        ("Product Manager", (100000, 150000)),
        ("Senior Product Manager", (125000, 180000))
    ],
    "Sales": [
        ("Sales Executive", (100000, 180000)),
        ("Sales Manager", (160000, 280000))
    ],
    "Marketing": [
        ("Marketing Manager", (80000, 104000)),
        ("VP of Marketing", (200000, 300000))
    ],
    "Customer Support": [
        ("Support Specialist", (50000, 90000)),
        ("Customer Support Manager", (75000, 120000))
    ],
    "IT": [
        ("IT Analyst", (70000, 100000)),
        ("IT Manager", (95000, 135000))
    ],
    "Human Resources": [
        ("HR Manager", (90000, 130000)),
        ("Recruiter", (70000, 110000))
    ],
    "Finance": [
        ("Financial Analyst", (70000, 100000)),
        ("Controller", (120000, 170000))
    ],
    "Legal": [
        ("Legal Counsel", (150000, 250000)),
        ("Legal IT Support", (46500, 94000))
    ],
    "Administrative": [
        ("Admin Assistant", (35000, 60000)),
        ("IT Services Admin", (50000, 75000))
    ],
    "Executive Leadership": [
        ("VP", (200000, 400000)),
        ("CFO", (250000, 500000))
    ]
}

def generate_random_date(start_date, end_date):
    """Generate a random date between two dates"""
    time_between = end_date - start_date
    random_days = random.randint(0, time_between.days)
    return start_date + timedelta(days=random_days)

def create_birth_date():
    """Generate a realistic birth date for working adults"""
    current_date = datetime.today()
    max_age_date = current_date - timedelta(days=65*365)
    min_age_date = current_date - timedelta(days=20*365)
    return generate_random_date(max_age_date, min_age_date).date()

def create_hire_date(birth_date):
    """Generate hire date ensuring employee was at least 20 when hired"""
    earliest_possible = max(datetime(2010, 1, 1),
        datetime.combine(birth_date, datetime.min.time()) + timedelta(days=365*20))
    return generate_random_date(earliest_possible, datetime.today()).date()

# Generate employee records
employee_records = []
for record_num in range(10000):
    employee_id = 100000000 + record_num
    birth_country = random.choices(origin_countries, weights=origin_probabilities)[0]
    locale_setting = country_localization[birth_country]
    data_generator = fake_generators[locale_setting]

    full_name = us_faker.name()
    contact_number = us_faker.phone_number()
    email_address = us_faker.email()
    employee_gender = random.choices(gender_options, weights=gender_distribution)[0]
    dob = create_birth_date()
    employment_date = create_hire_date(dob)

    org_unit = random.choices(list(org_units.keys()), weights=list(org_units.values()))[0]
    position, (min_salary, max_salary) = random.choice(department_positions[org_unit])
    annual_salary = random.randint(min_salary, max_salary)
    social_security = us_faker.ssn()

    employee_records.append({
        "EmployeeID": employee_id,
        "NationalOrigin": birth_country,
        "FullName": full_name,
        "ContactNumber": contact_number,
        "Email": email_address,
        "Gender": employee_gender,
        "DateOfBirth": dob,
        "EmploymentDate": employment_date,
        "Department": org_unit,
        "JobTitle": position,
        "AnnualSalary": annual_salary,
        "SSN": social_security
    })


emp_df = pd.DataFrame(employee_records)
emp_df.to_csv("emp_df.csv", index=False)

emp_df.describe(include='all')

emp_df.head(10)

total_payroll = emp_df['AnnualSalary'].sum()
print(f"Total yearly payroll: ${total_payroll:,.2f}")

import matplotlib.pyplot as plt
import seaborn as sns

# Plot
plt.figure(figsize=(10, 6))
country_counts = emp_df['NationalOrigin'].value_counts().sort_values(ascending=False)
sns.barplot(x=country_counts.index, y=country_counts.values, palette="viridis")
plt.title("Employee Count by Country of Birth")
plt.xlabel("Country")
plt.ylabel("Number of Employees")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

plt.figure(figsize=(10, 6))
dept_counts = emp_df['Department'].value_counts().sort_values(ascending=False)
sns.barplot(x=dept_counts.index, y=dept_counts.values, palette="magma")
plt.title("Employee Count by Department")
plt.xlabel("Department")
plt.ylabel("Number of Employees")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

emp_df['HireDay'] = pd.to_datetime(emp_df['EmploymentDate']).dt.day_name()
day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

plt.figure(figsize=(10, 6))
sns.countplot(data=emp_df, x='HireDay', order=day_order, palette="rocket")
plt.title("Employees Hired by Day of the Week")
plt.xlabel("Day of the Week")
plt.ylabel("Number of Hires")
plt.tight_layout()
plt.show()

plt.figure(figsize=(10, 6))
sns.kdeplot(data=emp_df, x='AnnualSalary', fill=True, color="blue")
plt.title("Distribution of Salaries (KDE Plot)")
plt.xlabel("Annual Salary ($)")
plt.ylabel("Density")
plt.tight_layout()
plt.show()

emp_df['BirthYear'] = pd.to_datetime(emp_df['DateOfBirth']).dt.year
birth_year_counts = emp_df['BirthYear'].value_counts().sort_index()

plt.figure(figsize=(10, 6))
sns.lineplot(x=birth_year_counts.index, y=birth_year_counts.values, marker="o")
plt.title("Employee Birth Years Over Time")
plt.xlabel("Year")
plt.ylabel("Number of Employees Born")
plt.tight_layout()
plt.show()

plt.figure(figsize=(12, 8))
sns.kdeplot(data=emp_df, x='AnnualSalary', hue='Department', fill=True, common_norm=False, palette="tab20")
plt.title("Salary Distribution by Department (KDE)")
plt.xlabel("Annual Salary ($)")
plt.ylabel("Density")
plt.tight_layout()
plt.show()

emp_df['DateOfBirth'] = pd.to_datetime(emp_df['DateOfBirth'])
current_year = datetime.now().year
emp_df['Age'] = current_year - emp_df['DateOfBirth'].dt.year

emp_df['Weight'] = 1
emp_df.loc[emp_df['Age'].between(40, 49), 'Weight'] = 3

# Normalize weights to sum to 1 (required for sample())
emp_df['Weight'] = emp_df['Weight'] / emp_df['Weight'].sum()

smpl_df = emp_df.sample(n=500, weights='Weight', random_state=42)

summary = smpl_df.describe(include='all')
print(summary)

print(smpl_df.head(10))

import pandas as pd
import numpy as np

salary_range = emp_df['AnnualSalary'].max() - emp_df['AnnualSalary'].min()
sigma = salary_range * 0.05

np.random.seed(42)
noise = np.random.normal(loc=0, scale=sigma, size=len(emp_df))
emp_df['PerturbedSalary'] = emp_df['AnnualSalary'] + noise

# Ensure no negative salaries
emp_df['PerturbedSalary'] = emp_df['PerturbedSalary'].clip(lower=30000)

# Create perturbed DataFrame
prtrb_df = emp_df.copy()

summary = prtrb_df.describe(include='all')
print(summary)

prtrb_df.head(10)

!pip install ydata-profiling
from ydata_profiling import ProfileReport
profile = ProfileReport(emp_df, title="Employee Data Profile", explorative=True)
profile.to_notebook_iframe()