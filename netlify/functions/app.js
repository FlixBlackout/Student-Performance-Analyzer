const serverless = require('serverless-http');
const express = require('express');
const app = express();

// Serve static files from the public directory
app.use(express.static('public'));

// Redirect all requests to the index.html file
app.get('*', (req, res) => {
  res.sendFile('index.html', { root: './public' });
});

// Export the serverless function
module.exports.handler = serverless(app);
