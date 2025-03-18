import mysql.connector
import csv
import matplotlib.pyplot as plt

def get_customer_data():
    customers = []
    while True:
        print("\nEnter customer details:")
        name = input("Name: ").strip()
        try:
            while True:
                age = int(input("Age: "))
                if age<=0:
                    print("Age cannot be negative or 0")
                else:
                    break
            while True:
                payments_made = int(input("Payments Made Till Date: "))
                if payments_made<=0:
                    print("Payments Made Till Date cannot be negative")
                else:
                    break
            while True:
                purchases = int(input("Number of Purchases: "))
                if purchases<=0:
                    print("Number of Purcahses cannot be negative")
                else:
                    break
            while True:
                is_active = int(input("Currently Active User (1-Yes, 0-No): "))
                if is_active==1 or is_active==0:
                    break
                else:
                    print("Invalid choice. Please enter 1 for Yes or 0 for No.")
                    continue
            customers.append([name, age, payments_made, purchases, is_active])
        except ValueError:
            print("Invalid input! Please enter the correct data type for each field.")

        while True:
            more_data = input("Do you want to enter details for another user? (yes/no): ").strip().lower()
            if more_data == "yes" or more_data=="no":
                break
            else:
                print("Invalid input,Please enter yes or no.")
        if more_data=="no":
            break

    return customers

def insert_customer_data(customers):
    try:
        conn = mysql.connector.connect(host="localhost", user="root", password="", database="churn_prediction")
        cursor = conn.cursor()
        for customer in customers:
            cursor.execute("INSERT INTO customers (name, age, payments_made, purchases, is_active) VALUES (%s, %s, %s, %s, %s)", customer)
        conn.commit()
        conn.close()
        print("Customer data inserted successfully.")
    except mysql.connector.Error as e:
        print(f"Error inserting data into the database: {e}")

def predict_churn():
    try:
        conn = mysql.connector.connect(host="localhost", user="root", password="", database="churn_prediction")
        cursor = conn.cursor()
        cursor.execute("SELECT customer_id, name, payments_made, is_active FROM customers")
        customers = cursor.fetchall()
        conn.close()

        churned_customers = []
        all_customers_with_churn = []

        for customer_id, name, payments_made, is_active in customers:
            churn=None
            if payments_made < 500 or is_active == 0:
                churn=1
            else:
                churn=0
            all_customers_with_churn.append([customer_id, name, churn])
            if churn == 1:
                churned_customers.append([customer_id, name, payments_made, is_active])

        # Save churned customers to CSV
        with open("churned_customers.csv", "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["customer_id", "name", "payments_made", "is_active"])
            writer.writerows(churned_customers)

        # Save all customers with churn info to CSV
        with open("customers_with_churn.csv", "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["customer_id", "name", "churn"])  # Header
            writer.writerows(all_customers_with_churn)

        #Churned Customer to database
        try:
            conn = mysql.connector.connect(host="localhost", user="root", password="", database="churn_prediction")
            cursor = conn.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS churned_customers (customer_id INT, name VARCHAR(255), payments_made INT, is_active INT)")
            for customer in churned_customers:
                cursor.execute("INSERT INTO churned_customers (customer_id, name, payments_made, is_active) VALUES (%s, %s, %s, %s)", customer)
            conn.commit()
            conn.close()
            print("Churned Customer data inserted successfully.")
        except mysql.connector.Error as e:
            print(f"Error inserting data into the database: {e}")

        # Visualization
        churn_counts = {0: 0, 1: 0}
        payments_made_groups = {}
        for _, _, payments_made, is_active in customers:
            churn = 1 if payments_made < 500 or is_active == 0 else 0
            churn_counts[churn] += 1
            bin_label = get_payment_bin(payments_made)
            if bin_label not in payments_made_groups:
                payments_made_groups[bin_label] = {"churned": 0, "total": 0}
            payments_made_groups[bin_label]["total"] += 1
            if churn == 1:
                payments_made_groups[bin_label]["churned"] += 1
        # Pie chart
        labels = ["No Churn", "Churn"]
        colors = ["lightblue", "lightcoral"]
        plt.pie(list(churn_counts.values()), labels=labels, autopct="%1.1f%%", startangle=90, colors=colors)
        plt.title("Churn Distribution")
        plt.show()
        # Bar chart
        bin_labels = ["0-100", "101-200", "201-300", "301-400", "401-500", "501+"]
        churn_rates = []
        for bin_label in bin_labels:
            group_data = payments_made_groups.get(bin_label)
            if group_data:
                churn_rate = (group_data["churned"] / group_data["total"]) * 100 if group_data["total"] > 0 else 0
                churn_rates.append(churn_rate)
            else:
                churn_rates.append(0)

        plt.bar(bin_labels, churn_rates, color="red", alpha=0.7)
        plt.xlabel("Payments Made (Range)")
        plt.ylabel("Average Churn Rate (%)")
        plt.title("Payments Made vs. Churn")
        plt.xticks(rotation=45)
        plt.show()

    except mysql.connector.Error as e:
        print(f"Database error: {e}")

def get_payment_bin(payments_made):
    if payments_made <= 100:
        return "0-100"
    elif payments_made <= 200:
        return "101-200"
    elif payments_made <= 300:
        return "201-300"
    elif payments_made <= 400:
        return "301-400"
    elif payments_made <= 500:
        return "401-500"
    else:
        return "501+"

customers = get_customer_data()
insert_customer_data(customers)
predict_churn()
print("\nPrediction complete. Results saved to database and CSV files.")