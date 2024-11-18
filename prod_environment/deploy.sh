#!/bin/bash

if ! [ -x "$(command -v nginx)" ]; then
  echo "Nginx не установлен. Установка Nginx..."
  sudo apt update
  sudo apt install nginx -y
  sudo systemctl enable nginx
  sudo systemctl start nginx
  echo "Nginx успешно установлен."
else
  echo "Nginx уже установлен."
fi

if ! [ -x "$(command -v certbot)" ]; then
  echo "Certbot не установлен. Установка Certbot..."
  sudo add-apt-repository ppa:certbot/certbot -y
  sudo apt update
  sudo apt install certbot python3-certbot-nginx -y
  echo "Certbot успешно установлен."
else
  echo "Certbot уже установлен"
fi

CERT_DIR="/etc/letsencrypt/live/example.com"
if [ -d "$CERT_DIR" ]; then
  echo "Existing SSL certificate found at $CERT_DIR."
  read -p "Вы хотите обновить SSL сертификат? (y/n) " UPDATE_CERT
  if [ "$UPDATE_CERT" = "y" ]; then
    echo "Обновление SSL сертификата..."
    sudo certbot --nginx -d star-burg.ru -d www.star-burg.ru --email alex_tolchin@mail.ru --agree-tos --non-interactive --expand
  else
    echo "Сохранение существующего SSL-сертификата."
  fi
else
  echo "Существующий сертификат SSL не найден. Получение нового..."
  sudo certbot --nginx -d example.com -d www.example.com --email your_email@example.com --agree-tos --non-interactive --expand
fi

echo "Configuring Nginx to use SSL certificates..."
sudo nano /etc/nginx/sites-available/starburger
echo "server {
    listen 80;
    server_name example.com www.example.com;
    return 301 https://\$host\$request_uri;
}

server {
    listen 443 ssl;
    server_name star-burg.ru www.star-burg.ru;
    ssl_certificate /etc/letsencrypt/live/star-burg.ru/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/star-burg.ru/privkey.pem;
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
    }
}" | sudo tee /etc/nginx/sites-available/example.com
sudo nginx -t
sudo systemctl reload nginx

echo "Проверка конфигурации SSL..."
curl -I https://star-burg.ru
openssl s_client -connect star-burg.ru:443 -servername star-burg.ru

echo "Создание и запуск Docker-контейнеров..."
cd /opt/star-burger/prod_environment
docker compose up -d --build

echo "Развертывание успешно завершено."
