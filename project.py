# Importing Libaries
import streamlit as st
import pandas as pd
import mysql.connector
from datetime import date

# Webpage Title
st.set_page_config(page_title="Sales Management System")

if not st.session_state.get("logged_in", False):
    st.switch_page("login.py")

# Connecting with Database
def connect_db():
    cfg = st.secrets["mysql"]
    return mysql.connector.connect(
        host=cfg["host"],
        port=int(cfg.get("port", 3306)),
        user=cfg["user"],
        password=cfg["password"],
        database=cfg["database"],
    )

def read_data(sql, params=None):
    conn = connect_db()
    try:
        return pd.read_sql_query(sql, conn, params=params)
    finally:
        conn.close()

def save_data(sql, params):
    conn = connect_db()
    try:
        cursor = conn.cursor()
        cursor.execute(sql, params)
        conn.commit()
    finally:
        conn.close()


# Authenticating Users 
username = str(
    st.session_state.get("username")
    or st.session_state.get("user")
    or st.session_state.get("name")
    or ""
).strip()
role_value = str(st.session_state.get("role", "")).strip().lower()

if not username or username.lower() in {"none", "guest"}:
    st.warning("Please log in to access the Sales Management System.")
    st.switch_page("login.py")
    st.stop()

is_superadmin = (
    username.lower() == "superadmin"
    or "superadmin" in role_value
    or bool(st.session_state.get("is_superadmin", False))
)

try:
    branches_df = read_data(
        "SELECT branch_id, branch_name FROM branches ORDER BY branch_name"
    )
except Exception as exc:
    st.error(f"Could not load branches from MySQL: {exc}")
    st.stop()

# Resolve branch access using session values first, then the username suffix.
user_branch_id = st.session_state.get("branch_id")
user_branch_name = st.session_state.get("branch_name")

if not is_superadmin:
    if user_branch_id is not None:
        try:
            user_branch_id = int(user_branch_id)
        except (TypeError, ValueError):
            user_branch_id = None

    if user_branch_id is None and user_branch_name:
        matches = branches_df[
            branches_df["branch_name"].astype(str).str.strip().str.lower()
            == str(user_branch_name).strip().lower()
        ]
        if not matches.empty:
            user_branch_id = int(matches.iloc[0]["branch_id"])
            user_branch_name = str(matches.iloc[0]["branch_name"])

    if user_branch_id is None and username.lower().startswith("admin_"):
        suffix = username.split("_", 1)[1].replace("_", " ").strip().lower()
        matches = branches_df[
            branches_df["branch_name"].astype(str).str.strip().str.lower() == suffix
        ]
        if not matches.empty:
            user_branch_id = int(matches.iloc[0]["branch_id"])
            user_branch_name = str(matches.iloc[0]["branch_name"])

    if user_branch_id is not None:
        branch_match = branches_df[branches_df["branch_id"] == user_branch_id]
        if not branch_match.empty:
            user_branch_name = str(branch_match.iloc[0]["branch_name"])

    if user_branch_id is None or user_branch_name is None:
        st.error(
            "Your account is not linked to a branch. Set branch_id or branch_name "
            "in login.py session state, or use a username like admin_chennai that "
            "matches a branch in the branches table."
        )
        st.stop()

# Database Table_name and Column_name
SALES_DATE = "dates"
RECEIVED_COLUMN = "recieved_amount"  # Your database uses this spelling
PAYMENT_AMOUNT = "amount_paid"


# Navigation Menu
st.sidebar.title("Navigation")

pages = ["Dashboard & Reports", "Data Entry Workspace"]

if is_superadmin:pages.append("Advanced SQL Engine")

page = st.sidebar.radio("Go to", pages, key="project_navigation")

st.sidebar.divider()

######################################################################################


######################################################################################################
if st.sidebar.button("Customer Sales", key="customer_sales_button",type="secondary"):
    st.switch_page("c.sales.py")

st.sidebar.divider()

st.sidebar.write(f"👤 User: **{username}**")
st.sidebar.write(f"🔑 Role: **{'Superadmin' if is_superadmin else 'Branch Admin'}**")

if st.sidebar.button("Log Out", key="project_logout", use_container_width=True):
        # Clear authentication/user-specific session state, then return to login.
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.switch_page("login.py")

# Common branch information used by multiple pages.
all_branch_names = branches_df["branch_name"].dropna().astype(str).tolist()
if not is_superadmin:
    visible_branches = branches_df[branches_df["branch_id"] == user_branch_id].copy()
else:
    visible_branches = branches_df.copy()




# Page-1:Dashboard and Reports 
if page == "Dashboard & Reports":
    st.title("📈**Student Enrollment Dashboard**")

    st.header("🔍Filter Control")

   
    branches = read_data("SELECT branch_id, branch_name FROM branches ORDER BY branch_name")
    products = read_data("SELECT DISTINCT product_name FROM customer_sales " "WHERE product_name IS NOT NULL ORDER BY product_name")
    dates = read_data(f"SELECT MIN({SALES_DATE}) AS min_date, MAX({SALES_DATE}) AS max_date ""FROM customer_sales")

    if dates.empty or pd.isna(dates.loc[0, "min_date"]):
            start_default = end_default = date.today()
    else:
            start_default = pd.to_datetime(dates.loc[0, "min_date"]).date()
            end_default = pd.to_datetime(dates.loc[0, "max_date"]).date()


    branch_names = ["All"] + branches["branch_name"].dropna().tolist()
    product_names = ["All"] + products["product_name"].dropna().tolist()


    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if is_superadmin:
                branch_names = ["All"] + all_branch_names
                selected_branch = st.selectbox("Branch Name", branch_names, key="dashboard_branch")

        else:
            
            selected_branch = user_branch_name
            st.selectbox(
                "Branch Name",
                [user_branch_name],
                index=0,
                disabled=True,
                key="dashboard_branch_locked",
            )


    with col2: 
            product = st.selectbox("Product Name", product_names)

    with col3:
            start_date = st.date_input("Start Date", start_default)

    with col4:
            end_date = st.date_input("End Date", end_default)



    if start_date > end_date:
            st.error("Start date cannot be after end date.")
            st.stop()

    sql = f"""
        SELECT
            cs.sale_id,
            cs.branch_id,
            cs.{SALES_DATE} AS dates,
            cs.name,
            cs.mobile_number,
            cs.product_name,
            cs.gross_sales,
            cs.{RECEIVED_COLUMN} AS recieved_amount,
            (COALESCE(cs.gross_sales, 0) - COALESCE(cs.{RECEIVED_COLUMN}, 0)) AS pending_amount,
            cs.status,
            b.branch_name
        FROM customer_sales AS cs
        LEFT JOIN branches AS b ON cs.branch_id = b.branch_id
        WHERE DATE(cs.{SALES_DATE}) BETWEEN %s AND %s
    """
    params = [start_date, end_date]

    if not is_superadmin:
        sql += " AND cs.branch_id = %s"
        params.append(user_branch_id)
    elif selected_branch != "All":
        sql += " AND b.branch_name = %s"
        params.append(selected_branch)

    if product != "All":
        sql += " AND cs.product_name = %s"
        params.append(product)

    sql += f" ORDER BY cs.{SALES_DATE} DESC"

    try:
        sales = read_data(sql, params)
    except Exception as exc:
        st.error(f"Dashboard query failed: {exc}")
        st.stop()


    gross = pd.to_numeric(sales["gross_sales"], errors="coerce").fillna(0).sum()
    received = pd.to_numeric(sales[RECEIVED_COLUMN], errors="coerce").fillna(0).sum()
    pending = gross - received
    pending_pct = (pending / gross * 100) if gross else 0
    
    st.divider()

    st.header("💵Financial Summary")


    st.markdown("""
<style>
div[data-testid="stMetricValue"] {
    font-size: 25px !important;
    white-space: nowrap !important;
    overflow: visible !important;
}

div[data-testid="stMetricValue"] > div {
    overflow: visible !important;
    text-overflow: clip !important;
}
</style>
""", unsafe_allow_html=True)




    col1, col2, col3, col4 = st.columns(4)

    with col1:
         st.metric("Overall Revenue (Gross)", value = f"**₹{gross:,.2f}**")

    with col2:
         
         st.metric("Total Received Amount", f"**₹{received:,.2f}**")

    with col3:

        st.metric("Total Pending Amount", f"**₹{pending:,.2f}**")

    with col4:

        st.metric("Pending Percentage Pct", f"**{pending_pct:.2f}%**")


 

  

# Page-2:Data Entry Workspace
elif page == "Data Entry Workspace":

    st.title("**📝 Operations Record Creator**")

    tab1, tab2 = st.tabs(["Add New Sales Entry", "Log Payment Splits Details"])

    with tab1:

        st.header("New Sale Generation")

        branches = visible_branches.copy()

        if is_superadmin:
            branch_name = st.selectbox("Branch",branches["branch_name"].tolist(),key="new_sale_branch")
        else:
            branch_name = user_branch_name
            st.selectbox(
                "Branch",
                [user_branch_name],
                index=0,
                disabled=True,
                key="new_sale_branch_locked",
            )

        col1, col2 = st.columns(2)

        with col1:  
            customer_name = st.text_input("Student Name")

        with col2:
             product = st.text_input("Course Name")

        col1, col2 = st.columns(2)

        with col1: 
             mobile = st.text_input("Mobile Number")

        with col2:
             sale_date = st.date_input("Joining Date", date.today())
        
        gross = st.number_input("Gross Sales Amount (₹)", min_value=0.0, step=100.0)


        status = st.selectbox("Initial Order Status", ["Open", "Close"])


        submit_sale = st.button("Publish Sale Entry", type="primary")

        if submit_sale:
                if not customer_name.strip() or not mobile.strip() or not product.strip():
                    st.error("Please fill in customer name, mobile number, and product.")
                else:
                    branch_id = int(
                        branches.loc[branches["branch_name"] == branch_name, "branch_id"].iloc[0]
                    )
                    save_data(
                        f"""INSERT INTO customer_sales
                        (branch_id, {SALES_DATE}, name, mobile_number, product_name,
                         gross_sales, {RECEIVED_COLUMN}, status)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                        (branch_id, sale_date, customer_name.strip(), mobile.strip(),
                         product.strip(), gross, 0, status),
                    )
                    st.success("Sale saved to MySQL.")
                    st.rerun()
        

    with tab2:

            st.header("Post Payment Installment Split")
            sales = read_data("SELECT sale_id, name, product_name FROM customer_sales ORDER BY sale_id DESC")

           
            methods = ["Cash", "UPI", "Card"]
            sale_ids = sales["sale_id"].tolist()
            sale_id = st.selectbox("Select Target Active Sale ID Asset", sale_ids)
            method = st.selectbox("Payment Collection Channel", methods)
            amount = st.number_input("Collected Split Amount Balance (₹)", min_value=0.01, step=100.0)
            payment_date = st.date_input("Payment Date", date.today())
            submit_payment = st.button("Save Payment", type="primary")

            if submit_payment:
                    save_data(
                        f"""INSERT INTO payment_splits
                        (sale_id, payment_method, {PAYMENT_AMOUNT}, payment_date)
                        VALUES (%s, %s, %s, %s)""",
                        (int(sale_id), method, amount, payment_date),
                    )
                    st.success("Payment saved to MySQL.")
                    st.rerun()

            st.subheader("Recent Payments")
            st.dataframe(
                read_data("SELECT * FROM payment_splits ORDER BY payment_id DESC LIMIT 100"),
                use_container_width=True,
                hide_index=True,
            )



# Page-3:Advanced SQL Engine
else:
    #Header
    st.header("🛢️ Advanced SQL Engine")

    #Questions
    questions = {
        "1.	Retrieve all records from the customer_sales table": {
                "tier": "Basic Queries ",
                "query": "select * from customer_sales;"
            },
            "2.	Retrieve all records from the branches table": {
                "tier": "Basic Queries",
                "query": "select * from branches;"
            },
            "3. Retrieve all records from the payment_splits table": {
                "tier": "Basic Queries",
                "query": "select * from payment_splits;"
            },
            "4. Display all sales with status = 'Open'": {
                "tier": "Basic Queries",
                "query": "SELECT * FROM customer_sales where status = 'open';"
            },
            "5. Retrieve all sales belonging to the Chennai branch": {
                "tier": "Basic Queries",
                "query": "select * from customer_sales where branch_id =1;"
            },
            "6. Calculate the total gross sales across all branches": {
                "tier": "Aggregation Queries ",
                "query": "select branch_id , sum(gross_sales)as Total_Gross_Sales from customer_sales group by branch_id;"
            },
            "7.	Calculate the total received amount across all sales": {
                    "tier": "Aggregation Queries ",
                    "query": "select sale_id , sum(recieved_amount)as Total_Received_Amount from customer_sales group by sale_id;"
            },
            "8. Calculate the total pending amount across all sales": {
                    "tier": "Aggregation Queries ",
                    "query": "select sale_id , sum(pending_amount)as Total_Pending_amount from customer_sales group by sale_id;"
            },
            "9. Count the total number of sales per branch": {
                    "tier": "Aggregation Queries ",
                    "query": "select branch_id , count(sale_id) as Total_number_of_sale from customer_sales group by branch_id;"
            },
            "10.Find the average gross sales amount": {
                    "tier": "Aggregation Queries ",
                    "query": "select avg(gross_sales) as average_gross_sale_amount from customer_sales;"
            },
            "11.Retrieve sales details along with the branch name": {
                        "tier": "Join-Based Queries  ",
                        "query": "select cs.sale_id, cs.branch_id, b.branch_name, cs.dates, cs.name, cs.mobile_number, cs.product_name, cs.gross_sales, cs.recieved_amount, cs.pending_amount, cs.status from branches as b inner join customer_sales as cs on b.branch_id = cs.branch_id ;"
            },
            "12.Retrieve sales details along with total payment received (using payment_splits)": {
                            "tier": "Join-Based Queries  ",
                            "query": "select cs.* ,sum(ps.amount_paid) as total_payment_recieved from customer_sales as cs inner join payment_splits as ps on cs.sale_id = ps.sale_id  group by cs.sale_id, cs.branch_id, cs.dates, cs.name, cs.mobile_number, cs.product_name, cs.gross_sales,  cs.pending_amount ;"
            },
            "13.Show branch-wise total gross sales (using JOIN & GROUP BY)": {
                        "tier": "Join-Based Queries  ",
                        "query": "select b.branch_id, b.branch_name,  sum(cs.gross_sales) as total_gross_sales from branches as b inner join customer_sales as cs on b.branch_id = cs.branch_id group by b.branch_id, b.branch_name order by total_gross_sales desc;"
            },
            "14.Display sales along with payment method used": {
                        "tier": "Join-Based Queries  ",
                        "query": "select cs.*,ps.payment_method from customer_sales as cs join payment_splits as ps on cs.sale_id = ps.sale_id;"
            },
            "15.Retrieve sales along with branch admin name": {
                        "tier": "Join-Based Queries  ",
                        "query": "select cs.*, b.branch_name,  b.branch_admin_name from customer_sales as cs join branches as b on cs.branch_id = b.branch_id;"
            },
            "16.Find sales where the pending amount is greater than 5000": {
                        "tier": "Financial Tracking Queries   ",
                        "query": "select * from customer_sales where pending_amount > 5000;"
            },
            "17.Retrieve top 3 highest gross sales": {
                        "tier": "Financial Tracking Queries   ",
                        "query": "select * from customer_sales order by gross_sales desc limit 3;"
            },
            "18.Find the branch with highest total gross sales": {
                            "tier": "Financial Tracking Queries   ",
                            "query": "select branch_id , max(gross_sales) as total_gross_sales from customer_sales group  by branch_id  order by total_gross_sales desc limit 1;"
            },
            "19.Retrieve monthly sales summary (group by month & year)": {
                            "tier": "Financial Tracking Queries  ",
                            "query": "select year(dates) as sales_year , month(dates) as sales_month, sum(gross_sales)as Total_Gross_Sales , sum(pending_amount)as Total_Pending_amount , sum(recieved_amount)as Total_Received_Amount from customer_sales group by year(dates), month(dates) order by sales_year , sales_month ;"
            },
            "20.Calculate payment method-wise total collection (Cash / UPI / Card)": {
                            "tier": "Financial Tracking Queries  ",
                            "query": "select payment_method , sum(amount_paid) from payment_splits group by payment_method;"
            }
    }

   # Query question selection
    selected_question = st.selectbox("Choose a predefined query", list(questions.keys()),
                            key="questions",
                            #on_change=update_query
                            )


    # Get selected question details
    question_tier = questions[selected_question]["tier"]
    default_query = questions[selected_question]["query"]

    # Display difficulty tier
    st.markdown(
    f"**Query Classification Tier:** `{question_tier}`"
)
    # Store and display SQL query
    sql_query = default_query
    st.code(sql_query, language="sql")

    #Execution Button
    if st.button("Execute Live Database Transcation", type="primary"):
        cleaned = sql_query.strip().rstrip(";")
        if not cleaned.upper().startswith("SELECT") or ";" in cleaned:
            st.error("Only one SELECT query is allowed here.")
        else:
            try:
                result = read_data(cleaned)
                st.success("Query Executed")
                st.dataframe(result, use_container_width=True, hide_index=True)
                st.caption(f"Rows returned: {len(result)}")
            except Exception as e:
                st.error(f"MySQL error: {e}")

