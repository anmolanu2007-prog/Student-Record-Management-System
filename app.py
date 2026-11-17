import streamlit as st
import pandas as pd
import os

# Page Configuration
st.set_page_config(
    page_title="Student Management System",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 Student Record Management System")
st.write("Manage student records using CRUD operations.")

FILE = "students.csv"

# Load student data
if os.path.exists(FILE):
    df = pd.read_csv(FILE)
else:
    df = pd.DataFrame(columns=["ID", "Name", "Age", "Course", "Marks"])


# Sidebar Menu
st.sidebar.title("Student Management")
choice = st.sidebar.selectbox(
    "Select Operation",
    ["Add Student", "View Students", "Update Student", "Delete Student"]
)


# ---------------- CREATE ----------------

if choice == "Add Student":

    st.subheader("➕ Add New Student")

    with st.form("add_student_form"):

        sid = st.number_input("Student ID", min_value=1, step=1)
        name = st.text_input("Student Name")
        age = st.number_input("Age", min_value=1, max_value=100, value=18)
        course = st.text_input("Course")
        marks = st.number_input("Marks", min_value=0, max_value=100)

        submit = st.form_submit_button("Add Student")

        if submit:

            if not name.strip() or not course.strip():
                st.error("Please enter all student details.")

            elif sid in df["ID"].values:
                st.error("Student ID already exists!")

            else:

                new_student = pd.DataFrame([{
                    "ID": sid,
                    "Name": name,
                    "Age": age,
                    "Course": course,
                    "Marks": marks
                }])

                df = pd.concat([df, new_student], ignore_index=True)

                df.to_csv(FILE, index=False)

                st.success("Student added successfully!")


# ---------------- READ ----------------

elif choice == "View Students":

    st.subheader("📋 All Student Records")

    if df.empty:
        st.info("No student records available.")

    else:
        st.dataframe(df, use_container_width=True)

        st.write("Total Students:", len(df))


# ---------------- UPDATE ----------------

elif choice == "Update Student":

    st.subheader("✏️ Update Student Details")

    if df.empty:
        st.info("No student records available.")

    else:

        sid = st.selectbox(
            "Select Student ID",
            df["ID"].tolist()
        )

        student = df[df["ID"] == sid].iloc[0]

        with st.form("update_student_form"):

            name = st.text_input(
                "Student Name",
                value=str(student["Name"])
            )

            age = st.number_input(
                "Age",
                min_value=1,
                max_value=100,
                value=int(student["Age"])
            )

            course = st.text_input(
                "Course",
                value=str(student["Course"])
            )

            marks = st.number_input(
                "Marks",
                min_value=0,
                max_value=100,
                value=int(student["Marks"])
            )

            update = st.form_submit_button("Update Student")

            if update:

                if not name.strip() or not course.strip():
                    st.error("Name and course cannot be empty.")

                else:

                    df.loc[
                        df["ID"] == sid,
                        ["Name", "Age", "Course", "Marks"]
                    ] = [name, age, course, marks]

                    df.to_csv(FILE, index=False)

                    st.success("Student updated successfully!")


# ---------------- DELETE ----------------

elif choice == "Delete Student":

    st.subheader("🗑️ Delete Student Record")

    if df.empty:
        st.info("No student records available.")

    else:

        sid = st.selectbox(
            "Select Student ID",
            df["ID"].tolist()
        )

        student = df[df["ID"] == sid].iloc[0]

        st.write("Student Name:", student["Name"])

        confirm = st.checkbox("I confirm that I want to delete this student.")

        if st.button("Delete Student", type="primary"):

            if confirm:

                df = df[df["ID"] != sid]

                df.to_csv(FILE, index=False)

                st.success("Student deleted successfully!")

            else:
                st.warning("Please confirm before deleting.")