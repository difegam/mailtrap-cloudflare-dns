import httpx

from mailtrap_cloudflare_dns.common.types import CloudflareRecord, MailtrapRecord


def sending_domains_parser(domains: dict) -> dict[str, tuple[CloudflareRecord, ...]]:
    """Parse sending domains DNS records"""
    return {domain["domain_name"]: dns_records_parser(domain["dns_records"]) for domain in domains}


def dns_records_parser(data: dict) -> tuple[CloudflareRecord, ...]:
    """Parse DNS records"""
    return tuple(CloudflareRecord(**record) for record in data)


def generate_auth_headers(api_token: str) -> dict[str, str]:
    """Generate Mailtrap API authentication headers"""
    return {"Accept": "application/json", "Api-Token": api_token}


def get_accounts(headers: dict[str, str]) -> dict:
    """Get Mailtrap accounts information"""
    url = "https://mailtrap.io/api/accounts"
    with httpx.Client(headers=headers) as client:
        response = client.get(url)
        return response.json()


def get_sending_domains(headers: dict[str, str], account_id: str) -> dict:
    """Get sending domains"""
    url = f"https://mailtrap.io/api/accounts/{account_id}/sending_domains"
    with httpx.Client(headers=headers) as client:
        response = client.get(url)
        return response.json()


def parse_sending_domains_dns_records(data: dict) -> dict[str, list[MailtrapRecord]]:
    """Parse sending domains DNS records"""
    return {
        domain["domain_name"]: [MailtrapRecord(**mt_record) for mt_record in domain["dns_records"]]
        for domain in data["data"]
    }


def get_mailtrap_domain_id(headers: dict[str, str]) -> str:
    """Get Mailtrap domain ID"""
    accounts = get_accounts(headers)
    return accounts[0]["id"] if accounts else ""


if __name__ == "__main__":
    ...
