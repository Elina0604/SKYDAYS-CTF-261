FROM php:7.2-apache

# Copy PHP files from root
COPY *.php /var/www/html/

# Copy directory structure
COPY pages/ /var/www/html/pages/
COPY includes/ /var/www/html/includes/
COPY assets/ /var/www/html/assets/

# Copy flag
COPY flag.txt /flag.txt

# Create uploads directory with proper permissions
RUN mkdir -p /var/www/html/uploads
RUN chown -R www-data:www-data /var/www/html/uploads
RUN chmod -R 777 /var/www/html/uploads

# ==============================================
# GIT LEAK SETUP - Full Repository with History
# ==============================================

# Copy complete .git directory with all objects and commit history
COPY fake_git/ /var/www/html/.git/

# Ensure web server can read .git directory
RUN chown -R www-data:www-data /var/www/html/.git
RUN chmod -R 755 /var/www/html/.git

# ==============================================
# APACHE CONFIGURATION
# ==============================================

# AllowOverride'ı aktif et
RUN sed -i '/<Directory \/var\/www\/>/,/<\/Directory>/ s/AllowOverride None/AllowOverride All/' /etc/apache2/apache2.conf

# PHP short_open_tag'i aktif et
RUN echo "short_open_tag = On" >> /usr/local/etc/php/php.ini

EXPOSE 80

CMD ["apache2-foreground"]
