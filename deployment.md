# DigitalOcean Deployment Guide for `digitalocean_django`

This documents exactly what was done to deploy the app to an Ubuntu Droplet at `138.197.46.186`. Adapt hostnames/IPs as needed.

## 1) Base server setup
- Created/used Ubuntu 22.04 Droplet.
- SSH in as root: `ssh root@138.197.46.186`.
- Installed system packages:
  - `apt update`
  - `apt install -y python3-venv python3-pip python3-dev build-essential nginx git`

## 2) Fetch project code
- Target directory: `/opt/helloworld`
- Clone repository:
  - `git clone https://github.com/mohdazlanabas/digitalocean_django /opt/helloworld`

## 3) Python virtual environment and dependencies
- Create venv: `cd /opt/helloworld && python3 -m venv .venv`
- Install packages inside venv:
  - `.venv/bin/pip install --upgrade pip`
  - `.venv/bin/pip install django gunicorn`

## 4) Django production settings
- File: `helloworld_project/settings.py`
- Changes made:
  - `DEBUG = False`
  - `ALLOWED_HOSTS = ['138.197.46.186', 'localhost']`
  - Added static root: `STATIC_ROOT = BASE_DIR / 'staticfiles'`
- Database: default SQLite (`db.sqlite3`).
- Apply migrations: `.venv/bin/python manage.py migrate`
- Collect static: `.venv/bin/python manage.py collectstatic --noinput`

## 5) Gunicorn service (systemd)
- Service file: `/etc/systemd/system/helloworld.service`
```
[Unit]
Description=Gunicorn daemon for Django HelloWorld
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/opt/helloworld
Environment="PATH=/opt/helloworld/.venv/bin"
ExecStart=/opt/helloworld/.venv/bin/gunicorn --workers 3 --bind unix:/opt/helloworld/helloworld.sock helloworld_project.wsgi:application
Restart=on-failure

[Install]
WantedBy=multi-user.target
```
- Ownership for app dir/socket: `chown -R www-data:www-data /opt/helloworld`
- Enable and start:
  - `systemctl daemon-reload`
  - `systemctl enable helloworld`
  - `systemctl start helloworld`
  - Check: `systemctl status helloworld`

## 6) Nginx reverse proxy
- Site config: `/etc/nginx/sites-available/helloworld`
```
server {
    listen 80;
    server_name 138.197.46.186;

    location / {
        include proxy_params;
        proxy_pass http://unix:/opt/helloworld/helloworld.sock;
    }
}
```
- Enable site and disable default:
  - `ln -sf /etc/nginx/sites-available/helloworld /etc/nginx/sites-enabled/helloworld`
  - `rm /etc/nginx/sites-enabled/default` (if present)
- Test and reload Nginx:
  - `nginx -t`
  - `systemctl reload nginx`

## 7) Smoke test
- `curl -I http://138.197.46.186` → `200 OK`
- Browser: visit `http://138.197.46.186/` to see the Hello World page.

## 8) Managing the app
- Restart after code changes: `systemctl restart helloworld`
- Follow logs: `journalctl -u helloworld -f`
- Check Nginx logs: `/var/log/nginx/access.log` and `/var/log/nginx/error.log`

## 9) Optional: HTTPS with Certbot (needs a domain)
- Point a domain to the Droplet IP via DNS A record.
- Install Certbot: `apt install -y certbot python3-certbot-nginx`
- Issue certificates: `certbot --nginx -d yourdomain.com -d www.yourdomain.com`
- Certificates auto-renew via systemd timer.

## Notes for future changes
- After pulling new code, repeat: migrate (if models changed), collectstatic (if static changed), restart Gunicorn.
- Update `ALLOWED_HOSTS` when adding domains; prefer moving `SECRET_KEY` to an environment variable for production.
