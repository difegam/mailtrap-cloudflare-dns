import re

import httpx

from mailtrap_cloudflare_dns.common.types import (
    CloudflareBatchRecords,
    CloudflareResponse,
    HTTPMethod,
    MailtrapRecord,
    Record,
    RecordName,
    ZoneID,
)

CF_API_BASE_URL = "https://api.cloudflare.com/client/v4"


class CloudflareConnectionInfo:
    """Cloudflare API connection information"""

    def __init__(self, api_token: str, domain: str) -> None:
        self.api_token = api_token
        self._domain = domain

    @property
    def api_token(self) -> str:
        return self._api_token

    @api_token.setter
    def api_token(self, value: str) -> None:
        # Force headers to be re-generated on api_token change
        if hasattr(self, "_auth_headers"):
            del self._auth_headers
        self._api_token = value

    @property
    def domain(self) -> str:
        return self._domain

    @property
    def auth_headers(self) -> httpx.Headers:
        if not hasattr(self, "_headers"):
            self._auth_headers = httpx.Headers({
                "Authorization": f"Bearer {self._api_token}",
                "Content-Type": "application/json",
            })
        return self._auth_headers


def _request_cloudflare(
    method: HTTPMethod,
    url: str,
    headers: httpx.Headers,
    *,
    params: httpx.QueryParams | None = None,
    data: dict | Record | CloudflareBatchRecords | None = None,
) -> CloudflareResponse:
    """Generic function to make requests to the Cloudflare API"""
    with httpx.Client(headers=headers) as client:
        response = client.request(method, url, params=params, json=data)
        return response.json()


def list_zones(headers: httpx.Headers, parameters: httpx.QueryParams) -> CloudflareResponse:
    """List all zones in a Cloudflare account"""
    endpoint = f"{CF_API_BASE_URL}/zones"
    return _request_cloudflare("GET", endpoint, headers, params=parameters)


def list_dns_records(headers: httpx.Headers, zone_id: ZoneID) -> CloudflareResponse:
    """List all DNS records in a Cloudflare zone"""
    endpoint = f"{CF_API_BASE_URL}/zones/{zone_id}/dns_records"
    return _request_cloudflare("GET", endpoint, headers)


def overwrite_cf_dns_records(
    headers: httpx.Headers, zone_id: ZoneID, dns_record_id: str, data: Record
) -> CloudflareResponse:
    """List all DNS records in a Cloudflare zone"""
    endpoint = f"{CF_API_BASE_URL}/zones/{zone_id}/dns_records/{dns_record_id}"
    return _request_cloudflare("PUT", endpoint, headers, data=data)


def create_cf_record(headers: httpx.Headers, zone_id: ZoneID, data: Record) -> CloudflareResponse:
    """Create a DNS record in a Cloudflare zone"""
    endpoint = f"{CF_API_BASE_URL}/zones/{zone_id}/dns_records"
    return _request_cloudflare("POST", endpoint, headers, data=data)


def get_zone_id_by_name(headers: httpx.Headers, name: RecordName) -> dict[RecordName, ZoneID]:
    """Get the zone ID by the zone name"""
    parameters = httpx.QueryParams(name=name, status="active")
    zones = list_zones(headers, parameters)
    return {zone["name"]: zone["id"] for zone in zones.get("result", [{}]) if zone}


def mailtrap_to_cf_record(
    mailtrap_record: MailtrapRecord,
    comment: str = "",
    proxied: bool = False,
    tags: list[str] | None = None,
    settings: dict | None = None,
    ttl: int = 1,
) -> Record:
    """Convert a Mailtrap DNS record to a Cloudflare DNS record

    Args:
        mailtrap_record (dict): mailtrap DNS records
        comment (str, optional): Comments or notes about the DNS record. Defaults "".
        proxied (bool, optional): proxied record. Defaults to False.
        tags (list[str] | None, optional): Custom tags for the DNS record. Defaults to None.
        settings (dict | None, optional): Settings for the DNS record. Defaults to None.
        ttl (int, optional): Time To Live (TTL) of the DNS record in seconds. Value must
        be between 60 and 86400. Defaults to 1 (automatic).

    Returns:
        Record: Cloudflare DNS record format
    """

    def txt_type_format(value: str) -> str:
        """Add double quotes to the TXT record value"""
        return f'"{value}"'

    if mailtrap_record.type == "TXT":
        mailtrap_record.value = txt_type_format(mailtrap_record.value)

    record: Record = {
        "comment": comment or "Mailtrap domain verification record",
        "name": mailtrap_record.name,
        "proxied": proxied,
        "settings": settings or {},
        "tags": tags or [],
        "ttl": ttl,
        "content": mailtrap_record.value,
        "type": mailtrap_record.type,
    }
    return record


def fetch_zone_id_by(domain: str, auth_headers: httpx.Headers) -> ZoneID:
    """Fetch the zone ID by the domain name"""

    # Regular expression to match domain names
    fqdn_pattern = r"^(?:[-\w]+\.)+[a-z]{2,}$"
    if not domain or not re.match(fqdn_pattern, domain):
        raise ValueError(f"Invalid domain name provided. {domain}")
    zone = get_zone_id_by_name(auth_headers, domain)
    return zone.get(domain, "")


def batch_dns_records(
    headers: httpx.Headers, zone_id: ZoneID, data: CloudflareBatchRecords
) -> CloudflareResponse:
    """Batch create DNS records in a Cloudflare zone"""
    endpoint = f"{CF_API_BASE_URL}/zones/{zone_id}/dns_records/batch"
    return _request_cloudflare("POST", endpoint, headers, data=data)


if __name__ == "__main__":
    ...
