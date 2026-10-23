#Importing Streamilt Library
import streamlit as st

# Entering Admin's Username and Password
users = {
    "superadmin": {
        "password": "super123",
        "role": "superadmin",
        "branch_id": None
    },
    "admin_chennai": {
        "password": "admin123",
        "role": "admin",
        "branch_id": 1
    },
    "admin_bangalore": {
        "password": "admin123",
        "role": "admin",
        "branch_id": 2
    },
    "admin_hyderabad": {
        "password": "admin123",
        "role": "admin",
        "branch_id": 3
    },
    "admin_delhi": {
        "password": "admin123",
        "role": "admin",
        "branch_id": 4
    },
    "admin_mumbai": {
        "password": "admin123",
        "role": "admin",
        "branch_id": 5
    },
    "admin_pune": {
        "password": "admin123",
        "role": "admin",
        "branch_id": 6
    },
    "admin_kolkata": {
        "password": "admin123",
        "role": "admin",
        "branch_id": 7
    },
    "admin_ahmedabad": {
        "password": "admin123",
        "role": "admin",
        "branch_id": 8
    }
}

# Hiding sidebar only on login page
st.markdown("""
    <style>
        [data-testid="stSidebar"] {
            display: none;
        }

        [data-testid="collapsedControl"] {
            display: none;
        }
    </style>
""", unsafe_allow_html=True)


# Creating Title,Heading,Info
st.title("Sales Management System")
st.header("Welcome to the Login Page")
st.info("Please login to check the customer sales report")


with st.form("login_form",border=False):
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    login_button = st.form_submit_button(
        "Login",
        use_container_width=False
    )


# Login Validation
if login_button:

    if not username or not password:
        st.warning("Please enter both username and password.")

    elif username in users and password == users[username]["password"]:

        # Store login details
        st.session_state["logged_in"] = True
        st.session_state["username"] = username
        st.session_state["role"] = users[username]["role"]
        st.session_state["branch_id"] = users[username]["branch_id"]

        st.success("Login successful!")

        # Navigate to sales management page
        st.switch_page("project.py")

    else:
        st.error("Invalid username or password.")