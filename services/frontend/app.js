const express = require('express');
const axios = require('axios');

const app = express();
const PORT = 3000;

// Backend service URL (K8s service name)
const BACKEND_URL = process.env.BACKEND_URL || "http://backend";

// Health check
app.get('/health', (req, res) => {
  res.status(200).send("OK");
});

// Home route
app.get('/', async (req, res) => {
  try {
    const response = await axios.get(`${BACKEND_URL}/api`);
    res.send(`
      <h1>Frontend Service 🚀</h1>
      <p>Backend Response: ${response.data}</p>
    `);
  } catch (error) {
    res.send(`
      <h1>Frontend Service 🚀</h1>
      <p>Backend not reachable ❌</p>
    `);
  }
});

// API proxy
app.get('/api', async (req, res) => {
  try {
    const response = await axios.get(`${BACKEND_URL}/api`);
    res.json(response.data);
  } catch (error) {
    res.status(500).send("Backend error");
  }
});

app.listen(PORT, () => {
  console.log(`Frontend running on port ${PORT}`);
});