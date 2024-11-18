#!/bin/bash

echo "Сборка и запуск контейнеров..."

docker compose up -d --build

echo "Запуск Certbot для получения SSL сертификата..."
docker compose run --rm certbot certonly --webroot --webroot-path=/var/www/certbot --email alex_tolchin@mail.ru --agree-tos --no-eff-email -d star-burg.ru -d www.star-burg.ru

echo "Перезагрузка Nginx для применения новой конфигурации SSL..."
docker compose exec nginx nginx -s reload

if [ $? -ne 0 ]; then
  echo "Certbot не удалось получить SSL-сертификат. Проверьте логи для получения подробностей."
  exit 1
fi

  echo "Развертывание и настройка SSL-сертификата завершены."
