// 7 Mountains API Integration
// Handles pledges, badges, and leaderboards on mountain hub pages

const MOUNTAINS_API = 'https://lcmogvl3v2.execute-api.us-east-1.amazonaws.com/prod/mountains';

function getAuthToken() {
    return localStorage.getItem('auth_token');
}

function isLoggedIn() {
    return !!getAuthToken();
}

async function mountainApiCall(action, method, body, extraParams) {
    const token = getAuthToken();
    if (!token) return null;

    let url = `${MOUNTAINS_API}?action=${action}`;
    if (extraParams) url += `&${extraParams}`;

    const options = {
        method,
        headers: { 'Authorization': `Bearer ${token}`, 'Content-Type': 'application/json' }
    };
    if (body) options.body = JSON.stringify(body);

    const res = await fetch(url, options);
    return res.json();
}

async function takePledge(mountain) {
    const btn = document.getElementById('pledge-btn');
    btn.disabled = true;
    btn.textContent = 'Submitting...';

    try {
        const data = await mountainApiCall('create_pledge', 'POST', { mountain });
        if (data.error && data.error.includes('already exists')) {
            btn.textContent = '✅ Already Pledged';
            btn.classList.add('pledged');
        } else if (data.pledge) {
            btn.textContent = '✅ Pledge Taken!';
            btn.classList.add('pledged');
            if (data.badge_awarded) {
                showBadgeNotification(data.badge_awarded.badge_type);
            }
        } else {
            btn.textContent = 'Take the Pledge ✊';
            btn.disabled = false;
        }
    } catch (e) {
        console.error('Pledge error:', e);
        btn.textContent = 'Take the Pledge ✊';
        btn.disabled = false;
    }
}

function showBadgeNotification(badgeType) {
    const icons = { pledge: '🤝', contributor: '⭐', warrior: '⚔️', champion: '🏆' };
    const el = document.createElement('div');
    el.className = 'badge-notification';
    el.innerHTML = `${icons[badgeType] || '🎉'} Badge Earned: <strong>${badgeType.charAt(0).toUpperCase() + badgeType.slice(1)}</strong>`;
    document.body.appendChild(el);
    setTimeout(() => el.classList.add('show'), 10);
    setTimeout(() => { el.classList.remove('show'); setTimeout(() => el.remove(), 300); }, 4000);
}

async function checkPledgeStatus(mountain) {
    const btn = document.getElementById('pledge-btn');
    if (!isLoggedIn()) {
        btn.textContent = 'Log in to Pledge';
        btn.onclick = () => window.location.href = 'login.html';
        return;
    }
    try {
        const data = await mountainApiCall('get_pledges', 'GET');
        const pledged = (data.pledges || []).some(p => p.mountain === mountain);
        if (pledged) {
            btn.textContent = '✅ Already Pledged';
            btn.classList.add('pledged');
            btn.disabled = true;
        }
    } catch (e) {
        console.error('Pledge check error:', e);
    }
}

async function loadLeaderboard(mountain) {
    const container = document.getElementById('leaderboard-list');
    if (!container) return;

    try {
        const data = await mountainApiCall('get_leaderboard', 'GET', null, `mountain=${mountain}`);
        const board = data.leaderboard || [];

        if (board.length === 0) {
            container.innerHTML = '<p class="text-muted text-center">No contributors yet. Be the first!</p>';
            return;
        }

        const medals = ['🥇', '🥈', '🥉'];
        container.innerHTML = board.slice(0, 10).map((entry, i) => `
            <div class="leaderboard-entry">
                <span class="lb-rank">${medals[i] || (i + 1)}</span>
                <span class="lb-name">${entry.name}</span>
                <span class="lb-count">${entry.contribution_count} contributions</span>
            </div>
        `).join('');
    } catch (e) {
        console.error('Leaderboard error:', e);
        container.innerHTML = '<p class="text-muted text-center">Could not load leaderboard</p>';
    }
}

async function loadUserBadges(mountain) {
    const container = document.getElementById('user-badges');
    if (!container || !isLoggedIn()) return;

    try {
        const data = await mountainApiCall('get_badges', 'GET');
        const badges = (data.badges || []).filter(b => b.mountain === mountain);
        const icons = { pledge: '🤝', contributor: '⭐', warrior: '⚔️', champion: '🏆' };

        if (badges.length === 0) {
            container.innerHTML = '<p class="text-muted">Take the pledge to earn your first badge!</p>';
            return;
        }

        container.innerHTML = badges.map(b => `
            <span class="mountain-badge">${icons[b.badge_type] || '🎖️'} ${b.badge_type.charAt(0).toUpperCase() + b.badge_type.slice(1)}</span>
        `).join('');
    } catch (e) {
        console.error('Badges error:', e);
    }
}

function initMountainHub(mountain) {
    checkPledgeStatus(mountain);
    loadLeaderboard(mountain);
    loadUserBadges(mountain);
}
