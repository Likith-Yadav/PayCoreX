# API Testing Status

## Current Issue
- API authentication is failing
- Middleware is running but merchant is not accessible in views
- Error: "Authentication required" from view, not from middleware

## Root Cause
REST Framework wraps the Django request, and `request.merchant` set by middleware on Django request is not accessible via `request._request.merchant` in the view.

## Next Steps
1. Fix middleware to set merchant on both request objects
2. Or create a custom REST Framework authentication class
3. Or access merchant differently in views

## Test Credentials
- API Key: y5XQpcXhxzzGfk5ND3b3iU0Np7HaZWYw_Z4w2b42h64
- Secret: -9iJc1OZXohB4gf3lanGob4M9ypMLFH4FeiyYCEPfKwNIa-dBjrs7Z_XiRqMD3paMgqCVYxH5k3oDDH1saikFQ
