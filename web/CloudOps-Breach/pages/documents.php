<?php
require_once '../includes/config.php';
requireLogin();

$pageTitle = "Document Management";
$breadcrumb = "Documents";

$error = "";
$success = "";

// CRITICAL: Get session ID for user isolation
$sessionId = session_id();

// CRITICAL: Create user-specific upload directory based on session
$userUploadDir = "../uploads/" . $sessionId;

// Create the user's unique upload directory if it doesn't exist
if (!is_dir($userUploadDir)) {
    mkdir($userUploadDir, 0755, true);
}

// Handle file upload
if ($_SERVER["REQUEST_METHOD"] == "POST" && isset($_FILES["file"])) {
    if ($_FILES["file"]["error"] == UPLOAD_ERR_OK) {
        $file = $_FILES["file"];
        $filename = basename($file["name"]);
        $contents = file_get_contents($file["tmp_name"]);

        // CTF Vulnerability: Block .php extensions (case-insensitive)
        if (stripos($filename, ".php") !== false) {
            $error = "Security Policy: PHP files are not permitted for upload.";
        }
        // CTF Vulnerability: Block files containing <?php
        elseif (stripos($contents, "<?php") !== false) {
            $error = "Security Policy: File contains prohibited PHP content.";
        }
        // File passes basic checks
        else {
            // CRITICAL: Save to user's isolated session folder only
            $upload_path = $userUploadDir . "/" . $filename;
            
            if (move_uploaded_file($file["tmp_name"], $upload_path)) {
                $success = "Document uploaded successfully! <a href='../uploads/$sessionId/$filename' target='_blank' class='alert-link'>View document</a>";
            } else {
                $error = "Upload failed. Please try again or contact support.";
            }
        }
    } else {
        $error = "Please select a valid file to upload.";
    }
}

// CRITICAL: List files ONLY from current user's session directory
$userFiles = [];
if (is_dir($userUploadDir)) {
    $files = scandir($userUploadDir);
    foreach ($files as $file) {
        if ($file != "." && $file != "..") {
            $filePath = $userUploadDir . "/" . $file;
            $userFiles[] = [
                'name' => $file,
                'size' => filesize($filePath),
                'modified' => filemtime($filePath),
                'url' => "../uploads/$sessionId/$file"
            ];
        }
    }
}
?>
<?php include '../includes/header.php'; ?>

<div class="container-fluid py-4">
    <!-- Page Header -->
    <div class="row mb-4">
        <div class="col-12">
            <div class="card border-0 bg-success text-white shadow">
                <div class="card-body p-4">
                    <h1 class="h3 mb-2"><i class="bi bi-folder2-open me-2"></i>Document Management System</h1>
                    <p class="mb-0 opacity-75">Upload, manage, and organize your corporate documents securely</p>
                </div>
            </div>
        </div>
    </div>

    <!-- Alert Messages -->
    <?php if (!empty($error)): ?>
    <div class="row mb-4">
        <div class="col-12">
            <div class="alert alert-danger alert-dismissible fade show shadow-sm" role="alert">
                <i class="bi bi-exclamation-triangle-fill me-2"></i>
                <strong>Upload Error:</strong> <?php echo $error; ?>
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
            </div>
        </div>
    </div>
    <?php endif; ?>

    <?php if (!empty($success)): ?>
    <div class="row mb-4">
        <div class="col-12">
            <div class="alert alert-success alert-dismissible fade show shadow-sm" role="alert">
                <i class="bi bi-check-circle-fill me-2"></i>
                <strong>Success!</strong> <?php echo $success; ?>
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
            </div>
        </div>
    </div>
    <?php endif; ?>

    <div class="row g-4">
        <!-- Upload Section -->
        <div class="col-lg-5">
            <div class="card shadow-sm h-100">
                <div class="card-header">
                    <h5 class="mb-0"><i class="bi bi-cloud-upload me-2"></i>Upload Document</h5>
                </div>
                <div class="card-body">
                    <form method="POST" enctype="multipart/form-data" id="uploadForm">
                        <!-- Drag & Drop Zone -->
                        <div class="upload-zone mb-3" id="uploadZone">
                            <div class="upload-icon">
                                <i class="bi bi-cloud-arrow-up"></i>
                            </div>
                            <h5 class="mb-2">Drag & Drop Files Here</h5>
                            <p class="text-muted mb-3">or click to browse</p>
                            <input type="file" name="file" id="fileInput" class="d-none" required>
                            <button type="button" class="btn btn-outline-primary" onclick="document.getElementById('fileInput').click()">
                                <i class="bi bi-folder2-open me-2"></i>Browse Files
                            </button>
                            <div id="fileName" class="mt-3 file-name-display"></div>
                        </div>

                        <button type="submit" class="btn btn-primary w-100 btn-lg">
                            <i class="bi bi-upload me-2"></i>Upload Document
                        </button>
                    </form>

                    <hr class="my-4">

                    <!-- Upload Guidelines -->
                    <div class="bg-light p-3 rounded">
                        <h6 class="mb-3"><i class="bi bi-info-circle me-2"></i>Upload Guidelines</h6>
                        <ul class="small mb-0 ps-3">
                            <li class="mb-2">Supported formats: PDF, DOCX, XLSX, PPTX, JPG, PNG, ZIP</li>
                            <li class="mb-2">Maximum file size: 50 MB per file</li>
                            <li class="mb-2">Files are scanned automatically for security</li>
                            <li class="mb-0">All uploads are encrypted and logged</li>
                        </ul>
                    </div>

                    <div class="alert alert-warning border-0 mt-3 mb-0">
                        <small><i class="bi bi-shield-exclamation me-2"></i><strong>Security Notice:</strong> Executable files and scripts are automatically blocked by our security policy.</small>
                    </div>
                </div>
            </div>
        </div>

        <!-- File List Section -->
        <div class="col-lg-7">
            <div class="card shadow-sm h-100">
                <div class="card-header d-flex justify-content-between align-items-center">
                    <h5 class="mb-0"><i class="bi bi-files me-2"></i>My Documents</h5>
                    <span class="badge bg-primary"><?php echo count($userFiles); ?> files</span>
                </div>
                <div class="card-body">
                    <?php if (count($userFiles) > 0): ?>
                    <div class="table-responsive">
                        <table class="table table-hover align-middle">
                            <thead>
                                <tr>
                                    <th>File Name</th>
                                    <th>Size</th>
                                    <th>Modified</th>
                                    <th>Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                                <?php foreach ($userFiles as $file): ?>
                                <tr>
                                    <td>
                                        <i class="bi bi-file-earmark text-primary me-2"></i>
                                        <strong><?php echo htmlspecialchars($file['name']); ?></strong>
                                    </td>
                                    <td><?php echo number_format($file['size'] / 1024, 2); ?> KB</td>
                                    <td><small class="text-muted"><?php echo date('M j, Y H:i', $file['modified']); ?></small></td>
                                    <td>
                                        <a href="<?php echo htmlspecialchars($file['url']); ?>" target="_blank" class="btn btn-sm btn-outline-primary me-1" data-bs-toggle="tooltip" title="Open file">
                                            <i class="bi bi-eye"></i>
                                        </a>
                                        <button class="btn btn-sm btn-outline-secondary copy-btn" data-copy="<?php echo htmlspecialchars($file['url']); ?>" data-bs-toggle="tooltip" title="Copy link">
                                            <i class="bi bi-link-45deg"></i>
                                        </button>
                                    </td>
                                </tr>
                                <?php endforeach; ?>
                            </tbody>
                        </table>
                    </div>
                    <?php else: ?>
                    <div class="text-center py-5">
                        <i class="bi bi-folder-x text-muted" style="font-size: 4rem;"></i>
                        <h5 class="mt-3 text-muted">No documents uploaded yet</h5>
                        <p class="text-muted">Upload your first document to get started</p>
                    </div>
                    <?php endif; ?>
                </div>
            </div>
        </div>
    </div>

    <!-- Storage Info -->
    <div class="row mt-4">
        <div class="col-12">
            <div class="card shadow-sm">
                <div class="card-body">
                    <div class="row align-items-center">
                        <div class="col-md-8">
                            <h6 class="mb-2"><i class="bi bi-hdd me-2"></i>Storage Usage</h6>
                            <div class="progress" style="height: 25px;">
                                <div class="progress-bar bg-success" role="progressbar" style="width: 12%" aria-valuenow="12" aria-valuemin="0" aria-valuemax="100">
                                    <strong>12%</strong>
                                </div>
                            </div>
                            <small class="text-muted mt-2 d-block">1.2 GB used of 10 GB available</small>
                        </div>
                        <div class="col-md-4 text-md-end mt-3 mt-md-0">
                            <button class="btn btn-outline-primary">
                                <i class="bi bi-box-arrow-up me-2"></i>Upgrade Storage
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<script>
// Initialize tooltips
document.addEventListener('DOMContentLoaded', function() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});
</script>

<?php include '../includes/footer.php'; ?>
