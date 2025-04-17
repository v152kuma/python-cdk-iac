def compose_id(base: str) -> str:
    return f"MyCompany-{base}"  # Adjust the prefix as needed

config = {
    "IS_PROD": False,
    "IS_STAGING": True,
    "EVO_PORTAL_UI_BASE_URL": "staging.example.com",
    "ZONE": "example.com",
    "DNS_NAME": "staging"
}
