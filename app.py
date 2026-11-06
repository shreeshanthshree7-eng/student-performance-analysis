
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# -------------------------------
# 1. PAGE CONFIGURATION
# -------------------------------

st.set_page_config(
    page_title="Student Performance Analysis",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 Student Attendance and Performance Analysis")
st.write("Statistical analysis of student attendance and academic marks")

# -------------------------------
# 2. LOAD STUDENT DATA
# -------------------------------

uploaded_file = st.file_uploader(
    "Upload Student CSV File",
    type=["csv"]
)

try:
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_csv("students.csv")

except FileNotFoundError:
    st.error("students.csv file not found!")
    st.stop()

# Required columns
required_columns = [
    "Roll_No",
    "Name",
    "Total_Classes",
    "Attended_Classes",
    "Marks"
]

if not all(col in df.columns for col in required_columns):
    st.error("CSV file has incorrect column names.")
    st.stop()

# Convert numeric columns
numeric_columns = [
    "Roll_No",
    "Total_Classes",
    "Attended_Classes",
    "Marks"
]

for col in numeric_columns:
    df[col] = pd.to_numeric(df[col], errors="coerce")

if df[required_columns].isnull().any().any():
    st.error("Please check your data. Missing or invalid values found.")
    st.stop()

if df["Roll_No"].duplicated().any():
    st.error("Duplicate roll numbers found.")
    st.stop()

if (
    (df["Total_Classes"] <= 0).any()
    or (df["Attended_Classes"] < 0).any()
    or (df["Attended_Classes"] > df["Total_Classes"]).any()
    or (df["Marks"] < 0).any()
    or (df["Marks"] > 100).any()
):
    st.error("Invalid attendance or marks values.")
    st.stop()

# -------------------------------
# 3. CALCULATE ATTENDANCE
# -------------------------------

df["Attendance_Percentage"] = (
    df["Attended_Classes"] /
    df["Total_Classes"]
) * 100

# -------------------------------
# 4. STUDENT PERFORMANCE STATUS
# -------------------------------

def get_status(row):

    if row["Attendance_Percentage"] < 75:
        return "Low Attendance"

    elif row["Marks"] < 40:
        return "Poor Performance"

    else:
        return "Good Performance"


df["Status"] = df.apply(get_status, axis=1)

# -------------------------------
# 5. DASHBOARD METRICS
# -------------------------------

st.header("Student Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Students", len(df))

col2.metric(
    "Average Attendance",
    f"{df['Attendance_Percentage'].mean():.2f}%"
)

col3.metric(
    "Average Marks",
    f"{df['Marks'].mean():.2f}"
)

col4.metric(
    "Highest Marks",
    f"{df['Marks'].max():.2f}"
)

st.divider()

# -------------------------------
# 6. STUDENT RECORDS
# -------------------------------

st.header("Student Records")

st.dataframe(
    df,
    use_container_width=True
)

# -------------------------------
# 7. STATISTICAL ANALYSIS
# -------------------------------

st.header("Statistical Analysis of Marks")

marks = df["Marks"]

mean = marks.mean()
median = marks.median()
mode = marks.mode().tolist()
variance = marks.var()
std_dev = marks.std()

col1, col2, col3 = st.columns(3)

col1.metric("Mean", f"{mean:.2f}")
col2.metric("Median", f"{median:.2f}")
col3.metric("Variance", f"{variance:.2f}")

col4, col5 = st.columns(2)

col4.metric("Standard Deviation", f"{std_dev:.2f}")

col5.metric(
    "Mode",
    ", ".join(map(str, mode))
)

# -------------------------------
# 8. ATTENDANCE ANALYSIS
# -------------------------------

st.header("Attendance Analysis")

low_attendance = df[
    df["Attendance_Percentage"] < 75
]

st.write(
    "Students below 75% attendance:",
    len(low_attendance)
)

st.dataframe(
    low_attendance,
    use_container_width=True
)

# -------------------------------
# 9. PERFORMANCE ANALYSIS
# -------------------------------

st.header("Performance Analysis")

poor_students = df[df["Marks"] < 40]

st.write(
    "Students scoring below 40 marks:",
    len(poor_students)
)

st.dataframe(
    poor_students,
    use_container_width=True
)

# -------------------------------
# 10. GRAPHS
# -------------------------------

st.header("Data Visualization")

# Student marks bar chart
st.subheader("Student Marks Comparison")

marks_chart = df.set_index("Name")[["Marks"]]

st.bar_chart(marks_chart)

# Attendance chart
st.subheader("Attendance Percentage")

attendance_chart = df.set_index("Name")[
    ["Attendance_Percentage"]
]

st.bar_chart(attendance_chart)

# Marks distribution
st.subheader("Marks Distribution")

fig, ax = plt.subplots()

ax.hist(marks, bins=5, edgecolor="black")

ax.set_xlabel("Marks")
ax.set_ylabel("Number of Students")
ax.set_title("Distribution of Student Marks")

st.pyplot(fig)
plt.close(fig)

# -------------------------------
# 11. CORRELATION ANALYSIS
# -------------------------------

st.header("Attendance and Marks Correlation")

correlation = df[
    ["Attendance_Percentage", "Marks"]
].corr().iloc[0, 1]

st.metric(
    "Correlation Coefficient",
    f"{correlation:.3f}"
)

st.scatter_chart(
    df,
    x="Attendance_Percentage",
    y="Marks"
)

st.write(
    "Correlation close to +1 indicates a strong "
    "positive linear relationship."
)

# -------------------------------
# 12. DOWNLOAD REPORT
# -------------------------------

st.header("Download Student Report")

csv_data = df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Analysis Report",
    data=csv_data,
    file_name="student_analysis_report.csv",
    mime="text/csv"
)

st.success("Student analysis completed successfully!")
