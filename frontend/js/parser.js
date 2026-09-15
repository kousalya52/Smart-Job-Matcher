/* ============================================================
   parser.js — turns an uploaded file (or pasted text) into
   clean text, then extracts skills, contact info, and sections.
   ============================================================ */

const Parser = (() => {

  // Normalize a term the exact same way resume text gets normalized,
  // so names containing "&", "/", "." etc. still match ("Git & GitHub" -> "git github").
  function normalize(s) {
    return s.toLowerCase().replace(/[^a-z0-9+.#\s]/g, ' ').replace(/\s+/g, ' ').trim();
  }

  // Build a flat lookup: every normalized alias/name -> skill id
  const ALIAS_LOOKUP = (() => {
    const map = {};
    Object.entries(SKILL_DB.skills).forEach(([id, skill]) => {
      const terms = [id.replace(/-/g, ' '), skill.name, ...(skill.aliases || [])];
      terms.forEach(t => {
        const key = normalize(t);
        if (key) map[key] = id;
      });
    });
    return map;
  })();

  // Sort terms longest-first so "react native" matches before "react"
  const ALL_TERMS = Object.keys(ALIAS_LOOKUP).sort((a, b) => b.length - a.length);

  async function extractTextFromFile(file) {
    const name = file.name.toLowerCase();
    if (name.endsWith('.pdf')) return extractPdf(file);
    if (name.endsWith('.docx')) return extractDocx(file);
    if (name.endsWith('.txt')) return file.text();
    throw new Error('Unsupported file type. Please upload a PDF, DOCX, or TXT file.');
  }

  async function extractPdf(file) {
    const buf = await file.arrayBuffer();
    const pdf = await pdfjsLib.getDocument({ data: buf }).promise;
    let text = '';
    for (let i = 1; i <= pdf.numPages; i++) {
      const page = await pdf.getPage(i);
      const content = await page.getTextContent();
      text += content.items.map(it => it.str).join(' ') + '\n';
    }
    return text;
  }

  async function extractDocx(file) {
    const buf = await file.arrayBuffer();
    const result = await mammoth.extractRawText({ arrayBuffer: buf });
    return result.value;
  }

  function extractSkills(text) {
    const lower = ' ' + normalize(text) + ' ';
    const found = new Set();
    ALL_TERMS.forEach(term => {
      // word-boundary-ish match, tolerant of punctuation already stripped
      const needle = ' ' + term + ' ';
      if (term.length > 1 && lower.includes(needle)) {
        found.add(ALIAS_LOOKUP[term]);
      }
    });
    return Array.from(found);
  }

  function extractContact(text) {
    const emailMatch = text.match(/[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/);
    const phoneMatch = text.match(/(?:\+?\d{1,3}[-.\s]?)?\d{10}/);
    const linkedinMatch = text.match(/linkedin\.com\/[a-zA-Z0-9\-\/_]+/i);
    const githubMatch = text.match(/github\.com\/[a-zA-Z0-9\-\/_]+/i);
    return {
      email: emailMatch ? emailMatch[0] : null,
      phone: phoneMatch ? phoneMatch[0] : null,
      linkedin: linkedinMatch ? linkedinMatch[0] : null,
      github: githubMatch ? githubMatch[0] : null
    };
  }

  const SECTION_PATTERNS = {
    'Contact Info': /email|phone|contact/i,
    'Education': /education|academic|b\.?tech|b\.?e\.?|degree|university|college/i,
    'Skills': /skills|technical skills|competenc/i,
    'Experience / Projects': /experience|projects|internship|work history/i,
    'Certifications': /certification|certificate|course completed/i
  };

  function extractSections(text) {
    const found = {};
    Object.entries(SECTION_PATTERNS).forEach(([label, pattern]) => {
      found[label] = pattern.test(text);
    });
    return found;
  }

  function countBulletsAndActionVerbs(text) {
    const bulletLines = (text.match(/^[\s]*[•\-\*▪●][\s]/gm) || []).length;
    const actionVerbs = ['developed','built','designed','implemented','created','led','managed',
      'analyzed','optimized','automated','deployed','collaborated','improved','launched','achieved',
      'reduced','increased','tested','integrated','maintained'];
    const lower = text.toLowerCase();
    const verbHits = actionVerbs.filter(v => lower.includes(v)).length;
    return { bulletLines, verbHits };
  }

  function wordCount(text) {
    return (text.trim().match(/\S+/g) || []).length;
  }

  function analyzeResumeText(text) {
    return {
      rawText: text,
      skills: extractSkills(text),
      contact: extractContact(text),
      sections: extractSections(text),
      structure: countBulletsAndActionVerbs(text),
      words: wordCount(text)
    };
  }

  return { extractTextFromFile, extractSkills, analyzeResumeText };
})();
