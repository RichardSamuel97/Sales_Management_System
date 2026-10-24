<h1 align="center">  Sales Management System</h1>

<p align="center">
  <strong>A Multi-Branch Sales Management & Business Analytics Platform</strong>
  <br>
  <em>Streamline sales operations, track payments, and monitor financial performance.</em>
</p>

---


<p align="center">
  <strong>Built with Python • Streamlit • MySQL • Pandas</strong>
  <br>
  <sub>Sales Management System | Project Documentation & Business Analytics</sub>
</p>

---

## 🎯 Project Objective

To develop a centralized and secure platform for managing multi-branch sales operations, improving payment visibility, monitoring financial performance, and supporting data-driven business decisions.



## 📄 Project Documentation

<p align="center">
  <a href="./Sales_Management_System_Project_Documentation.pdf">
    <img src="https://img.shields.io/badge/📘_Read_Project_Documentation-Download_or_View_PDF-1F6FEB?style=for-the-badge" alt="View Project Documentation">
  </a>
</p>

Explore the complete technical documentation covering the application architecture, login module, role-based access control, database design, dashboard features, testing requirements, and deployment pipeline.

---

## 📌 Project Overview

The **Sales Management System** is a centralized, multi-branch business management and analytics application built using Python, Streamlit, MySQL, and Pandas. It simplifies sales entry, customer record management, payment tracking, and financial reporting through an interactive dashboard.

The application implements **Role-Based Access Control (RBAC)**, providing organization-wide access to the Super Admin while restricting Admin users to their assigned branches.

## ✨ Key Features

- 🔐 **Role-Based Authentication** — Separate permissions for Super Admin and branch Admin users.
- 🧾 **Sales Management** — Create and manage customer sales records.
- 💳 **Payment Tracking** — Record payment splits and monitor outstanding balances.
- 📊 **Interactive Dashboard** — Monitor sales performance and financial KPIs.
- 🏢 **Branch-Wise Analytics** — Analyze branch performance within authorized access.
- 💰 **Financial Reporting** — Track gross sales, received amounts, pending collections, and collection percentages.
- 🗄️ **SQL Analytics Engine** — Execute predefined SQL queries for business insights.
- 🛡️ **Data Security** — Enforce branch-level restrictions and secure database configuration.

## 🛠️ Technology Stack

<table align="center">
  <thead>
    <tr>
      <th>Technology</th>
      <th>Role in the Project</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>🐍 <strong>Python</strong></td>
      <td>Application logic and data processing</td>
    </tr>
    <tr>
      <td>🎈 <strong>Streamlit</strong></td>
      <td>Interactive dashboard and user interface</td>
    </tr>
    <tr>
      <td>🐬 <strong>MySQL</strong></td>
      <td>Relational database and data storage</td>
    </tr>
    <tr>
      <td>🐼 <strong>Pandas</strong></td>
      <td>Data manipulation and analytical operations</td>
    </tr>
    <tr>
      <td>🔌 <strong>mysql.connector</strong></td>
      <td>Python-to-MySQL database connectivity</td>
    </tr>
    <tr>
      <td>🗃️ <strong>SQL</strong></td>
      <td>Data retrieval, filtering, and business analytics</td>
    </tr>
  </tbody>
</table>


## 👥 User Roles & Access

<table align="center">
  <thead>
    <tr>
      <th>Capability</th>
      <th>Super Admin</th>
      <th>Branch Admin</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>View all branch records</td>
      <td align="center">✅</td>
      <td align="center">❌</td>
    </tr>
    <tr>
      <td>Create sales entries</td>
      <td align="center">✅</td>
      <td align="center">Assigned branch only</td>
    </tr>
    <tr>
      <td>Manage payment records</td>
      <td align="center">Authorized access</td>
      <td align="center">Assigned branch only</td>
    </tr>
    <tr>
      <td>View financial KPIs</td>
      <td align="center">All branches</td>
      <td align="center">Assigned branch</td>
    </tr>
    <tr>
      <td>Compare branch performance</td>
      <td align="center">✅</td>
      <td align="center">❌</td>
    </tr>
    <tr>
      <td>Access SQL analytics</td>
      <td align="center">Authorized queries</td>
      <td align="center">Restricted queries</td>
    </tr>
  </tbody>
</table>

