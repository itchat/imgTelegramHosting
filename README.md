# Telegram Image Hosting Bot

```shell
pkill gunicorn
gunicorn app:app -w 4 -b 127.0.0.1:5000 --daemon --log-file gunicorn.log
apt install caddy
```

## Caddyfile

```text
https://localhost.com {
  reverse_proxy 127.0.0.1:5000
  tls xxx@xxx.com
}
```

Register the domain name, do not enable CDN acceleration and rewrites in the Cloudflare management interface, and finally assign the hosting DNS.Cloudflare 不写 https rewrites, DNS 分配主机

```shell
systemctl enable caddy
service caddy start
caddy run --config Caddyfile
```

Write a service file for easy operation and maintenance.
