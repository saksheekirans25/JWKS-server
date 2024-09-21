**JWKS Server**

This is a simple JWKS (JSON Web Key Set) server that generates and serves public keys with expiry and unique kid to verify JWTs. 
It supports issuing JWTs to authenticated users and handling requests for expired keys.

Features:
1. Serve RSA public keys through the .well-known/jwks.json endpoint.
2. Authenticate users via /auth endpoint.
3. Issue JWT tokens with an optional "expired" key.
