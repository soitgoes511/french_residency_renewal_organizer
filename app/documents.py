"""
Document definitions for French residence permit applications.
Source: service-public.gouv.fr (official French government portal)
"""

PERMIT_TYPES = {
    "carte_resident": {
        "id": "carte_resident",
        "name_fr": "Carte de Résident de Longue Durée-UE",
        "name_en": "EU Long-Term Resident Card (10 years)",
        "description": "A 10-year residence card for foreigners who have lived legally in France for at least 5 years.",
        "official_url": "https://www.service-public.fr/particuliers/vosdroits/F17359",
    },
    "titre_sejour": {
        "id": "titre_sejour",
        "name_fr": "Titre de Séjour",
        "name_en": "Residence Permit (Renewal)",
        "description": "Renewal of your current residence permit (typically 1-4 years).",
        "official_url": "https://www.service-public.fr/particuliers/vosdroits/N110",
    },
}

# Document definitions for Carte de Résident de Longue Durée-UE
CARTE_RESIDENT_DOCUMENTS = [
    {
        "id": "cr_passport",
        "name_fr": "Passeport valide",
        "name_en": "Valid Passport",
        "description": "Pages showing civil status, validity dates, entry stamps, and visas.",
        "category": "identity",
        "link": None,
        "link_text": "Already possessed",
    },
    {
        "id": "cr_birth_certificate",
        "name_fr": "Copie intégrale d'acte de naissance",
        "name_en": "Full Birth Certificate Copy",
        "description": "Recent copy with all mentions. For foreign-born, must be apostilled and translated by a sworn translator.",
        "category": "identity",
        "link": "https://www.diplomatie.gouv.fr/fr/services-aux-francais/l-annuaire-des-traducteurs-interpretes-assermenters/",
        "link_text": "Find a sworn translator",
    },
    {
        "id": "cr_proof_of_address",
        "name_fr": "Justificatif de domicile (moins de 6 mois)",
        "name_en": "Proof of Address (less than 6 months)",
        "description": "Utility bill (electricity, gas, water, internet), rent receipt, or property tax notice.",
        "category": "residence",
        "link": "https://www.service-public.fr/particuliers/vosdroits/F33052",
        "link_text": "Official requirements",
    },
    {
        "id": "cr_photos",
        "name_fr": "3 photos d'identité / e-photo",
        "name_en": "3 ID Photos / e-photo",
        "description": "Recent passport-style photos or digital e-photo code from an approved service.",
        "category": "identity",
        "link": "https://www.service-public.fr/particuliers/vosdroits/F10619",
        "link_text": "Photo requirements",
    },
    {
        "id": "cr_residence_proof_5years",
        "name_fr": "Justificatifs de séjour régulier (5 ans)",
        "name_en": "Proof of Legal Residence (5 years)",
        "description": "Previous residence permits, renewal receipts, school certificates, tax notices proving continuous legal residence.",
        "category": "residence",
        "link": None,
        "link_text": "Gather from your records",
    },
    {
        "id": "cr_resources_5years",
        "name_fr": "Justificatifs de ressources (5 dernières années)",
        "name_en": "Proof of Resources (last 5 years)",
        "description": "Pay slips, tax notices (avis d'imposition), pension statements, employment contracts. Social benefits are excluded.",
        "category": "financial",
        "link": "https://www.impots.gouv.fr/",
        "link_text": "Tax portal (avis d'imposition)",
    },
    {
        "id": "cr_health_insurance",
        "name_fr": "Justificatif d'assurance maladie",
        "name_en": "Health Insurance Certificate",
        "description": "Carte Vitale or attestation from Ameli showing your affiliation to French social security.",
        "category": "administrative",
        "link": "https://www.ameli.fr/",
        "link_text": "Ameli - Download attestation",
    },
    {
        "id": "cr_french_b1",
        "name_fr": "Attestation niveau B1 français",
        "name_en": "French B1 Level Certificate",
        "description": "Diploma, test result, or linguistic attestation proving French proficiency at B1 level or higher. Exempt if over 65.",
        "category": "integration",
        "link": "https://www.service-public.fr/particuliers/vosdroits/F34501",
        "link_text": "Language requirements",
    },
    {
        "id": "cr_civic_exam",
        "name_fr": "Attestation de réussite examen civique",
        "name_en": "Civic Exam Success Certificate",
        "description": "Certificate proving you passed the civic examination about French values and institutions.",
        "category": "integration",
        "link": "https://www.service-public.fr/particuliers/vosdroits/F39530",
        "link_text": "Civic exam information",
    },
    {
        "id": "cr_republican_commitment",
        "name_fr": "Engagement à respecter les principes de la République",
        "name_en": "Republican Principles Commitment",
        "description": "Signed document committing to respect the principles of the French Republic.",
        "category": "integration",
        "link": "https://www.service-public.fr/particuliers/vosdroits/F38329",
        "link_text": "Download form",
    },
    {
        "id": "cr_non_polygamy",
        "name_fr": "Déclaration sur l'honneur de non polygamie",
        "name_en": "Declaration of Non-Polygamy",
        "description": "Required if married and from a country where polygamy is legal. Sworn statement that you are not in a polygamous marriage.",
        "category": "administrative",
        "link": None,
        "link_text": "Signed personal statement",
    },
    {
        "id": "cr_timbre_fiscal",
        "name_fr": "Timbre fiscal (225€)",
        "name_en": "Tax Stamp (€225)",
        "description": "€200 tax + €25 stamp duty. Can be purchased online. Required at card pickup.",
        "category": "payment",
        "link": "https://timbres.impots.gouv.fr/",
        "link_text": "Purchase online",
    },
]

# Document definitions for Titre de Séjour Renewal
TITRE_SEJOUR_DOCUMENTS = [
    {
        "id": "ts_passport",
        "name_fr": "Passeport valide",
        "name_en": "Valid Passport",
        "description": "Pages showing civil status, validity dates, entry stamps, and visas.",
        "category": "identity",
        "link": None,
        "link_text": "Already possessed",
    },
    {
        "id": "ts_current_permit",
        "name_fr": "Titre de séjour actuel",
        "name_en": "Current Residence Permit",
        "description": "Your current titre de séjour that you are renewing.",
        "category": "identity",
        "link": None,
        "link_text": "Already possessed",
    },
    {
        "id": "ts_proof_of_address",
        "name_fr": "Justificatif de domicile (moins de 3 mois)",
        "name_en": "Proof of Address (less than 3 months)",
        "description": "Utility bill (electricity, gas, water, internet), rent receipt, or property tax notice.",
        "category": "residence",
        "link": "https://www.service-public.fr/particuliers/vosdroits/F33052",
        "link_text": "Official requirements",
    },
    {
        "id": "ts_photos",
        "name_fr": "3 photos d'identité / e-photo",
        "name_en": "3 ID Photos / e-photo",
        "description": "Recent passport-style photos or digital e-photo code from an approved service.",
        "category": "identity",
        "link": "https://www.service-public.fr/particuliers/vosdroits/F10619",
        "link_text": "Photo requirements",
    },
    {
        "id": "ts_resources",
        "name_fr": "Justificatifs de ressources",
        "name_en": "Proof of Resources",
        "description": "Last 3 pay slips, employer attestation letter, or employment contract.",
        "category": "financial",
        "link": None,
        "link_text": "Request from employer",
    },
    {
        "id": "ts_tax_notice",
        "name_fr": "Avis d'imposition",
        "name_en": "Tax Notice",
        "description": "Your most recent French tax notice (avis d'imposition).",
        "category": "financial",
        "link": "https://www.impots.gouv.fr/",
        "link_text": "Tax portal",
    },
    {
        "id": "ts_health_insurance",
        "name_fr": "Attestation d'affiliation Sécurité Sociale",
        "name_en": "Social Security Certificate",
        "description": "Attestation from Ameli showing your affiliation to French social security.",
        "category": "administrative",
        "link": "https://www.ameli.fr/",
        "link_text": "Ameli - Download attestation",
    },
    {
        "id": "ts_birth_certificate",
        "name_fr": "Acte de naissance",
        "name_en": "Birth Certificate",
        "description": "Full copy of your birth certificate. For foreign-born, may need apostille and sworn translation.",
        "category": "identity",
        "link": None,
        "link_text": "Already possessed or request from home country",
    },
    {
        "id": "ts_republican_commitment",
        "name_fr": "Engagement à respecter les principes de la République",
        "name_en": "Republican Principles Commitment",
        "description": "Signed document committing to respect the principles of the French Republic (required since July 2024).",
        "category": "integration",
        "link": "https://www.service-public.fr/particuliers/vosdroits/F38329",
        "link_text": "Download form",
    },
    {
        "id": "ts_timbre_fiscal",
        "name_fr": "Timbre fiscal (225€)",
        "name_en": "Tax Stamp (€225)",
        "description": "€200 tax + €25 stamp duty. Can be purchased online. Required at card pickup.",
        "category": "payment",
        "link": "https://timbres.impots.gouv.fr/",
        "link_text": "Purchase online",
    },
]

# Category display names
CATEGORIES = {
    "identity": {
        "name_en": "Identity Documents",
        "name_fr": "Documents d'identité",
        "icon": "🪪",
    },
    "residence": {
        "name_en": "Proof of Residence",
        "name_fr": "Justificatifs de domicile",
        "icon": "🏠",
    },
    "financial": {
        "name_en": "Financial Documents",
        "name_fr": "Documents financiers",
        "icon": "💰",
    },
    "administrative": {
        "name_en": "Administrative Documents",
        "name_fr": "Documents administratifs",
        "icon": "📋",
    },
    "integration": {
        "name_en": "Integration Requirements",
        "name_fr": "Conditions d'intégration",
        "icon": "🇫🇷",
    },
    "payment": {"name_en": "Payment", "name_fr": "Paiement", "icon": "💳"},
}

# Important links
IMPORTANT_LINKS = [
    {
        "name_fr": "ANEF - Portail de demande en ligne",
        "name_en": "ANEF - Online Application Portal",
        "url": "https://administration-etrangers-en-france.interieur.gouv.fr/",
        "description": "Submit your application online through the official French immigration portal.",
    },
    {
        "name_fr": "Service-Public - Informations officielles",
        "name_en": "Service-Public - Official Information",
        "url": "https://www.service-public.fr/particuliers/vosdroits/N110",
        "description": "Official French government information about residence permits.",
    },
    {
        "name_fr": "Achat de timbre fiscal",
        "name_en": "Purchase Tax Stamp",
        "url": "https://timbres.impots.gouv.fr/",
        "description": "Official portal to purchase the required tax stamp online.",
    },
]


def get_documents_for_permit(permit_type: str) -> list:
    """Get the list of required documents for a given permit type."""
    if permit_type == "carte_resident":
        return CARTE_RESIDENT_DOCUMENTS
    elif permit_type == "titre_sejour":
        return TITRE_SEJOUR_DOCUMENTS
    else:
        return []
