/* ============================================================
   app.js — wires up the UI: uploads, tabs, role selection,
   the one orchestrated hero animation, and rendering results.
   ============================================================ */

document.addEventListener('DOMContentLoaded', () => {

  /* ---------- Hero: single orchestrated demo moment ---------- */
  (function heroDemo() {
    const el = document.getElementById('heroTypewriter');
    const sample = 'Aditi Sharma\nB.Tech CSE, 2026\nSkills: Python, SQL, Pandas, Excel...';
    let i = 0;
    const cursor = '<span class="cursor"></span>';
    const type = () => {
      el.innerHTML = sample.slice(0, i).replace(/\n/g, '<br>') + cursor;
      i++;
      if (i <= sample.length) {
        setTimeout(type, 22);
      } else {
        setTimeout(drawDemoChart, 350);
      }
    };
    function drawDemoChart() {
      const demoChart = document.getElementById('heroChart');
      const holder = document.createElement('div');
      holder.style.width = '150px';
      demoChart.appendChild(holder);
      Charts.renderGauge(holder, 78, 'Data Analyst');
    }
    setTimeout(type, 500);
  })();

  /* ---------- Populate role catalog (searchable + category filtered) ---------- */
  const roleGrid = document.getElementById('roleGrid');
  const roleSearch = document.getElementById('roleSearch');
  const catFilter = document.getElementById('catFilter');
  const roleEmpty = document.getElementById('roleEmpty');
  let selectedRoleId = null;
  let activeCategory = 'All';

  const ROLE_ENTRIES = Object.entries(SKILL_DB.roles);
  const CATEGORIES = ['All', ...Array.from(new Set(ROLE_ENTRIES.map(([, r]) => r.category))).sort()];

  // Category filter chips
  CATEGORIES.forEach(cat => {
    const chip = document.createElement('button');
    chip.className = 'cat-chip' + (cat === 'All' ? ' active' : '');
    chip.textContent = cat === 'All' ? `All (${ROLE_ENTRIES.length})` : cat;
    chip.addEventListener('click', () => {
      activeCategory = cat;
      catFilter.querySelectorAll('.cat-chip').forEach(c => c.classList.remove('active'));
      chip.classList.add('active');
      renderRoles();
    });
    catFilter.appendChild(chip);
  });

  roleSearch.addEventListener('input', renderRoles);

  function renderRoles() {
    const q = roleSearch.value.trim().toLowerCase();
    roleGrid.innerHTML = '';

    const visible = ROLE_ENTRIES.filter(([id, role]) => {
      if (activeCategory !== 'All' && role.category !== activeCategory) return false;
      if (!q) return true;
      // match role title, tagline, category, or any of its required skill names
      const skillNames = role.skills.map(s => SKILL_DB.skills[s.id].name.toLowerCase()).join(' ');
      return (role.title + ' ' + role.tagline + ' ' + role.category + ' ' + skillNames)
        .toLowerCase().includes(q);
    });

    roleEmpty.classList.toggle('show', visible.length === 0);

    // Group under category headings when showing more than one category
    let lastCat = null;
    visible.forEach(([id, role]) => {
      if (activeCategory === 'All' && role.category !== lastCat) {
        const label = document.createElement('div');
        label.className = 'role-cat-label';
        label.textContent = role.category;
        roleGrid.appendChild(label);
        lastCat = role.category;
      }
      const btn = document.createElement('button');
      btn.className = 'role-chip' + (id === selectedRoleId ? ' selected' : '');
      btn.dataset.role = id;
      btn.innerHTML = `<strong>${role.title}</strong>${role.tagline}`;
      btn.addEventListener('click', () => {
        selectedRoleId = id;
        roleGrid.querySelectorAll('.role-chip').forEach(c => c.classList.remove('selected'));
        btn.classList.add('selected');
        updateRunButton();
      });
      roleGrid.appendChild(btn);
    });
  }

  // Sort entries by category so the grouped headings come out in order
  ROLE_ENTRIES.sort((a, b) => a[1].category.localeCompare(b[1].category) || a[1].title.localeCompare(b[1].title));
  renderRoles();

  /* ---------- Tabs: role vs JD ---------- */
  document.querySelectorAll('.tab-btn').forEach(tab => {
    tab.addEventListener('click', () => {
      document.querySelectorAll('.tab-btn').forEach(t => t.classList.remove('active'));
      tab.classList.add('active');
      const isRole = tab.dataset.tab === 'role';
      document.getElementById('tab-role').style.display = isRole ? '' : 'none';
      document.getElementById('tab-jd').style.display = isRole ? 'none' : '';
      updateRunButton();
    });
  });

  /* ---------- File upload / dropzone ---------- */
  const dropzone = document.getElementById('dropzone');
  const fileInput = document.getElementById('fileInput');
  const fileChip = document.getElementById('fileChip');
  const fileChipName = document.getElementById('fileChipName');
  const resumeText = document.getElementById('resumeText');
  let uploadedFile = null;

  dropzone.addEventListener('click', () => fileInput.click());
  dropzone.addEventListener('dragover', e => { e.preventDefault(); dropzone.classList.add('dropzone--active'); });
  dropzone.addEventListener('dragleave', () => dropzone.classList.remove('dropzone--active'));
  dropzone.addEventListener('drop', e => {
    e.preventDefault();
    dropzone.classList.remove('dropzone--active');
    if (e.dataTransfer.files.length) handleFile(e.dataTransfer.files[0]);
  });
  fileInput.addEventListener('change', e => { if (e.target.files.length) handleFile(e.target.files[0]); });

  function handleFile(file) {
    uploadedFile = file;
    fileChipName.textContent = file.name;
    fileChip.classList.add('show');
    updateRunButton();
  }
  document.getElementById('fileChipRemove').addEventListener('click', (e) => {
    e.stopPropagation();
    uploadedFile = null;
    fileInput.value = '';
    fileChip.classList.remove('show');
    updateRunButton();
  });
  resumeText.addEventListener('input', updateRunButton);
  document.getElementById('jdText').addEventListener('input', updateRunButton);

  function hasResumeInput() {
    return !!uploadedFile || resumeText.value.trim().length > 30;
  }
  function hasTargetInput() {
    const jdTab = document.getElementById('tab-jd').style.display !== 'none';
    if (jdTab) return document.getElementById('jdText').value.trim().length > 40;
    return !!selectedRoleId;
  }
  function updateRunButton() {
    document.getElementById('runBtn').disabled = !(hasResumeInput() && hasTargetInput());
  }

  /* ---------- Run analysis ---------- */
  document.getElementById('runBtn').addEventListener('click', runAnalysis);

  async function runAnalysis() {
    const btn = document.getElementById('runBtn');
    const spinner = document.getElementById('runSpinner');
    const status = document.getElementById('scanStatus');
    btn.disabled = true;
    spinner.classList.add('show');
    document.getElementById('runBtnText').textContent = 'Analyzing...';

    const steps = ['Reading resume...', 'Extracting skills...', 'Comparing against role requirements...', 'Scoring ATS compatibility...'];
    for (const s of steps) {
      status.textContent = s;
      await wait(380);
    }

    try {
      let text = resumeText.value.trim();
      if (!text && uploadedFile) {
        text = await Parser.extractTextFromFile(uploadedFile);
      }
      if (!text || text.trim().length < 20) {
        throw new Error('Could not read enough text from that resume. Try pasting the text directly.');
      }

      const analysis = Parser.analyzeResumeText(text);

      const jdTab = document.getElementById('tab-jd').style.display !== 'none';
      let roleTitle, roleSkillsSpec, roleIdForHighlight;

      if (jdTab) {
        roleTitle = 'Custom job description';
        roleSkillsSpec = Matcher.buildRoleFromJobText(document.getElementById('jdText').value);
        roleIdForHighlight = null;
      } else {
        const role = SKILL_DB.roles[selectedRoleId];
        roleTitle = role.title;
        roleSkillsSpec = role.skills;
        roleIdForHighlight = selectedRoleId;
      }

      const matchResult = Matcher.scoreAgainstRoleSkills(analysis.skills, roleSkillsSpec);
      const ats = Matcher.atsScore(analysis, matchResult.percent);
      const roadmap = Matcher.buildRoadmap(matchResult.missing);
      const ranked = Matcher.rankAllRoles(analysis.skills);

      renderResults({ roleTitle, roleIdForHighlight, matchResult, ats, roadmap, ranked, analysis });

      status.textContent = '';
      document.getElementById('results').classList.add('show');
      document.getElementById('results').scrollIntoView({ behavior: 'smooth' });

    } catch (err) {
      status.textContent = err.message || 'Something went wrong reading that file.';
    } finally {
      btn.disabled = false;
      spinner.classList.remove('show');
      document.getElementById('runBtnText').textContent = 'Run analysis';
      updateRunButton();
    }
  }

  function wait(ms) { return new Promise(r => setTimeout(r, ms)); }

  /* ---------- Render results ---------- */
  function renderResults({ roleTitle, roleIdForHighlight, matchResult, ats, roadmap, ranked, analysis }) {
    document.getElementById('matchRoleName').textContent = 'Matched against: ' + roleTitle;

    const gaugeContainer = document.getElementById('gaugeContainer');
    Charts.renderGauge(gaugeContainer, matchResult.percent, roleTitle.length > 22 ? 'Match' : roleTitle);

    const verdict = document.getElementById('verdictText');
    if (matchResult.percent >= 75) verdict.textContent = "Strong fit — you're close to ready for this role.";
    else if (matchResult.percent >= 45) verdict.textContent = "Partial fit — a focused skill push will close the gap.";
    else verdict.textContent = "Early stage — treat the roadmap below as your study plan.";

    document.getElementById('atsScoreNum').textContent = ats.score;
    const checklist = document.getElementById('atsChecklist');
    checklist.innerHTML = '';
    ats.checks.forEach(c => {
      const row = document.createElement('div');
      row.className = 'check-item';
      row.innerHTML = `
        <div class="check-item__icon ${c.pass ? 'pass' : 'fail'}">${c.pass ? '✓' : '!'}</div>
        <div class="check-item__body">
          <strong>${c.label}</strong>
          <p>${c.tip}</p>
        </div>
        <div class="check-item__pts">${c.points}/${c.max}</div>`;
      checklist.appendChild(row);
    });

    const radarContainer = document.getElementById('radarContainer');
    const radarSkills = [...matchResult.matched.map(m => ({ ...m, matched: true })),
                         ...matchResult.missing.map(m => ({ ...m, matched: false }))]
                         .sort((a, b) => b.weight - a.weight).slice(0, 9);
    Charts.renderRadar(radarContainer, radarSkills);

    const gapList = document.getElementById('gapList');
    gapList.innerHTML = '';
    if (roadmap.length === 0) {
      gapList.innerHTML = '<p style="color:var(--text-muted); font-size:0.88rem;">No gaps detected — your skill set already covers this role\'s requirements.</p>';
    }
    roadmap.forEach(r => {
      const badgeClass = r.priority === 'Must-have' ? 'badge--must' : r.priority === 'Important' ? 'badge--imp' : 'badge--nice';
      const item = document.createElement('div');
      item.className = 'gap-item';
      item.innerHTML = `
        <div class="gap-item__top"><strong>${r.skill}</strong><span class="badge ${badgeClass}">${r.priority}</span></div>
        <p><b>${r.platform}</b> — ${r.action}</p>`;
      gapList.appendChild(item);
    });

    const rankingContainer = document.getElementById('rankingContainer');
    Charts.renderRankedBars(rankingContainer, ranked, roleIdForHighlight);
  }

});
