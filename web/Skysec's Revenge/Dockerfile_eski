FROM php:7.2-apache

COPY *.php /var/www/html/
COPY flag.txt /flag.txt

RUN mkdir -p /var/www/html/uploads
RUN chown -R www-data:www-data /var/www/html/uploads

EXPOSE 80

CMD ["apache2-foreground"]
