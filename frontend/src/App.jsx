import { useState } from "react";

function App() {
  const [form, setForm] = useState({
    username: "",
    password: ""
  });

  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const res = await fetch(
        "http://127.0.0.1:8000/api/v1/users/register",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify(form)
        }
      );

      const data = await res.json();
      console.log("Response:", data);

      alert(data?.message || "User registered successfully ✔");

      setForm({ username: "", password: "" });
    } catch (error) {
      console.error(error);
      alert("Something went wrong ❌");
    }

    setLoading(false);
  };

  return (
    <div style={styles.page}>
      <div style={styles.card}>
        <h2 style={styles.title}>Welcome 👋</h2>
        <p style={styles.sub}>Register your account</p>

        <form onSubmit={handleSubmit} style={styles.form}>
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

          <button type="submit" style={styles.button} disabled={loading}>
            {loading ? "Registering..." : "Register"}
          </button>
        </form>
      </div>
    </div>
  );
}

const styles = {
  page: {
    height: "100vh",
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    background: "linear-gradient(135deg, #667eea, #764ba2)",
    fontFamily: "Arial"
  },
  card: {
    width: "320px",
    padding: "25px",
    borderRadius: "12px",
    background: "white",
    boxShadow: "0 10px 25px rgba(0,0,0,0.2)",
    textAlign: "center"
  },
  title: {
    margin: 0,
    fontSize: "22px"
  },
  sub: {
    fontSize: "12px",
    color: "gray",
    marginBottom: "20px"
  },
  form: {
    display: "flex",
    flexDirection: "column",
    gap: "12px"
  },
  input: {
    padding: "10px",
    borderRadius: "6px",
    border: "1px solid #ccc",
    outline: "none"
  },
  button: {
    padding: "10px",
    background: "#667eea",
    color: "white",
    border: "none",
    borderRadius: "6px",
    cursor: "pointer"
  }
};

export default App;