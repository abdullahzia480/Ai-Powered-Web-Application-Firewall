document.addEventListener('DOMContentLoaded', function () {
    console.log('[SentinAI] UI Overhaul Initialized - final_design');

    // --- 1. System Stats (Clock/Uptime) ---
    function updateTime() {
        const now = new Date();
        const timeStr = now.toLocaleTimeString('en-US', { hour12: false });
        document.getElementById('system-time').textContent = `${timeStr} UTC`;
    }
    setInterval(updateTime, 1000);
    updateTime();

    const startTime = Date.now();
    function updateUptime() {
        const elapsed = Date.now() - startTime;
        const h = Math.floor(elapsed / 3600000);
        const m = Math.floor((elapsed % 3600000) / 60000);
        const s = Math.floor((elapsed % 60000) / 1000);
        document.getElementById('uptime-val').textContent =
            `UP ${String(h).padStart(2, '0')}:${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`;
    }
    setInterval(updateUptime, 1000);

    // --- 2. Chart Initialization (Matching User's Style) ---
    const MAX_POINTS = 30; // approx 60s
    let safeHistory = Array(MAX_POINTS).fill(0);
    let attackHistory = Array(MAX_POINTS).fill(0);

    // Traffic Chart (Line)
    const ctxTraffic = document.getElementById('trafficChart').getContext('2d');
    const trafficChart = new Chart(ctxTraffic, {
        type: 'line',
        data: {
            labels: Array(MAX_POINTS).fill(''),
            datasets: [
                {
                    label: 'Safe Requests',
                    data: safeHistory,
                    borderColor: '#2563eb', // Blue
                    backgroundColor: 'rgba(37, 99, 235, 0.1)',
                    borderWidth: 2,
                    tension: 0.4,
                    fill: true,
                    pointRadius: 0
                },
                {
                    label: 'Blocked Requests',
                    data: attackHistory,
                    borderColor: '#ef4444', // Red
                    backgroundColor: 'rgba(239, 68, 68, 0.1)',
                    borderWidth: 2,
                    tension: 0.4,
                    fill: true,
                    pointRadius: 0
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { position: 'top' }, tooltip: { enabled: true } },
            scales: { x: { display: false }, y: { beginAtZero: true } }
        }
    });

    // Threat Chart (Doughnut)
    const ctxThreat = document.getElementById('threatChart').getContext('2d');
    const threatChart = new Chart(ctxThreat, {
        type: 'doughnut',
        data: {
            labels: ['SQL Injection', 'XSS', 'Brute Force', 'Other', 'Safe'],
            datasets: [{
                data: [0, 0, 0, 0, 100],
                backgroundColor: [
                    '#ef4444', // Red (SQLi)
                    '#f97316', // Orange (XSS)
                    '#f59e0b', // Amber (Brute)
                    '#06b6d4', // Cyan (Other)
                    '#64748b'  // Slate (Safe)
                ],
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            cutout: '65%',
            plugins: { legend: { position: 'right' } }
        }
    });

    // --- 3. Data Fetching & UI Update Loop ---
    const els = {
        total: document.getElementById('stat-total'),
        blocked: document.getElementById('stat-blocked'),
        allowed: document.getElementById('stat-allowed'),
        attackRate: document.getElementById('stat-attack-rate'),
        logsBody: document.getElementById('logs-body')
    };

    let previousStats = { total: 0, blocked: 0, allowed: 0 };
    let isFirstLoad = true;

    function updateDashboard() {
        // A. Stats
        fetch('/waf/api/stats')
            .then(r => r.json())
            .then(stats => {
                // Update Cards
                els.total.textContent = stats.total_requests.toLocaleString() + 'M'; // Mock M suffix if wanted, or just raw
                if (stats.total_requests < 1000) els.total.textContent = stats.total_requests.toLocaleString();

                els.blocked.textContent = stats.blocked_threats.toLocaleString();
                els.allowed.textContent = stats.safe_requests.toLocaleString();

                let rate = 0;
                if (stats.total_requests > 0) rate = ((stats.blocked_threats / stats.total_requests) * 100).toFixed(1);
                els.attackRate.textContent = rate + '%';

                // Chart Updates
                // Fix: On first load, don't show the massive jump from 0 to Current Total
                let totalDelta = 0;
                let blockedDelta = 0;

                if (!isFirstLoad) {
                    totalDelta = Math.max(0, stats.total_requests - previousStats.total);
                    blockedDelta = Math.max(0, stats.blocked_threats - previousStats.blocked);
                } else {
                    isFirstLoad = false;
                }

                // Fix: Determine Pure Safe Traffic (Total - Blocked) so lines don't overlap
                const safeDelta = Math.max(0, totalDelta - blockedDelta);

                safeHistory.push(safeDelta); safeHistory.shift();
                attackHistory.push(blockedDelta); attackHistory.shift();
                trafficChart.update('none');

                // Real Threat Distribution
                const sqli = stats.sqli_count || 0;
                const xss = stats.xss_count || 0;
                const other = stats.other_count || 0;

                threatChart.data.datasets[0].data = [sqli, xss, 0, other, stats.safe_requests];
                threatChart.update('none');

                previousStats = { total: stats.total_requests, blocked: stats.blocked_threats, allowed: stats.safe_requests };
            })
            .catch(e => console.error(e));

        // B. Logs
        fetch('/waf/api/logs')
            .then(r => r.json())
            .then(logs => {
                if (!logs || logs.length === 0) return;

                // Strict Newest First
                const sortedLogs = logs.slice().sort((a, b) => new Date(b.time).getTime() - new Date(a.time).getTime());

                els.logsBody.innerHTML = sortedLogs.map(log => {
                    const isBlocked = log.verdict === 'BLOCKED';
                    const time = log.time.split(' ')[1] || log.time;

                    // Determine "Type" based on payload content (Simple heuristic)
                    let type = "Standard Request";
                    if (isBlocked) {
                        if (log.payload.toLowerCase().includes('select') || log.payload.includes('1=1')) type = "SQL Injection";
                        else if (log.payload.includes('<script')) type = "XSS Attack";
                        else type = "Suspicious Activity";
                    }

                    // Score to text severity
                    const scoreVal = parseFloat(log.score);
                    let severity = "Low";
                    let sevClass = "severity-low";
                    if (scoreVal > 0.8) { severity = "High"; sevClass = "severity-high"; }
                    else if (scoreVal > 0.5) { severity = "Medium"; sevClass = "severity-medium"; }

                    return `
                        <tr>
                            <td>${time}</td>
                            <td>${log.ip}</td>
                            <td>${log.path}</td>
                            <td>${type}</td>
                            <td class="${sevClass}">${isBlocked ? severity : 'Safe'}</td>
                            <td><span class="status-badge ${isBlocked ? 'status-blocked' : 'status-allowed'}">${isBlocked ? 'Blocked' : 'Allowed'}</span></td>
                        </tr>
                    `;
                }).join('');
            })
            .catch(e => console.error(e));
    }

    setInterval(updateDashboard, 2000);
    updateDashboard();
});
