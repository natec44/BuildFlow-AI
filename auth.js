const express = require('express');
const jwt = require('express-jwt');
const jwksRsa = require('jwks-rsa');
const cors = require('cors');

const app = express();
app.use(cors());

// Auth0 config
const authConfig = {
  domain: process.env.dev-7d8ppk5jqirxkzaf.us.auth0.com,
  audience: process.env.AUTH0_AUDIENCE,
};

// JWT middleware to validate tokens from Auth0
const checkJwt = jwt({
  secret: jwksRsa.expressJwtSecret({
    cache: true,
    rateLimit: true,
    jwksRequestsPerMinute: 5,
    jwksUri: `https://${authConfig.domain}/.well-known/jwks.json`,
  }),
  audience: authConfig.audience,
  issuer: `https://${authConfig.domain}/`,
  algorithms: ['RS256'],
});

// Example protected route
app.get('/api/protected', checkJwt, (req, res) => {
  res.json({ message: 'You are authenticated!' });
});

app.listen(3001, () => console.log('API listening on 3001'));
