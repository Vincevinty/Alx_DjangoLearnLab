# Ngix
server {
    listen 443 ssl;
    server_name yourdomain.com;

    ssl_certificate /etc/ssl/certs/your_cert.crt;
    ssl_certificate_key /etc/ssl/private/your_key.key;

    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
}

# Apache
<VirtualHost *:443>
    ServerName yourdomain.com

    SSLEngine on
    SSLCertificateFile /path/to/your_cert.crt
    SSLCertificateKeyFile /path/to/your_key.key

    Header always set Strict-Transport-Security "max-age=31536000; includeSubDomains; preload"
</VirtualHost>