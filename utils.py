"""
Utility functions for the DSW Ventures startup screener.
"""

FEMALE_NAMES = {
    "Emma", "Sophie", "Sarah", "Charlotte", "Emily", "Hannah", "Laura",
    "Priya", "Ananya", "Mei", "Fatima", "Aisha", "Zara", "Olivia", "Amelia",
    "Grace", "Chloe", "Shreya", "Nadia", "Elena", "Maria", "Yasmin", "Leila",
    "Anika", "Riya", "Sian", "Niamh", "Aoife", "Bridget", "Megan", "Wei",
    "Rhiannon", "Kavya", "Divya", "Pooja", "Sunita", "Deepa", "Asha",
    "Lakshmi", "Xiao", "Lin", "Yuki", "Hana", "Sakura", "Amara", "Zainab",
    "Iman", "Nour",
}

GOLDEN_TRIANGLE_PREFIXES = [
    "EC", "WC", "W1", "W2", "W6", "W8", "SW", "SE", "E1", "E14", "N1", "NW",
    "OX", "CB", "GU", "RG", "SG13", "SG14",
]

HARD_TECH_SECTORS = {
    "Medical Devices & Diagnostics",
    "Drug Discovery & Therapeutics",
    "Quantum Computing",
    "Photonics & Semiconductors",
    "Genomics & Synthetic Biology",
    "Biotechnology",
    "Materials Science & Engineering",
    "Robotics & Automation",
}

TIER_1_UNIVERSITIES = {
    "University of Oxford",
    "University of Cambridge",
    "Imperial College London",
    "University College London",
    "King's College London",
    "London School of Economics",
    "Queen Mary University of London",
}

TIER_2_UNIVERSITIES = {
    "University of Manchester",
    "University of Edinburgh",
    "University of Bristol",
    "University of Leeds",
    "University of Glasgow",
    "University of Birmingham",
    "University of Warwick",
    "University of Sheffield",
    "University of Nottingham",
    "University of Southampton",
    "Durham University",
    "University of Liverpool",
    "University of Bath",
    "Heriot-Watt University",
    "University of Exeter",
    "Cardiff University",
    "Newcastle University",
    "University of Leicester",
}

SECTOR_SCORES = {
    10: {
        "Medical Devices & Diagnostics",
        "Drug Discovery & Therapeutics",
        "Machine Learning & AI",
        "Computer Vision",
        "Natural Language Processing",
        "Robotics & Automation",
        "Quantum Computing",
        "Photonics & Semiconductors",
    },
    8: {
        "Genomics & Synthetic Biology",
        "Biotechnology",
        "Renewable Energy & Storage",
        "Carbon Capture & Climate Tech",
        "Materials Science & Engineering",
    },
    5: {
        "Agricultural Technology",
        "SaaS / Enterprise Software",
    },
    2: {
        "Consumer Technology",
        "EdTech",
        "FinTech",
    },
}


def infer_female_founder(founder_names_str: str) -> bool:
    """
    Return True if any founder in the semicolon-separated list has a first
    name that appears in the female names set.
    """
    if not founder_names_str or not isinstance(founder_names_str, str):
        return False
    for name in founder_names_str.split(";"):
        first_name = name.strip().split()[0] if name.strip() else ""
        if first_name in FEMALE_NAMES:
            return True
    return False


def is_golden_triangle(postcode_district: str) -> bool:
    """
    Return True if postcode_district begins with any Golden Triangle prefix.
    Comparison is case-insensitive; whitespace is stripped.
    """
    if not postcode_district or not isinstance(postcode_district, str):
        return False
    code = postcode_district.strip().upper()
    # Longer prefixes must be checked first to avoid false matches (SG13 vs SG)
    for prefix in sorted(GOLDEN_TRIANGLE_PREFIXES, key=len, reverse=True):
        if code.startswith(prefix):
            return True
    return False


def map_sector_score(sector: str) -> int:
    """Return the DSW sector fit score (2, 5, 8, or 10) for a given sector."""
    for score, sectors in SECTOR_SCORES.items():
        if sector in sectors:
            return score
    return 2  # default: unrecognised sectors treated as lowest tier


def map_university_tier(university_affiliation: str) -> str:
    """
    Return 'Tier 1', 'Tier 2', or 'None' based on the university name.
    Empty strings and NaN-like values resolve to 'None'.
    """
    if not university_affiliation or not isinstance(university_affiliation, str):
        return "None"
    name = university_affiliation.strip()
    if not name:
        return "None"
    if name in TIER_1_UNIVERSITIES:
        return "Tier 1"
    if name in TIER_2_UNIVERSITIES:
        return "Tier 2"
    return "None"
