import streamlit as st
import pandas as pd
import mysql.connector

# Database connection
def connect_db():
    cfg = st.secrets["mysql"]
    return mysql.connector.connect(
        host=cfg["host"],
        port=int(cfg.get("port", 3306)),
        user=cfg["user"],
        password=cfg["password"],
        database=cfg["database"]
    )

# Read SQL table
def read_data(query, params=None):
    conn = connect_db()
    try:
        return pd.read_sql_query(query, conn, params=params)
    finally:
        conn.close()


# ---------------- LOGIN VALIDATION ----------------
if not st.session_state.get("logged_in", False):
    st.switch_page("login.py")
    st.stop()

role = st.session_state.get("role")
username = st.session_state.get("username")
branch_id = st.session_state.get("branch_id")


# creating Home Button,Title

if st.button("Home", key="home_button"):
    st.switch_page("project.py")

st.title("📋Customer Sales Table")

# Role Based Table 
try:
    if role == "superadmin":

        # Superadmin can see all branches
        query = """
            SELECT *
            FROM customer_sales
            ORDER BY sale_id DESC
        """
        c_sales = read_data(query)

    elif role == "admin" and branch_id is not None:

        # Branch admin can see only their assigned branch
        query = """
            SELECT *
            FROM customer_sales
            WHERE branch_id = %s
            ORDER BY sale_id DESC
        """
        c_sales = read_data(query, params=(branch_id,))

    else:
        st.error("Invalid role or branch assignment.")
        st.stop()

    st.dataframe(
        c_sales,
        use_container_width=True,
        hide_index=True
    )

    st.caption(f"Total records: {len(c_sales)}")
except Exception as e:
    st.error(f"Error loading customer sales table: {e}")


if st.button("Logout",key="Logout_Button"):
    st.switch_page("login.py")
