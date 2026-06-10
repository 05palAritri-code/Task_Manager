
import { useEffect, useState } from "react";

function App() {
  const [page, setPage] = useState("auth"); // auth | dashboard
  const [isLogin, setIsLogin] = useState(false);

  const [form, setForm] = useState({
    username: "",
    password: ""
  });

  const [tasks, setTasks] = useState([]);
  const [taskForm, setTaskForm] = useState({
    title: "",
    description: ""
  });

  const [loading, setLoading] = useState(false);

  // ---------------- INPUT HANDLERS ----------------

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleTaskChange = (e) => {
    setTaskForm({ ...taskForm, [e.target.name]: e.target.value });
  };

  // ---------------- AUTH ----------------

  const handleAuth = async (e) => {
    e.preventDefault();
    setLoading(true);

    const url = isLogin
      ? "http://127.0.0.1:8000/api/v1/users/login"
      : "http://127.0.0.1:8000/api/v1/users/register";

    try {
      const res = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(form)
      });

      const data = await res.json();
      if (!res.ok) {
  alert(data.detail || data.message);
  return;
}

localStorage.setItem("token", data.data.token);
localStorage.setItem("username", data.data.username);

setPage("dashboard");

      if (!res.ok) {
        alert(data.detail || data.message || "Auth failed");
        return;
      }

      // ✅ FIXED TOKEN HANDLING (backend might return token directly OR inside data)
      const token = data?.data?.token || data?.token;

      if (token) {
        localStorage.setItem("token", token);
      }

      alert(data.message || "Success");

      setPage("dashboard");

      // load tasks after login
      fetchTasks();

    } catch (err) {
      console.error(err);
      alert("Server error");
    } finally {
      setLoading(false);
    }
  };

  // ---------------- TASKS ----------------

  const fetchTasks = async () => {
    try {
      const res = await fetch("http://127.0.0.1:8000/api/v1/tasks");
      const data = await res.json();

      setTasks(data.data || []);
    } catch (err) {
      console.error(err);
    }
  };

  const addTask = async () => {
    if (!taskForm.title || !taskForm.description) {
      alert("Fill all fields");
      return;
    }

    const res = await fetch("http://127.0.0.1:8000/api/v1/tasks", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        title: taskForm.title,
        description: taskForm.description,
        status: false
      })
    });

    const data = await res.json();

    if (!res.ok) {
      alert(data.detail || "Failed to add task");
      return;
    }

    setTaskForm({ title: "", description: "" });
    fetchTasks();
  };

  const deleteTask = async (id) => {
    await fetch(`http://127.0.0.1:8000/api/v1/tasks/${id}`, {
      method: "DELETE"
    });

    fetchTasks();
  };

  const toggleStatus = async (task) => {
    await fetch(`http://127.0.0.1:8000/api/v1/tasks/${task.id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        title: task.title,
        description: task.description,
        status: !task.status
      })
    });

    fetchTasks();
  };

  const logout = () => {
    localStorage.removeItem("token");
    setPage("auth");
    setForm({ username: "", password: "" });
    setTasks([]);
  };

  // ---------------- DASHBOARD ----------------

  if (page === "dashboard") {
    return (
      <div style={styles.dashboard}>
        <h1 style={styles.heading}>📋 Task Dashboard</h1>

        {/* ADD TASK */}
        <div style={styles.card}>
          <h3>Add Task</h3>

          <input
            name="title"
            placeholder="Title"
            value={taskForm.title}
            onChange={handleTaskChange}
            style={styles.input}
          />

          <input
            name="description"
            placeholder="Description"
            value={taskForm.description}
            onChange={handleTaskChange}
            style={styles.input}
          />

          <button onClick={addTask} style={styles.primaryBtn}>
            + Add Task
          </button>
        </div>

        {/* TASK LIST */}
        <div style={styles.list}>
          {tasks.length === 0 ? (
            <p style={{ color: "#777" }}>No tasks yet</p>
          ) : (
            tasks.map((task) => (
              <div key={task.id} style={styles.taskCard}>
                <div>
                  <h3 style={{ margin: 0 }}>{task.title}</h3>
                  <p style={{ margin: "5px 0", color: "#666" }}>
                    {task.description}
                  </p>
                  <small>
                    Status: {task.status ? "✅ Done" : "⏳ Pending"}
                  </small>
                </div>

                <div style={styles.actions}>
                  <button
                    onClick={() => toggleStatus(task)}
                    style={styles.smallBtn}
                  >
                    Toggle
                  </button>

                  <button
                    onClick={() => deleteTask(task.id)}
                    style={styles.deleteBtn}
                  >
                    Delete
                  </button>
                </div>
              </div>
            ))
          )}
        </div>

        <button onClick={logout} style={styles.logout}>
          Logout
        </button>
      </div>
    );
  }

  // ---------------- AUTH ----------------

  return (
    <div style={styles.page}>
      <div style={styles.card}>
        <h2>{isLogin ? "Login" : "Register"}</h2>

        <form onSubmit={handleAuth} style={styles.form}>
          <input
            name="username"
            placeholder="Username"
            value={form.username}
            onChange={handleChange}
            style={styles.input}
          />

          <input
            name="password"
            type="password"
            placeholder="Password"
            value={form.password}
            onChange={handleChange}
            style={styles.input}
          />

          <button type="submit" style={styles.primaryBtn}>
            {loading ? "Loading..." : isLogin ? "Login" : "Register"}
          </button>
        </form>

        <p onClick={() => setIsLogin(!isLogin)} style={styles.switch}>
          {isLogin ? "Create account" : "Already have account?"}
        </p>
      </div>
    </div>
  );
}

// ---------------- STYLES ----------------

const styles = {
  page: {
    height: "100vh",
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    background: "linear-gradient(135deg, #667eea, #764ba2)",
    fontFamily: "Arial"
  },

  dashboard: {
    padding: 25,
    fontFamily: "Arial",
    background: "#f4f6f8",
    minHeight: "100vh"
  },

  heading: {
    marginBottom: 20
  },

  card: {
    background: "white",
    padding: 15,
    borderRadius: 10,
    boxShadow: "0 2px 8px rgba(0,0,0,0.1)",
    marginBottom: 20,
    maxWidth: 400
  },

  list: {
    maxWidth: 600
  },

  taskCard: {
    background: "white",
    padding: 15,
    borderRadius: 10,
    marginBottom: 10,
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    boxShadow: "0 2px 6px rgba(0,0,0,0.08)"
  },

  input: {
    display: "block",
    width: "100%",
    margin: "8px 0",
    padding: 10,
    borderRadius: 6,
    border: "1px solid #ccc"
  },

  primaryBtn: {
    padding: "10px",
    width: "100%",
    background: "#667eea",
    color: "white",
    border: "none",
    borderRadius: 6,
    cursor: "pointer",
    marginTop: 10
  },

  smallBtn: {
    padding: "6px 10px",
    border: "none",
    borderRadius: 5,
    cursor: "pointer",
    background: "#eee"
  },

  deleteBtn: {
    padding: "6px 10px",
    border: "none",
    borderRadius: 5,
    cursor: "pointer",
    background: "#ff4d4d",
    color: "white"
  },

  logout: {
    marginTop: 20,
    padding: 10,
    background: "black",
    color: "white",
    border: "none",
    borderRadius: 6,
    cursor: "pointer"
  },

  switch: {
    cursor: "pointer",
    color: "#555"
  }
};

export default App;