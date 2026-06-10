const BASE_URL = "http://127.0.0.1:8000/api/v1";

export const getToken = () => localStorage.getItem("token");

// AUTH
export const login = async (data) => {
  return fetch(`${BASE_URL}/users/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data)
  });
};

export const register = async (data) => {
  return fetch(`${BASE_URL}/users/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data)
  });
};

// TASKS (PROTECTED)
export const getTasks = async () => {
  return fetch(`${BASE_URL}/tasks`, {
    headers: {
      Authorization: `Bearer ${getToken()}`
    }
  });
};

export const createTask = async (data) => {
  return fetch(`${BASE_URL}/tasks`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${getToken()}`
    },
    body: JSON.stringify(data)
  });
};

export const deleteTask = async (id) => {
  return fetch(`${BASE_URL}/tasks/${id}`, {
    method: "DELETE",
    headers: {
      Authorization: `Bearer ${getToken()}`
    }
  });
};

export const updateTask = async (id, data) => {
  return fetch(`${BASE_URL}/tasks/${id}`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${getToken()}`
    },
    body: JSON.stringify(data)
  });
};