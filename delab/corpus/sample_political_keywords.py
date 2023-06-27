"""
the topic list and the corresponding search phrases were generated by Chatgpt using the prompt:
- provide a list of 100 phrases to search for current salient political topics
- can you create a python array and also write a dictionary with search phrases (keywords that can be used in google or twitter search) for each.
"""

topics = [
    "Climate change policies",
    "Income inequality",
    "Universal basic income",
    "Gun control laws",
    "Immigration reforms",
    "Electoral reform",
    "Cybersecurity regulations",
    "Taxation policies",
    "Healthcare reforms",
    "Police reform",
    "Foreign policy strategies",
    "Infrastructure investment",
    "LGBTQ+ rights",
    "Racial justice movements",
    "Women's reproductive rights",
    "Minimum wage increase",
    "Education funding",
    "Affordable housing initiatives",
    "Global trade agreements",
    "Privacy rights",
    "Social media regulations",
    "Renewable energy initiatives",
    "Voting rights",
    "National security measures",
    "Government surveillance programs",
    "Digital privacy laws",
    "Nuclear disarmament",
    "Job creation programs",
    "Criminal justice reforms",
    "Mass surveillance",
    "Internet neutrality",
    "Indigenous rights",
    "Consumer protection regulations",
    "Election interference",
    "Healthcare accessibility",
    "Free speech rights",
    "International aid programs",
    "Campaign finance reforms",
    "Wealth distribution policies",
    "Online censorship",
    "Foreign aid policies",
    "Defense spending",
    "Welfare programs",
    "Drug policy reform",
    "Social security reforms",
    "Privacy invasion",
    "Anti-corruption measures",
    "Refugee policies",
    "Hate speech legislation",
    "Climate action plans",
    "Nuclear power policies",
    "Space exploration funding",
    "Military interventions",
    "Education reform",
    "Freedom of the press",
    "Cyber warfare policies",
    "Government transparency",
    "Hate crime legislation",
    "Surveillance state",
    "Immigration enforcement",
    "Ethical AI regulations",
    "Labor rights",
    "Political lobbying",
    "National debt management",
    "Environmental conservation",
    "Right to protest",
    "Wealth tax proposals",
    "Diplomatic relations",
    "Technology monopolies",
    "Police accountability",
    "Internet censorship",
    "Criminal justice funding",
    "Universal healthcare",
    "Public transportation funding",
    "Foreign aid allocation",
    "Income tax reforms",
    "Digital divide",
    "Social welfare programs",
    "Climate change adaptation",
    "Electoral college reform",
    "Nuclear weapons proliferation",
    "Gender pay gap",
    "Internet privacy laws",
    "Renewable energy subsidies",
    "Government surveillance oversight",
    "Immigration quotas",
    "Affordable childcare",
    "Gerrymandering",
    "Cybersecurity threats",
    "Social justice movements",
    "Online disinformation",
    "Defense contractor oversight",
    "Reproductive healthcare access",
    "Police militarization",
    "Economic sanctions",
    "Anti-trust laws",
    "Workplace discrimination",
    "Government corruption",
    "Data protection regulations",
    "Political polarization"
]

search_phrases = {
    "Climate change policies": ["climate change policies", "climate action", "renewable energy initiatives", "carbon emissions reduction"],
    "Income inequality": ["income inequality", "wealth gap", "economic disparity", "wealth distribution"],
    "Universal basic income": ["universal basic income", "basic income guarantee", "UBI pilot programs", "cash transfer schemes"],
    "Gun control laws": ["gun control laws", "firearm regulations", "gun violence prevention", "background checks"],
    "Immigration reforms": ["immigration reforms", "immigration policy", "border control", "pathway to citizenship"],
    "Electoral reform": ["electoral reform", "voting rights", "campaign finance reform", "gerrymandering"],
    "Cybersecurity regulations": ["cybersecurity regulations", "data protection laws", "cyber threats", "privacy regulations"],
    "Taxation policies": ["taxation policies", "tax reforms", "tax rates", "wealth tax proposals"],
    "Healthcare reforms": ["healthcare reforms", "universal healthcare", "health insurance", "pharmaceutical pricing"],
    "Police reform": ["police reform", "police accountability", "community policing", "use of force"],
    "Foreign policy strategies": ["foreign policy strategies", "diplomatic relations", "international conflicts", "human rights advocacy"],
    "Infrastructure investment": ["infrastructure investment", "transportation infrastructure", "public works projects", "smart cities"],
    "LGBTQ+ rights": ["LGBTQ+ rights", "gay rights", "transgender rights", "marriage equality"],
    "Racial justice movements": ["racial justice movements", "racial inequality", "systemic racism", "Black Lives Matter"],
    "Women's reproductive rights": ["women's reproductive rights", "abortion access", "birth control", "family planning"],
    "Minimum wage increase": ["minimum wage increase", "living wage", "income floor", "wage inequality"],
    "Education funding": ["education funding", "school budgets", "student loans", "teacher salaries"],
    "Affordable housing initiatives": ["affordable housing initiatives", "housing affordability", "rent control", "homelessness"],
    "Global trade agreements": ["global trade agreements", "free trade deals", "tariffs", "trade deficits"],
    "Privacy rights": ["privacy rights", "data privacy", "surveillance", "online privacy"],
    "Social media regulations": ["social media regulations", "platform moderation", "online misinformation", "data breaches"],
    "Renewable energy initiatives": ["renewable energy initiatives", "clean energy transition", "sustainable power generation", "solar and wind energy"],
    "Voting rights": ["voting rights", "voter suppression", "voter ID laws", "voting access"],
    "National security measures": ["national security measures", "counterterrorism", "surveillance programs", "border security"],
    "Government surveillance programs": ["government surveillance programs", "mass surveillance", "surveillance state", "privacy invasion"],
    "Digital privacy laws": ["digital privacy laws", "data protection regulations", "cybersecurity", "online tracking"],
    "Nuclear disarmament": ["nuclear disarmament", "non-proliferation treaty", "arms control", "nuclear weapons ban"],
    "Job creation programs": ["job creation programs", "employment initiatives", "unemployment rates", "job training"],
    "Criminal justice reforms": ["criminal justice reforms", "prison system", "sentencing reform", "rehabilitation programs"],
    "Mass surveillance": ["mass surveillance", "government spying", "privacy erosion", "surveillance technology"],
    "Internet neutrality": ["internet neutrality", "net neutrality", "open internet", "ISP regulations"],
    "Indigenous rights": ["indigenous rights", "land rights", "cultural preservation", "sovereignty"],
    "Consumer protection regulations": ["consumer protection regulations", "product safety", "fraud prevention", "consumer rights"],
    "Election interference": ["election interference", "foreign meddling", "cyber attacks", "disinformation campaigns"],
    "Healthcare accessibility": ["healthcare accessibility", "healthcare disparities", "healthcare deserts", "healthcare for all"],
    "Free speech rights": ["free speech rights", "freedom of expression", "censorship", "hate speech"],
    "International aid programs": ["international aid programs", "foreign aid", "humanitarian assistance", "global development"],
    "Campaign finance reforms": ["campaign finance reforms", "money in politics", "campaign contributions", "dark money"],
    "Wealth distribution policies": ["wealth distribution policies", "income redistribution", "wealth tax", "economic equality"],
    "Online censorship": ["online censorship", "content moderation", "internet bans", "freedom of information"],
    "Foreign aid policies": ["foreign aid policies", "international assistance", "aid allocation", "development programs"],
    "Defense spending": ["defense spending", "military budget", "arms race", "military-industrial complex"],
    "Welfare programs": ["welfare programs", "social safety net", "poverty alleviation", "government assistance"],
    "Drug policy reform": ["drug policy reform", "decriminalization", "drug legalization", "harm reduction"],
    "Social security reforms": ["social security reforms", "retirement benefits", "pension system", "elderly care"],
    "Privacy invasion": ["privacy invasion", "surveillance capitalism", "data exploitation", "online tracking"],
    "Anti-corruption measures": ["anti-corruption measures", "government accountability", "corruption scandals", "transparency"],
    "Refugee policies": ["refugee policies", "asylum seekers", "immigration crisis", "border crossings"],
    "Hate speech legislation": ["hate speech legislation", "hate crime laws", "freedom of expression", "hate speech regulation"],
    "Climate action plans": ["climate action plans", "green initiatives", "carbon neutrality", "sustainability goals"],
    "Nuclear power policies": ["nuclear power policies", "nuclear energy", "nuclear waste", "nuclear safety"],
    "Space exploration funding": ["space exploration funding", "NASA budget", "space missions", "private space companies"],
    "Military interventions": ["military interventions", "armed conflicts", "peacekeeping missions", "war on terror"],
    "Education reform": ["education reform", "school system", "curriculum changes", "teacher training"],
    "Freedom of the press": ["freedom of the press", "press freedom", "media censorship", "journalism ethics"],
    "Cyber warfare policies": ["cyber warfare policies", "state-sponsored hacking", "cyber attacks", "information warfare"],
    "Government transparency": ["government transparency", "open government", "freedom of information", "public records"],
    "Hate crime legislation": ["hate crime legislation", "hate crime laws", "hate crime prevention", "bias-motivated crimes"],
    "Surveillance state": ["surveillance state", "government surveillance", "mass surveillance", "privacy erosion"],
    "Immigration enforcement": ["immigration enforcement", "border control", "ICE policies", "undocumented immigrants"],
    "Ethical AI regulations": ["ethical AI regulations", "algorithmic bias", "AI accountability", "AI governance"],
    "Labor rights": ["labor rights", "workers' rights", "labor unions", "collective bargaining"],
    "Political lobbying": ["political lobbying", "lobbying regulations", "corporate influence", "campaign contributions"],
    "National debt management": ["national debt management", "government debt", "budget deficit", "fiscal responsibility"],
    "Environmental conservation": ["environmental conservation", "climate conservation", "ecosystem protection", "biodiversity preservation"],
    "Right to protest": ["right to protest", "freedom of assembly", "civil disobedience", "demonstration rights"],
    "Wealth tax proposals": ["wealth tax proposals", "wealth tax rates", "billionaire tax", "income inequality"],
    "Diplomatic relations": ["diplomatic relations", "international diplomacy", "diplomatic negotiations", "peace talks"],
    "Technology monopolies": ["technology monopolies", "big tech companies", "antitrust laws", "market competition"],
    "Police accountability": ["police accountability", "police misconduct", "use of force", "body cameras"],
    "Internet censorship": ["internet censorship", "online freedom", "censorship laws", "content blocking"],
    "Criminal justice funding": ["criminal justice funding", "prison budget", "justice system reform", "law enforcement"],
    "Universal healthcare": ["universal healthcare", "healthcare for all", "single-payer system", "healthcare access"],
    "Public transportation funding": ["public transportation funding", "mass transit", "public transit infrastructure", "urban mobility"],
    "Foreign aid allocation": ["foreign aid allocation", "aid distribution", "aid effectiveness", "donor coordination"],
    "Income tax reforms": ["income tax reforms", "tax brackets", "progressive taxation", "tax deductions"],
    "Digital divide": ["digital divide", "internet access", "broadband availability", "technological inequality"],
    "Social welfare programs": ["social welfare programs", "safety net programs", "poverty alleviation", "government assistance"],
    "Climate change adaptation": ["climate change adaptation", "resilience strategies", "climate resilience", "disaster preparedness"],
    "Electoral college reform": ["electoral college reform", "presidential elections", "electoral system", "popular vote"],
    "Nuclear weapons proliferation": ["nuclear weapons proliferation", "nuclear disarmament", "nonproliferation treaty", "arms control"],
    "Gender pay gap": ["gender pay gap", "equal pay", "pay equity", "gender wage disparity"],
    "Internet privacy laws": ["internet privacy laws", "data privacy regulations", "online tracking", "cookie consent"],
    "Renewable energy subsidies": ["renewable energy subsidies", "clean energy incentives", "solar panel grants", "wind power subsidies"],
    "Government surveillance oversight": ["government surveillance oversight", "surveillance regulation", "intelligence agencies", "privacy safeguards"],
    "Immigration quotas": ["immigration quotas", "immigration caps", "entry restrictions", "immigration policy"],
    "Affordable childcare": ["affordable childcare", "childcare subsidies", "early childhood education", "parental leave"],
    "Gerrymandering": ["gerrymandering", "district boundary manipulation", "redistricting", "voter representation"],
    "Cybersecurity threats": ["cybersecurity threats", "cyber attacks", "data breaches", "malware"],
    "Social justice movements": ["social justice movements", "civil rights", "activism", "equality"],
    "Online disinformation": ["online disinformation", "fake news", "misinformation", "information manipulation"],
    "Defense contractor oversight": ["defense contractor oversight", "military-industrial complex", "defense industry", "government contracts"],
    "Reproductive healthcare access": ["reproductive healthcare access", "women's healthcare", "family planning services", "abortion clinics"],
    "Police militarization": ["police militarization", "militarized police forces", "surplus military equipment", "SWAT teams"],
    "Economic sanctions": ["economic sanctions", "trade embargoes", "financial restrictions", "international diplomacy"],
    "Anti-trust laws": ["anti-trust laws", "monopoly regulation", "market competition", "business monopolies"],
    "Workplace discrimination": ["workplace discrimination", "equal employment opportunity", "gender discrimination", "racial bias"],
    "Government corruption": ["government corruption", "political graft", "bribery", "corruption scandals"],
    "Data protection regulations": ["data protection regulations", "privacy laws", "data security", "GDPR compliance"],
    "Political polarization": ["political polarization", "partisan divide", "political extremism", "polarized politics"]
}