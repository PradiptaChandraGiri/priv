const { Client } = require('pg');
require('dotenv').config();

const connString = process.env.DATABASE_URL;
const directConnString = connString.replace('-pooler', '');

async function testConn(url, label) {
  console.log(`Testing ${label}...`);
  const client = new Client({
    connectionString: url,
    ssl: { rejectUnauthorized: false }
  });
  try {
    await client.connect();
    console.log(`✅ Success connecting to ${label}!`);
    const res = await client.query('SELECT NOW()');
    console.log(`Time: ${res.rows[0].now}`);
    await client.end();
    return true;
  } catch (err) {
    console.error(`❌ Failed to connect to ${label}:`, err.message);
    return false;
  }
}

async function main() {
  const pooledOk = await testConn(connString, "Pooled Connection String");
  if (!pooledOk) {
    await testConn(directConnString, "Direct (Non-pooled) Connection String");
  }
}

main();
