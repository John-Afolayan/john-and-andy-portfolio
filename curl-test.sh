curl --request POST http://localhost:5000/api/timeline_post -d 'name=John&email= john@mlh.com &content=Just Added Database to my portfolio site!' {"content":"Just Added Database to my portfolio site!","created_at":"Tuesday, 28 June 2022 03:22:30 EST","email":" john@mlh.com ","id":3,"name":"John"}

curl -X POST http://localhost:5000/api/timeline_post -d 'name=John&email= john@mlh.com &content=Testing my endpoints with postman and curl.' {"content":"Just Added Database to my portfolio site!","created_at":"Tuesday, 28 June 2022 03:22:30 EST","email":" john@mlh.com ","id":3,"name":"John"}

curl --request GET http://localhost:5000/api/timeline_post {{"timeline_posts":[]}
curl http://localhost:5000/api/timeline_post {"timeline_posts":[]}
