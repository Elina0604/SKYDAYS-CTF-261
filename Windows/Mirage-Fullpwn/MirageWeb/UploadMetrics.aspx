<%@ Page Language="C#" AutoEventWireup="true" CodeFile="UploadMetrics.aspx.cs" Inherits="UploadMetrics" %>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Upload Metrics &mdash; IT Dashboard</title>

    <!-- Bootstrap 5 -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css"
          rel="stylesheet"
          integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH"
          crossorigin="anonymous" />

    <!-- Bootstrap Icons -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css"
          rel="stylesheet" />

    <style>
        /* ── Base ── */
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
            --danger:       #f85149;
        }

        *, *::before, *::after { box-sizing: border-box; }

        html, body {
            height: 100%;
            margin: 0;
            background-color: var(--bg-base);
            color: var(--text-primary);
            font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
        }

        /* ── Top nav bar ── */
        .topbar {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 2rem;
            height: 56px;
            background: var(--bg-surface);
            border-bottom: 1px solid var(--border-color);
            position: sticky;
            top: 0;
            z-index: 100;
        }

        .topbar-brand {
            display: flex;
            align-items: center;
            gap: .6rem;
            font-weight: 600;
            font-size: 1rem;
            color: var(--text-primary);
            text-decoration: none;
            letter-spacing: .02em;
        }

        .topbar-brand .brand-icon {
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

        .topbar-meta {
            display: flex;
            align-items: center;
            gap: 1.2rem;
            font-size: .8rem;
            color: var(--text-muted);
        }

        .topbar-meta .badge-env {
            background: var(--bg-elevated);
            border: 1px solid var(--border-color);
            color: var(--text-muted);
            padding: .2rem .6rem;
            border-radius: 20px;
            font-size: .72rem;
            font-weight: 500;
            letter-spacing: .03em;
        }

        /* ── Breadcrumb strip ── */
        .breadcrumb-strip {
            padding: .6rem 2rem;
            background: var(--bg-surface);
            border-bottom: 1px solid var(--border-color);
            font-size: .78rem;
        }

        .breadcrumb-strip .breadcrumb {
            margin: 0;
            --bs-breadcrumb-divider-color: var(--text-muted);
            --bs-breadcrumb-item-active-color: var(--text-primary);
        }

        .breadcrumb-strip .breadcrumb-item a {
            color: var(--accent);
            text-decoration: none;
        }

        .breadcrumb-strip .breadcrumb-item a:hover {
            text-decoration: underline;
        }

        /* ── Main content ── */
        .page-wrapper {
            min-height: calc(100vh - 56px - 37px);
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 3rem 1rem;
        }

        /* ── Upload card ── */
        .upload-card {
            width: 100%;
            max-width: 520px;
            background: var(--bg-surface);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 2.4rem 2.6rem 2.8rem;
            box-shadow: 0 8px 40px rgba(0,0,0,.45);
        }

        .upload-card-header {
            display: flex;
            align-items: flex-start;
            gap: 1rem;
            margin-bottom: 1.8rem;
        }

        .upload-card-icon {
            width: 46px;
            height: 46px;
            background: var(--bg-elevated);
            border: 1px solid var(--border-color);
            border-radius: 10px;
            display: grid;
            place-items: center;
            font-size: 1.3rem;
            color: var(--accent);
            flex-shrink: 0;
        }

        .upload-card-title {
            font-size: 1.15rem;
            font-weight: 600;
            color: var(--text-primary);
            margin: 0 0 .25rem;
            line-height: 1.3;
        }

        .upload-card-subtitle {
            font-size: .8rem;
            color: var(--text-muted);
            margin: 0;
            line-height: 1.5;
        }

        /* ── Divider ── */
        .card-divider {
            border: none;
            border-top: 1px solid var(--border-color);
            margin: 0 0 1.8rem;
        }

        /* ── Drop zone ── */
        .drop-zone {
            border: 2px dashed var(--border-color);
            border-radius: 10px;
            padding: 1.6rem 1.2rem;
            text-align: center;
            cursor: pointer;
            transition: border-color .2s, background .2s;
            position: relative;
            margin-bottom: 1.4rem;
            background: var(--bg-elevated);
        }

        .drop-zone:hover,
        .drop-zone.dragover {
            border-color: var(--accent);
            background: rgba(47, 129, 247, .06);
        }

        .drop-zone input[type="file"] {
            position: absolute;
            inset: 0;
            opacity: 0;
            cursor: pointer;
            width: 100%;
            height: 100%;
        }

        .drop-zone-icon {
            font-size: 2rem;
            color: var(--text-muted);
            margin-bottom: .5rem;
            transition: color .2s;
        }

        .drop-zone:hover .drop-zone-icon,
        .drop-zone.dragover .drop-zone-icon {
            color: var(--accent);
        }

        .drop-zone-label {
            display: block;
            font-size: .9rem;
            font-weight: 500;
            color: var(--text-primary);
            margin-bottom: .3rem;
        }

        .drop-zone-hint {
            font-size: .76rem;
            color: var(--text-muted);
        }

        .drop-zone-hint strong {
            color: var(--accent);
        }

        /* ── File preview chip ── */
        #fileChip {
            display: none;
            align-items: center;
            gap: .6rem;
            background: var(--bg-elevated);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: .55rem .9rem;
            margin-bottom: 1.4rem;
            font-size: .82rem;
        }

        #fileChip .chip-icon {
            color: var(--accent);
            font-size: 1.1rem;
            flex-shrink: 0;
        }

        #fileChip .chip-name {
            flex: 1;
            color: var(--text-primary);
            font-weight: 500;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }

        #fileChip .chip-size {
            color: var(--text-muted);
            white-space: nowrap;
        }

        #fileChip .chip-remove {
            background: none;
            border: none;
            color: var(--text-muted);
            cursor: pointer;
            padding: 0;
            line-height: 1;
            font-size: 1rem;
            transition: color .15s;
            flex-shrink: 0;
        }

        #fileChip .chip-remove:hover { color: var(--danger); }

        /* ── Constraint row ── */
        .constraint-row {
            display: flex;
            gap: 1rem;
            margin-bottom: 1.8rem;
        }

        .constraint-item {
            flex: 1;
            background: var(--bg-elevated);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: .55rem .8rem;
            display: flex;
            align-items: center;
            gap: .5rem;
            font-size: .76rem;
            color: var(--text-muted);
        }

        .constraint-item i {
            font-size: .9rem;
            color: var(--text-muted);
        }

        /* ── Upload button ── */
        .btn-upload {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: .55rem;
            width: 100%;
            padding: .72rem 1rem;
            background: var(--accent);
            border: none;
            border-radius: 8px;
            font-size: .92rem;
            font-weight: 600;
            color: #fff;
            cursor: pointer;
            transition: background .2s, box-shadow .2s, opacity .2s;
            letter-spacing: .01em;
        }

        .btn-upload:hover:not(:disabled) {
            background: var(--accent-hover);
            box-shadow: 0 0 0 4px var(--accent-glow);
        }

        .btn-upload:disabled {
            opacity: .45;
            cursor: not-allowed;
        }

        /* ── Progress bar ── */
        #progressWrap {
            display: none;
            margin-bottom: 1.4rem;
        }

        .prog-label {
            display: flex;
            justify-content: space-between;
            font-size: .75rem;
            color: var(--text-muted);
            margin-bottom: .35rem;
        }

        .custom-progress {
            height: 6px;
            background: var(--bg-elevated);
            border-radius: 20px;
            overflow: hidden;
            border: 1px solid var(--border-color);
        }

        .custom-progress-bar {
            height: 100%;
            background: var(--accent);
            border-radius: 20px;
            width: 0%;
            transition: width .25s ease;
        }

        /* ── Alert ── */
        #alertBox {
            display: none;
            margin-top: 1.2rem;
            border-radius: 8px;
            font-size: .82rem;
            padding: .65rem .9rem;
        }

        /* ── Footer ── */
        .page-footer {
            text-align: center;
            padding: .9rem 1rem;
            font-size: .72rem;
            color: var(--text-muted);
            border-top: 1px solid var(--border-color);
            background: var(--bg-surface);
        }
    </style>
</head>
<body>

    <!-- ── Top Navigation Bar ── -->
    <nav class="topbar">
        <a href="Default.aspx" class="topbar-brand">
            <span class="brand-icon"><i class="bi bi-grid-3x3-gap-fill"></i></span>
            MirageWeb IT Dashboard
        </a>
        <div class="topbar-meta">
            <span class="badge-env">PRODUCTION</span>
            <span><i class="bi bi-clock me-1"></i><span id="liveClock"></span></span>
        </div>
    </nav>

    <!-- ── Breadcrumb ── -->
    <div class="breadcrumb-strip">
        <ol class="breadcrumb">
            <li class="breadcrumb-item"><a href="Default.aspx">Dashboard</a></li>
            <li class="breadcrumb-item active">Upload Metrics</li>
        </ol>
    </div>

    <!-- ── Page Content ── -->
    <main class="page-wrapper">
        <div class="upload-card">

            <!-- Card Header -->
            <div class="upload-card-header">
                <div class="upload-card-icon">
                    <i class="bi bi-bar-chart-line-fill"></i>
                </div>
                <div>
                    <p class="upload-card-title">Upload CSV Report</p>
                    <p class="upload-card-subtitle">
                        Import a comma-separated metrics file to update the dashboard data pipeline.
                    </p>
                </div>
            </div>

            <hr class="card-divider" />

            <!-- ASP.NET Web Form -->
            <form id="uploadForm" runat="server" enctype="multipart/form-data" method="post">

                <!-- Drop Zone -->
                <div class="drop-zone" id="dropZone">
                    <asp:FileUpload ID="csvFileInput" runat="server"
                        accept=".csv"
                        aria-label="Select a CSV file" />
                    <div class="drop-zone-icon"><i class="bi bi-cloud-arrow-up"></i></div>
                    <span class="drop-zone-label">Drag &amp; drop your CSV file here</span>
                    <p class="drop-zone-hint mb-0">or <strong>click to browse</strong> from your computer</p>
                </div>

                <!-- File Preview Chip -->
                <div id="fileChip">
                    <i class="bi bi-file-earmark-spreadsheet chip-icon"></i>
                    <span class="chip-name" id="chipName"></span>
                    <span class="chip-size" id="chipSize"></span>
                    <button type="button" class="chip-remove" id="chipRemove" aria-label="Remove file">
                        <i class="bi bi-x-circle"></i>
                    </button>
                </div>

                <!-- Constraints -->
                <div class="constraint-row">
                    <div class="constraint-item">
                        <i class="bi bi-filetype-csv"></i>
                        CSV format only
                    </div>
                    <div class="constraint-item">
                        <i class="bi bi-hdd"></i>
                        Max size: 10 MB
                    </div>
                    <div class="constraint-item">
                        <i class="bi bi-shield-check"></i>
                        UTF-8 encoded
                    </div>
                </div>

                <!-- Progress -->
                <div id="progressWrap">
                    <div class="prog-label">
                        <span>Uploading&hellip;</span>
                        <span id="progPct">0%</span>
                    </div>
                    <div class="custom-progress">
                        <div class="custom-progress-bar" id="progressBar"></div>
                    </div>
                </div>

                <!-- Upload Button -->
                <asp:Button ID="btnUpload" runat="server"
                    Text="Upload CSV Report"
                    CssClass="btn-upload"
                    OnClick="btnUpload_Click"
                    UseSubmitBehavior="true" />

                <!-- Alert feedback -->
                <div id="alertBox" role="alert"></div>

            </form>
        </div>
    </main>

    <!-- ── Footer ── -->
    <footer class="page-footer">
        &copy; 2026 MirageWeb &mdash; IT Operations &middot; All rights reserved
    </footer>

    <!-- Bootstrap 5 JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"
            integrity="sha384-YvpcrYf0tY3lHB60NNkmXc4s9bIOgUxi8T/jzmQ7GDZQ4GVdE6GEbNFi1DZ0dLe"
            crossorigin="anonymous"></script>

    <script>
        /* ── Live clock ── */
        (function () {
            function tick() {
                const now = new Date();
                document.getElementById('liveClock').textContent =
                    now.toLocaleTimeString('en-GB', { hour12: false });
            }
            tick();
            setInterval(tick, 1000);
        })();

        /* ── Drop zone ── */
        const dropZone   = document.getElementById('dropZone');
        const fileInput  = document.getElementById('<%= csvFileInput.ClientID %>');
        const fileChip   = document.getElementById('fileChip');
        const chipName   = document.getElementById('chipName');
        const chipSize   = document.getElementById('chipSize');
        const chipRemove = document.getElementById('chipRemove');
        const btnUpload  = document.getElementById('<%= btnUpload.ClientID %>');
        const alertBox   = document.getElementById('alertBox');

        function formatBytes(bytes) {
            if (bytes < 1024) return bytes + ' B';
            if (bytes < 1048576) return (bytes / 1024).toFixed(1) + ' KB';
            return (bytes / 1048576).toFixed(2) + ' MB';
        }

        function showAlert(type, message) {
            alertBox.className = 'alert alert-' + type + ' d-flex align-items-center gap-2';
            alertBox.style.display = 'flex';
            const icon = type === 'success' ? 'bi-check-circle-fill' : 'bi-exclamation-triangle-fill';
            alertBox.innerHTML =
                '<i class="bi ' + icon + '"></i><span>' + message + '</span>';
        }

        function clearAlert() {
            alertBox.style.display = 'none';
            alertBox.innerHTML = '';
        }

        function applyFile(file) {
            clearAlert();

            if (!file || !file.name.toLowerCase().endsWith('.csv')) {
                showAlert('danger', 'Only <strong>.csv</strong> files are accepted.');
                clearFile();
                return;
            }

            if (file.size > 10 * 1024 * 1024) {
                showAlert('danger', 'File exceeds the 10 MB size limit.');
                clearFile();
                return;
            }

            chipName.textContent = file.name;
            chipSize.textContent = formatBytes(file.size);
            fileChip.style.display = 'flex';
            dropZone.style.display = 'none';
            btnUpload.disabled = false;
        }

        function clearFile() {
            fileInput.value = '';
            fileChip.style.display = 'none';
            dropZone.style.display = '';
            btnUpload.disabled = true;
        }

        /* Initial state — disable upload until file chosen */
        btnUpload.disabled = true;

        fileInput.addEventListener('change', function () {
            if (this.files && this.files.length > 0) applyFile(this.files[0]);
        });

        chipRemove.addEventListener('click', function () {
            clearFile();
            clearAlert();
        });

        /* Drag & drop */
        ['dragenter', 'dragover'].forEach(function (evt) {
            dropZone.addEventListener(evt, function (e) {
                e.preventDefault();
                dropZone.classList.add('dragover');
            });
        });

        ['dragleave', 'drop'].forEach(function (evt) {
            dropZone.addEventListener(evt, function (e) {
                e.preventDefault();
                dropZone.classList.remove('dragover');
            });
        });

        dropZone.addEventListener('drop', function (e) {
            const dt = e.dataTransfer;
            if (dt && dt.files && dt.files.length > 0) {
                // Transfer dropped file to the hidden file input
                try {
                    const dataTransfer = new DataTransfer();
                    dataTransfer.items.add(dt.files[0]);
                    fileInput.files = dataTransfer.files;
                } catch (_) { /* Safari fallback — validation only */ }
                applyFile(dt.files[0]);
            }
        });

        /* ── Simulated progress bar on submit ── */
        document.getElementById('uploadForm').addEventListener('submit', function () {
            if (fileInput.files && fileInput.files.length > 0) {
                const wrap = document.getElementById('progressWrap');
                const bar  = document.getElementById('progressBar');
                const pct  = document.getElementById('progPct');
                wrap.style.display = 'block';
                btnUpload.style.pointerEvents = 'none';
                btnUpload.style.opacity = '0.5';
                let progress = 0;
                const iv = setInterval(function () {
                    progress = Math.min(progress + Math.random() * 18, 92);
                    bar.style.width  = progress.toFixed(0) + '%';
                    pct.textContent  = progress.toFixed(0) + '%';
                    if (progress >= 92) clearInterval(iv);
                }, 200);
            }
        });
    </script>
</body>
</html>
