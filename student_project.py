import os
import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

CSV_FILE = "students_data.csv"

# 1. TUPLE: Fixed subjects aur sections
SUBJECTS = ("Maths", "Python", "Electronics")
SECTIONS = ("A", "B", "C")


# --- AUTO-CREATE 50 STUDENTS CSV DATASET ---
def create_csv():
    if os.path.exists(CSV_FILE):
        return

    np.random.seed(42)  # Taaki har baar same realistic marks banein
    names = [
        "Aarav", "Priya", "Rohan", "Sneha", "Kabir", "Ananya", "Vikas", "Neha", "Dev", "Pooja",
        "Arjun", "Meera", "Sahil", "Karan", "Riya", "Aditya", "Tanvi", "Harsh", "Simran", "Nikhil",
        "Ishita", "Manish", "Divya", "Yash", "Kriti", "Gaurav", "Shruti", "Pranav", "Sakshi", "Abhishek",
        "Nandini", "Deepak", "Muskan", "Varun", "Aayushi", "Tushar", "Bhavna", "Mayank", "Kunal", "Pallavi",
        "Shubham", "Jahnvi", "Utkarsh", "Roshni", "Mohit", "Anjali", "Saurabh", "Vanshika", "Aman", "Diya"
    ]

    with open(CSV_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Roll_No", "Name", "Section", "Maths", "Python", "Electronics", "Attendance"])
        for i, name in enumerate(names):
            roll = 101 + i
            sec = SECTIONS[i % 3]
            m = "" if i == 4 else int(np.random.randint(35, 98))   # Intentional missing value
            p = "" if i == 11 else int(np.random.randint(40, 99))  # Intentional missing value
            e = int(np.random.randint(35, 96))
            att = int(np.random.randint(65, 98))
            writer.writerow([roll, name, sec, m, p, e, att])
    print("50 students ka 'students_data.csv' create ho gaya!\n")


def get_grade(pct):
    if pct >= 90: return "A+"
    elif pct >= 75: return "A"
    elif pct >= 60: return "B"
    elif pct >= 40: return "C"
    return "F"


def load_data():
    df = pd.read_csv(CSV_FILE)
    # Missing Values Handling (blank marks ko subject mean se fill karo)
    for sub in SUBJECTS:
        df[sub] = df[sub].fillna(round(df[sub].mean(), 1))

    marks_2d = df[list(SUBJECTS)].to_numpy()
    df["Total"] = np.sum(marks_2d, axis=1)
    df["Percentage"] = np.round((df["Total"] / 300) * 100, 2)
    df["Grade"] = df["Percentage"].apply(get_grade)
    df["Eligible"] = np.where(df["Attendance"] >= 75, "Yes", "No")
    return df


def save_data(df):
    cols = ["Roll_No", "Name", "Section", "Maths", "Python", "Electronics", "Attendance"]
    df[cols].to_csv(CSV_FILE, index=False)


# --- CRUD OPERATIONS ---
def display_all():
    df = load_data()
    cols = ["Roll_No", "Name", "Section", "Total", "Percentage", "Grade", "Attendance", "Eligible"]
    print(f"\n--- ALL STUDENTS (Total: {len(df)}) ---")
    print(df[cols].to_string(index=False))
    print()


def add_student():
    df = load_data()
    existing_rolls = set(df["Roll_No"])  # SET for duplicate check

    roll = int(input("Roll No: "))
    if roll in existing_rolls:
        print("Error: Roll No already exists!\n")
        return

    rec = {
        "Roll_No": roll,
        "Name": input("Name: ").strip(),
        "Section": input("Section (A/B/C): ").strip().upper(),
        "Maths": float(input("Maths marks: ")),
        "Python": float(input("Python marks: ")),
        "Electronics": float(input("Electronics marks: ")),
        "Attendance": float(input("Attendance %: "))
    }
    df = pd.concat([df, pd.DataFrame([rec])], ignore_index=True)
    save_data(df)
    print("Student added successfully!\n")


def search_student():
    df = load_data()
    q = input("Enter Roll No or Name: ").strip()
    res = df[df["Roll_No"] == int(q)] if q.isdigit() else df[df["Name"].str.lower().str.contains(q.lower())]
    print("\nNot found!\n" if res.empty else f"\n{res.to_string(index=False)}\n")


def update_student():
    df = load_data()
    roll = int(input("Enter Roll No to update: "))
    if roll not in df["Roll_No"].values:
        print("Roll No not found!\n")
        return

    idx = df.index[df["Roll_No"] == roll][0]
    print(f"Updating {df.loc[idx, 'Name']}:")
    for sub in SUBJECTS:
        df.loc[idx, sub] = float(input(f"New {sub} marks: "))
    df.loc[idx, "Attendance"] = float(input("New Attendance %: "))
    save_data(df)
    print("Record updated!\n")


def delete_student():
    df = load_data()
    roll = int(input("Enter Roll No to delete: "))
    if roll not in df["Roll_No"].values:
        print("Roll No not found!\n")
        return
    df = df[df["Roll_No"] != roll]
    save_data(df)
    print(f"Roll No {roll} deleted!\n")


# --- NUMPY & PANDAS ANALYTICS ---
def numpy_stats():
    df = load_data()
    pct_1d = np.array(df["Percentage"])               # 1D Array
    marks_2d = df[list(SUBJECTS)].to_numpy()          # 2D Array

    print("\n===== NUMPY ANALYSIS =====")
    print(f"1D Shape: {pct_1d.shape} | 2D Shape: {marks_2d.shape}")
    print(f"Indexing (1st Student %): {pct_1d[0]}%")
    print(f"Slicing (First 5 %): {pct_1d[:5]}")
    print(f"2D Slice (First 3 Students Marks):\n{marks_2d[:3]}")
    print(f"\nSum: {np.sum(pct_1d):.2f} | Mean: {np.mean(pct_1d):.2f}%")
    print(f"Max: {np.max(pct_1d):.2f}% | Min: {np.min(pct_1d):.2f}% | Std Dev: {np.std(pct_1d):.2f}\n")


def pandas_report():
    df = load_data()
    top5 = df.sort_values(by="Percentage", ascending=False).head(5)
    defaulters = df[df["Attendance"] < 75]
    sec_avg = df.groupby("Section")[["Percentage", "Attendance"]].mean().round(2)

    print("\n===== PANDAS SUMMARY REPORT =====")
    print("\n1. TOP 5 TOPPERS:")
    print(top5[["Roll_No", "Name", "Section", "Percentage", "Grade"]].to_string(index=False))
    print(f"\n2. ATTENDANCE DEFAULTERS (<75%): {len(defaulters)} students")
    print("\n3. SECTION-WISE AVERAGE (GroupBy):")
    print(sec_avg.to_string())
    print("\n4. STATISTICAL SUMMARY (describe):")
    print(df[["Maths", "Python", "Electronics", "Percentage"]].describe().round(2).to_string())

    # File Handling: Save summary to text file
    with open("student_report.txt", "w") as f:
        f.write("TOP 5 TOPPERS:\n" + top5[["Roll_No", "Name", "Percentage"]].to_string(index=False))
        f.write("\n\nSECTION AVERAGE:\n" + sec_avg.to_string())
    print("\nReport saved to 'student_report.txt'!\n")


def show_graph():
    df = load_data()
    sec_avg = df.groupby("Section")[["Percentage", "Attendance"]].mean()
    sec_avg.plot(kind="bar", color=["royalblue", "orange"], edgecolor="black")
    plt.axhline(75, color="red", linestyle="--", label="75% Rule")
    plt.title("Section-Wise Average Percentage vs Attendance")
    plt.ylabel("Average (%)")
    plt.xticks(rotation=0)
    plt.legend()
    plt.tight_layout()
    plt.show()


# --- MAIN MENU ---
create_csv()
while True:
    print("===== STUDENT SCORE & PERCENTAGE ANALYSER =====")
    print("1. Display All (50+)   2. Add Student     3. Search Student")
    print("4. Update Student      5. Delete Student  6. NumPy Analysis")
    print("7. Pandas Report       8. Show Graph      9. Exit")
    ch = input("Choice (1-9): ").strip()

    if ch == "1": display_all()
    elif ch == "2": add_student()
    elif ch == "3": search_student()
    elif ch == "4": update_student()
    elif ch == "5": delete_student()
    elif ch == "6": numpy_stats()
    elif ch == "7": pandas_report()
    elif ch == "8": show_graph()
    elif ch == "9": break
    else: print("Invalid choice!\n")