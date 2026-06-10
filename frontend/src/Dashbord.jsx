import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

function Dashboard() {
  const [tasks, setTasks] = useState([]);
  const [form, setForm] = useState({
    title: "",
    description: ""
  });

  const navigate = useNavigate();

  const token = localStorage.getItem("token");
  const username = localStorage.getItem("username");

  useEffect(() => {
    if (!token) {
      navigate("/");
    }
  }, [token, navigate]);

  const fetchTasks = async () => {
    console.log("FETCH TOKEN:", token);

    try {
      const res = await fetch(
        "http://127.0.0.1:8000/api/v1/tasks",
        {
          headers: {
            Authorization: `Bearer ${token}`
          }
        }
      );

      const data = await res.json();

      if (!res.ok) {
        alert(data.detail || "Failed to fetch tasks");
        return;
      }

      setTasks(data.data || []);
    } catch (error) {
      console.error(error);
    }
  };

  useEffect(() => {
    fetchTasks();
  }, []);

  const handleChange = (e) => {
    setForm({
      ...form,
      [e.target.name]: e.target.value
    });
  };

  const addTask = async () => {
    console.log("TOKEN:", token);

    try {
      const res = await fetch(
        "http://127.0.0.1:8000/api/v1/tasks",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`
          },
          body: JSON.stringify({
            title: form.title,
            description: form.description,
            status: false
          })
        }
      );

      const data = await res.json();

      if (!res.ok) {
        alert(data.detail || "Failed to create task");
        return;
      }

      setForm({
        title: "",
        description: ""
      });

      fetchTasks();
    } catch (error) {
      console.error(error);
    }
  };

  const deleteTask = async (id) => {
    try {
      const res = await fetch(
        `http://127.0.0.1:8000/api/v1/tasks/${id}`,
        {
          method: "DELETE",
          headers: {
            Authorization: `Bearer ${token}`
          }
        }
      );

      if (!res.ok) {
        const data = await res.json();
        alert(data.detail);
        return;
      }

      fetchTasks();
    } catch (error) {
      console.error(error);
    }
  };

  const toggleTask = async (task) => {
    try {
      const res = await fetch(
        `http://127.0.0.1:8000/api/v1/tasks/${task.id}`,
        {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`
          },
          body: JSON.stringify({
            title: task.title,
            description: task.description,
            status: !task.status
          })
        }
      );

      if (!res.ok) {
        const data = await res.json();
        alert(data.detail);
        return;
      }

      fetchTasks();
    } catch (error) {
      console.error(error);
    }
  };

  const logout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("username");
    navigate("/");
  };

  return (
    <div style={styles.page}>
      <div style={styles.header}>
        <div>
          <h1>📋 Task Manager</h1>
          <p>Welcome, {username} 👋</p>
        </div>

        <button onClick={logout} style={styles.logout}>
          Logout
        </button>
      </div>

      <div style={styles.card}>
        <h3>Create Task</h3>

        <input
          name="title"
          placeholder="Task Title"
          value={form.title}
          onChange={handleChange}
          style={styles.input}
        />

        <input
          name="description"
          placeholder="Task Description"
          value={form.description}
          onChange={handleChange}
          style={styles.input}
        />

        <button onClick={addTask} style={styles.button}>
          Add Task
        </button>
      </div>

      <h2>Your Tasks</h2>

      {tasks.length === 0 ? (
        <p>No tasks found.</p>
      ) : (
        tasks.map((task) => (
          <div key={task.id} style={styles.task}>
            <h3>{task.title}</h3>

            <p>{task.description}</p>

            <p>
              Status:{" "}
              {task.status ? "✅ Completed" : "⏳ Pending"}
            </p>

            <div style={styles.actions}>
              <button
                onClick={() => toggleTask(task)}
                style={styles.smallButton}
              >
                Toggle Status
              </button>

              <button
                onClick={() => deleteTask(task.id)}
                style={styles.deleteButton}
              >
                Delete
              </button>
            </div>
          </div>
        ))
      )}
    </div>
  );
}

const styles = {
  page: {
    maxWidth: "900px",
    margin: "0 auto",
    padding: "20px",
    fontFamily: "Arial"
  },

  header: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center"
  },

  card: {
    border: "1px solid #ddd",
    borderRadius: "10px",
    padding: "20px",
    marginTop: "20px",
    marginBottom: "20px"
  },

  input: {
    width: "100%",
    padding: "10px",
    marginBottom: "10px",
    boxSizing: "border-box"
  },

  button: {
    padding: "10px 20px",
    cursor: "pointer"
  },

  task: {
    border: "1px solid #ddd",
    borderRadius: "10px",
    padding: "15px",
    marginBottom: "10px"
  },

  actions: {
    display: "flex",
    gap: "10px"
  },

  smallButton: {
    padding: "8px"
  },

  deleteButton: {
    padding: "8px"
  },

  logout: {
    padding: "10px 15px"
  }
};

export default Dashboard;