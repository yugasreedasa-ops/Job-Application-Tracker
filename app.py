import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date

from database import (
    create_table,
    add_application,
    get_applications,
    update_application,
    delete_application
)


# =========================
# DATABASE
# =========================

create_table()


# =========================
# PAGE CONFIGURATION
# =========================

st.set_page_config(
    page_title="Job Application Tracker",
    page_icon="💼",
    layout="wide"
)


# =========================
# HEADER
# =========================

st.title("💼 Job Application Tracker")

st.markdown(
    "### Track your job search from application to selection."
)

st.caption(
    "Manage applications, monitor progress, and analyze your job search activity."
)


# =========================
# SIDEBAR
# =========================

st.sidebar.title("💼 Job Tracker")

st.sidebar.write(
    "Manage your job applications and track your career progress."
)

st.sidebar.divider()

menu = st.sidebar.radio(
    "Select an option",
    [
        "Dashboard",
        "Add Application",
        "View Applications"
    ]
)


# =========================================================
# DASHBOARD
# =========================================================

if menu == "Dashboard":

    st.header("📊 Dashboard")

    applications = get_applications()

    if applications:

        df = pd.DataFrame(
            applications,
            columns=[
                "ID",
                "Company",
                "Job Role",
                "Application Date",
                "Status",
                "Job Link",
                "Notes"
            ]
        )

        df["Application Date"] = pd.to_datetime(
            df["Application Date"]
        )

        # =========================
        # METRICS
        # =========================

        total = len(df)

        applied = len(
            df[df["Status"] == "Applied"]
        )

        interview = len(
            df[df["Status"] == "Interview"]
        )

        selected = len(
            df[df["Status"] == "Selected"]
        )

        rejected = len(
            df[df["Status"] == "Rejected"]
        )

        if total > 0:
            interview_rate = (
                interview / total
            ) * 100
        else:
            interview_rate = 0

        col1, col2, col3, col4, col5 = st.columns(5)

        col1.metric(
            "Total Applications",
            total
        )

        col2.metric(
            "Applied",
            applied
        )

        col3.metric(
            "Interviews",
            interview
        )

        col4.metric(
            "Selected",
            selected
        )

        col5.metric(
            "Rejected",
            rejected
        )

        st.metric(
            "Interview Conversion Rate",
            f"{interview_rate:.1f}%"
        )

        st.divider()

        # =========================
        # ANALYTICS
        # =========================

        st.subheader("📈 Application Analytics")

        col1, col2 = st.columns(2)

        # =========================
        # PIE CHART
        # =========================

        with col1:

            status_counts = (
                df["Status"]
                .value_counts()
                .reset_index()
            )

            status_counts.columns = [
                "Status",
                "Count"
            ]

            fig = px.pie(
                status_counts,
                names="Status",
                values="Count",
                title="Applications by Status",
                hole=0.4
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        # =========================
        # MONTHLY APPLICATIONS
        # =========================

        with col2:

            monthly_data = (
                df.groupby(
                    df["Application Date"].dt.to_period("M")
                )
                .size()
                .reset_index(
                    name="Applications"
                )
            )

            monthly_data["Application Date"] = (
                monthly_data["Application Date"]
                .astype(str)
            )

            fig = px.line(
                monthly_data,
                x="Application Date",
                y="Applications",
                markers=True,
                title="Monthly Applications"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        # =========================
        # RECENT APPLICATIONS
        # =========================

        st.subheader("📋 Recent Applications")

        recent_df = (
            df.sort_values(
                "Application Date",
                ascending=False
            )
            .head(10)
        )

        st.dataframe(
            recent_df[
                [
                    "Company",
                    "Job Role",
                    "Application Date",
                    "Status"
                ]
            ],
            use_container_width=True
        )

    else:

        st.info(
            "No applications added yet."
        )

        st.write(
            "Go to **Add Application** from the sidebar "
            "to add your first application."
        )


# =========================================================
# ADD APPLICATION
# =========================================================

elif menu == "Add Application":

    st.header("➕ Add Job Application")

    with st.form("application_form"):

        company = st.text_input(
            "Company Name",
            placeholder="Example: TCS"
        )

        job_role = st.text_input(
            "Job Role",
            placeholder="Example: Python Developer"
        )

        application_date = st.date_input(
            "Application Date",
            value=date.today()
        )

        status = st.selectbox(
            "Application Status",
            [
                "Applied",
                "Interview",
                "Selected",
                "Rejected"
            ]
        )

        job_link = st.text_input(
            "Job Link",
            placeholder="https://example.com/job"
        )

        notes = st.text_area(
            "Notes",
            placeholder="Add any additional information..."
        )

        submitted = st.form_submit_button(
            "➕ Add Application"
        )

        if submitted:

            if (
                company.strip() == ""
                or job_role.strip() == ""
            ):

                st.error(
                    "Please enter both Company Name "
                    "and Job Role."
                )

            else:

                add_application(
                    company,
                    job_role,
                    str(application_date),
                    status,
                    job_link,
                    notes
                )

                st.success(
                    "Application added successfully!"
                )

                st.rerun()


# =========================================================
# VIEW APPLICATIONS
# =========================================================

elif menu == "View Applications":

    st.header("📋 Manage Applications")

    applications = get_applications()

    if applications:

        df = pd.DataFrame(
            applications,
            columns=[
                "ID",
                "Company",
                "Job Role",
                "Application Date",
                "Status",
                "Job Link",
                "Notes"
            ]
        )

        # =========================
        # SEARCH AND FILTER
        # =========================

        col1, col2 = st.columns(2)

        with col1:

            search = st.text_input(
                "🔍 Search by Company or Job Role",
                placeholder="Search..."
            )

        with col2:

            filter_status = st.selectbox(
                "📌 Filter by Status",
                [
                    "All",
                    "Applied",
                    "Interview",
                    "Selected",
                    "Rejected"
                ]
            )

        filtered_df = df.copy()

        # Search
        if search:

            filtered_df = filtered_df[
                filtered_df["Company"].str.contains(
                    search,
                    case=False,
                    na=False
                )
                |
                filtered_df["Job Role"].str.contains(
                    search,
                    case=False,
                    na=False
                )
            ]

        # Status filter
        if filter_status != "All":

            filtered_df = filtered_df[
                filtered_df["Status"] == filter_status
            ]

        st.divider()

        # =========================
        # APPLICATION TABLE
        # =========================

        st.subheader("📄 Applications")

        st.dataframe(
            filtered_df,
            column_config={
                "Job Link": st.column_config.LinkColumn(
                    "Job Link",
                    display_text="Open Job"
                )
            },
            use_container_width=True,
            hide_index=True
        )

        # =========================
        # EDIT APPLICATION
        # =========================

        st.divider()

        st.subheader("✏️ Edit Application")

        if not filtered_df.empty:

            edit_id = st.selectbox(
                "Select Application to Edit",
                filtered_df["ID"].tolist()
            )

            selected_application = filtered_df[
                filtered_df["ID"] == edit_id
            ].iloc[0]

            status_options = [
                "Applied",
                "Interview",
                "Selected",
                "Rejected"
            ]

            current_status = (
                selected_application["Status"]
            )

            if current_status in status_options:

                current_status_index = (
                    status_options.index(
                        current_status
                    )
                )

            else:

                current_status_index = 0

            with st.form("edit_application_form"):

                edit_company = st.text_input(
                    "Company Name",
                    value=selected_application[
                        "Company"
                    ]
                )

                edit_job_role = st.text_input(
                    "Job Role",
                    value=selected_application[
                        "Job Role"
                    ]
                )

                edit_date = st.date_input(
                    "Application Date",
                    value=pd.to_datetime(
                        selected_application[
                            "Application Date"
                        ]
                    ).date()
                )

                edit_status = st.selectbox(
                    "Application Status",
                    status_options,
                    index=current_status_index
                )

                edit_job_link = st.text_input(
                    "Job Link",
                    value=(
                        str(
                            selected_application[
                                "Job Link"
                            ]
                        )
                        if pd.notna(
                            selected_application[
                                "Job Link"
                            ]
                        )
                        else ""
                    )
                )

                edit_notes = st.text_area(
                    "Notes",
                    value=(
                        str(
                            selected_application[
                                "Notes"
                            ]
                        )
                        if pd.notna(
                            selected_application[
                                "Notes"
                            ]
                        )
                        else ""
                    )
                )

                update_button = st.form_submit_button(
                    "💾 Update Application"
                )

                if update_button:

                    if (
                        edit_company.strip() == ""
                        or edit_job_role.strip() == ""
                    ):

                        st.error(
                            "Company Name and Job Role "
                            "cannot be empty."
                        )

                    else:

                        update_application(
                            edit_id,
                            edit_company,
                            edit_job_role,
                            str(edit_date),
                            edit_status,
                            edit_job_link,
                            edit_notes
                        )

                        st.success(
                            "Application updated successfully!"
                        )

                        st.rerun()

        else:

            st.warning(
                "No application matches your search."
            )

        # =========================
        # DELETE APPLICATION
        # =========================

        st.divider()

        st.subheader("🗑️ Delete Application")

        application_ids = (
            filtered_df["ID"].tolist()
        )

        if application_ids:

            selected_id = st.selectbox(
                "Select Application ID to Delete",
                application_ids
            )

            if st.button(
                "🗑️ Delete Application"
            ):

                delete_application(
                    selected_id
                )

                st.success(
                    "Application deleted successfully!"
                )

                st.rerun()

        # =========================
        # DOWNLOAD CSV
        # =========================

        st.divider()

        st.subheader("📥 Export Applications")

        csv = filtered_df.to_csv(
            index=False
        )

        st.download_button(
            label="📥 Download Applications CSV",
            data=csv,
            file_name="job_applications.csv",
            mime="text/csv"
        )

    else:

        st.info(
            "No applications available."
        )

        st.write(
            "Go to **Add Application** to create your first record."
        )