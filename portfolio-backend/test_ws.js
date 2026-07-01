const { Client, neonConfig } = require('@neondatabase/serverless');
const ws = require('ws');
require('dotenv').config();

// Set the webSocketConstructor so it uses the 'ws' package in Node.js
neonConfig.webSocketConstructor = ws;

async function main() {
  console.log("Testing WebSocket Connection to Neon...");
  const client = new Client({
    connectionString: process.env.DATABASE_URL,
  });
  try {
    await client.connect();
    console.log("✅ Success connecting to Neon via WebSockets on port 443!");
    const res = await client.query('SELECT NOW()');
    console.log(`Time from DB: ${res.rows[0].now}`);
    await client.end();
  } catch (err) {
    console.error("❌ Failed to connect via WebSockets:", err.message);
  }
}

main();
