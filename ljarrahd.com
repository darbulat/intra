upstream channels-backend {
    server localhost:8000;
}

server {
	listen 80 default_server;
	listen [::]:80 default_server;

    charset  utf-8;
    # max upload size
    client_max_body_size 512M;   # adjust to taste

    location / {
        try_files $uri @proxy_to_app;
    }

    location @proxy_to_app {
        proxy_pass http://channels-backend;

        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";

        proxy_redirect off;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Host $server_name;
    }

    location /static {
        alias /project/rush01/static;
    }
    location /media {
        alias /project/rush01/media;
    }
    # disable all robots
    location /robots.txt {
        return 200 "User-agent: *\nDisallow: /";

    }
}

