from dataclasses import dataclass
from enum import StrEnum
from typing import Annotated, Any, Literal, Required, TypedDict

RecordName = Annotated[str, "DNS Record Name"]
ZoneID = Annotated[str, "Cloudflare Zone ID"]
RecordID = Annotated[str, "Cloudflare DNS Record ID"]
HTTPMethod = Literal["GET", "POST", "PUT", "DELETE"]


RecordType = Literal[
    "TXT",
    "CNAME",
    "MX",
    "A",
    "AAAA",
    "NS",
    "SRV",
    "LOC",
    "SPF",
    "CERT",
    "DNSKEY",
    "DS",
    "NAPTR",
    "SMIMEA",
    "SSHFP",
    "TLSA",
    "URI",
]


class Record(TypedDict, total=False):
    id: Annotated[str, "Identifier"]
    name: Annotated[Required[str], "DNS record name"]
    type: Annotated[Required[RecordType], "Record type"]
    content: Annotated[Required[str], "Record content"]
    ttl: Annotated[int, "Time to Live"]
    proxied: Annotated[bool, "Proxied"]
    settings: Annotated[dict, "Settings for the DNS record"]
    tags: Annotated[list[str], "Custom tags for the DNS record"]
    comment: Annotated[str, "Comments or notes about the DNS record."]


class CloudflareBatchRecords(TypedDict, total=False):
    delete: list[dict[Literal["id"], RecordID]]
    patches: Annotated[list[Record], "List of DNS records to update"]
    posts: Annotated[list[Record], "List of DNS records to create"]
    put: Annotated[list[Record], "List of DNS records to overwrite"]


class CloudflareResponse(TypedDict):
    errors: list[Any]
    messages: list[Any]
    success: bool
    result_info: dict
    result: list[dict]


@dataclass
class CloudflareRecord:
    type: RecordType
    name: str
    value: str

    def __repr__(self) -> str:
        return f"Cloudflare({self.type=} {self.name=} {self.value=})"


@dataclass
class MailtrapRecord:
    key: str
    domain: str
    type: Annotated[RecordType, "Record type"]
    value: str
    status: str
    name: str

    def __str__(self) -> str:
        return f"name={self.name} value={self.value} type={self.type}"

    def __repr__(self) -> str:
        return f"MailtrapRecord(name={self.name} value={self.value} type={self.type}, domain={self.domain})"


class OperationMethod(StrEnum):
    CREATE = "posts"
    UPDATE = "patches"
    DELETE = "deletes"
    OVERWRITE = "puts"

    def __str__(self) -> str:
        return self.value


def resolve_dns_action_enum(action: str) -> OperationMethod:
    actions = {
        "create": OperationMethod.CREATE,
        "update": OperationMethod.UPDATE,
        "delete": OperationMethod.DELETE,
        "overwrite": OperationMethod.OVERWRITE,
    }
    return actions[action]
