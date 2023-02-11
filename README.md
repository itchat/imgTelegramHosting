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

Cloudflare 不写 https rewrites, DNS 分配主机

```shell
systemctl enable caddy
service caddy start
caddy run --config Caddyfile
```

最后写一个 service 文件，启动即可