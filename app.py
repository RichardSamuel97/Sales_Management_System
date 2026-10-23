# Importing Streamilt Libary
import streamlit as st

# Defining pages
login_page = st.Page("login.py",title="Login")
project_page = st.Page("project.py", title="Sales Management System")
sales_page = st.Page("c.sales.py", title="Customer Sales")


# Navigation between pages
pg = st.navigation([login_page, project_page, sales_page],position="hidden")

# Run page
pg.run()


