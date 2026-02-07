"""
YAML configuration loader for residence permit documents.
Loads document definitions from YAML files for easier maintenance.
"""

import os
import yaml
from typing import Dict, List, Any, Optional

CONFIG_DIR = os.environ.get("CONFIG_DIR", "/app/config")


def load_yaml_file(filename: str) -> Dict[str, Any]:
    """Load a YAML file from the config directory."""
    filepath = os.path.join(CONFIG_DIR, filename)
    with open(filepath, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def get_profiles() -> Dict[str, Any]:
    """Load profile definitions."""
    data = load_yaml_file("profiles.yaml")
    return data.get("profiles", {})


def get_categories() -> Dict[str, Any]:
    """Load category definitions."""
    data = load_yaml_file("profiles.yaml")
    return data.get("categories", {})


def get_metadata() -> Dict[str, Any]:
    """Load metadata (last verified date, source URL)."""
    data = load_yaml_file("profiles.yaml")
    return data.get("metadata", {})


def get_permit_type_config(permit_type: str) -> Dict[str, Any]:
    """Load permit type configuration."""
    filename = f"{permit_type}.yaml"
    try:
        data = load_yaml_file(filename)
        return data.get("permit_type", {})
    except FileNotFoundError:
        return {}


def get_documents_for_permit(
    permit_type: str, selected_profiles: Optional[List[str]] = None
) -> List[Dict[str, Any]]:
    """
    Load documents for a permit type, optionally filtered by profiles.

    Args:
        permit_type: Either 'carte_resident' or 'titre_sejour'
        selected_profiles: List of profile IDs to include. If None, returns all.
                          Always includes 'common' profile.

    Returns:
        List of document dictionaries
    """
    filename = f"{permit_type}.yaml"
    try:
        data = load_yaml_file(filename)
        documents = data.get("documents", [])

        if selected_profiles is None:
            return documents

        # Always include 'common' profile
        profiles_to_include = set(selected_profiles)
        profiles_to_include.add("common")

        # Filter documents by profile
        filtered = []
        for doc in documents:
            doc_profiles = set(doc.get("profiles", []))
            if doc_profiles & profiles_to_include:
                filtered.append(doc)

        return filtered

    except FileNotFoundError:
        return []


def get_all_permit_types() -> List[Dict[str, Any]]:
    """Load all permit type definitions."""
    permit_types = []

    for permit_id in ["carte_resident", "titre_sejour"]:
        config = get_permit_type_config(permit_id)
        if config:
            permit_types.append(config)

    return permit_types


def get_important_links() -> List[Dict[str, Any]]:
    """Return important application links."""
    return [
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
