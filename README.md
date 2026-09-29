# 💼 Job Application Tracker

A web-based Job Application Tracker built using Python and Streamlit to help users manage, monitor, and analyze their job applications in one place.

The application uses SQLite for data storage and provides an interactive dashboard with application statistics, status tracking, monthly trends, search, filtering, editing, deletion, and CSV export functionality.

---

## 🚀 Live Demo

🔗 **Live Demo:**  
Coming soon

---

## 📌 Project Overview

Managing multiple job applications can become difficult when application details are stored across different documents or platforms.

The Job Application Tracker provides a centralized dashboard where users can:

- Add job applications
- Track application status
- Edit application details
- Delete applications
- Search applications
- Filter applications by status
- Open job links directly
- View application statistics
- Analyze monthly application trends
- Export application data as CSV

---

## ✨ Features

### 📊 Interactive Dashboard

The dashboard provides an overview of the job search activity with:

- Total Applications
- Applied Applications
- Interviews
- Selected Applications
- Rejected Applications
- Interview Conversion Rate

### 📈 Data Visualization

Interactive Plotly charts are used to visualize:

- Applications by Status
- Monthly Application Trends

### ➕ Add Applications

Users can add:

- Company Name
- Job Role
- Application Date
- Application Status
- Job Link
- Notes

### ✏️ Edit Applications

Existing application details can be updated, including:

- Company
- Job Role
- Application Date
- Status
- Job Link
- Notes

### 🗑️ Delete Applications

Users can remove applications that are no longer required.

### 🔍 Search and Filter

Applications can be searched by:

- Company Name
- Job Role

Applications can also be filtered by:

- Applied
- Interview
- Selected
- Rejected

### 🔗 Job Link Management

Job links are displayed as clickable links, allowing users to open the original job posting directly from the application table.

### 📥 CSV Export

Filtered application data can be downloaded as a CSV file for further analysis or backup.

### 💾 SQLite Database

Application data is stored locally using SQLite, providing persistent data storage without requiring an external database server.

---

## 🛠️ Technologies Used

| Technology | Purpose |
|------------|---------|
| Python | Application development |
| Streamlit | Web application and user interface |
| SQLite | Database and data storage |
| Pandas | Data processing and analysis |
| Plotly | Interactive data visualization |
| Git | Version control |
| GitHub | Source code hosting |
| Streamlit Cloud | Application deployment |

---

## 🏗️ Project Structure

```text
Job-Application-Tracker/
│
├── app.py
├── database.py
├── requirements.txt
├── .gitignore
├── README.md
│
└── venv/
