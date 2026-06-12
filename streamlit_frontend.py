import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()

api_url = os.getenv("API_URL")
# st.write("API_URL =", api_url)
# if st.button("Get Tasks"):
#     res = requests.get(f"{API_URL}/tasks")
#     st.write(res.json())
# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "token" not in st.session_state:
    st.session_state.token = None

if "username" not in st.session_state:
    st.session_state.username = None

# --------------------------------------------------
# AUTH PAGE
# --------------------------------------------------

if not st.session_state.token:

    st.title("Task Manager")

    auth_type = st.radio(
        "Select",
        ["Login", "Register"]
    )

    username = st.text_input("Username")
    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button(auth_type):

        endpoint = (
            f"{api_url}/users/login"
            if auth_type == "Login"
            else f"{api_url}/users/register"
        )

        payload = {
            "username": username,
            "password": password
        }

        response = requests.post(
            endpoint,
            json=payload
        )
        # st.write("Endpoint:", endpoint)
        # st.write("Status Code:", response.status_code)
        # st.write("Response Text:", response.text)
        try:
            data = response.json()
        except Exception:
            st.error(response.text)
            st.stop()

       
        data = response.json()

        if response.status_code in [200, 201]:

            if auth_type == "Login":
                st.session_state.token = data["data"]["token"]
                st.session_state.username = data["data"]["username"]
                st.rerun()

            else:
                st.success("Registration successful")

        else:
            st.error(data.get("detail", "Something went wrong"))

# --------------------------------------------------
# DASHBOARD
# --------------------------------------------------

else:

    st.title("Task Dashboard")

    st.write(
        f"Welcome **{st.session_state.username}** "
    )

    headers = {
        "Authorization": f"Bearer {st.session_state.token}"
    }

    # ---------------- CREATE TASK ----------------

    st.subheader("Create Task")

    title = st.text_input("Title")
    description = st.text_area("Description")

    if st.button("Add Task"):

        if not title.strip():
            st.warning("Please enter a task title")
            st.stop()

        if len(title.strip()) < 3:
            st.warning("Title must be at least 3 characters")
            st.stop()

        if len(description.strip()) < 5:
            st.warning("Description must be at least 5 characters")
            st.stop()

        payload = {
            "title": title,
            "description": description,
            "status": False
        }

        response = requests.post(
            f"{api_url}/tasks",
            json=payload,
            headers=headers
        )

    # if st.button("Add Task"):

    #     payload = {
    #         "title": title,
    #         "description": description,
    #         "status": False
    #     }

    #     response = requests.post(
    #         f"{api_url}/tasks",
    #         json=payload,
    #         headers=headers
    #     )

    #     if response.status_code == 201:
    #         st.success("Task created")
    #         st.rerun()

    #     else:
    #         try:
    #             message = response.json().get("detail")
    #             st.error(message)
    #         except Exception:
    #             st.error("Unexpected server error")

    # ---------------- GET TASKS ----------------

    response = requests.get(
        f"{api_url}/tasks",
        headers=headers
    )

    if response.status_code == 200:

        tasks = response.json()["data"]

        st.subheader("My Tasks")

        if not tasks:
            st.info("No tasks found")

        for task in tasks:

            with st.container():

                st.write(f"### {task['title']} , id : {task['id']}")
                st.write(task["description"])

                st.write(
                    "✅ Completed"
                    if task["status"]
                    else "⏳ Pending"
                )

                col1, col2 = st.columns(2)

                # Toggle Status
                with col1:

                    if st.button(
                        f"id:{task['id']} Status"
                    ):

                        requests.put(
                            f"{api_url}/tasks/{task['id']}",
                            json={
                                "title": task["title"],
                                "description": task["description"],
                                "status": not task["status"]
                            },
                            headers=headers
                        )

                        st.rerun()

                # Delete
                with col2:

                    if st.button(
                        f"id:{task['id']} Delete"
                    ):

                        requests.delete(
                            f"{api_url}/tasks/{task['id']}",
                            headers=headers
                        )

                        st.rerun()

                st.divider()

    # ---------------- LOGOUT ----------------

    if st.button("Logout"):
        st.session_state.token = None
        st.session_state.username = None
        st.rerun()