<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login | CloudOps DevOps Portal</title>
    
    <!-- Bootstrap 5 CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN" crossorigin="anonymous">
    
    <!-- Bootstrap Icons -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css">
    
    <!-- Custom CSS -->
    <link rel="stylesheet" href="/assets/css/portal.css">
    
    <style>
        body {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            position: relative;
            overflow: hidden;
        }
        
        /* Animated background pattern */
        body::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 320"><path fill="%23ffffff" fill-opacity="0.1" d="M0,96L48,112C96,128,192,160,288,160C384,160,480,128,576,112C672,96,768,96,864,112C960,128,1056,160,1152,160C1248,160,1344,128,1392,112L1440,96L1440,320L1392,320C1344,320,1248,320,1152,320C1056,320,960,320,864,320C768,320,672,320,576,320C480,320,384,320,288,320C192,320,96,320,48,320L0,320Z"></path></svg>') bottom center no-repeat;
            background-size: cover;
            animation: wave 10s ease-in-out infinite;
        }
        
        @keyframes wave {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-20px); }
        }
        
        .login-container {
            background: white;
            border-radius: 16px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            overflow: hidden;
            max-width: 480px;
            width: 100%;
            z-index: 1;
            position: relative;
            animation: slideUp 0.6s ease-out;
        }
        
        @keyframes slideUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .login-header {
            background: linear-gradient(135deg, #0066cc 0%, #004c99 100%);
            color: white;
            padding: 3rem 2.5rem;
            text-align: center;
            position: relative;
            overflow: hidden;
        }
        
        .login-header::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
            animation: rotate 20s linear infinite;
        }
        
        @keyframes rotate {
            from { transform: rotate(0deg); }
            to { transform: rotate(360deg); }
        }
        
        .login-header-content {
            position: relative;
            z-index: 1;
        }
        
        .login-icon {
            font-size: 3.5rem;
            margin-bottom: 1rem;
            display: inline-block;
            animation: float 3s ease-in-out infinite;
        }
        
        @keyframes float {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-10px); }
        }
        
        .login-header h1 {
            font-size: 1.75rem;
            font-weight: 300;
            margin-bottom: 0.5rem;
            letter-spacing: 1px;
        }
        
        .login-header p {
            opacity: 0.95;
            margin-bottom: 0;
            font-size: 0.95rem;
        }
        
        .login-body {
            padding: 2.5rem 2.5rem 2rem;
        }
        
        .form-floating {
            margin-bottom: 1.25rem;
        }
        
        .form-floating > .form-control {
            border: 2px solid #e9ecef;
            border-radius: 8px;
            padding: 1rem 0.75rem;
            height: calc(3.5rem + 2px);
        }
        
        .form-floating > .form-control:focus {
            border-color: #0066cc;
            box-shadow: 0 0 0 0.25rem rgba(0, 102, 204, 0.15);
        }
        
        .form-floating > label {
            padding: 1rem 0.75rem;
            color: #6c757d;
        }
        
        .btn-login {
            width: 100%;
            padding: 0.875rem;
            font-size: 1rem;
            font-weight: 600;
            letter-spacing: 0.5px;
            border-radius: 8px;
            background: linear-gradient(135deg, #0066cc 0%, #004c99 100%);
            border: none;
            color: white;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        
        .btn-login::before {
            content: '';
            position: absolute;
            top: 50%;
            left: 50%;
            width: 0;
            height: 0;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.2);
            transform: translate(-50%, -50%);
            transition: width 0.6s, height 0.6s;
        }
        
        .btn-login:hover::before {
            width: 300px;
            height: 300px;
        }
        
        .btn-login:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(0, 102, 204, 0.4);
        }
        
        .btn-login span {
            position: relative;
            z-index: 1;
        }
        
        .security-notice {
            background: #f8f9fa;
            border-left: 4px solid #0066cc;
            padding: 1rem;
            margin-top: 1.5rem;
            border-radius: 4px;
            font-size: 0.875rem;
            color: #6c757d;
        }
        
        .security-notice i {
            color: #0066cc;
            margin-right: 0.5rem;
        }
        
        .login-footer {
            background-color: #f8f9fa;
            padding: 1.5rem 2.5rem;
            text-align: center;
            border-top: 1px solid #e9ecef;
        }
        
        .login-footer p {
            margin: 0.25rem 0;
            font-size: 0.875rem;
            color: #6c757d;
        }
        
        .login-footer a {
            color: #0066cc;
            text-decoration: none;
            transition: color 0.3s ease;
        }
        
        .login-footer a:hover {
            color: #004c99;
            text-decoration: underline;
        }
        
        .feature-list {
            list-style: none;
            padding: 0;
            margin: 1.5rem 0 0;
        }
        
        .feature-list li {
            padding: 0.5rem 0;
            color: #6c757d;
            font-size: 0.875rem;
        }
        
        .feature-list li i {
            color: #28a745;
            margin-right: 0.5rem;
        }
        
        @media (max-width: 576px) {
            .login-container {
                margin: 1rem;
            }
            
            .login-header {
                padding: 2rem 1.5rem;
            }
            
            .login-body {
                padding: 2rem 1.5rem 1.5rem;
            }
            
            .login-footer {
                padding: 1.25rem 1.5rem;
            }
        }
    </style>
</head>
<body>
    <div class="login-container">
        <div class="login-header">
            <div class="login-header-content">
                <div class="login-icon">
                    <i class="bi bi-cloud-check-fill"></i>
                </div>
                <h1>CloudOps DevOps Portal</h1>
                <p>Enterprise Infrastructure Management System</p>
            </div>
        </div>
        
        <div class="login-body">
            <div class="text-center mb-4">
                <h2 class="h5 text-dark mb-1">Welcome Back</h2>
                <p class="text-muted small">Please sign in to access your dashboard</p>
            </div>
            
            <form method="POST" action="login.php" id="loginForm">
                <div class="form-floating">
                    <input type="text" class="form-control" id="username" name="username" placeholder="Username" required autocomplete="username">
                    <label for="username"><i class="bi bi-person-fill me-2"></i>Username</label>
                </div>
                
                <div class="form-floating">
                    <input type="password" class="form-control" id="password" name="password" placeholder="Password" required autocomplete="current-password">
                    <label for="password"><i class="bi bi-lock-fill me-2"></i>Password</label>
                </div>
                
                <div class="form-check mb-3">
                    <input class="form-check-input" type="checkbox" id="rememberMe">
                    <label class="form-check-label text-muted small" for="rememberMe">
                        Remember me for 30 days
                    </label>
                </div>
                
                <button type="submit" class="btn btn-login">
                    <span><i class="bi bi-box-arrow-in-right me-2"></i>Sign In Securely</span>
                </button>
            </form>
            
            <div class="security-notice">
                <i class="bi bi-shield-check"></i>
                <strong>Secure Connection:</strong> Your credentials are encrypted using industry-standard SSL/TLS protocols.
            </div>
            
            <ul class="feature-list">
                <li><i class="bi bi-check-circle-fill"></i> Multi-factor authentication enabled</li>
                <li><i class="bi bi-check-circle-fill"></i> Real-time infrastructure monitoring</li>
                <li><i class="bi bi-check-circle-fill"></i> Advanced security compliance</li>
            </ul>
        </div>
        
        <div class="login-footer">
            <p><strong>CloudOps Technologies Inc.</strong></p>
            <p>&copy; <?php echo date('Y'); ?> All rights reserved. | <a href="#">Privacy Policy</a> | <a href="#">Terms of Service</a></p>
            <p class="mt-2 small text-muted">Version 3.2.1 | Build <?php echo date('Ymd'); ?></p>
        </div>
    </div>
    
    <!-- Bootstrap 5 JS Bundle -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-C6RzsynM9kWDrMNeT87bh95OGNyZPhcTNXj1NW7RuBCsyN/o0jlpcV8Qyq46cDfL" crossorigin="anonymous"></script>
    
    <script>
        // Form submission with loading state
        document.getElementById('loginForm').addEventListener('submit', function(e) {
            const btn = this.querySelector('.btn-login');
            btn.disabled = true;
            btn.innerHTML = '<span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span><span>Authenticating...</span>';
        });
        
        // Add focus animations
        const inputs = document.querySelectorAll('.form-control');
        inputs.forEach(input => {
            input.addEventListener('focus', function() {
                this.parentElement.style.transform = 'translateY(-2px)';
                this.parentElement.style.transition = 'transform 0.3s ease';
            });
            
            input.addEventListener('blur', function() {
                this.parentElement.style.transform = 'translateY(0)';
            });
        });
    </script>
</body>
</html>
