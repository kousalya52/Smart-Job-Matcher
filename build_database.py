"""
build_database.py — expands the skills/roles knowledge base with
IT and non-IT roles, then regenerates frontend/js/data.js.

Run from the project root:  python3 build_database.py
"""
import json
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(ROOT, 'backend', 'data', 'skills_database.json')
JS_PATH = os.path.join(ROOT, 'frontend', 'js', 'data.js')

with open(DB_PATH, encoding='utf-8') as f:
    db = json.load(f)


def skill(sid, name, category, aliases=None):
    db['skills'][sid] = {'name': name, 'category': category, 'aliases': aliases or []}


def resource(sid, platform, action):
    db['resources'][sid] = {'platform': platform, 'action': action}


def role(rid, title, tagline, category, pairs):
    db['roles'][rid] = {
        'title': title,
        'tagline': tagline,
        'category': category,
        'skills': [{'id': s, 'weight': w} for s, w in pairs],
    }


# ======================================================================
# CATEGORY on existing IT roles
# ======================================================================
EXISTING_CATEGORIES = {
    'frontend-developer': 'Information Technology',
    'backend-developer': 'Information Technology',
    'fullstack-developer': 'Information Technology',
    'android-developer': 'Information Technology',
    'qa-engineer': 'Information Technology',
    'devops-engineer': 'Information Technology',
    'cybersecurity-analyst': 'Information Technology',
    'data-analyst': 'Data & AI',
    'data-scientist': 'Data & AI',
    'ml-engineer': 'Data & AI',
    'ui-ux-designer': 'Design & Creative',
    'digital-marketing': 'Marketing & Sales',
}
for rid, cat in EXISTING_CATEGORIES.items():
    db['roles'][rid]['category'] = cat


# ======================================================================
# NEW SKILLS
# ======================================================================

# ---- Finance & Accounting ----
skill('tally', 'Tally ERP', 'Finance', ['tally erp', 'tally prime'])
skill('bookkeeping', 'Bookkeeping', 'Finance', ['book keeping'])
skill('financial-accounting', 'Financial Accounting', 'Finance', ['accounting'])
skill('taxation', 'Taxation', 'Finance', ['gst', 'income tax', 'tds'])
skill('auditing', 'Auditing', 'Finance', ['audit', 'internal audit'])
skill('financial-analysis', 'Financial Analysis', 'Finance', [])
skill('financial-modeling', 'Financial Modeling', 'Finance', ['dcf', 'valuation'])
skill('accounts-payable', 'Accounts Payable', 'Finance', ['accounts payable'])
skill('accounts-receivable', 'Accounts Receivable', 'Finance', ['accounts receivable'])
skill('sap', 'SAP ERP', 'Finance', ['sap fico', 'sap mm'])
skill('quickbooks', 'QuickBooks', 'Finance', [])
skill('payroll', 'Payroll Processing', 'Finance', ['payroll'])
skill('banking-operations', 'Banking Operations', 'Finance', ['retail banking'])
skill('risk-analysis', 'Risk Analysis', 'Finance', ['credit risk', 'risk assessment'])
skill('equity-research', 'Equity Research', 'Finance', ['stock analysis'])

# ---- Human Resources ----
skill('recruitment', 'Recruitment', 'HR', ['talent acquisition', 'hiring', 'sourcing candidates'])
skill('interviewing', 'Interviewing', 'HR', ['conducting interviews'])
skill('onboarding', 'Employee Onboarding', 'HR', ['onboarding'])
skill('hr-policies', 'HR Policies', 'HR', ['hr operations'])
skill('hrms', 'HRMS Tools', 'HR', ['hris', 'workday', 'zoho people'])
skill('employee-engagement', 'Employee Engagement', 'HR', [])
skill('labour-law', 'Labour Law Compliance', 'HR', ['labour law', 'statutory compliance'])
skill('performance-management', 'Performance Management', 'HR', ['appraisal'])

# ---- Sales, Marketing & Retail ----
skill('crm', 'CRM Tools', 'Sales', ['salesforce', 'zoho crm', 'hubspot crm'])
skill('lead-generation', 'Lead Generation', 'Sales', ['prospecting'])
skill('negotiation', 'Negotiation', 'Sales', ['negotiating'])
skill('cold-calling', 'Cold Calling', 'Sales', ['telecalling', 'tele calling'])
skill('b2b-sales', 'B2B Sales', 'Sales', ['corporate sales', 'field sales'])
skill('market-research', 'Market Research', 'Sales', ['competitor analysis'])
skill('presentation-skills', 'Presentation Skills', 'Soft Skill', ['client presentation'])
skill('customer-service', 'Customer Service', 'Sales', ['customer support', 'client servicing'])
skill('retail-operations', 'Retail Operations', 'Sales', ['store operations'])
skill('inventory-management', 'Inventory Management', 'Operations', ['stock management'])
skill('visual-merchandising', 'Visual Merchandising', 'Sales', ['merchandising'])

# ---- Operations & Supply Chain ----
skill('supply-chain', 'Supply Chain Management', 'Operations', ['scm'])
skill('logistics', 'Logistics', 'Operations', ['transportation management'])
skill('procurement', 'Procurement', 'Operations', ['purchasing', 'vendor sourcing'])
skill('warehouse-management', 'Warehouse Management', 'Operations', ['warehousing'])
skill('lean-six-sigma', 'Lean Six Sigma', 'Operations', ['six sigma', 'kaizen', 'lean manufacturing'])
skill('process-improvement', 'Process Improvement', 'Operations', ['process optimization'])
skill('vendor-management', 'Vendor Management', 'Operations', ['supplier management'])

# ---- Business Analysis & Project Management ----
skill('requirement-gathering', 'Requirement Gathering', 'Business', ['requirements analysis'])
skill('business-analysis', 'Business Analysis', 'Business', ['brd', 'gap analysis'])
skill('stakeholder-management', 'Stakeholder Management', 'Business', ['client management'])
skill('project-management', 'Project Management', 'Business', ['project planning'])
skill('agile-scrum', 'Agile & Scrum', 'Business', ['agile', 'scrum', 'kanban'])
skill('ms-office', 'MS Office', 'Tools', ['microsoft office', 'ms word', 'powerpoint', 'ms excel'])
skill('documentation', 'Documentation', 'Business', ['technical documentation', 'sop'])
skill('reporting', 'Reporting & Dashboards', 'Business', ['mis reporting', 'mis'])
skill('data-entry', 'Data Entry', 'Tools', ['data entry operator'])
skill('typing-speed', 'Typing Speed', 'Tools', ['typing'])

# ---- Mechanical / Manufacturing ----
skill('autocad', 'AutoCAD', 'Engineering', ['auto cad'])
skill('solidworks', 'SolidWorks', 'Engineering', ['solid works'])
skill('catia', 'CATIA', 'Engineering', [])
skill('ansys', 'ANSYS', 'Engineering', ['fea', 'finite element analysis'])
skill('gd-t', 'GD&T', 'Engineering', ['geometric dimensioning'])
skill('cnc', 'CNC Machining', 'Engineering', ['cnc', 'vmc'])
skill('manufacturing-process', 'Manufacturing Processes', 'Engineering', ['production process'])
skill('thermodynamics', 'Thermodynamics', 'Engineering', ['heat transfer'])
skill('quality-control', 'Quality Control', 'Engineering', ['qc', 'quality assurance', 'qa qc'])
skill('iso-standards', 'ISO Standards', 'Engineering', ['iso 9001'])
skill('preventive-maintenance', 'Preventive Maintenance', 'Engineering', ['maintenance planning'])
skill('production-planning', 'Production Planning', 'Engineering', ['ppc'])

# ---- Civil ----
skill('staad-pro', 'STAAD Pro', 'Engineering', ['staad'])
skill('revit', 'Revit', 'Engineering', ['bim'])
skill('structural-analysis', 'Structural Analysis', 'Engineering', ['structural design'])
skill('surveying', 'Surveying', 'Engineering', ['total station', 'land surveying'])
skill('construction-management', 'Construction Management', 'Engineering', ['site management'])
skill('estimation-costing', 'Estimation & Costing', 'Engineering', ['quantity surveying', 'boq'])
skill('concrete-technology', 'Concrete Technology', 'Engineering', ['concrete mix design'])
skill('site-supervision', 'Site Supervision', 'Engineering', ['site execution'])

# ---- Electrical / Electronics ----
skill('circuit-design', 'Circuit Design', 'Engineering', ['circuit analysis'])
skill('plc-scada', 'PLC & SCADA', 'Engineering', ['plc', 'scada', 'automation'])
skill('power-systems', 'Power Systems', 'Engineering', ['power distribution'])
skill('embedded-systems', 'Embedded Systems', 'Engineering', ['microcontroller', 'arduino'])
skill('matlab', 'MATLAB', 'Engineering', ['simulink'])
skill('electrical-safety', 'Electrical Safety', 'Engineering', ['electrical maintenance'])
skill('vlsi', 'VLSI Design', 'Engineering', ['verilog', 'vhdl'])
skill('iot', 'IoT', 'Engineering', ['internet of things'])
skill('pcb-design', 'PCB Design', 'Engineering', ['pcb'])

# ---- Healthcare ----
skill('patient-care', 'Patient Care', 'Healthcare', ['nursing care'])
skill('clinical-procedures', 'Clinical Procedures', 'Healthcare', ['clinical skills'])
skill('medical-terminology', 'Medical Terminology', 'Healthcare', [])
skill('pharmacology', 'Pharmacology', 'Healthcare', ['pharmaceutics'])
skill('dispensing', 'Dispensing & Prescription Handling', 'Healthcare', ['dispensing'])
skill('lab-techniques', 'Laboratory Techniques', 'Healthcare', ['lab testing', 'pathology'])
skill('phlebotomy', 'Phlebotomy', 'Healthcare', ['blood collection'])
skill('infection-control', 'Infection Control', 'Healthcare', ['sterilization'])
skill('emr', 'EMR Systems', 'Healthcare', ['electronic medical records', 'hospital management system'])
skill('anatomy', 'Anatomy & Physiology', 'Healthcare', ['anatomy'])
skill('physiotherapy-techniques', 'Physiotherapy Techniques', 'Healthcare', ['rehabilitation'])
skill('vital-signs', 'Vital Signs Monitoring', 'Healthcare', ['patient monitoring'])

# ---- Education ----
skill('lesson-planning', 'Lesson Planning', 'Education', ['lesson plans'])
skill('classroom-management', 'Classroom Management', 'Education', [])
skill('curriculum-development', 'Curriculum Development', 'Education', ['curriculum design'])
skill('student-assessment', 'Student Assessment', 'Education', ['evaluation'])
skill('subject-expertise', 'Subject Expertise', 'Education', ['subject knowledge'])
skill('edtech-tools', 'EdTech Tools', 'Education', ['google classroom', 'smart class'])

# ---- Media & Creative ----
skill('content-writing', 'Content Writing', 'Creative', ['copywriting', 'blog writing'])
skill('editing-proofreading', 'Editing & Proofreading', 'Creative', ['proofreading'])
skill('storytelling', 'Storytelling', 'Creative', ['narrative'])
skill('wordpress', 'WordPress', 'Creative', ['cms'])
skill('adobe-photoshop', 'Adobe Photoshop', 'Creative', ['photoshop'])
skill('adobe-illustrator', 'Adobe Illustrator', 'Creative', ['illustrator'])
skill('canva', 'Canva', 'Creative', [])
skill('premiere-pro', 'Adobe Premiere Pro', 'Creative', ['premiere pro', 'premiere'])
skill('after-effects', 'After Effects', 'Creative', ['motion graphics'])
skill('video-editing', 'Video Editing', 'Creative', ['film editing'])
skill('photography', 'Photography', 'Creative', ['videography'])
skill('typography', 'Typography', 'Creative', [])
skill('branding', 'Branding', 'Creative', ['brand identity'])
skill('journalism', 'Reporting & Journalism', 'Creative', ['news reporting', 'news writing'])
skill('script-writing', 'Script Writing', 'Creative', ['scripting'])

# ---- Legal ----
skill('legal-research', 'Legal Research', 'Legal', ['case research'])
skill('contract-drafting', 'Contract Drafting', 'Legal', ['drafting agreements'])
skill('compliance', 'Regulatory Compliance', 'Legal', ['legal compliance'])
skill('litigation', 'Litigation Support', 'Legal', ['court procedures'])
skill('legal-documentation', 'Legal Documentation', 'Legal', ['legal drafting'])

# ---- Hospitality & Tourism ----
skill('front-office', 'Front Office Operations', 'Hospitality', ['front desk', 'reception'])
skill('guest-relations', 'Guest Relations', 'Hospitality', ['guest handling'])
skill('food-beverage', 'Food & Beverage Service', 'Hospitality', ['f&b service'])
skill('culinary-skills', 'Culinary Skills', 'Hospitality', ['cooking', 'food preparation'])
skill('food-safety', 'Food Safety & Hygiene', 'Hospitality', ['haccp', 'fssai'])
skill('housekeeping', 'Housekeeping Operations', 'Hospitality', ['housekeeping'])
skill('pos-systems', 'POS Systems', 'Hospitality', ['billing software'])
skill('event-management', 'Event Management', 'Hospitality', ['event planning'])
skill('menu-planning', 'Menu Planning', 'Hospitality', ['menu costing'])

# ---- Agriculture ----
skill('agronomy', 'Agronomy', 'Agriculture', [])
skill('soil-science', 'Soil Science', 'Agriculture', ['soil testing'])
skill('crop-management', 'Crop Management', 'Agriculture', ['crop production'])
skill('farm-equipment', 'Farm Equipment', 'Agriculture', ['farm machinery'])
skill('pest-management', 'Pest Management', 'Agriculture', ['plant protection'])

# ---- Extra soft skills ----
skill('time-management', 'Time Management', 'Soft Skill', [])
skill('adaptability', 'Adaptability', 'Soft Skill', ['flexibility'])
skill('leadership', 'Leadership', 'Soft Skill', ['team leading'])
skill('attention-to-detail', 'Attention to Detail', 'Soft Skill', ['detail oriented'])
skill('multitasking', 'Multitasking', 'Soft Skill', [])
skill('empathy', 'Empathy', 'Soft Skill', ['compassion'])


# ======================================================================
# LEARNING RESOURCES for the new skills
# ======================================================================
RESOURCES = {
    'tally': ('Tally Education (free learning portal)', 'Complete the Tally Essentials Level 1 modules'),
    'bookkeeping': ('OpenLearn / Alison free courses', 'Practice recording a full month of entries in a ledger'),
    'financial-accounting': ('NPTEL / Swayam free course', 'Work through journal, ledger, and final accounts problems'),
    'taxation': ('ClearTax learning centre', 'Practice filing a sample GST return and an ITR-1'),
    'auditing': ('ICAI study material (free)', 'Study the audit procedures module and work one sample audit checklist'),
    'financial-analysis': ('CFI free courses', 'Analyze one listed company\'s annual report end to end'),
    'financial-modeling': ('CFI free modeling course', 'Build a 3-statement model for one company in Excel'),
    'accounts-payable': ('AccountingCoach (free)', 'Practice the full purchase-to-pay cycle with sample invoices'),
    'accounts-receivable': ('AccountingCoach (free)', 'Practice ageing analysis and collections tracking in Excel'),
    'sap': ('openSAP (free courses)', 'Complete an SAP S/4HANA fundamentals course'),
    'quickbooks': ('QuickBooks official tutorials', 'Set up a sample company file and record a month of transactions'),
    'payroll': ('ClearTax / Zoho Payroll guides', 'Compute a sample payroll with PF, ESI, and TDS deductions'),
    'banking-operations': ('IIBF free resources', 'Study the retail banking products and KYC norms modules'),
    'risk-analysis': ('CFI free credit fundamentals', 'Assess the creditworthiness of one sample borrower profile'),
    'equity-research': ('Zerodha Varsity (free)', 'Write one equity research note on a listed company'),

    'recruitment': ('LinkedIn Talent Blog / HubSpot Academy', 'Source and shortlist 10 candidates for a sample job description'),
    'interviewing': ('Harvard Business Review articles', 'Run three mock interviews using a structured scorecard'),
    'onboarding': ('SHRM free resources', 'Design a 30-day onboarding plan for one role'),
    'hr-policies': ('SHRM / Indian labour law portals', 'Draft a sample leave and attendance policy'),
    'hrms': ('Zoho People / Keka free trials', 'Set up a demo employee database and run one attendance cycle'),
    'employee-engagement': ('Gallup research articles (free)', 'Design an employee pulse survey and analyze sample results'),
    'labour-law': ('India Code / labour ministry portal', 'Study the PF, ESI, and Shops & Establishments Act basics'),
    'performance-management': ('SHRM free toolkit', 'Write sample KRAs and an appraisal form for one role'),

    'crm': ('HubSpot Academy (free)', 'Complete the CRM fundamentals course and set up a demo pipeline'),
    'lead-generation': ('HubSpot Academy (free)', 'Build a list of 50 qualified leads for a sample product'),
    'negotiation': ('Coursera "Successful Negotiation" (free audit)', 'Practice three role-play negotiations with a peer'),
    'cold-calling': ('HubSpot Sales Blog', 'Write a 30-second pitch script and practice 20 calls'),
    'b2b-sales': ('HubSpot Academy (free)', 'Complete the inbound sales certification'),
    'market-research': ('Google Market Finder + free reports', 'Write one competitor analysis report for a chosen product'),
    'presentation-skills': ('TED Talks + practice', 'Deliver one 5-minute pitch and record yourself to review'),
    'customer-service': ('HubSpot Academy (free)', 'Complete the customer service certification'),
    'retail-operations': ('Alison free retail courses', 'Study store layout, billing, and stock replenishment basics'),
    'inventory-management': ('Alison / Coursera free audit', 'Practice EOQ and reorder-level calculations on sample data'),
    'visual-merchandising': ('Alison free course', 'Redesign one store display and document the reasoning'),

    'supply-chain': ('MIT OpenCourseWare / Coursera audit', 'Map an end-to-end supply chain for one product'),
    'logistics': ('Alison free logistics course', 'Plan a sample shipment route with cost comparison'),
    'procurement': ('CIPS free resources', 'Run a sample vendor comparison and write a purchase recommendation'),
    'warehouse-management': ('Alison free course', 'Design a sample warehouse layout with picking strategy'),
    'lean-six-sigma': ('ASQ / Coursera free audit', 'Complete a Six Sigma Yellow Belt course and one DMAIC case'),
    'process-improvement': ('Lean Enterprise Institute (free articles)', 'Map and improve one real process you know well'),
    'vendor-management': ('CIPS free resources', 'Build a vendor scorecard and evaluate three sample suppliers'),

    'requirement-gathering': ('IIBA free resources', 'Write a requirements document for a small app idea'),
    'business-analysis': ('IIBA BABOK overview (free)', 'Prepare a BRD and process flow for one business scenario'),
    'stakeholder-management': ('PMI free articles', 'Build a stakeholder matrix for a sample project'),
    'project-management': ('Google Project Management (Coursera, free audit)', 'Plan one project end to end with timeline and risks'),
    'agile-scrum': ('Scrum.org free Scrum Guide', 'Read the Scrum Guide and run one sprint on a personal project'),
    'ms-office': ('Microsoft Learn (free)', 'Practice Word formatting, Excel formulas, and PowerPoint decks'),
    'documentation': ('Google Technical Writing (free)', 'Complete Technical Writing One and document one process'),
    'reporting': ('Microsoft Learn / Excel training', 'Build one automated MIS dashboard from raw data'),
    'data-entry': ('TypingClub + Excel basics', 'Practice accurate bulk entry with validation checks'),
    'typing-speed': ('TypingClub / Keybr (free)', 'Practice daily until you reach 40+ WPM with high accuracy'),

    'autocad': ('Autodesk free tutorials', 'Draft one complete 2D component drawing with dimensions'),
    'solidworks': ('SolidWorks tutorials (built-in)', 'Model and assemble one multi-part product'),
    'catia': ('Dassault free learning resources', 'Complete a part design and assembly exercise'),
    'ansys': ('ANSYS Innovation Courses (free)', 'Run one structural stress simulation end to end'),
    'gd-t': ('ASME / free GD&T primers', 'Annotate one drawing fully with GD&T symbols'),
    'cnc': ('Titans of CNC Academy (free)', 'Complete the beginner CNC programming series'),
    'manufacturing-process': ('NPTEL free course', 'Study casting, welding, machining, and forming modules'),
    'thermodynamics': ('NPTEL / MIT OCW', 'Work through the core thermodynamics problem sets'),
    'quality-control': ('ASQ free resources', 'Practice building control charts and inspection plans'),
    'iso-standards': ('ISO official overviews', 'Study ISO 9001 clauses and draft a sample quality manual section'),
    'preventive-maintenance': ('Alison free maintenance course', 'Build a preventive maintenance schedule for sample machinery'),
    'production-planning': ('NPTEL / Alison free course', 'Create a sample production plan with capacity calculations'),

    'staad-pro': ('Bentley official tutorials', 'Analyze and design one simple steel frame'),
    'revit': ('Autodesk free tutorials', 'Model one small building with BIM elements'),
    'structural-analysis': ('NPTEL free course', 'Solve beam, truss, and frame analysis problem sets'),
    'surveying': ('NPTEL / field practice', 'Complete one site survey exercise with a total station'),
    'construction-management': ('NPTEL / Coursera free audit', 'Build a construction schedule for a small project'),
    'estimation-costing': ('NPTEL free course', 'Prepare a complete BOQ for a single-room structure'),
    'concrete-technology': ('NPTEL free course', 'Work through mix design calculations for M20 and M25'),
    'site-supervision': ('Alison free construction course', 'Study site safety, quality checks, and daily progress reporting'),

    'circuit-design': ('All About Circuits (free textbook)', 'Design and simulate five basic circuits'),
    'plc-scada': ('Free PLC simulator + YouTube courses', 'Program one ladder-logic automation sequence'),
    'power-systems': ('NPTEL free course', 'Study load flow, fault analysis, and protection modules'),
    'embedded-systems': ('Arduino official tutorials', 'Build three microcontroller projects end to end'),
    'matlab': ('MATLAB Onramp (free)', 'Complete the official MATLAB and Simulink Onramp courses'),
    'electrical-safety': ('OSHA / NEC free resources', 'Study the electrical safety and earthing standards'),
    'vlsi': ('NPTEL free VLSI course', 'Write and simulate five Verilog modules'),
    'iot': ('Cisco Networking Academy (free)', 'Complete "Introduction to IoT" and build one sensor project'),
    'pcb-design': ('KiCad official docs (free tool)', 'Design one complete two-layer PCB'),

    'patient-care': ('Nursing council guidelines + clinical practice', 'Practice care plans across common ward scenarios'),
    'clinical-procedures': ('WHO / clinical skill guides', 'Practice core procedures under supervised clinical training'),
    'medical-terminology': ('Free medical terminology courses (Alison)', 'Learn root words, prefixes, and suffixes systematically'),
    'pharmacology': ('NPTEL / standard pharmacology texts', 'Revise drug classes, mechanisms, and interactions'),
    'dispensing': ('Pharmacy council guidelines', 'Practice prescription reading and dispensing documentation'),
    'lab-techniques': ('WHO lab manuals (free)', 'Practice sample handling, staining, and analyzer operation'),
    'phlebotomy': ('WHO phlebotomy guidelines (free)', 'Practice venipuncture technique under supervision'),
    'infection-control': ('WHO infection prevention course (free)', 'Complete the hand hygiene and sterilization modules'),
    'emr': ('Hospital HMIS demos / free trials', 'Practice patient record entry on a demo system'),
    'anatomy': ('Kenhub / free anatomy atlases', 'Revise systems one at a time with self-testing'),
    'physiotherapy-techniques': ('Physiopedia (free)', 'Study common rehab protocols and practice assessments'),
    'vital-signs': ('WHO / nursing skill guides', 'Practice accurate BP, pulse, temperature, and SpO2 recording'),

    'lesson-planning': ('Khan Academy Teacher resources', 'Write five lesson plans with objectives and assessments'),
    'classroom-management': ('Edutopia (free articles)', 'Study behaviour management strategies and try them in practice'),
    'curriculum-development': ('NCERT / CBSE frameworks', 'Map one term\'s curriculum with learning outcomes'),
    'student-assessment': ('Edutopia / assessment guides', 'Design formative and summative assessments for one unit'),
    'subject-expertise': ('NPTEL / subject textbooks', 'Revise the full syllabus you intend to teach and self-test'),
    'edtech-tools': ('Google for Education (free training)', 'Complete the Google Classroom educator course'),

    'content-writing': ('HubSpot Academy (free)', 'Write 10 blog posts and build a portfolio'),
    'editing-proofreading': ('Grammarly Handbook / Purdue OWL', 'Edit five sample articles against a style guide'),
    'storytelling': ('Pixar in a Box (Khan Academy, free)', 'Complete the storytelling course and write one narrative piece'),
    'wordpress': ('WordPress.org learn portal', 'Build and publish one complete website'),
    'adobe-photoshop': ('Adobe free tutorials', 'Recreate five designs to practice core tools'),
    'adobe-illustrator': ('Adobe free tutorials', 'Design five vector logos from scratch'),
    'canva': ('Canva Design School (free)', 'Complete the graphic design essentials course'),
    'premiere-pro': ('Adobe free tutorials', 'Edit one complete 3-minute video with transitions and audio'),
    'after-effects': ('Adobe free tutorials', 'Create one animated title sequence'),
    'video-editing': ('DaVinci Resolve free training', 'Edit three short videos end to end'),
    'photography': ('Free photography courses (Alison)', 'Practice exposure triangle with 100 deliberate shots'),
    'typography': ('Practical Typography (free online book)', 'Redesign one poster focusing only on type'),
    'branding': ('Free branding courses (HubSpot)', 'Build one complete brand identity kit for a fictional company'),
    'journalism': ('Reuters / BBC Academy free resources', 'Write five news reports following the inverted pyramid'),
    'script-writing': ('BBC Writers Room (free)', 'Write one short film script with proper formatting'),

    'legal-research': ('Indian Kanoon / SCC Online basics', 'Research and summarize five judgments on one legal issue'),
    'contract-drafting': ('Free legal drafting guides', 'Draft an NDA, a service agreement, and a lease deed'),
    'compliance': ('MCA / SEBI official portals', 'Study the compliance calendar for one company type'),
    'litigation': ('Court procedure handbooks', 'Study civil and criminal procedure basics, observe court proceedings'),
    'legal-documentation': ('Free legal drafting guides', 'Practice drafting plaints, notices, and affidavits'),

    'front-office': ('Alison free hospitality course', 'Practice check-in, check-out, and reservation handling'),
    'guest-relations': ('Alison free hospitality course', 'Study complaint handling and service-recovery techniques'),
    'food-beverage': ('Alison free F&B course', 'Study service sequences, cutlery, and order-taking'),
    'culinary-skills': ('Culinary basics courses (Alison)', 'Master five mother sauces and core knife skills'),
    'food-safety': ('FSSAI / FoSTaC training', 'Complete a food-safety supervisor training module'),
    'housekeeping': ('Alison free hospitality course', 'Study room-cleaning standards and linen management'),
    'pos-systems': ('Free POS software trials', 'Practice full billing, discount, and settlement flows'),
    'event-management': ('Alison free event course', 'Plan one full event with budget, timeline, and vendor list'),
    'menu-planning': ('Culinary management resources', 'Build one menu with costing and profit margins'),

    'agronomy': ('ICAR / NPTEL free courses', 'Study cropping systems and nutrient management'),
    'soil-science': ('ICAR e-courses (free)', 'Practice soil sample collection and testing interpretation'),
    'crop-management': ('ICAR / KVK resources', 'Prepare a season-long crop management plan'),
    'farm-equipment': ('ICAR e-courses (free)', 'Study tractor and implement operation and maintenance'),
    'pest-management': ('ICAR / FAO free resources', 'Study integrated pest management for two major crops'),

    'time-management': ('Free productivity courses', 'Track your time for one week and restructure your schedule'),
    'adaptability': ('Practice + reflection', 'Take on one task outside your comfort zone each week'),
    'leadership': ('Free leadership courses (Coursera audit)', 'Lead one group project or college initiative end to end'),
    'attention-to-detail': ('Practice exercises', 'Proofread and verify your own work with a checklist every time'),
    'multitasking': ('Practice + prioritization frameworks', 'Practice using Eisenhower matrix to juggle parallel tasks'),
    'empathy': ('Free communication courses', 'Practice active listening in every conversation for two weeks'),
}
for sid, (platform, action) in RESOURCES.items():
    resource(sid, platform, action)


# ======================================================================
# NEW ROLES
# ======================================================================

IT = 'Information Technology'
DATA = 'Data & AI'
DESIGN = 'Design & Creative'
MKT = 'Marketing & Sales'
FIN = 'Finance & Accounting'
HR = 'Human Resources'
BIZ = 'Business & Operations'
ENGG = 'Core Engineering'
HEALTH = 'Healthcare'
EDU = 'Education'
LEGAL = 'Legal'
HOSP = 'Hospitality & Tourism'
AGRI = 'Agriculture'

# ---- Information Technology (additions) ----
role('cloud-engineer', 'Cloud Engineer', 'Runs the infrastructure everything else sits on', IT, [
    ('aws', 3), ('linux', 3), ('docker', 2), ('kubernetes', 2), ('ci-cd', 2),
    ('python', 2), ('azure', 1), ('gcp', 1), ('git', 1)])

role('database-administrator', 'Database Administrator', 'Keeps the data fast, safe, and available', IT, [
    ('sql', 3), ('mongodb', 2), ('linux', 2), ('python', 1), ('aws', 1),
    ('documentation', 1), ('problem-solving', 2)])

role('technical-support-engineer', 'Technical Support Engineer', 'The person who actually fixes it', IT, [
    ('communication', 3), ('problem-solving', 3), ('linux', 2), ('sql', 2),
    ('customer-service', 2), ('jira', 1), ('rest-api', 1), ('documentation', 1)])

# ---- Design & Creative ----
role('graphic-designer', 'Graphic Designer', 'Makes ideas look like something', DESIGN, [
    ('adobe-photoshop', 3), ('adobe-illustrator', 3), ('typography', 2), ('branding', 2),
    ('canva', 1), ('figma', 1), ('attention-to-detail', 1)])

role('video-editor', 'Video Editor', 'Turns raw footage into something worth watching', DESIGN, [
    ('video-editing', 3), ('premiere-pro', 3), ('after-effects', 2), ('storytelling', 2),
    ('photography', 1), ('attention-to-detail', 1)])

role('content-writer', 'Content Writer', 'Writes the words that sell and explain', DESIGN, [
    ('content-writing', 3), ('editing-proofreading', 3), ('seo', 2), ('storytelling', 2),
    ('wordpress', 1), ('market-research', 1), ('communication', 2)])

role('journalist', 'Journalist / Reporter', 'Finds the story and gets it right', DESIGN, [
    ('journalism', 3), ('content-writing', 3), ('editing-proofreading', 2), ('interviewing', 2),
    ('communication', 2), ('market-research', 1), ('photography', 1)])

# ---- Marketing & Sales ----
role('sales-executive', 'Sales Executive', 'Turns conversations into closed deals', MKT, [
    ('communication', 3), ('negotiation', 3), ('crm', 2), ('lead-generation', 2),
    ('cold-calling', 2), ('presentation-skills', 2), ('ms-office', 1), ('customer-service', 1)])

role('business-development-executive', 'Business Development Executive', 'Opens the doors nobody opened yet', MKT, [
    ('lead-generation', 3), ('b2b-sales', 3), ('communication', 3), ('market-research', 2),
    ('negotiation', 2), ('crm', 2), ('presentation-skills', 1)])

role('customer-support-executive', 'Customer Support Executive', 'Keeps customers from walking away', MKT, [
    ('customer-service', 3), ('communication', 3), ('empathy', 2), ('crm', 2),
    ('problem-solving', 2), ('ms-office', 1), ('multitasking', 1)])

role('retail-store-manager', 'Retail Store Executive / Manager', 'Runs the floor and the numbers behind it', MKT, [
    ('retail-operations', 3), ('customer-service', 3), ('inventory-management', 2),
    ('visual-merchandising', 2), ('leadership', 2), ('pos-systems', 1), ('ms-office', 1)])

# ---- Finance & Accounting ----
role('accountant', 'Accountant', 'Keeps the books honest and current', FIN, [
    ('financial-accounting', 3), ('tally', 3), ('excel', 3), ('taxation', 2),
    ('bookkeeping', 2), ('accounts-payable', 1), ('accounts-receivable', 1),
    ('attention-to-detail', 2), ('sap', 1)])

role('financial-analyst', 'Financial Analyst', 'Turns financial data into decisions', FIN, [
    ('excel', 3), ('financial-analysis', 3), ('financial-modeling', 2), ('financial-accounting', 2),
    ('sql', 1), ('powerbi', 1), ('reporting', 2), ('communication', 1)])

role('auditor', 'Audit Associate', 'Checks that the numbers say what they claim', FIN, [
    ('auditing', 3), ('financial-accounting', 3), ('excel', 2), ('compliance', 2),
    ('attention-to-detail', 3), ('documentation', 1), ('taxation', 1)])

role('tax-associate', 'Tax Associate', 'Navigates the rules so the filing is clean', FIN, [
    ('taxation', 3), ('financial-accounting', 2), ('excel', 2), ('compliance', 2),
    ('tally', 1), ('attention-to-detail', 2), ('documentation', 1)])

role('banking-officer', 'Banking Officer / Associate', 'The front line of retail banking', FIN, [
    ('banking-operations', 3), ('customer-service', 3), ('communication', 2),
    ('ms-office', 2), ('risk-analysis', 1), ('attention-to-detail', 2), ('crm', 1)])

# ---- Human Resources ----
role('hr-recruiter', 'HR Recruiter', 'Finds the right person before someone else does', HR, [
    ('recruitment', 3), ('interviewing', 3), ('communication', 3), ('hrms', 2),
    ('ms-office', 1), ('onboarding', 1), ('time-management', 1)])

role('hr-generalist', 'HR Generalist / Executive', 'Holds the people side of the company together', HR, [
    ('hr-policies', 3), ('recruitment', 2), ('payroll', 2), ('employee-engagement', 2),
    ('labour-law', 2), ('hrms', 2), ('communication', 2), ('performance-management', 1)])

# ---- Business & Operations ----
role('business-analyst', 'Business Analyst', 'Translates what the business wants into what gets built', BIZ, [
    ('business-analysis', 3), ('requirement-gathering', 3), ('excel', 2), ('sql', 2),
    ('documentation', 2), ('stakeholder-management', 2), ('agile-scrum', 1), ('communication', 2)])

role('operations-executive', 'Operations Executive', 'Makes the day-to-day actually run', BIZ, [
    ('process-improvement', 2), ('ms-office', 3), ('excel', 2), ('reporting', 2),
    ('vendor-management', 1), ('time-management', 2), ('communication', 2), ('problem-solving', 2)])

role('supply-chain-executive', 'Supply Chain / Logistics Executive', 'Gets things where they need to be', BIZ, [
    ('supply-chain', 3), ('logistics', 3), ('inventory-management', 2), ('procurement', 2),
    ('excel', 2), ('warehouse-management', 1), ('vendor-management', 1), ('sap', 1)])

role('project-coordinator', 'Project Coordinator', 'Keeps the plan, the people, and the dates aligned', BIZ, [
    ('project-management', 3), ('communication', 3), ('ms-office', 2), ('agile-scrum', 2),
    ('stakeholder-management', 2), ('documentation', 2), ('time-management', 2)])

role('data-entry-operator', 'Data Entry Operator', 'Accuracy at speed, every single record', BIZ, [
    ('data-entry', 3), ('typing-speed', 3), ('ms-office', 2), ('excel', 2),
    ('attention-to-detail', 3), ('time-management', 1)])

# ---- Core Engineering ----
role('mechanical-design-engineer', 'Mechanical Design Engineer', 'Designs the part before it exists', ENGG, [
    ('autocad', 3), ('solidworks', 3), ('gd-t', 2), ('manufacturing-process', 2),
    ('catia', 1), ('ansys', 1), ('thermodynamics', 1), ('problem-solving', 1)])

role('production-engineer', 'Production / Manufacturing Engineer', 'Keeps the line running and improving', ENGG, [
    ('manufacturing-process', 3), ('production-planning', 3), ('lean-six-sigma', 2),
    ('quality-control', 2), ('cnc', 1), ('preventive-maintenance', 2), ('ms-office', 1), ('leadership', 1)])

role('quality-engineer', 'Quality Engineer (QA/QC)', 'The last check before it reaches the customer', ENGG, [
    ('quality-control', 3), ('iso-standards', 3), ('gd-t', 2), ('lean-six-sigma', 2),
    ('documentation', 2), ('attention-to-detail', 3), ('manufacturing-process', 1)])

role('civil-engineer', 'Civil Engineer', 'Designs the structures people live and work in', ENGG, [
    ('autocad', 3), ('structural-analysis', 3), ('estimation-costing', 2), ('staad-pro', 2),
    ('concrete-technology', 2), ('revit', 1), ('surveying', 1), ('construction-management', 1)])

role('site-engineer', 'Site Engineer / Supervisor', 'Turns the drawing into the building', ENGG, [
    ('site-supervision', 3), ('construction-management', 3), ('autocad', 2), ('surveying', 2),
    ('estimation-costing', 2), ('quality-control', 1), ('leadership', 2), ('communication', 1)])

role('electrical-engineer', 'Electrical Engineer', 'Designs and maintains the power behind it', ENGG, [
    ('power-systems', 3), ('circuit-design', 3), ('electrical-safety', 2), ('autocad', 2),
    ('plc-scada', 2), ('matlab', 1), ('preventive-maintenance', 1), ('problem-solving', 1)])

role('electronics-engineer', 'Electronics / Embedded Engineer', 'Builds the intelligence into the hardware', ENGG, [
    ('embedded-systems', 3), ('circuit-design', 3), ('c', 2), ('pcb-design', 2),
    ('matlab', 1), ('vlsi', 1), ('iot', 1), ('problem-solving', 1)])

role('automobile-engineer', 'Automobile Engineer', 'Designs and services what moves people', ENGG, [
    ('autocad', 3), ('catia', 2), ('thermodynamics', 2), ('manufacturing-process', 2),
    ('solidworks', 2), ('quality-control', 1), ('preventive-maintenance', 1), ('problem-solving', 1)])

# ---- Healthcare ----
role('staff-nurse', 'Staff Nurse', 'The constant presence at the bedside', HEALTH, [
    ('patient-care', 3), ('clinical-procedures', 3), ('vital-signs', 3), ('infection-control', 2),
    ('medical-terminology', 2), ('anatomy', 2), ('empathy', 2), ('emr', 1), ('communication', 2)])

role('pharmacist', 'Pharmacist', 'The last safety check on every prescription', HEALTH, [
    ('pharmacology', 3), ('dispensing', 3), ('medical-terminology', 2), ('inventory-management', 2),
    ('attention-to-detail', 3), ('customer-service', 1), ('compliance', 1)])

role('medical-lab-technician', 'Medical Lab Technician', 'Produces the result the diagnosis depends on', HEALTH, [
    ('lab-techniques', 3), ('phlebotomy', 3), ('infection-control', 2), ('medical-terminology', 2),
    ('attention-to-detail', 3), ('documentation', 1), ('emr', 1)])

role('physiotherapist', 'Physiotherapist', 'Gets people moving again', HEALTH, [
    ('physiotherapy-techniques', 3), ('anatomy', 3), ('patient-care', 2), ('clinical-procedures', 2),
    ('empathy', 2), ('communication', 2), ('documentation', 1)])

# ---- Education ----
role('school-teacher', 'School Teacher', 'Where most careers actually begin', EDU, [
    ('subject-expertise', 3), ('lesson-planning', 3), ('classroom-management', 3),
    ('student-assessment', 2), ('communication', 3), ('edtech-tools', 1), ('empathy', 2)])

role('academic-content-developer', 'Academic Content Developer', 'Builds what students actually learn from', EDU, [
    ('curriculum-development', 3), ('subject-expertise', 3), ('content-writing', 2),
    ('editing-proofreading', 2), ('student-assessment', 2), ('edtech-tools', 1), ('ms-office', 1)])

# ---- Legal ----
role('legal-associate', 'Legal Associate', 'Does the research the case is built on', LEGAL, [
    ('legal-research', 3), ('legal-documentation', 3), ('contract-drafting', 2),
    ('compliance', 2), ('litigation', 2), ('editing-proofreading', 1), ('attention-to-detail', 2),
    ('communication', 2)])

# ---- Hospitality & Tourism ----
role('hotel-front-office', 'Hotel Front Office Executive', 'The first face every guest meets', HOSP, [
    ('front-office', 3), ('guest-relations', 3), ('communication', 3), ('customer-service', 2),
    ('pos-systems', 1), ('ms-office', 1), ('multitasking', 2)])

role('chef', 'Chef / Commis', 'Consistency under pressure, every service', HOSP, [
    ('culinary-skills', 3), ('food-safety', 3), ('menu-planning', 2), ('inventory-management', 2),
    ('time-management', 2), ('teamwork', 2), ('leadership', 1)])

role('event-manager', 'Event Management Executive', 'Makes a hundred moving parts land on time', HOSP, [
    ('event-management', 3), ('vendor-management', 2), ('communication', 3), ('project-management', 2),
    ('negotiation', 2), ('time-management', 2), ('ms-office', 1), ('multitasking', 2)])

# ---- Agriculture ----
role('agriculture-officer', 'Agriculture Officer', 'Bridges the science and the field', AGRI, [
    ('agronomy', 3), ('crop-management', 3), ('soil-science', 2), ('pest-management', 2),
    ('farm-equipment', 1), ('communication', 2), ('reporting', 1)])


# ======================================================================
# VALIDATE + WRITE
# ======================================================================
errors = []
for rid, r in db['roles'].items():
    if 'category' not in r:
        errors.append(f'role {rid} missing category')
    for s in r['skills']:
        if s['id'] not in db['skills']:
            errors.append(f'role {rid} references unknown skill "{s["id"]}"')
for sid in db['skills']:
    if sid not in db['resources']:
        errors.append(f'skill {sid} has no learning resource')

if errors:
    print('VALIDATION FAILED:')
    for e in errors:
        print('  -', e)
    raise SystemExit(1)

with open(DB_PATH, 'w', encoding='utf-8') as f:
    json.dump(db, f, indent=2, ensure_ascii=False)

with open(JS_PATH, 'w', encoding='utf-8') as f:
    f.write('const SKILL_DB = ' + json.dumps(db, indent=2, ensure_ascii=False) + ';\n')

cats = {}
for r in db['roles'].values():
    cats[r['category']] = cats.get(r['category'], 0) + 1

print(f"OK — {len(db['skills'])} skills, {len(db['roles'])} roles, {len(db['resources'])} resources")
for c, n in sorted(cats.items()):
    print(f'  {c}: {n}')
