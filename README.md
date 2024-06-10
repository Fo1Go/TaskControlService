tech stack:<br>
drf, django, postgresql<br>
JWT-based token authentication<br>
Docker-compose application launch<br>
<h2>Models</h2>
User:
<ul>
<li>first_name</li>
<li>last_name</li>
<li>surname</li>
<li>email</li>
<li>phone_number</li>
<li>is_staff</li>
<li>is_active</li>
<li>date_joined </li>
<li>groups</li>
</ul>
Task:
<ul>
<li>task_goal</li>
<li>status</li>
<li>report</li>
<li>date_created</li>
<li>date_updated</li>
<li>date_closed</li>
<li>employer</li>
<li>customer</li>
</ul>


<h2>Endpoints</h2>
<ul>
<li>GET, POST host/admin</li>
<li>GET, POST host/api/v1/tasks</li>
<li>GET, POST, PATCH, PUT host/api/v1/tasks/{pk}</li>
<li>POST host/api/v1/tasks/{pk}/close</li>
<li>GET host/api/v1/employers</li>
<li>GET, POST host/api/v1/users</li>
<li>GET host/api/v1/users/{pk}</li>
<li>GET host/api/v1/me</li>
<li>GET host/api/v1/me/tasks</li>
<li>POST host/api/v1/token</li>
<li>POST host/api/v1/refresh</li>
</ul>
