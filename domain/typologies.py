ARCH_DOMAINS = {
    "Residential": ["Luxury Villa", "Modern Apartment", "Townhouse"],
    "Commercial": ["Boutique Office", "Corporate Hub", "Hotel Resort", "Medical Clinic"],
    "Industrial": ["Distribution Warehouse", "Advanced Manufacturing Plant"]
}


def get_domain(btype: str) -> str:
    for domain, types in ARCH_DOMAINS.items():
        if btype in types:
            return domain
    return "Unknown"