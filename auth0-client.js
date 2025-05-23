import { Auth0Client } from "@auth0/auth0-spa-js";

const auth0 = new Auth0Client({
  domain: "dev-7d8ppk5jqirxkzaf.us.auth0.com",
  client_id: "AONRosAUU7BNmT2Z8Db14pySGRxCAJ8y",
  redirect_uri: window.location.origin,
  audience: "YOUR_AUDIENCE", // Optional, for API access
});

// To login (shows all enabled providers)
await auth0.loginWithRedirect();

// To get the user's token
const token = await auth0.getTokenSilently();
