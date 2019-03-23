To enable Clearbit enrichment and emailhunter verification set env vars:
```bash
export CLEARBIT_ENRICHMENT=1
export CLEARBIT_API_KEY=<your clearbit api key>
export EMAILHUNTER_VALIDATION=1
export EMAILHUNTER_API_KEY=<your emailhunter api key>
```

Quickly test-drive the API using curl:
```bash
curl -X POST -H "Content-Type: application/json" -d '{"username": "steli", "password": "Start123!@#ASD", "email": "steli@close.io"}' http://localhost:8000/api/auth/register/
curl -X POST -H "Content-Type: application/json" -d '{"username": "steli", "password": "Start123!@#ASD"}' http://localhost:8000/api/auth/token/
curl -X POST -H "Content-Type: application/json" -H "Authorization: Bearer <jwt access token from previous request>" -d '{"title": "The Title", "text": "The Text"}' http://localhost:8000/api/posts/
curl -X POST -H "Authorization: Bearer <jwt access token from previous request>" http://localhost:8000/api/posts/1/like/
curl -X POST -H "Authorization: Bearer <jwt access token from previous request>" http://localhost:8000/api/posts/1/unlike/
```
