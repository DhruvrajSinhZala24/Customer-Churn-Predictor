# Customer Churn Predictor

## 🚀 Overview
The **Customer Churn Predictor** is a Python-based project that helps identify potential customer churn based on payment activity and user status. It uses MySQL for data storage, exports results to CSV, and generates visualizations using `matplotlib` to analyze churn patterns.

---

## ⚙️ Features
- **Customer Data Entry:** Input customer details including name, age, payments made, purchases, and activity status.
- **Database Integration:** Stores customer data and churn predictions in a MySQL database.
- **Churn Prediction:** Flags customers with low payments or inactive status as potential churn.
- **CSV Export:** Saves churned and non-churned customer data to CSV files.
- **Data Visualization:** Generates pie and bar charts for churn distribution analysis.

---

## 🛠️ Technologies Used
- Python
- MySQL
- CSV
- `matplotlib` for visualization

---

## 📊 Churn Prediction Logic
- **Churn Criteria:** 
  - Payments made < 500 → Marked as churn.
  - Inactive users (is_active = 0) → Marked as churn.
- **Visualization:** 
  - Pie chart shows the overall churn distribution.
  - Bar chart displays churn rates across different payment ranges.

---

## 📦 Database Schema
- **Database:** `churn_prediction`
- **Tables:**
  - `customers`: Stores customer details.
  - `churned_customers`: Stores customers identified as churned.
  

## 📊 Output
-**CSV Files:**
- **churned_customers.csv:** Contains details of churned customers.
- **customers_with_churn.csv:** Contains all customer data with churn status.
- **Visualizations:**
   -Pie chart for churn distribution.
   -Bar chart for payments made vs. churn rate.

---

## ⭐ Contribution

Contributions are always welcome! Whether it's a bug fix, a new feature, or an improvement to the project.
