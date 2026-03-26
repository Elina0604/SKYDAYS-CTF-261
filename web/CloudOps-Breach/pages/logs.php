<?php
require_once '../includes/config.php';
requireLogin();

$pageTitle = "Server Logs";
$breadcrumb = "Server Logs";

// Generate fake log entries
$logEntries = [
    ['time' => '2026-03-19 09:42:15', 'level' => 'INFO', 'ip' => '192.168.1.105', 'message' => 'User login successful', 'user' => 'admin'],
    ['time' => '2026-03-19 09:40:32', 'level' => 'INFO', 'ip' => '192.168.1.105', 'message' => 'Document uploaded: quarterly_report.pdf', 'user' => 'admin'],
    ['time' => '2026-03-19 09:38:47', 'level' => 'WARNING', 'ip' => '203.0.113.42', 'message' => 'Failed login attempt - invalid password', 'user' => 'unknown'],
    ['time' => '2026-03-19 09:35:21', 'level' => 'INFO', 'ip' => '192.168.1.88', 'message' => 'Database backup completed successfully', 'user' => 'system'],
    ['time' => '2026-03-19 09:30:15', 'level' => 'INFO', 'ip' => '192.168.1.105', 'message' => 'User accessed dashboard', 'user' => 'admin'],
    ['time' => '2026-03-19 09:28:44', 'level' => 'ERROR', 'ip' => '198.51.100.23', 'message' => 'API rate limit exceeded', 'user' => 'api_client'],
    ['time' => '2026-03-19 09:25:12', 'level' => 'INFO', 'ip' => '192.168.1.50', 'message' => 'SSL certificate renewed successfully', 'user' => 'system'],
    ['time' => '2026-03-19 09:20:33', 'level' => 'WARNING', 'ip' => '203.0.113.89', 'message' => 'Suspicious file upload blocked', 'user' => 'security'],
    ['time' => '2026-03-19 09:15:07', 'level' => 'INFO', 'ip' => '192.168.1.105', 'message' => 'User session started', 'user' => 'admin'],
    ['time' => '2026-03-19 09:10:45', 'level' => 'INFO', 'ip' => '192.168.1.72', 'message' => 'Scheduled task executed: cleanup_temp_files', 'user' => 'system'],
    ['time' => '2026-03-19 09:05:18', 'level' => 'ERROR', 'ip' => '198.51.100.67', 'message' => 'Database connection timeout', 'user' => 'system'],
    ['time' => '2026-03-19 09:00:00', 'level' => 'INFO', 'ip' => '192.168.1.88', 'message' => 'Automated backup initiated', 'user' => 'system'],
    ['time' => '2026-03-19 08:55:23', 'level' => 'WARNING', 'ip' => '203.0.113.15', 'message' => 'Multiple failed login attempts detected', 'user' => 'security'],
    ['time' => '2026-03-19 08:50:41', 'level' => 'INFO', 'ip' => '192.168.1.105', 'message' => 'Configuration updated: security_settings', 'user' => 'admin'],
    ['time' => '2026-03-19 08:45:12', 'level' => 'INFO', 'ip' => '192.168.1.62', 'message' => 'Cache cleared successfully', 'user' => 'system'],
    ['time' => '2026-03-19 08:40:35', 'level' => 'INFO', 'ip' => '192.168.1.105', 'message' => 'User logout completed', 'user' => 'admin'],
    ['time' => '2026-03-19 08:35:19', 'level' => 'ERROR', 'ip' => '198.51.100.91', 'message' => 'Disk space warning: 85% used on /var', 'user' => 'system'],
    ['time' => '2026-03-19 08:30:47', 'level' => 'INFO', 'ip' => '192.168.1.45', 'message' => 'Service health check passed', 'user' => 'monitoring'],
    ['time' => '2026-03-19 08:25:03', 'level' => 'INFO', 'ip' => '192.168.1.105', 'message' => 'Report generated: monthly_analytics.pdf', 'user' => 'admin'],
    ['time' => '2026-03-19 08:20:28', 'level' => 'WARNING', 'ip' => '203.0.113.56', 'message' => 'Firewall rule triggered: blocked port scan', 'user' => 'security'],
];
?>
<?php include '../includes/header.php'; ?>

<div class="container-fluid py-4">
    <!-- Page Header -->
    <div class="row mb-4">
        <div class="col-12">
            <div class="card border-0 bg-dark text-white shadow">
                <div class="card-body p-4">
                    <h1 class="h3 mb-2"><i class="bi bi-journal-text me-2"></i>Server Activity Logs</h1>
                    <p class="mb-0 opacity-75">Real-time monitoring and logging of all server activities</p>
                </div>
            </div>
        </div>
    </div>

    <!-- Statistics Row -->
    <div class="row g-4 mb-4">
        <div class="col-md-3">
            <div class="card shadow-sm h-100">
                <div class="card-body text-center">
                    <i class="bi bi-check-circle-fill text-success fs-1"></i>
                    <div class="stat-value mt-2">1,247</div>
                    <div class="stat-label">Info Messages</div>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card shadow-sm h-100">
                <div class="card-body text-center">
                    <i class="bi bi-exclamation-triangle-fill text-warning fs-1"></i>
                    <div class="stat-value mt-2">38</div>
                    <div class="stat-label">Warnings</div>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card shadow-sm h-100">
                <div class="card-body text-center">
                    <i class="bi bi-x-circle-fill text-danger fs-1"></i>
                    <div class="stat-value mt-2">5</div>
                    <div class="stat-label">Errors</div>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card shadow-sm h-100">
                <div class="card-body text-center">
                    <i class="bi bi-clock-history text-primary fs-1"></i>
                    <div class="stat-value mt-2">24h</div>
                    <div class="stat-label">Log Retention</div>
                </div>
            </div>
        </div>
    </div>

    <!-- Logs Table -->
    <div class="row">
        <div class="col-12">
            <div class="card shadow-sm">
                <div class="card-header d-flex justify-content-between align-items-center">
                    <h5 class="mb-0"><i class="bi bi-list-ul me-2"></i>Access & Activity Logs</h5>
                    <div class="btn-group" role="group">
                        <button type="button" class="btn btn-sm btn-outline-primary active">All</button>
                        <button type="button" class="btn btn-sm btn-outline-primary">Info</button>
                        <button type="button" class="btn btn-sm btn-outline-warning">Warnings</button>
                        <button type="button" class="btn btn-sm btn-outline-danger">Errors</button>
                    </div>
                </div>
                <div class="card-body p-0">
                    <!-- Search Bar -->
                    <div class="p-3 border-bottom bg-light">
                        <div class="row g-3">
                            <div class="col-md-6">
                                <div class="input-group">
                                    <span class="input-group-text"><i class="bi bi-search"></i></span>
                                    <input type="text" class="form-control table-search" placeholder="Search logs..." data-target=".logs-table">
                                </div>
                            </div>
                            <div class="col-md-3">
                                <select class="form-select">
                                    <option>Last 24 Hours</option>
                                    <option>Last 7 Days</option>
                                    <option>Last 30 Days</option>
                                    <option>Custom Range</option>
                                </select>
                            </div>
                            <div class="col-md-3">
                                <button class="btn btn-primary w-100"><i class="bi bi-download me-2"></i>Export Logs</button>
                            </div>
                        </div>
                    </div>

                    <!-- Logs Table -->
                    <div class="table-responsive">
                        <table class="table table-hover logs-table mb-0">
                            <thead class="table-light">
                                <tr>
                                    <th style="width: 180px;">Timestamp</th>
                                    <th style="width: 100px;">Level</th>
                                    <th style="width: 150px;">IP Address</th>
                                    <th style="width: 120px;">User</th>
                                    <th>Message</th>
                                    <th style="width: 80px;">Action</th>
                                </tr>
                            </thead>
                            <tbody>
                                <?php foreach ($logEntries as $log): ?>
                                <tr>
                                    <td><small class="text-muted"><?php echo $log['time']; ?></small></td>
                                    <td>
                                        <?php
                                        $badgeClass = 'bg-secondary';
                                        $icon = 'info-circle';
                                        if ($log['level'] == 'INFO') {
                                            $badgeClass = 'bg-success';
                                            $icon = 'check-circle';
                                        } elseif ($log['level'] == 'WARNING') {
                                            $badgeClass = 'bg-warning';
                                            $icon = 'exclamation-triangle';
                                        } elseif ($log['level'] == 'ERROR') {
                                            $badgeClass = 'bg-danger';
                                            $icon = 'x-circle';
                                        }
                                        ?>
                                        <span class="badge <?php echo $badgeClass; ?>">
                                            <i class="bi bi-<?php echo $icon; ?> me-1"></i><?php echo $log['level']; ?>
                                        </span>
                                    </td>
                                    <td><code class="small"><?php echo $log['ip']; ?></code></td>
                                    <td><span class="badge bg-light text-dark"><?php echo $log['user']; ?></span></td>
                                    <td><?php echo $log['message']; ?></td>
                                    <td>
                                        <button class="btn btn-sm btn-outline-secondary" data-bs-toggle="tooltip" title="View Details">
                                            <i class="bi bi-eye"></i>
                                        </button>
                                    </td>
                                </tr>
                                <?php endforeach; ?>
                            </tbody>
                        </table>
                    </div>

                    <!-- Pagination -->
                    <div class="p-3 border-top bg-light">
                        <div class="d-flex justify-content-between align-items-center">
                            <small class="text-muted">Showing 20 of 1,290 log entries</small>
                            <nav>
                                <ul class="pagination pagination-sm mb-0">
                                    <li class="page-item disabled">
                                        <a class="page-link" href="#"><i class="bi bi-chevron-left"></i></a>
                                    </li>
                                    <li class="page-item active"><a class="page-link" href="#">1</a></li>
                                    <li class="page-item"><a class="page-link" href="#">2</a></li>
                                    <li class="page-item"><a class="page-link" href="#">3</a></li>
                                    <li class="page-item"><a class="page-link" href="#">4</a></li>
                                    <li class="page-item"><a class="page-link" href="#">5</a></li>
                                    <li class="page-item">
                                        <a class="page-link" href="#"><i class="bi bi-chevron-right"></i></a>
                                    </li>
                                </ul>
                            </nav>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Additional Info -->
    <div class="row mt-4">
        <div class="col-md-6">
            <div class="card shadow-sm">
                <div class="card-header">
                    <h5 class="mb-0"><i class="bi bi-graph-up me-2"></i>Log Activity Trend</h5>
                </div>
                <div class="card-body">
                    <p class="text-muted mb-3">Activity distribution over the last 24 hours:</p>
                    <div class="mb-3">
                        <div class="d-flex justify-content-between mb-1">
                            <span><i class="bi bi-circle-fill text-success me-2" style="font-size: 0.5rem;"></i>INFO (96.5%)</span>
                            <strong>1,247 events</strong>
                        </div>
                        <div class="progress" style="height: 8px;">
                            <div class="progress-bar bg-success" style="width: 96.5%"></div>
                        </div>
                    </div>
                    <div class="mb-3">
                        <div class="d-flex justify-content-between mb-1">
                            <span><i class="bi bi-circle-fill text-warning me-2" style="font-size: 0.5rem;"></i>WARNING (2.9%)</span>
                            <strong>38 events</strong>
                        </div>
                        <div class="progress" style="height: 8px;">
                            <div class="progress-bar bg-warning" style="width: 2.9%"></div>
                        </div>
                    </div>
                    <div>
                        <div class="d-flex justify-content-between mb-1">
                            <span><i class="bi bi-circle-fill text-danger me-2" style="font-size: 0.5rem;"></i>ERROR (0.6%)</span>
                            <strong>5 events</strong>
                        </div>
                        <div class="progress" style="height: 8px;">
                            <div class="progress-bar bg-danger" style="width: 0.6%"></div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="col-md-6">
            <div class="card shadow-sm">
                <div class="card-header">
                    <h5 class="mb-0"><i class="bi bi-shield-check me-2"></i>Security Events</h5>
                </div>
                <div class="card-body">
                    <div class="alert alert-warning border-0 mb-2">
                        <small><strong>03:42 AM</strong> - Failed login attempts from IP 203.0.113.42</small>
                    </div>
                    <div class="alert alert-info border-0 mb-2">
                        <small><strong>02:15 AM</strong> - Firewall rules updated successfully</small>
                    </div>
                    <div class="alert alert-success border-0 mb-0">
                        <small><strong>12:00 AM</strong> - Security scan completed - No threats detected</small>
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
