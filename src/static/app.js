const API_URL = '/api';

// State
let currentView = 'dashboard';
let isGenerating = false;

// Init
document.addEventListener('DOMContentLoaded', () => {
    refreshData();
    setInterval(refreshData, 3000); // Poll every 3s
});

function showView(viewName) {
    document.querySelectorAll('.view').forEach(el => el.classList.remove('active'));
    document.querySelectorAll('.nav-btn').forEach(el => el.classList.remove('active'));

    document.getElementById(`${viewName}-view`).classList.add('active');
    // Find nav button
    const navBtns = document.querySelectorAll('.nav-btn');
    if (viewName === 'dashboard') navBtns[0].classList.add('active');
    if (viewName === 'sections') navBtns[1].classList.add('active');
    if (viewName === 'settings') navBtns[2].classList.add('active');

    currentView = viewName;
    if (viewName === 'sections') loadSections();
}

async function refreshData() {
    try {
        // 1. Get Status
        const statusRes = await fetch(`${API_URL}/status`);
        const statusData = await statusRes.json();

        isGenerating = statusData.is_generating;
        document.getElementById('current-model').textContent = statusData.model;

        const dot = document.getElementById('system-dot');
        const text = document.getElementById('system-text');

        if (isGenerating) {
            dot.classList.add('busy');
            text.textContent = "Generating...";
            document.getElementById('active-task').style.display = 'block';
        } else {
            dot.classList.remove('busy');
            text.textContent = "Ready";
            document.getElementById('active-task').style.display = 'none';
        }

        // 2. Get Progress (if generating)
        if (isGenerating) {
            const progressRes = await fetch(`${API_URL}/progress`);
            const progressData = await progressRes.json();

            // Find active section
            const sectionNum = statusData.current_section;
            if (sectionNum && progressData[sectionNum]) {
                const p = progressData[sectionNum];
                document.getElementById('current-section-title').textContent = p.title;
                document.getElementById('current-subsection').textContent = p.current_subsection || "Processing...";

                const pct = (p.completed_subsections / p.total_subsections) * 100;
                document.getElementById('current-progress-bar').style.width = `${pct}%`;
            }
        }

        // 3. Update Stats (Total words, etc)
        // For simplicity, we'll just sum up from sections endpoint
        if (currentView === 'dashboard') {
            const sectionsRes = await fetch(`${API_URL}/sections`);
            const sections = await sectionsRes.json();

            const completed = sections.filter(s => s.status === 'complete').length;
            document.getElementById('completed-count').textContent = `${completed}/${sections.length}`;

            // Total words would ideally come from API, but we can estimate or fetch if available
            // For now, placeholder
        }

    } catch (e) {
        console.error("Refresh failed", e);
    }
}

async function loadSections() {
    const res = await fetch(`${API_URL}/sections`);
    const sections = await res.json();

    const container = document.getElementById('sections-list');
    container.innerHTML = '';

    sections.forEach(s => {
        const div = document.createElement('div');
        div.className = 'section-item';

        let actionBtn = '';
        if (s.status === 'complete') {
            actionBtn = `<button class="btn-download">Download</button>`;
        } else if (isGenerating) {
            actionBtn = `<button class="btn-generate" disabled>Wait</button>`;
        } else {
            actionBtn = `<button class="btn-generate" onclick="startGeneration('${s.section_number}')">Generate</button>`;
        }

        div.innerHTML = `
            <div class="section-info">
                <h4>Section ${s.section_number}: ${s.section_title}</h4>
                <small>${s.chapter}</small>
            </div>
            <div class="section-actions">
                ${actionBtn}
            </div>
        `;
        container.appendChild(div);
    });
}

async function startGeneration(sectionNum) {
    if (confirm(`Start generating Section ${sectionNum}?`)) {
        try {
            const res = await fetch(`${API_URL}/generate/${sectionNum}`, { method: 'POST' });
            if (res.ok) {
                alert('Generation started!');
                refreshData();
            } else {
                const err = await res.json();
                alert('Error: ' + err.detail);
            }
        } catch (e) {
            alert('Failed to start generation');
        }
    }
}
