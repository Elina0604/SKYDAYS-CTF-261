#!/bin/bash
set -e

echo "==================================="
echo "  Git Leak Generator for CTF"
echo "==================================="
echo ""

# Clean up any existing .git directory
if [ -d ".git" ]; then
    echo "🧹 Removing old .git directory..."
    rm -rf .git
fi

if [ -d "git-files" ]; then
    echo "🧹 Removing old git-files directory..."
    rm -rf git-files
fi

# Create temporary directory
TEMP_DIR=$(mktemp -d)
echo "📁 Creating temporary Git repository in: $TEMP_DIR"
cd "$TEMP_DIR"

# Initialize Git repository
echo "🔧 Initializing Git repository..."
git init
git config user.name "Alex Morgan"
git config user.email "alex.morgan@cloudops.local"

# Step 1: Create initial login.php (secure version)
echo "📝 Creating initial login.php..."
cat > login.php << 'EOF'
<?php
    error_reporting(0);
    session_start();
    
    if ($_SERVER["REQUEST_METHOD"] == "POST") {
        $username = $_POST["username"];
        $password = $_POST["password"];
        
        $stored_username = "admin";
        $stored_password_hash = password_hash("change_me_later", PASSWORD_DEFAULT);
        
        if ($username === $stored_username && password_verify($password, $stored_password_hash)) {
            $_SESSION["logged_in"] = true;
            $_SESSION["username"] = $username;
            header("Location: pages/dashboard.php");
            exit();
        }
    }
    
    header("Location: index.php");
?>
EOF

git add login.php
git commit -m "Initial commit"

# Step 2: Create vulnerable version (realistic corporate bug)
echo "📝 Updating login.php with new auth logic..."
cat > login.php << 'EOF'
<?php
    error_reporting(0);
    session_start();
    $admin_password = bin2hex(random_bytes(16));
    
    if ($_SERVER["REQUEST_METHOD"] == "POST") {
        $username = $_POST["username"];
        $password = $_POST["password"];
        
        if ($username == "skysec" && strcmp($admin_password, $password) == 0) {
            $_SESSION["logged_in"] = true;
            $_SESSION["username"] = $username;
            header("Location: pages/dashboard.php");
            exit();
        }
    }
    
    header("Location: index.php");
?>
EOF

git add login.php
git commit -m "Update auth logic"

# Step 3: Add realistic config file
echo "📝 Adding configuration file..."
cat > config.php << 'EOF'
<?php
define('DB_HOST', 'localhost');
define('DB_USER', 'cloudops_admin');
define('DB_PASS', 'CloudOps2026!SecureDB');
define('DB_NAME', 'devops_portal');

define('ADMIN_USERNAME', 'skysec');
define('SESSION_TIMEOUT', 3600);
define('MAX_UPLOAD_SIZE', 52428800);
?>
EOF

git add config.php
git commit -m "Add database config"

# Step 4: Create boring corporate README
echo "📝 Creating README..."
cat > README.md << 'EOF'
# CloudOps DevOps Portal

Version 3.2.1

## Description

Enterprise-grade infrastructure management and monitoring platform for cloud operations teams.

## Installation

1. Deploy files to web server document root
2. Configure database connection in config.php
3. Set proper permissions on uploads directory
4. Access via web browser

## Requirements

- PHP 7.2 or higher
- Apache with mod_rewrite
- MySQL 5.7+
- Minimum 2GB RAM

## Support

Contact: support@cloudops.local
Documentation: https://docs.cloudops.local

## License

Proprietary - CloudOps Technologies Inc.
All Rights Reserved.
EOF

git add README.md
git commit -m "Add README"

# Step 5: Add Apache config
echo "📝 Adding Apache configuration..."
cat > .htaccess << 'EOF'
RewriteEngine On

<FilesMatch "\.(env|log|sql)$">
    Order allow,deny
    Deny from all
</FilesMatch>

Header set X-Frame-Options "SAMEORIGIN"
Header set X-Content-Type-Options "nosniff"

php_value upload_max_filesize 50M
php_value post_max_size 50M
EOF

git add .htaccess
git commit -m "Add apache config"

# Step 6: Remove config.php (simulate security cleanup)
echo "📝 Removing hardcoded credentials..."
git rm config.php
git commit -m "Remove hardcoded DB creds"

echo ""
echo "✅ Git repository created with realistic commit history!"
echo ""
echo "📊 Commit log:"
git log --oneline --all
echo ""

# Copy .git directory to project
echo "📦 Copying .git directory to project..."
cd - > /dev/null
cp -r "$TEMP_DIR/.git" ./.git

# Clean up temp directory
echo "🧹 Cleaning up temporary files..."
rm -rf "$TEMP_DIR"

echo ""
echo "✅ Git leak generation complete!"
echo ""
echo "📁 The .git directory is now in your project root"
echo ""
echo "🔍 Players will need to:"
echo "   1. Discover .git directory exposure"
echo "   2. Extract repository with git-dumper"
echo "   3. Read commit history and source code"
echo "   4. Find username 'skysec' in login.php"
echo "   5. Analyze strcmp vulnerability"
echo ""
