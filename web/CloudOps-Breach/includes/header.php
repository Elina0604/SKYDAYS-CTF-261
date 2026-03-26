<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title><?php echo isset($pageTitle) ? $pageTitle . ' | ' : ''; ?><?php echo PORTAL_NAME; ?></title>
    
    <!-- Bootstrap 5 CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN" crossorigin="anonymous">
    
    <!-- Bootstrap Icons -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css">
    
    <!-- Custom CSS -->
    <link rel="stylesheet" href="/assets/css/portal.css">
    
    <!-- Favicon -->
    <link rel="icon" type="image/png" href="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==">
</head>
<body>
    <!-- Top Navigation Bar -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary shadow-sm">
        <div class="container-fluid">
            <a class="navbar-brand d-flex align-items-center" href="/pages/dashboard.php">
                <i class="bi bi-cloud-check-fill me-2 fs-4"></i>
                <span class="fw-bold"><?php echo PORTAL_NAME; ?></span>
            </a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item">
                        <a class="nav-link <?php echo (getCurrentPage() == 'dashboard') ? 'active' : ''; ?>" href="/pages/dashboard.php">
                            <i class="bi bi-speedometer2 me-1"></i> Dashboard
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link <?php echo (getCurrentPage() == 'logs') ? 'active' : ''; ?>" href="/pages/logs.php">
                            <i class="bi bi-journal-text me-1"></i> Server Logs
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link <?php echo (getCurrentPage() == 'documents') ? 'active' : ''; ?>" href="/pages/documents.php">
                            <i class="bi bi-folder2-open me-1"></i> Documents
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link <?php echo (getCurrentPage() == 'profile') ? 'active' : ''; ?>" href="/pages/profile.php">
                            <i class="bi bi-person-circle me-1"></i> Profile
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link text-warning" href="/logout.php">
                            <i class="bi bi-box-arrow-right me-1"></i> Logout
                        </a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>

    <!-- Breadcrumb Navigation -->
    <div class="bg-light border-bottom py-2">
        <div class="container-fluid">
            <nav aria-label="breadcrumb">
                <ol class="breadcrumb mb-0 small">
                    <li class="breadcrumb-item"><a href="/pages/dashboard.php" class="text-decoration-none">Home</a></li>
                    <?php if (isset($breadcrumb)): ?>
                        <li class="breadcrumb-item active" aria-current="page"><?php echo $breadcrumb; ?></li>
                    <?php endif; ?>
                </ol>
            </nav>
        </div>
    </div>

    <!-- Main Content Wrapper -->
    <div class="content-wrapper">
