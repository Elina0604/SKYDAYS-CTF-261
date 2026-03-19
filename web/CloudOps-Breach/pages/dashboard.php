<?php
require_once '../includes/config.php';
requireLogin();

$pageTitle = "Dashboard";
$breadcrumb = "Dashboard";
?>
<?php include '../includes/header.php'; ?>

<div class="container-fluid py-4">
    <!-- Welcome Header -->
    <div class="row mb-4">
        <div class="col-12">
            <div class="card border-0 bg-primary text-white shadow">
                <div class="card-body p-4">
                    <h1 class="h3 mb-2"><i class="bi bi-speedometer2 me-2"></i>Welcome back, <?php echo getCurrentUser(); ?>!</h1>
                    <p class="mb-0 opacity-75">Here's an overview of your infrastructure status and system metrics.</p>
                </div>
            </div>
        </div>
    </div>

    <!-- Statistics Cards -->
    <div class="row g-4 mb-4">
        <div class="col-md-3">
            <div class="card stat-card success shadow-sm h-100">
                <div class="card-body">
                    <div class="d-flex justify-content-between align-items-center mb-2">
                        <h6 class="stat-label mb-0">System Uptime</h6>
                        <i class="bi bi-arrow-up-circle text-success fs-4"></i>
                    </div>
                    <div class="stat-value">99.8%</div>
                    <small class="text-muted"><i class="bi bi-clock-history me-1"></i>47 days, 3 hours</small>
                </div>
            </div>
        </div>
        
        <div class="col-md-3">
            <div class="card stat-card info shadow-sm h-100">
                <div class="card-body">
                    <div class="d-flex justify-content-between align-items-center mb-2">
                        <h6 class="stat-label mb-0">Active Services</h6>
                        <i class="bi bi-hdd-network text-info fs-4"></i>
                    </div>
                    <div class="stat-value">24/25</div>
                    <small class="text-muted"><i class="bi bi-check-circle me-1"></i>All critical online</small>
                </div>
            </div>
        </div>
        
        <div class="col-md-3">
            <div class="card stat-card warning shadow-sm h-100">
                <div class="card-body">
                    <div class="d-flex justify-content-between align-items-center mb-2">
                        <h6 class="stat-label mb-0">CPU Usage</h6>
                        <i class="bi bi-cpu text-warning fs-4"></i>
                    </div>
                    <div class="stat-value">68%</div>
                    <small class="text-muted"><i class="bi bi-graph-up me-1"></i>Normal load</small>
                </div>
            </div>
        </div>
        
        <div class="col-md-3">
            <div class="card stat-card shadow-sm h-100">
                <div class="card-body">
                    <div class="d-flex justify-content-between align-items-center mb-2">
                        <h6 class="stat-label mb-0">Memory Usage</h6>
                        <i class="bi bi-memory text-primary fs-4"></i>
                    </div>
                    <div class="stat-value">12.4GB</div>
                    <small class="text-muted"><i class="bi bi-info-circle me-1"></i>of 32GB total</small>
                </div>
            </div>
        </div>
    </div>

    <!-- Charts and Metrics Row -->
    <div class="row g-4 mb-4">
        <!-- Server Status -->
        <div class="col-lg-8">
            <div class="card shadow-sm h-100">
                <div class="card-header">
                    <h5 class="mb-0"><i class="bi bi-server me-2"></i>Server Infrastructure Status</h5>
                </div>
                <div class="card-body">
                    <div class="table-responsive">
                        <table class="table table-hover align-middle">
                            <thead>
                                <tr>
                                    <th>Server</th>
                                    <th>Status</th>
                                    <th>CPU</th>
                                    <th>Memory</th>
                                    <th>Disk</th>
                                    <th>Uptime</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td><i class="bi bi-hdd-fill text-primary me-2"></i>web-prod-01</td>
                                    <td><span class="badge bg-success"><span class="status-indicator online"></span>Online</span></td>
                                    <td>45%</td>
                                    <td>8.2 GB</td>
                                    <td>
                                        <div class="progress" style="height: 8px;">
                                            <div class="progress-bar bg-success" role="progressbar" style="width: 35%" aria-valuenow="35" aria-valuemin="0" aria-valuemax="100"></div>
                                        </div>
                                    </td>
                                    <td>47d 3h</td>
                                </tr>
                                <tr>
                                    <td><i class="bi bi-hdd-fill text-primary me-2"></i>web-prod-02</td>
                                    <td><span class="badge bg-success"><span class="status-indicator online"></span>Online</span></td>
                                    <td>52%</td>
                                    <td>9.1 GB</td>
                                    <td>
                                        <div class="progress" style="height: 8px;">
                                            <div class="progress-bar bg-success" role="progressbar" style="width: 42%" aria-valuenow="42" aria-valuemin="0" aria-valuemax="100"></div>
                                        </div>
                                    </td>
                                    <td>47d 3h</td>
                                </tr>
                                <tr>
                                    <td><i class="bi bi-database-fill text-info me-2"></i>db-master-01</td>
                                    <td><span class="badge bg-success"><span class="status-indicator online"></span>Online</span></td>
                                    <td>28%</td>
                                    <td>24.7 GB</td>
                                    <td>
                                        <div class="progress" style="height: 8px;">
                                            <div class="progress-bar bg-warning" role="progressbar" style="width: 68%" aria-valuenow="68" aria-valuemin="0" aria-valuemax="100"></div>
                                        </div>
                                    </td>
                                    <td>89d 12h</td>
                                </tr>
                                <tr>
                                    <td><i class="bi bi-cloud-fill text-success me-2"></i>cache-redis-01</td>
                                    <td><span class="badge bg-success"><span class="status-indicator online"></span>Online</span></td>
                                    <td>15%</td>
                                    <td>6.4 GB</td>
                                    <td>
                                        <div class="progress" style="height: 8px;">
                                            <div class="progress-bar bg-success" role="progressbar" style="width: 22%" aria-valuenow="22" aria-valuemin="0" aria-valuemax="100"></div>
                                        </div>
                                    </td>
                                    <td>47d 3h</td>
                                </tr>
                                <tr>
                                    <td><i class="bi bi-shield-check text-warning me-2"></i>firewall-01</td>
                                    <td><span class="badge bg-warning"><span class="status-indicator warning"></span>Maintenance</span></td>
                                    <td>8%</td>
                                    <td>2.1 GB</td>
                                    <td>
                                        <div class="progress" style="height: 8px;">
                                            <div class="progress-bar bg-success" role="progressbar" style="width: 18%" aria-valuenow="18" aria-valuemin="0" aria-valuemax="100"></div>
                                        </div>
                                    </td>
                                    <td>2h 15m</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>

        <!-- System Information -->
        <div class="col-lg-4">
            <div class="card shadow-sm mb-4">
                <div class="card-header">
                    <h5 class="mb-0"><i class="bi bi-info-circle me-2"></i>System Information</h5>
                </div>
                <div class="card-body">
                    <ul class="list-unstyled mb-0">
                        <li class="mb-3">
                            <small class="text-muted d-block">Operating System</small>
                            <strong>Ubuntu 22.04.3 LTS</strong>
                        </li>
                        <li class="mb-3">
                            <small class="text-muted d-block">PHP Version</small>
                            <strong><?php echo PHP_VERSION; ?></strong>
                        </li>
                        <li class="mb-3">
                            <small class="text-muted d-block">Web Server</small>
                            <strong>Apache/2.4.52</strong>
                        </li>
                        <li class="mb-3">
                            <small class="text-muted d-block">Database</small>
                            <strong>MySQL 8.0.35</strong>
                        </li>
                        <li class="mb-3">
                            <small class="text-muted d-block">Server Time</small>
                            <strong><?php echo date('Y-m-d H:i:s T'); ?></strong>
                        </li>
                        <li>
                            <small class="text-muted d-block">Portal Version</small>
                            <strong><?php echo PORTAL_VERSION; ?></strong>
                        </li>
                    </ul>
                </div>
            </div>

            <div class="card shadow-sm">
                <div class="card-header">
                    <h5 class="mb-0"><i class="bi bi-exclamation-triangle me-2"></i>Recent Alerts</h5>
                </div>
                <div class="card-body">
                    <div class="alert alert-warning border-0 mb-2" role="alert">
                        <small><i class="bi bi-shield-exclamation me-2"></i><strong>Firewall:</strong> Scheduled maintenance in progress</small>
                    </div>
                    <div class="alert alert-info border-0 mb-2" role="alert">
                        <small><i class="bi bi-arrow-repeat me-2"></i><strong>System:</strong> Security patches applied successfully</small>
                    </div>
                    <div class="alert alert-success border-0 mb-0" role="alert">
                        <small><i class="bi bi-check-circle me-2"></i><strong>Backup:</strong> Daily backup completed at 02:00</small>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Resource Usage -->
    <div class="row g-4">
        <div class="col-md-6">
            <div class="card shadow-sm">
                <div class="card-header">
                    <h5 class="mb-0"><i class="bi bi-graph-up me-2"></i>Network Traffic (Last 24 Hours)</h5>
                </div>
                <div class="card-body">
                    <div class="mb-3">
                        <div class="d-flex justify-content-between mb-1">
                            <span class="text-muted small">Inbound Traffic</span>
                            <span class="fw-bold">2.4 TB</span>
                        </div>
                        <div class="progress" style="height: 20px;">
                            <div class="progress-bar bg-success" role="progressbar" style="width: 75%" aria-valuenow="75" aria-valuemin="0" aria-valuemax="100">75%</div>
                        </div>
                    </div>
                    <div class="mb-3">
                        <div class="d-flex justify-content-between mb-1">
                            <span class="text-muted small">Outbound Traffic</span>
                            <span class="fw-bold">1.8 TB</span>
                        </div>
                        <div class="progress" style="height: 20px;">
                            <div class="progress-bar bg-info" role="progressbar" style="width: 56%" aria-valuenow="56" aria-valuemin="0" aria-valuemax="100">56%</div>
                        </div>
                    </div>
                    <div>
                        <div class="d-flex justify-content-between mb-1">
                            <span class="text-muted small">Total Bandwidth Used</span>
                            <span class="fw-bold">4.2 TB / 10 TB</span>
                        </div>
                        <div class="progress" style="height: 20px;">
                            <div class="progress-bar bg-warning" role="progressbar" style="width: 42%" aria-valuenow="42" aria-valuemin="0" aria-valuemax="100">42%</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="col-md-6">
            <div class="card shadow-sm">
                <div class="card-header">
                    <h5 class="mb-0"><i class="bi bi-activity me-2"></i>Quick Actions</h5>
                </div>
                <div class="card-body">
                    <div class="d-grid gap-2">
                        <a href="documents.php" class="btn btn-primary btn-lg">
                            <i class="bi bi-folder2-open me-2"></i>Manage Documents
                        </a>
                        <a href="logs.php" class="btn btn-outline-primary">
                            <i class="bi bi-journal-text me-2"></i>View Server Logs
                        </a>
                        <a href="profile.php" class="btn btn-outline-secondary">
                            <i class="bi bi-person-circle me-2"></i>Update Profile
                        </a>
                    </div>
                    
                    <hr class="my-4">
                    
                    <div class="text-center">
                        <p class="text-muted small mb-2">System Health Score</p>
                        <div class="display-4 text-success fw-bold">96/100</div>
                        <p class="text-muted small mt-2">All systems operating normally</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<?php include '../includes/footer.php'; ?>
