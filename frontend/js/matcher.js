/* ============================================================
   matcher.js — the scoring brain:
   - role match % from weighted skill overlap
   - job-description free-text matching
   - ATS compatibility score with breakdown
   - skill gap + learning roadmap
   - best-fit role ranking across the whole catalog
   ============================================================ */

const Matcher = (() => {

  function scoreAgainstRoleSkills(candidateSkillIds, roleSkills) {
    const have = new Set(candidateSkillIds);
    let totalWeight = 0, gotWeight = 0;
    const matched = [], missing = [];

    roleSkills.forEach(req => {
      totalWeight += req.weight;
      const skill = SKILL_DB.skills[req.id];
      if (have.has(req.id)) {
        gotWeight += req.weight;
        matched.push({ id: req.id, name: skill.name, weight: req.weight });
      } else {
        missing.push({ id: req.id, name: skill.name, weight: req.weight });
      }
    });

    const pct = totalWeight === 0 ? 0 : Math.round((gotWeight / totalWeight) * 100);
    missing.sort((a, b) => b.weight - a.weight);
    matched.sort((a, b) => b.weight - a.weight);
    return { percent: pct, matched, missing };
  }

  // Rank every role in the catalog against the candidate's extracted skills
  function rankAllRoles(candidateSkillIds) {
    return Object.entries(SKILL_DB.roles).map(([roleId, role]) => {
      const result = scoreAgainstRoleSkills(candidateSkillIds, role.skills);
      return { roleId, title: role.title, tagline: role.tagline, percent: result.percent };
    }).sort((a, b) => b.percent - a.percent);
  }

  // Simple TF-IDF-free cosine-ish overlap for free-text job descriptions:
  // extract skills mentioned in the JD text itself and treat each as weight 2,
  // then score the resume against that ad-hoc "role".
  function buildRoleFromJobText(jdText) {
    const skillIds = Parser.extractSkills(jdText);
    return skillIds.map(id => ({ id, weight: 2 }));
  }

  function priorityLabel(weight) {
    if (weight >= 3) return 'Must-have';
    if (weight >= 2) return 'Important';
    return 'Good to have';
  }

  function buildRoadmap(missingSkills) {
    return missingSkills.slice(0, 8).map(m => {
      const res = SKILL_DB.resources[m.id] || { platform: 'Official documentation', action: 'Study the fundamentals and build one small project' };
      return {
        skill: m.name,
        priority: priorityLabel(m.weight),
        weight: m.weight,
        platform: res.platform,
        action: res.action
      };
    });
  }

  // ---------------- ATS SCORING ----------------
  function atsScore(analysis, matchPercent) {
    const checks = [];
    let score = 0;

    // 1. Contact info (10 pts)
    const hasEmail = !!analysis.contact.email;
    const hasPhone = !!analysis.contact.phone;
    const contactPts = (hasEmail ? 5 : 0) + (hasPhone ? 5 : 0);
    score += contactPts;
    checks.push({
      label: 'Contact details findable',
      pass: contactPts === 10,
      points: contactPts, max: 10,
      tip: contactPts === 10 ? 'Email and phone number are both present and machine-readable.' :
        'Add a clear email and 10-digit phone number near the top of the resume.'
    });

    // 2. Standard sections (25 pts, 5 each)
    const sectionEntries = Object.entries(analysis.sections);
    const sectionsFound = sectionEntries.filter(([, v]) => v).length;
    const sectionPts = sectionsFound * 5;
    score += sectionPts;
    const missingSections = sectionEntries.filter(([, v]) => !v).map(([k]) => k);
    checks.push({
      label: 'Standard resume sections present',
      pass: missingSections.length === 0,
      points: sectionPts, max: 25,
      tip: missingSections.length === 0 ? 'All key sections (Education, Skills, Experience, Certifications) were detected.' :
        `Add or clearly label: ${missingSections.join(', ')}.`
    });

    // 3. Word count in healthy range (15 pts)
    const wc = analysis.words;
    const wcGood = wc >= 250 && wc <= 900;
    const wcPts = wcGood ? 15 : (wc < 250 ? 5 : 8);
    score += wcPts;
    checks.push({
      label: 'Resume length is scanner-friendly',
      pass: wcGood,
      points: wcPts, max: 15,
      tip: wcGood ? `${wc} words is a healthy length for one or two pages.` :
        wc < 250 ? `Only ${wc} words found — add more detail on projects and impact.` :
        `${wc} words is on the longer side — tighten it to the most relevant points.`
    });

    // 4. Bullet points & action verbs (20 pts)
    const { bulletLines, verbHits } = analysis.structure;
    const structurePts = Math.min(10, bulletLines * 2) + Math.min(10, verbHits * 2);
    score += structurePts;
    checks.push({
      label: 'Uses bullet points and action verbs',
      pass: structurePts >= 14,
      points: structurePts, max: 20,
      tip: structurePts >= 14 ? 'Good use of bullet points and strong action verbs like "built" or "led".' :
        'Rewrite experience/project lines as bullet points starting with action verbs (Built, Developed, Automated).'
    });

    // 5. Keyword relevance to target role/JD (30 pts, scaled from match %)
    const keywordPts = Math.round((matchPercent / 100) * 30);
    score += keywordPts;
    checks.push({
      label: 'Keyword match with target role',
      pass: matchPercent >= 50,
      points: keywordPts, max: 30,
      tip: matchPercent >= 50 ? 'Resume keywords line up well with what the target role is scanning for.' :
        'Mirror more of the exact skill keywords used in the job description or role profile.'
    });

    return { score: Math.min(100, score), checks };
  }

  return { scoreAgainstRoleSkills, rankAllRoles, buildRoleFromJobText, buildRoadmap, atsScore };
})();
