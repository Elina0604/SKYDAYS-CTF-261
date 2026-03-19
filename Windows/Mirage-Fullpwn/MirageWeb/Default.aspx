<%@ Page Language="C#" AutoEventWireup="true" %>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Dashboard &mdash; MirageWeb IT</title>

    <!-- Bootstrap 5 -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css"
          rel="stylesheet"
          integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH"
          crossorigin="anonymous" />

    <!-- Bootstrap Icons -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css"
          rel="stylesheet" />

    <style>
        /* ═══════════════════════════════════════════
           DESIGN TOKENS  (same palette as UploadMetrics)
           ═══════════════════════════════════════════ */
        :root {
            --bg-base:      #0d1117;
            --bg-surface:   #161b22;
            --bg-elevated:  #1c2330;
            --border-color: #30363d;
            --accent:       #2f81f7;
            --accent-hover: #388bfd;
            --accent-glow:  rgba(47, 129, 247, 0.25);
            --text-primary: #e6edf3;
            --text-muted:   #8b949e;
            --success:      #3fb950;
            --warning:      #d29922;
            --danger:       #f85149;
            --sidebar-w:    240px;
            --topbar-h:     56px;
        }

        *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

        html, body {
            height: 100%;
            background: var(--bg-base);
            color: var(--text-primary);
            font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
            font-size: 14px;
        }

        /* ═══════════════════════════════════════════
           TOP NAV BAR
           ═══════════════════════════════════════════ */
        .topbar {
            position: fixed;
            top: 0; left: 0; right: 0;
            height: var(--topbar-h);
            background: var(--bg-surface);
            border-bottom: 1px solid var(--border-color);
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 1.5rem 0 calc(var(--sidebar-w) + 1.5rem);
            z-index: 200;
        }

        .topbar-left {
            display: flex;
            align-items: center;
            gap: .7rem;
        }

        .topbar-left h1 {
            font-size: .95rem;
            font-weight: 600;
            color: var(--text-primary);
            letter-spacing: .01em;
        }

        .topbar-left .page-badge {
            font-size: .7rem;
            font-weight: 500;
            background: var(--bg-elevated);
            border: 1px solid var(--border-color);
            color: var(--text-muted);
            padding: .15rem .55rem;
            border-radius: 20px;
            letter-spacing: .03em;
        }

        .topbar-right {
            display: flex;
            align-items: center;
            gap: 1.3rem;
            font-size: .78rem;
            color: var(--text-muted);
        }

        .topbar-right .live-indicator {
            display: flex;
            align-items: center;
            gap: .4rem;
        }

        .topbar-right .live-dot {
            width: 7px;
            height: 7px;
            border-radius: 50%;
            background: var(--success);
            animation: pulse-dot 2s infinite;
        }

        @keyframes pulse-dot {
            0%, 100% { opacity: 1; box-shadow: 0 0 0 0 rgba(63,185,80,.5); }
            50%       { opacity: .7; box-shadow: 0 0 0 5px rgba(63,185,80,0); }
        }

        .topbar-avatar {
            width: 30px;
            height: 30px;
            background: var(--accent);
            border-radius: 50%;
            display: grid;
            place-items: center;
            font-size: .75rem;
            font-weight: 700;
            color: #fff;
            cursor: pointer;
        }

        /* ═══════════════════════════════════════════
           SIDEBAR
           ═══════════════════════════════════════════ */
        .sidebar {
            position: fixed;
            top: 0; left: 0; bottom: 0;
            width: var(--sidebar-w);
            background: var(--bg-surface);
            border-right: 1px solid var(--border-color);
            display: flex;
            flex-direction: column;
            z-index: 300;
            overflow-y: auto;
        }

        .sidebar-brand {
            display: flex;
            align-items: center;
            gap: .65rem;
            padding: 0 1.2rem;
            height: var(--topbar-h);
            border-bottom: 1px solid var(--border-color);
            flex-shrink: 0;
            text-decoration: none;
        }

        .brand-logo {
            width: 30px;
            height: 30px;
            background: var(--accent);
            border-radius: 8px;
            display: grid;
            place-items: center;
            font-size: .9rem;
            color: #fff;
            flex-shrink: 0;
        }

        .brand-text {
            font-size: .88rem;
            font-weight: 600;
            color: var(--text-primary);
            letter-spacing: .01em;
            line-height: 1.2;
        }

        .brand-text small {
            display: block;
            font-size: .68rem;
            font-weight: 400;
            color: var(--text-muted);
            letter-spacing: .02em;
        }

        /* Sidebar nav sections */
        .sidebar-section {
            padding: 1.1rem .8rem .3rem;
        }

        .sidebar-section-label {
            font-size: .65rem;
            font-weight: 600;
            letter-spacing: .08em;
            text-transform: uppercase;
            color: var(--text-muted);
            padding: 0 .6rem;
            margin-bottom: .4rem;
        }

        .nav-item-link {
            display: flex;
            align-items: center;
            gap: .7rem;
            padding: .5rem .7rem;
            border-radius: 7px;
            text-decoration: none;
            color: var(--text-muted);
            font-size: .84rem;
            font-weight: 450;
            transition: background .15s, color .15s;
            margin-bottom: 2px;
        }

        .nav-item-link i {
            font-size: 1rem;
            width: 18px;
            text-align: center;
            flex-shrink: 0;
        }

        .nav-item-link:hover {
            background: var(--bg-elevated);
            color: var(--text-primary);
        }

        .nav-item-link.active {
            background: rgba(47, 129, 247, .15);
            color: var(--accent);
            font-weight: 600;
        }

        .nav-item-link .nav-badge {
            margin-left: auto;
            font-size: .65rem;
            font-weight: 600;
            background: var(--accent);
            color: #fff;
            padding: .1rem .45rem;
            border-radius: 20px;
        }

        .sidebar-footer {
            margin-top: auto;
            padding: .9rem 1.2rem;
            border-top: 1px solid var(--border-color);
            font-size: .74rem;
            color: var(--text-muted);
        }

        /* ═══════════════════════════════════════════
           MAIN CONTENT AREA
           ═══════════════════════════════════════════ */
        .main-content {
            margin-left: var(--sidebar-w);
            padding-top: var(--topbar-h);
            min-height: 100vh;
        }

        .content-inner {
            padding: 1.8rem 2rem 3rem;
        }

        /* ═══════════════════════════════════════════
           PAGE HEADER
           ═══════════════════════════════════════════ */
        .page-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 1.6rem;
            flex-wrap: wrap;
            gap: 1rem;
        }

        .page-header-title h2 {
            font-size: 1.25rem;
            font-weight: 700;
            color: var(--text-primary);
            margin-bottom: .2rem;
        }

        .page-header-title p {
            font-size: .8rem;
            color: var(--text-muted);
            margin: 0;
        }

        .btn-refresh {
            display: flex;
            align-items: center;
            gap: .45rem;
            padding: .45rem .9rem;
            background: var(--bg-elevated);
            border: 1px solid var(--border-color);
            border-radius: 7px;
            color: var(--text-primary);
            font-size: .8rem;
            font-weight: 500;
            cursor: pointer;
            transition: border-color .15s, background .15s;
        }

        .btn-refresh:hover {
            border-color: var(--accent);
            background: rgba(47,129,247,.08);
            color: var(--accent);
        }

        /* ═══════════════════════════════════════════
           KPI STAT CARDS
           ═══════════════════════════════════════════ */
        .stat-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 1rem;
            margin-bottom: 1.5rem;
        }

        .stat-card {
            background: var(--bg-surface);
            border: 1px solid var(--border-color);
            border-radius: 10px;
            padding: 1.1rem 1.2rem;
            position: relative;
            overflow: hidden;
            transition: border-color .2s;
        }

        .stat-card:hover { border-color: #484f58; }

        .stat-card-top {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: .7rem;
        }

        .stat-label {
            font-size: .73rem;
            font-weight: 500;
            color: var(--text-muted);
            letter-spacing: .03em;
            text-transform: uppercase;
        }

        .stat-icon {
            width: 32px;
            height: 32px;
            border-radius: 8px;
            display: grid;
            place-items: center;
            font-size: .95rem;
        }

        .stat-value {
            font-size: 1.7rem;
            font-weight: 700;
            color: var(--text-primary);
            line-height: 1;
            margin-bottom: .45rem;
        }

        .stat-value span {
            font-size: .85rem;
            font-weight: 400;
            color: var(--text-muted);
        }

        .stat-trend {
            display: flex;
            align-items: center;
            gap: .3rem;
            font-size: .73rem;
        }

        .trend-up   { color: var(--danger); }
        .trend-down { color: var(--success); }
        .trend-flat { color: var(--text-muted); }

        /* Thin sparkline strip at bottom */
        .stat-spark {
            position: absolute;
            bottom: 0; left: 0; right: 0;
            height: 3px;
            border-radius: 0 0 10px 10px;
        }

        /* ═══════════════════════════════════════════
           RESOURCE GAUGE CARDS (CPU / RAM / DISK)
           ═══════════════════════════════════════════ */
        .resource-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 1rem;
            margin-bottom: 1.5rem;
        }

        .resource-card {
            background: var(--bg-surface);
            border: 1px solid var(--border-color);
            border-radius: 10px;
            padding: 1.2rem 1.4rem 1rem;
        }

        .resource-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: .9rem;
        }

        .resource-title {
            display: flex;
            align-items: center;
            gap: .5rem;
            font-size: .8rem;
            font-weight: 600;
            color: var(--text-primary);
            text-transform: uppercase;
            letter-spacing: .04em;
        }

        .resource-title i { font-size: 1rem; }

        .resource-pct {
            font-size: 1.5rem;
            font-weight: 700;
            color: var(--text-primary);
        }

        .resource-bar-wrap {
            height: 8px;
            background: var(--bg-elevated);
            border-radius: 20px;
            overflow: hidden;
            margin-bottom: .6rem;
            border: 1px solid var(--border-color);
        }

        .resource-bar-fill {
            height: 100%;
            border-radius: 20px;
            transition: width 1.2s cubic-bezier(.4,0,.2,1);
        }

        .resource-meta {
            font-size: .73rem;
            color: var(--text-muted);
            display: flex;
            justify-content: space-between;
        }

        /* ═══════════════════════════════════════════
           CHART CARDS
           ═══════════════════════════════════════════ */
        .chart-row {
            display: grid;
            grid-template-columns: 2fr 1fr;
            gap: 1rem;
            margin-bottom: 1.5rem;
        }

        .chart-row-bottom {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 1rem;
            margin-bottom: 1.5rem;
        }

        .chart-card {
            background: var(--bg-surface);
            border: 1px solid var(--border-color);
            border-radius: 10px;
            padding: 1.2rem 1.4rem 1rem;
        }

        .chart-card-header {
            display: flex;
            align-items: flex-start;
            justify-content: space-between;
            margin-bottom: 1rem;
            gap: .5rem;
        }

        .chart-card-title {
            font-size: .85rem;
            font-weight: 600;
            color: var(--text-primary);
            margin-bottom: .15rem;
        }

        .chart-card-subtitle {
            font-size: .73rem;
            color: var(--text-muted);
        }

        .chart-legend {
            display: flex;
            gap: .8rem;
            flex-wrap: wrap;
        }

        .legend-item {
            display: flex;
            align-items: center;
            gap: .3rem;
            font-size: .72rem;
            color: var(--text-muted);
        }

        .legend-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            flex-shrink: 0;
        }

        .chart-wrap {
            position: relative;
        }

        /* ═══════════════════════════════════════════
           EVENTS TABLE CARD
           ═══════════════════════════════════════════ */
        .events-card {
            background: var(--bg-surface);
            border: 1px solid var(--border-color);
            border-radius: 10px;
            overflow: hidden;
        }

        .events-card-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 1rem 1.4rem;
            border-bottom: 1px solid var(--border-color);
        }

        .events-card-header h3 {
            font-size: .85rem;
            font-weight: 600;
            color: var(--text-primary);
            margin: 0;
        }

        .events-card-header .view-all {
            font-size: .75rem;
            color: var(--accent);
            text-decoration: none;
        }

        .events-card-header .view-all:hover { text-decoration: underline; }

        .events-table {
            width: 100%;
            border-collapse: collapse;
        }

        .events-table thead tr {
            background: var(--bg-elevated);
        }

        .events-table th {
            padding: .55rem 1.4rem;
            font-size: .7rem;
            font-weight: 600;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: .05em;
            text-align: left;
            border-bottom: 1px solid var(--border-color);
            white-space: nowrap;
        }

        .events-table td {
            padding: .65rem 1.4rem;
            font-size: .8rem;
            color: var(--text-primary);
            border-bottom: 1px solid var(--border-color);
            vertical-align: middle;
        }

        .events-table tbody tr:last-child td { border-bottom: none; }

        .events-table tbody tr:hover td { background: var(--bg-elevated); }

        .severity-badge {
            display: inline-flex;
            align-items: center;
            gap: .3rem;
            padding: .18rem .55rem;
            border-radius: 20px;
            font-size: .68rem;
            font-weight: 600;
        }

        .severity-critical { background: rgba(248,81,73,.15); color: var(--danger); }
        .severity-warning  { background: rgba(210,153,34,.15); color: var(--warning); }
        .severity-info     { background: rgba(47,129,247,.15); color: var(--accent); }
        .severity-ok       { background: rgba(63,185,80,.15);  color: var(--success); }

        .host-chip {
            font-family: 'Consolas', 'Courier New', monospace;
            font-size: .75rem;
            color: var(--text-muted);
        }

        /* ═══════════════════════════════════════════
           PAGE FOOTER
           ═══════════════════════════════════════════ */
        .page-footer {
            padding: .9rem 2rem;
            border-top: 1px solid var(--border-color);
            font-size: .72rem;
            color: var(--text-muted);
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: var(--bg-surface);
            flex-wrap: wrap;
            gap: .5rem;
        }

        /* ═══════════════════════════════════════════
           RESPONSIVE
           ═══════════════════════════════════════════ */
        @media (max-width: 900px) {
            .resource-grid { grid-template-columns: 1fr; }
            .chart-row     { grid-template-columns: 1fr; }
            .chart-row-bottom { grid-template-columns: 1fr; }
        }

        @media (max-width: 768px) {
            :root { --sidebar-w: 0px; }
            .sidebar { transform: translateX(-240px); transition: transform .25s; }
            .sidebar.open { transform: translateX(0); --sidebar-w: 240px; }
            .topbar { padding-left: 1.5rem; }
        }
    </style>
</head>
<body>

    <!-- ══════════════════════════════════
         SIDEBAR
         ══════════════════════════════════ -->
    <aside class="sidebar" id="sidebar">

        <a href="Default.aspx" class="sidebar-brand">
            <div class="brand-logo"><i class="bi bi-grid-3x3-gap-fill"></i></div>
            <div class="brand-text">
                MirageWeb
                <small>IT Operations</small>
            </div>
        </a>

        <!-- MAIN -->
        <div class="sidebar-section">
            <div class="sidebar-section-label">Main</div>
            <a href="Default.aspx" class="nav-item-link active">
                <i class="bi bi-speedometer2"></i> Dashboard
            </a>
            <a href="#" class="nav-item-link">
                <i class="bi bi-activity"></i> Live Monitor
                <span class="nav-badge">Live</span>
            </a>
            <a href="#" class="nav-item-link">
                <i class="bi bi-server"></i> Servers
            </a>
            <a href="#" class="nav-item-link">
                <i class="bi bi-diagram-3"></i> Network
            </a>
        </div>

        <!-- REPORTS -->
        <div class="sidebar-section">
            <div class="sidebar-section-label">Reports</div>
            <a href="UploadMetrics.aspx" class="nav-item-link">
                <i class="bi bi-cloud-arrow-up"></i> Upload Metrics
            </a>
            <a href="#" class="nav-item-link">
                <i class="bi bi-file-earmark-bar-graph"></i> Analytics
            </a>
            <a href="#" class="nav-item-link">
                <i class="bi bi-download"></i> Export Data
            </a>
        </div>

        <!-- SYSTEM -->
        <div class="sidebar-section">
            <div class="sidebar-section-label">System</div>
            <a href="#" class="nav-item-link">
                <i class="bi bi-bell"></i> Alerts
                <span class="nav-badge">3</span>
            </a>
            <a href="#" class="nav-item-link">
                <i class="bi bi-people"></i> Users
            </a>
            <a href="#" class="nav-item-link">
                <i class="bi bi-gear"></i> Settings
            </a>
        </div>

        <div class="sidebar-footer">
            v2.4.1 &middot; Build 20260310
        </div>

    </aside>

    <!-- ══════════════════════════════════
         TOP NAV BAR
         ══════════════════════════════════ -->
    <nav class="topbar">
        <div class="topbar-left">
            <h1>Overview</h1>
            <span class="page-badge">PRODUCTION</span>
        </div>
        <div class="topbar-right">
            <span class="live-indicator">
                <span class="live-dot"></span> Live
            </span>
            <span><i class="bi bi-clock me-1"></i><span id="liveClock"></span></span>
            <div class="topbar-avatar" title="Admin">AD</div>
        </div>
    </nav>

    <!-- ══════════════════════════════════
         MAIN CONTENT
         ══════════════════════════════════ -->
    <div class="main-content">
        <div class="content-inner">

            <!-- Page Header -->
            <div class="page-header">
                <div class="page-header-title">
                    <h2>System Dashboard</h2>
                    <p>Real-time infrastructure overview &mdash; last refreshed <span id="lastRefresh"></span></p>
                </div>
                <button class="btn-refresh" onclick="refreshAll()">
                    <i class="bi bi-arrow-clockwise" id="refreshIcon"></i> Refresh
                </button>
            </div>

            <!-- ── KPI Stat Cards ── -->
            <div class="stat-grid">

                <div class="stat-card">
                    <div class="stat-card-top">
                        <span class="stat-label">Uptime</span>
                        <div class="stat-icon" style="background:rgba(63,185,80,.12); color:var(--success);">
                            <i class="bi bi-check-circle-fill"></i>
                        </div>
                    </div>
                    <div class="stat-value">99.97<span>%</span></div>
                    <div class="stat-trend trend-flat"><i class="bi bi-dash"></i> Stable last 30 days</div>
                    <div class="stat-spark" style="background:var(--success);"></div>
                </div>

                <div class="stat-card">
                    <div class="stat-card-top">
                        <span class="stat-label">Active Servers</span>
                        <div class="stat-icon" style="background:rgba(47,129,247,.12); color:var(--accent);">
                            <i class="bi bi-server"></i>
                        </div>
                    </div>
                    <div class="stat-value">24<span> / 26</span></div>
                    <div class="stat-trend trend-flat"><i class="bi bi-dash"></i> 2 in maintenance</div>
                    <div class="stat-spark" style="background:var(--accent);"></div>
                </div>

                <div class="stat-card">
                    <div class="stat-card-top">
                        <span class="stat-label">Open Alerts</span>
                        <div class="stat-icon" style="background:rgba(210,153,34,.12); color:var(--warning);">
                            <i class="bi bi-exclamation-triangle-fill"></i>
                        </div>
                    </div>
                    <div class="stat-value" id="kpiAlerts">3</div>
                    <div class="stat-trend trend-up"><i class="bi bi-arrow-up-short"></i> +2 since yesterday</div>
                    <div class="stat-spark" style="background:var(--warning);"></div>
                </div>

                <div class="stat-card">
                    <div class="stat-card-top">
                        <span class="stat-label">Avg Response</span>
                        <div class="stat-icon" style="background:rgba(47,129,247,.12); color:var(--accent);">
                            <i class="bi bi-lightning-charge-fill"></i>
                        </div>
                    </div>
                    <div class="stat-value" id="kpiResponse">142<span> ms</span></div>
                    <div class="stat-trend trend-down"><i class="bi bi-arrow-down-short"></i> -18 ms from avg</div>
                    <div class="stat-spark" style="background:var(--accent);"></div>
                </div>

                <div class="stat-card">
                    <div class="stat-card-top">
                        <span class="stat-label">Network I/O</span>
                        <div class="stat-icon" style="background:rgba(63,185,80,.12); color:var(--success);">
                            <i class="bi bi-ethernet"></i>
                        </div>
                    </div>
                    <div class="stat-value" id="kpiNet">3.2<span> Gbps</span></div>
                    <div class="stat-trend trend-up"><i class="bi bi-arrow-up-short"></i> Peak hour traffic</div>
                    <div class="stat-spark" style="background:var(--success);"></div>
                </div>

                <div class="stat-card">
                    <div class="stat-card-top">
                        <span class="stat-label">DB Queries/s</span>
                        <div class="stat-icon" style="background:rgba(248,81,73,.12); color:var(--danger);">
                            <i class="bi bi-database-fill"></i>
                        </div>
                    </div>
                    <div class="stat-value" id="kpiDb">1,847</div>
                    <div class="stat-trend trend-up"><i class="bi bi-arrow-up-short"></i> High load detected</div>
                    <div class="stat-spark" style="background:var(--danger);"></div>
                </div>

            </div>

            <!-- ── Resource Gauges: CPU / RAM / Disk ── -->
            <div class="resource-grid">

                <!-- CPU -->
                <div class="resource-card">
                    <div class="resource-header">
                        <div class="resource-title" style="color:var(--warning);">
                            <i class="bi bi-cpu-fill" style="color:var(--warning);"></i> CPU Usage
                        </div>
                        <div class="resource-pct" id="cpuPct">68%</div>
                    </div>
                    <div class="resource-bar-wrap">
                        <div class="resource-bar-fill" id="cpuBar"
                             style="width:68%; background:var(--warning);"></div>
                    </div>
                    <div class="resource-meta">
                        <span>16 cores &middot; 3.6 GHz</span>
                        <span id="cpuDetail">Avg across 24 servers</span>
                    </div>
                </div>

                <!-- RAM -->
                <div class="resource-card">
                    <div class="resource-header">
                        <div class="resource-title" style="color:var(--accent);">
                            <i class="bi bi-memory" style="color:var(--accent);"></i> Memory Usage
                        </div>
                        <div class="resource-pct" id="ramPct">54%</div>
                    </div>
                    <div class="resource-bar-wrap">
                        <div class="resource-bar-fill" id="ramBar"
                             style="width:54%; background:var(--accent);"></div>
                    </div>
                    <div class="resource-meta">
                        <span>432 GB used of 800 GB</span>
                        <span id="ramDetail">Pool avg</span>
                    </div>
                </div>

                <!-- Disk -->
                <div class="resource-card">
                    <div class="resource-header">
                        <div class="resource-title" style="color:var(--danger);">
                            <i class="bi bi-hdd-fill" style="color:var(--danger);"></i> Disk Usage
                        </div>
                        <div class="resource-pct" id="diskPct">81%</div>
                    </div>
                    <div class="resource-bar-wrap">
                        <div class="resource-bar-fill" id="diskBar"
                             style="width:81%; background:var(--danger);"></div>
                    </div>
                    <div class="resource-meta">
                        <span>64.8 TB used of 80 TB</span>
                        <span id="diskDetail">SAN pool</span>
                    </div>
                </div>

            </div>

            <!-- ── Chart Row 1: Line + Doughnut ── -->
            <div class="chart-row">

                <!-- CPU / RAM line chart -->
                <div class="chart-card">
                    <div class="chart-card-header">
                        <div>
                            <div class="chart-card-title">CPU &amp; Memory &mdash; 24h Trend</div>
                            <div class="chart-card-subtitle">Averaged across all production servers</div>
                        </div>
                        <div class="chart-legend">
                            <div class="legend-item">
                                <div class="legend-dot" style="background:#d29922;"></div> CPU
                            </div>
                            <div class="legend-item">
                                <div class="legend-dot" style="background:#2f81f7;"></div> RAM
                            </div>
                        </div>
                    </div>
                    <div class="chart-wrap" style="height:220px;">
                        <canvas id="trendChart"></canvas>
                    </div>
                </div>

                <!-- Server status doughnut -->
                <div class="chart-card">
                    <div class="chart-card-header">
                        <div>
                            <div class="chart-card-title">Server Health</div>
                            <div class="chart-card-subtitle">Current status distribution</div>
                        </div>
                    </div>
                    <div class="chart-wrap" style="height:185px;">
                        <canvas id="healthChart"></canvas>
                    </div>
                    <div class="chart-legend mt-2" style="justify-content:center; gap:1.1rem;">
                        <div class="legend-item"><div class="legend-dot" style="background:#3fb950;"></div> Healthy (18)</div>
                        <div class="legend-item"><div class="legend-dot" style="background:#d29922;"></div> Warning (6)</div>
                        <div class="legend-item"><div class="legend-dot" style="background:#f85149;"></div> Critical (2)</div>
                    </div>
                </div>

            </div>

            <!-- ── Chart Row 2: Bar + Line ── -->
            <div class="chart-row-bottom">

                <!-- Request volume bar chart -->
                <div class="chart-card">
                    <div class="chart-card-header">
                        <div>
                            <div class="chart-card-title">Request Volume &mdash; Last 7 Days</div>
                            <div class="chart-card-subtitle">Total HTTP requests per day (millions)</div>
                        </div>
                    </div>
                    <div class="chart-wrap" style="height:200px;">
                        <canvas id="reqChart"></canvas>
                    </div>
                </div>

                <!-- Network throughput line -->
                <div class="chart-card">
                    <div class="chart-card-header">
                        <div>
                            <div class="chart-card-title">Network Throughput &mdash; 6h</div>
                            <div class="chart-card-subtitle">Inbound vs outbound (Gbps)</div>
                        </div>
                        <div class="chart-legend">
                            <div class="legend-item">
                                <div class="legend-dot" style="background:#3fb950;"></div> In
                            </div>
                            <div class="legend-item">
                                <div class="legend-dot" style="background:#2f81f7;"></div> Out
                            </div>
                        </div>
                    </div>
                    <div class="chart-wrap" style="height:200px;">
                        <canvas id="netChart"></canvas>
                    </div>
                </div>

            </div>

            <!-- ── Recent Events Table ── -->
            <div class="events-card">
                <div class="events-card-header">
                    <h3><i class="bi bi-journal-text me-2"></i>Recent System Events</h3>
                    <a href="#" class="view-all">View all &rarr;</a>
                </div>
                <table class="events-table">
                    <thead>
                        <tr>
                            <th>Time</th>
                            <th>Severity</th>
                            <th>Host</th>
                            <th>Event</th>
                            <th>Category</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td style="color:var(--text-muted); font-size:.75rem;">02:47:13</td>
                            <td><span class="severity-badge severity-critical"><i class="bi bi-x-circle-fill"></i> Critical</span></td>
                            <td><span class="host-chip">srv-db-03</span></td>
                            <td>Disk I/O wait exceeded 90% threshold for 5 minutes</td>
                            <td style="color:var(--text-muted);">Storage</td>
                        </tr>
                        <tr>
                            <td style="color:var(--text-muted); font-size:.75rem;">02:31:55</td>
                            <td><span class="severity-badge severity-warning"><i class="bi bi-exclamation-triangle-fill"></i> Warning</span></td>
                            <td><span class="host-chip">lb-prod-01</span></td>
                            <td>Connection pool nearing capacity (92 / 100)</td>
                            <td style="color:var(--text-muted);">Network</td>
                        </tr>
                        <tr>
                            <td style="color:var(--text-muted); font-size:.75rem;">02:18:40</td>
                            <td><span class="severity-badge severity-info"><i class="bi bi-info-circle-fill"></i> Info</span></td>
                            <td><span class="host-chip">srv-app-07</span></td>
                            <td>Scheduled certificate renewal completed successfully</td>
                            <td style="color:var(--text-muted);">Security</td>
                        </tr>
                        <tr>
                            <td style="color:var(--text-muted); font-size:.75rem;">01:59:02</td>
                            <td><span class="severity-badge severity-warning"><i class="bi bi-exclamation-triangle-fill"></i> Warning</span></td>
                            <td><span class="host-chip">srv-cache-02</span></td>
                            <td>Redis eviction rate spiked to 14k ops/s</td>
                            <td style="color:var(--text-muted);">Cache</td>
                        </tr>
                        <tr>
                            <td style="color:var(--text-muted); font-size:.75rem;">01:44:17</td>
                            <td><span class="severity-badge severity-ok"><i class="bi bi-check-circle-fill"></i> Resolved</span></td>
                            <td><span class="host-chip">srv-web-12</span></td>
                            <td>High CPU alert cleared &mdash; load normalised</td>
                            <td style="color:var(--text-muted);">Compute</td>
                        </tr>
                        <tr>
                            <td style="color:var(--text-muted); font-size:.75rem;">01:30:09</td>
                            <td><span class="severity-badge severity-critical"><i class="bi bi-x-circle-fill"></i> Critical</span></td>
                            <td><span class="host-chip">srv-db-01</span></td>
                            <td>Replication lag exceeded 30s on replica node</td>
                            <td style="color:var(--text-muted);">Database</td>
                        </tr>
                        <tr>
                            <td style="color:var(--text-muted); font-size:.75rem;">01:12:33</td>
                            <td><span class="severity-badge severity-info"><i class="bi bi-info-circle-fill"></i> Info</span></td>
                            <td><span class="host-chip">backup-srv-01</span></td>
                            <td>Nightly full backup completed &mdash; 2.3 TB written</td>
                            <td style="color:var(--text-muted);">Backup</td>
                        </tr>
                    </tbody>
                </table>
            </div>

        </div><!-- /content-inner -->

        <footer class="page-footer">
            <span>&copy; 2026 MirageWeb &mdash; IT Operations &middot; All rights reserved</span>
            <span>Environment: <strong style="color:var(--text-primary);">PRODUCTION</strong> &middot; Node: <strong style="color:var(--text-primary);">mw-dash-01</strong></span>
        </footer>
    </div><!-- /main-content -->

    <!-- Bootstrap 5 JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"
            integrity="sha384-YvpcrYf0tY3lHB60NNkmXc4s9bIOgUxi8T/jzmQ7GDZQ4GVdE6GEbNFi1DZ0dLe"
            crossorigin="anonymous"></script>

    <!-- Chart.js -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.3/dist/chart.umd.min.js"></script>

    <script>
    /* ═══════════════════════════════════════
       CHART.JS GLOBAL DEFAULTS
       ═══════════════════════════════════════ */
    Chart.defaults.color          = '#8b949e';
    Chart.defaults.borderColor    = '#30363d';
    Chart.defaults.font.family    = "'Segoe UI', system-ui, sans-serif";
    Chart.defaults.font.size      = 11;
    Chart.defaults.plugins.legend.display = false;

    /* Shared tick style */
    const tickStyle = { color: '#8b949e', font: { size: 10 } };
    const gridStyle = { color: '#21262d' };

    /* ── Helpers ── */
    function randBetween(min, max) {
        return Math.random() * (max - min) + min;
    }

    function makeHours(n) {
        const labels = [];
        const now = new Date();
        for (let i = n - 1; i >= 0; i--) {
            const d = new Date(now - i * 3600000);
            labels.push(d.getHours().toString().padStart(2, '0') + ':00');
        }
        return labels;
    }

    function makeDays(n) {
        const labels = [];
        const days = ['Sun','Mon','Tue','Wed','Thu','Fri','Sat'];
        const now = new Date();
        for (let i = n - 1; i >= 0; i--) {
            const d = new Date(now - i * 86400000);
            labels.push(days[d.getDay()]);
        }
        return labels;
    }

    /* ═══════════════════════════════════════
       1. CPU & RAM TREND (Line, 24 h)
       ═══════════════════════════════════════ */
    (function () {
        const labels = makeHours(24);
        const cpu = labels.map(() => randBetween(40, 85).toFixed(1));
        const ram = labels.map(() => randBetween(45, 70).toFixed(1));

        new Chart(document.getElementById('trendChart'), {
            type: 'line',
            data: {
                labels,
                datasets: [
                    {
                        label: 'CPU %',
                        data: cpu,
                        borderColor: '#d29922',
                        backgroundColor: 'rgba(210,153,34,.08)',
                        borderWidth: 2,
                        pointRadius: 2,
                        pointHoverRadius: 5,
                        tension: .4,
                        fill: true,
                    },
                    {
                        label: 'RAM %',
                        data: ram,
                        borderColor: '#2f81f7',
                        backgroundColor: 'rgba(47,129,247,.06)',
                        borderWidth: 2,
                        pointRadius: 2,
                        pointHoverRadius: 5,
                        tension: .4,
                        fill: true,
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                interaction: { mode: 'index', intersect: false },
                plugins: {
                    tooltip: {
                        backgroundColor: '#1c2330',
                        borderColor: '#30363d',
                        borderWidth: 1,
                        titleColor: '#e6edf3',
                        bodyColor: '#8b949e',
                        callbacks: { label: ctx => ` ${ctx.dataset.label}: ${ctx.parsed.y}%` }
                    }
                },
                scales: {
                    x: { ticks: tickStyle, grid: gridStyle },
                    y: {
                        min: 0, max: 100,
                        ticks: { ...tickStyle, callback: v => v + '%' },
                        grid: gridStyle
                    }
                }
            }
        });
    })();

    /* ═══════════════════════════════════════
       2. SERVER HEALTH (Doughnut)
       ═══════════════════════════════════════ */
    (function () {
        new Chart(document.getElementById('healthChart'), {
            type: 'doughnut',
            data: {
                labels: ['Healthy', 'Warning', 'Critical'],
                datasets: [{
                    data: [18, 6, 2],
                    backgroundColor: ['#3fb950', '#d29922', '#f85149'],
                    borderWidth: 3,
                    borderColor: '#161b22',
                    hoverBorderColor: '#161b22',
                    hoverOffset: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                cutout: '68%',
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        backgroundColor: '#1c2330',
                        borderColor: '#30363d',
                        borderWidth: 1,
                        titleColor: '#e6edf3',
                        bodyColor: '#8b949e',
                        callbacks: { label: ctx => ` ${ctx.label}: ${ctx.parsed} servers` }
                    }
                }
            }
        });
    })();

    /* ═══════════════════════════════════════
       3. REQUEST VOLUME (Bar, 7 days)
       ═══════════════════════════════════════ */
    (function () {
        const labels = makeDays(7);
        const data   = labels.map(() => parseFloat(randBetween(14, 32).toFixed(1)));

        new Chart(document.getElementById('reqChart'), {
            type: 'bar',
            data: {
                labels,
                datasets: [{
                    label: 'Requests (M)',
                    data,
                    backgroundColor: 'rgba(47,129,247,.55)',
                    hoverBackgroundColor: '#2f81f7',
                    borderRadius: 5,
                    borderSkipped: false,
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    tooltip: {
                        backgroundColor: '#1c2330',
                        borderColor: '#30363d',
                        borderWidth: 1,
                        titleColor: '#e6edf3',
                        bodyColor: '#8b949e',
                        callbacks: { label: ctx => ` ${ctx.parsed.y}M requests` }
                    }
                },
                scales: {
                    x: { ticks: tickStyle, grid: { display: false } },
                    y: {
                        ticks: { ...tickStyle, callback: v => v + 'M' },
                        grid: gridStyle
                    }
                }
            }
        });
    })();

    /* ═══════════════════════════════════════
       4. NETWORK THROUGHPUT (Line, 6 h)
       ═══════════════════════════════════════ */
    (function () {
        const labels = makeHours(6);
        const inbound  = labels.map(() => parseFloat(randBetween(1.2, 4.5).toFixed(2)));
        const outbound = labels.map(() => parseFloat(randBetween(0.8, 3.2).toFixed(2)));

        new Chart(document.getElementById('netChart'), {
            type: 'line',
            data: {
                labels,
                datasets: [
                    {
                        label: 'Inbound',
                        data: inbound,
                        borderColor: '#3fb950',
                        backgroundColor: 'rgba(63,185,80,.07)',
                        borderWidth: 2,
                        pointRadius: 3,
                        pointHoverRadius: 5,
                        tension: .4,
                        fill: true
                    },
                    {
                        label: 'Outbound',
                        data: outbound,
                        borderColor: '#2f81f7',
                        backgroundColor: 'rgba(47,129,247,.06)',
                        borderWidth: 2,
                        pointRadius: 3,
                        pointHoverRadius: 5,
                        tension: .4,
                        fill: true
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                interaction: { mode: 'index', intersect: false },
                plugins: {
                    tooltip: {
                        backgroundColor: '#1c2330',
                        borderColor: '#30363d',
                        borderWidth: 1,
                        titleColor: '#e6edf3',
                        bodyColor: '#8b949e',
                        callbacks: { label: ctx => ` ${ctx.dataset.label}: ${ctx.parsed.y} Gbps` }
                    }
                },
                scales: {
                    x: { ticks: tickStyle, grid: gridStyle },
                    y: {
                        ticks: { ...tickStyle, callback: v => v + ' G' },
                        grid: gridStyle
                    }
                }
            }
        });
    })();

    /* ═══════════════════════════════════════
       LIVE CLOCK
       ═══════════════════════════════════════ */
    function updateClock() {
        document.getElementById('liveClock').textContent =
            new Date().toLocaleTimeString('en-GB', { hour12: false });
    }
    updateClock();
    setInterval(updateClock, 1000);

    /* ═══════════════════════════════════════
       LAST REFRESH LABEL
       ═══════════════════════════════════════ */
    function setRefreshLabel() {
        const now = new Date();
        document.getElementById('lastRefresh').textContent =
            'at ' + now.toLocaleTimeString('en-GB', { hour12: false });
    }
    setRefreshLabel();

    /* ═══════════════════════════════════════
       SIMULATED LIVE METRICS UPDATE
       ═══════════════════════════════════════ */
    function randomWalk(current, min, max, step) {
        const next = current + (Math.random() - 0.5) * step * 2;
        return Math.min(max, Math.max(min, next));
    }

    let cpuVal  = 68;
    let ramVal  = 54;
    let diskVal = 81;

    setInterval(function () {
        cpuVal  = randomWalk(cpuVal,  20, 95, 3);
        ramVal  = randomWalk(ramVal,  30, 90, 2);
        diskVal = randomWalk(diskVal, 70, 95, 1);

        document.getElementById('cpuPct').textContent  = cpuVal.toFixed(0)  + '%';
        document.getElementById('ramPct').textContent  = ramVal.toFixed(0)  + '%';
        document.getElementById('diskPct').textContent = diskVal.toFixed(0) + '%';

        document.getElementById('cpuBar').style.width  = cpuVal  + '%';
        document.getElementById('ramBar').style.width  = ramVal  + '%';
        document.getElementById('diskBar').style.width = diskVal + '%';

        /* Response time flicker */
        const resp = Math.round(randomWalk(142, 80, 320, 20));
        document.getElementById('kpiResponse').innerHTML =
            resp + '<span> ms</span>';

        /* Network */
        const net = randomWalk(3.2, 1.5, 5.5, .3);
        document.getElementById('kpiNet').innerHTML =
            net.toFixed(1) + '<span> Gbps</span>';

        /* DB queries */
        const db = Math.round(randomWalk(1847, 800, 3200, 120));
        document.getElementById('kpiDb').textContent =
            db.toLocaleString('en-US');

    }, 3000);

    /* ═══════════════════════════════════════
       REFRESH BUTTON — spin icon + reset label
       ═══════════════════════════════════════ */
    function refreshAll() {
        const icon = document.getElementById('refreshIcon');
        icon.style.transition = 'transform .6s ease';
        icon.style.transform  = 'rotate(360deg)';
        setTimeout(function () {
            icon.style.transition = 'none';
            icon.style.transform  = 'rotate(0deg)';
        }, 650);
        setRefreshLabel();
    }
    </script>
</body>
</html>
