import React, { useState, useEffect } from "react";
import "./App.css";

function App() {
  const [users, setUsers] = useState([]);
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [message, setMessage] = useState("");

  const API_URL = "http://16.171.233.75:5000/api/users"; // your Flask backend

  // Fetch all users
  const fetchUsers = async () => {
    try {
      const response = await fetch(API_URL);
      if (!response.ok) throw new Error("Failed to fetch users");
      const data = await response.json();
      setUsers(data);
    } catch (err) {
      console.error(err);
      setMessage("Error fetching users.");
    }
  };

  // Add new user
  const addUser = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, email }),
      });
      if (!response.ok) throw new Error("Failed to add user");
      setMessage("User added successfully!");
      setName("");
      setEmail("");
      fetchUsers(); // refresh list
    } catch (err) {
      console.error(err);
      setMessage("Error adding user.");
    }
  };

  // Load users on page load
  useEffect(() => {
    fetchUsers();
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <h2>User Management</h2>

        <form onSubmit={addUser} style={{ marginBottom: "20px" }}>
          <input
            type="text"
            placeholder="Name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
            style={{ marginRight: "10px" }}
          />
          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            style={{ marginRight: "10px" }}
          />
          <button type="submit">Add User</button>
        </form>

        {message && <p>{message}</p>}

        <h3>User List</h3>
        <ul>
          {users.length > 0 ? (
            users.map((u, i) => (
              <li key={i}>
                {u.name} - {u.email}
              </li>
            ))
          ) : (
            <p>No users found.</p>
          )}
        </ul>
      </header>
    </div>
  );
}

export default App;