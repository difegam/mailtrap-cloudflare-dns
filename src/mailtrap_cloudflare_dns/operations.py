from typing import Any

from mailtrap_cloudflare_dns.common.types import Record


def add_ids_to_records(
    new_records: list[Record],
    current_records: list[dict[str, Any]],
    domain_name: str,
) -> list[Record]:
    """Add the Cloudflare record ID to the new records"""

    def update_cf_record(record: Record, patch_data: dict[str, Any]) -> Record:
        record.update({"id": patch_data["id"]})
        return record

    def is_record_matching(new_record: Record, cu_record: dict, domain_name: str) -> bool:
        new_record_name = new_record["name"]
        record_name = domain_name if new_record_name == "@" else f"{new_record_name}.{domain_name}"
        return (record_name == cu_record["name"]) and (cu_record["type"] == new_record["type"])

    return [
        update_cf_record(new_record, cu_record)
        for new_record in new_records
        for cu_record in current_records
        if is_record_matching(new_record, cu_record, domain_name)
    ]
