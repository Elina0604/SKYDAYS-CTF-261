<?php
require_once '../includes/config.php';
requireLogin();

$pageTitle = "User Profile";
$breadcrumb = "Profile Settings";
?>
<?php include '../includes/header.php'; ?>

<div class="container-fluid py-4">
    <!-- Page Header -->
    <div class="row mb-4">
        <div class="col-12">
            <div class="card border-0 bg-primary text-white shadow">
                <div class="card-body p-4">
                    <h1 class="h3 mb-2"><i class="bi bi-person-circle me-2"></i>User Profile & Settings</h1>
                    <p class="mb-0 opacity-75">Manage your account information and preferences</p>
                </div>
            </div>
        </div>
    </div>

    <div class="row g-4">
        <!-- Profile Sidebar -->
        <div class="col-lg-4">
            <!-- User Card -->
            <div class="card shadow-sm mb-4">
                <div class="card-body text-center p-4">
                    <div class="mb-3">
                        <div class="bg-primary text-white rounded-circle d-inline-flex align-items-center justify-content-center" style="width: 100px; height: 100px; font-size: 2.5rem;">
                            <i class="bi bi-person-fill"></i>
                        </div>
                    </div>
                    <h4 class="mb-1"><?php echo getCurrentUser(); ?></h4>
                    <p class="text-muted mb-2">System Administrator</p>
                    <span class="badge bg-success"><i class="bi bi-check-circle me-1"></i>Active</span>
                    
                    <hr class="my-4">
                    
                    <div class="row text-center">
                        <div class="col-6">
                            <div class="stat-value" style="font-size: 1.5rem;">47</div>
                            <small class="text-muted">Days Active</small>
                        </div>
                        <div class="col-6">
                            <div class="stat-value" style="font-size: 1.5rem;">124</div>
                            <small class="text-muted">Files Managed</small>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Account Info -->
            <div class="card shadow-sm mb-4">
                <div class="card-header">
                    <h5 class="mb-0"><i class="bi bi-info-circle me-2"></i>Account Information</h5>
                </div>
                <div class="card-body">
                    <ul class="list-unstyled mb-0">
                        <li class="mb-3">
                            <small class="text-muted d-block">User ID</small>
                            <strong><?php echo substr(session_id(), 0, 16); ?>...</strong>
                        </li>
                        <li class="mb-3">
                            <small class="text-muted d-block">Role</small>
                            <span class="badge bg-primary">Administrator</span>
                        </li>
                        <li class="mb-3">
                            <small class="text-muted d-block">Account Created</small>
                            <strong>January 15, 2026</strong>
                        </li>
                        <li class="mb-3">
                            <small class="text-muted d-block">Last Login</small>
                            <strong><?php echo date('F j, Y - H:i'); ?></strong>
                        </li>
                        <li>
                            <small class="text-muted d-block">Session Expires</small>
                            <strong><?php echo date('F j, Y - H:i', time() + 3600); ?></strong>
                        </li>
                    </ul>
                </div>
            </div>

            <!-- Security Status -->
            <div class="card shadow-sm">
                <div class="card-header">
                    <h5 class="mb-0"><i class="bi bi-shield-check me-2"></i>Security Status</h5>
                </div>
                <div class="card-body">
                    <div class="d-flex align-items-center mb-3">
                        <i class="bi bi-check-circle-fill text-success fs-4 me-3"></i>
                        <div>
                            <strong class="d-block">Two-Factor Auth</strong>
                            <small class="text-muted">Enabled</small>
                        </div>
                    </div>
                    <div class="d-flex align-items-center mb-3">
                        <i class="bi bi-check-circle-fill text-success fs-4 me-3"></i>
                        <div>
                            <strong class="d-block">Strong Password</strong>
                            <small class="text-muted">Last changed 15 days ago</small>
                        </div>
                    </div>
                    <div class="d-flex align-items-center">
                        <i class="bi bi-check-circle-fill text-success fs-4 me-3"></i>
                        <div>
                            <strong class="d-block">Email Verified</strong>
                            <small class="text-muted">admin@cloudops.local</small>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Profile Forms -->
        <div class="col-lg-8">
            <!-- Personal Information -->
            <div class="card shadow-sm mb-4">
                <div class="card-header">
                    <h5 class="mb-0"><i class="bi bi-person-badge me-2"></i>Personal Information</h5>
                </div>
                <div class="card-body">
                    <form>
                        <div class="row g-3">
                            <div class="col-md-6">
                                <label class="form-label">First Name</label>
                                <input type="text" class="form-control" value="System" placeholder="Enter first name">
                            </div>
                            <div class="col-md-6">
                                <label class="form-label">Last Name</label>
                                <input type="text" class="form-control" value="Administrator" placeholder="Enter last name">
                            </div>
                            <div class="col-md-6">
                                <label class="form-label">Email Address</label>
                                <input type="email" class="form-control" value="admin@cloudops.local" placeholder="Enter email">
                            </div>
                            <div class="col-md-6">
                                <label class="form-label">Phone Number</label>
                                <input type="tel" class="form-control" value="+1 (555) 123-4567" placeholder="Enter phone">
                            </div>
                            <div class="col-12">
                                <label class="form-label">Department</label>
                                <select class="form-select">
                                    <option selected>IT Operations</option>
                                    <option>Security</option>
                                    <option>Development</option>
                                    <option>Management</option>
                                </select>
                            </div>
                            <div class="col-12">
                                <label class="form-label">Bio</label>
                                <textarea class="form-control" rows="3" placeholder="Tell us about yourself">Senior DevOps Engineer with expertise in cloud infrastructure, automation, and security compliance. Responsible for maintaining enterprise-level systems and ensuring 99.9% uptime.</textarea>
                            </div>
                        </div>
                        <hr class="my-4">
                        <div class="d-flex justify-content-end gap-2">
                            <button type="button" class="btn btn-outline-secondary">Cancel</button>
                            <button type="submit" class="btn btn-primary"><i class="bi bi-save me-2"></i>Save Changes</button>
                        </div>
                    </form>
                </div>
            </div>

            <!-- Security Settings -->
            <div class="card shadow-sm mb-4">
                <div class="card-header">
                    <h5 class="mb-0"><i class="bi bi-key me-2"></i>Security Settings</h5>
                </div>
                <div class="card-body">
                    <form>
                        <div class="mb-4">
                            <h6 class="mb-3">Change Password</h6>
                            <div class="row g-3">
                                <div class="col-12">
                                    <label class="form-label">Current Password</label>
                                    <input type="password" class="form-control" placeholder="Enter current password">
                                </div>
                                <div class="col-md-6">
                                    <label class="form-label">New Password</label>
                                    <input type="password" class="form-control" placeholder="Enter new password">
                                </div>
                                <div class="col-md-6">
                                    <label class="form-label">Confirm New Password</label>
                                    <input type="password" class="form-control" placeholder="Confirm new password">
                                </div>
                            </div>
                        </div>

                        <hr class="my-4">

                        <div class="mb-4">
                            <h6 class="mb-3">Two-Factor Authentication</h6>
                            <div class="d-flex align-items-center justify-content-between p-3 bg-light rounded">
                                <div>
                                    <strong class="d-block mb-1">Authenticator App</strong>
                                    <small class="text-muted">Currently enabled via Google Authenticator</small>
                                </div>
                                <button type="button" class="btn btn-sm btn-outline-danger">Disable</button>
                            </div>
                        </div>

                        <hr class="my-4">

                        <div class="mb-4">
                            <h6 class="mb-3">Active Sessions</h6>
                            <div class="alert alert-info border-0">
                                <div class="d-flex align-items-start">
                                    <i class="bi bi-laptop me-3 fs-4"></i>
                                    <div class="flex-grow-1">
                                        <strong class="d-block">Current Session</strong>
                                        <small class="text-muted d-block">IP: 192.168.1.105 • Started: <?php echo date('M j, Y H:i'); ?></small>
                                        <small class="text-muted">Browser: Chrome 121 on Linux</small>
                                    </div>
                                    <span class="badge bg-success">Active</span>
                                </div>
                            </div>
                        </div>

                        <div class="d-flex justify-content-end gap-2">
                            <button type="button" class="btn btn-outline-secondary">Cancel</button>
                            <button type="submit" class="btn btn-primary"><i class="bi bi-shield-check me-2"></i>Update Security</button>
                        </div>
                    </form>
                </div>
            </div>

            <!-- Notification Preferences -->
            <div class="card shadow-sm">
                <div class="card-header">
                    <h5 class="mb-0"><i class="bi bi-bell me-2"></i>Notification Preferences</h5>
                </div>
                <div class="card-body">
                    <div class="form-check form-switch mb-3">
                        <input class="form-check-input" type="checkbox" id="emailNotif" checked>
                        <label class="form-check-label" for="emailNotif">
                            <strong>Email Notifications</strong>
                            <small class="d-block text-muted">Receive email alerts for important events</small>
                        </label>
                    </div>
                    <div class="form-check form-switch mb-3">
                        <input class="form-check-input" type="checkbox" id="securityAlerts" checked>
                        <label class="form-check-label" for="securityAlerts">
                            <strong>Security Alerts</strong>
                            <small class="d-block text-muted">Get notified about security events</small>
                        </label>
                    </div>
                    <div class="form-check form-switch mb-3">
                        <input class="form-check-input" type="checkbox" id="systemUpdates" checked>
                        <label class="form-check-label" for="systemUpdates">
                            <strong>System Updates</strong>
                            <small class="d-block text-muted">Notifications about system maintenance and updates</small>
                        </label>
                    </div>
                    <div class="form-check form-switch">
                        <input class="form-check-input" type="checkbox" id="weeklyReport">
                        <label class="form-check-label" for="weeklyReport">
                            <strong>Weekly Reports</strong>
                            <small class="d-block text-muted">Receive weekly summary reports</small>
                        </label>
                    </div>

                    <hr class="my-4">

                    <div class="d-flex justify-content-end gap-2">
                        <button type="button" class="btn btn-outline-secondary">Reset</button>
                        <button type="button" class="btn btn-primary"><i class="bi bi-save me-2"></i>Save Preferences</button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<?php include '../includes/footer.php'; ?>
