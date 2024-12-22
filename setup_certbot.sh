#!/bin/bash

# Убедитесь, что вы запускаете скрипт с правами суперпользователя
if [ "$EUID" -ne 0 ]; then
  echo "Пожалуйста, запустите скрипт с правами root (sudo)."
  exit
fi

# Установка Certbot и плагина для Nginx
echo "Устанавливаем Certbot и плагин Nginx..."
apt update
apt install -y certbot python3-certbot-nginx

# Запрашиваем у пользователя домены
read -p "Введите ваш основной домен (например, freelance.com.kz): " MAIN_DOMAIN
read -p "Введите дополнительные домены через пробел (например, www.freelance.com.kz): " ADDITIONAL_DOMAINS

# Формируем строку для доменов
DOMAINS="-d $MAIN_DOMAIN"
for DOMAIN in $ADDITIONAL_DOMAINS; do
  DOMAINS="$DOMAINS -d $DOMAIN"
done

# Выполняем настройку Certbot для Nginx
echo "Запускаем Certbot для получения SSL-сертификатов..."
certbot --nginx $DOMAINS

# Проверяем успешность установки
if [ $? -eq 0 ]; then
  echo "SSL-сертификаты успешно установлены для доменов: $MAIN_DOMAIN $ADDITIONAL_DOMAINS."
  echo "Проверяем автоматическое обновление сертификатов..."

  # Добавляем задачу в crontab для автоматического обновления
  (crontab -l 2>/dev/null; echo "0 3 * * * certbot renew --quiet && systemctl reload nginx") | crontab -
  echo "Задача для автоматического обновления сертификатов добавлена в crontab."
else
  echo "Произошла ошибка при установке сертификатов. Проверьте логи Certbot."
fi

echo "Настройка завершена."
