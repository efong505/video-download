// hub-cards-loader.js — Loads action cards from API for mountain hub pages
const HUB_CARDS_API = 'https://lcmogvl3v2.execute-api.us-east-1.amazonaws.com/prod/mountains';

async function loadHubCards(mountain) {
    try {
        const res = await fetch(`${HUB_CARDS_API}?action=list_cards&mountain=${mountain}`);
        const data = await res.json();
        const cards = data.cards || [];
        if (!cards.length) return; // keep hardcoded fallback

        const tabs = ['promote', 'expose', 'involved'];
        tabs.forEach(tab => {
            const tabCards = cards.filter(c => c.tab === tab);
            if (!tabCards.length) return;
            const container = document.querySelector(`#${tab} .action-grid`);
            if (!container) return;
            container.innerHTML = tabCards.map(c => {
                const btns = (c.buttons || []).map((b, i) => {
                    const target = b.external ? ' target="_blank"' : '';
                    const arrow = b.external ? ' ↗' : '';
                    const mt = i > 0 ? ' style="margin-top:8px;"' : '';
                    return `<a href="${escapeAttr(b.url)}"${target} class="action-btn"${mt}>${escapeHtml(b.label)}${arrow}</a>`;
                }).join('\n                ');
                return `<div class="action-card">
                <h3>${escapeHtml(c.icon || '')} ${escapeHtml(c.title)}</h3>
                <p>${escapeHtml(c.description)}</p>
                ${btns}
            </div>`;
            }).join('\n');
        });

        // Resources tab — render as link list
        const resCards = cards.filter(c => c.tab === 'resources').sort((a,b) => (a.sort_order||0) - (b.sort_order||0));
        const resContainer = document.getElementById('dynamic-quick-links');
        if (resCards.length && resContainer) {
            resContainer.innerHTML = '<ul class="resource-list">' + resCards.map(c => {
                const btn = (c.buttons || [])[0];
                if (!btn) return '';
                const target = btn.external ? ' target="_blank"' : '';
                return `<li><a href="${escapeAttr(btn.url)}"${target}><strong>${escapeHtml(c.title)}</strong></a> - ${escapeHtml(c.description)}</li>`;
            }).join('') + '</ul>';
        }
    } catch (e) {
        console.warn('Hub cards API unavailable, using hardcoded fallback:', e);
    }
}

function escapeHtml(t) {
    if (!t) return '';
    const d = document.createElement('div');
    d.textContent = t;
    return d.innerHTML;
}

function escapeAttr(t) {
    if (!t) return '';
    return t.replace(/&/g,'&amp;').replace(/"/g,'&quot;').replace(/'/g,'&#39;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
}
