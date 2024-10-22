import os
import sys
from types import SimpleNamespace
from typing import Any

import httpx
from dotenv import load_dotenv
from loguru import logger

from mailtrap_cloudflare_dns.cli import cli
from mailtrap_cloudflare_dns.cloudflare_api import (
    CloudflareConnectionInfo,
    batch_dns_records,
    create_cf_record,
    fetch_zone_id_by,
    list_dns_records,
    mailtrap_to_cf_record,
)
from mailtrap_cloudflare_dns.common.types import (
    CloudflareResponse,
    OperationMethod,
    Record,
    resolve_dns_action_enum,
)
from mailtrap_cloudflare_dns.mailtrap_api import (
    generate_auth_headers,
    get_mailtrap_domain_id,
    get_sending_domains,
    parse_sending_domains_dns_records,
)
from mailtrap_cloudflare_dns.operations import add_ids_to_records

# load .env file to environment
load_dotenv()
logger.remove()
logger.add(sys.stderr, format="<level>{message}</level>", level="INFO", colorize=True)


def load_env(app_args: SimpleNamespace) -> SimpleNamespace:
    """Load environment variables from the .env file"""

    env_variables = {"domain_name", "cloudflare_api_token", "mailtrap_api_token"}

    env_values = {
        f"{key.lower()}": value for key in env_variables if (value := os.getenv(key.upper(), None))
    }
    diff = env_variables - env_values.keys()
    if diff:
        logger.error(
            f"Missing environment variables. Add the following missing environment \
                variables to the .env file: {diff}."
        )
        sys.exit(1)

    return build_app_arguments(
        domain_name=app_args.domain_name or env_values["domain_name"],
        cloudflare_api_token=app_args.cloudflare_api_token or env_values["cloudflare_api_token"],
        mailtrap_api_token=app_args.mailtrap_api_token or env_values["mailtrap_api_token"],
    )


def build_app_arguments(
    *, domain_name: str, cloudflare_api_token: str, mailtrap_api_token: str
) -> SimpleNamespace:
    """Build application arguments"""
    return SimpleNamespace(
        domain_name=domain_name,
        cloudflare_api_token=cloudflare_api_token,
        mailtrap_api_token=mailtrap_api_token,
    )


def mailtrap_records_to_cloudflare(
    cf_auth_headers: httpx.Headers, cf_zone_id: str, cf_records: list[Record]
) -> list[dict[Any, Any]]:
    """Create Cloudflare DNS records from Mailtrap email sending domains"""
    responses = [create_cf_record(cf_auth_headers, cf_zone_id, record) for record in cf_records]
    return responses


def batch_records_to_cloudflare(
    operation: OperationMethod,
    cf_auth_headers: httpx.Headers,
    cf_zone_id: str,
    cf_records: list[Record],
) -> CloudflareResponse:
    """Batch DNS records to Cloudflare"""
    payload = {operation.value: cf_records}
    return batch_dns_records(cf_auth_headers, cf_zone_id, payload)


def parse_cf_response(
    response: CloudflareResponse, dns_action: OperationMethod, verbose: bool = False
) -> None:
    """Parse Cloudflare response"""
    if response["success"]:
        logger.success(f"DNS records operation [{dns_action.name.lower()}] completed successfully.")
    else:
        logger.error(f"DNS records operation failed. Errors: {response["errors"]}")
    if verbose:
        logger.debug(response)


def main() -> None:
    args = cli()

    dns_action = resolve_dns_action_enum(args.action)
    verbose_mode = args.verbose
    cf_dns_comment = args.comment

    app_args = build_app_arguments(
        domain_name=args.domain_name,
        cloudflare_api_token=args.cloudflare_api_token,
        mailtrap_api_token=args.mailtrap_api_token,
    )

    if args.load_env:
        app_args = load_env(app_args)

    if not all({app_args.domain_name, app_args.cloudflare_api_token, app_args.mailtrap_api_token}):
        logger.error("Please provide all the required arguments")
        return

    # Get Mailtrap account ID
    mt_auth_headers = generate_auth_headers(app_args.mailtrap_api_token)
    mt_account_id = get_mailtrap_domain_id(mt_auth_headers)

    # Get Cloudflare zone ID
    cf_conn_info = CloudflareConnectionInfo(app_args.cloudflare_api_token, app_args.domain_name)
    cf_zone_id = fetch_zone_id_by(cf_conn_info.domain, cf_conn_info.auth_headers)

    # Get Mailtrap sending domains DNS records
    mt_sending_domains = get_sending_domains(mt_auth_headers, mt_account_id)
    mt_records = parse_sending_domains_dns_records(mt_sending_domains)

    if not mt_records:
        logger.error("No DNS records found in Mailtrap")
        return

    cf_records = [
        mailtrap_to_cf_record(mt_records, comment=cf_dns_comment)
        for mt_records in mt_records[app_args.domain_name]
    ]

    if dns_action in {OperationMethod.OVERWRITE, OperationMethod.DELETE}:
        current_cf_dns_records = list_dns_records(cf_conn_info.auth_headers, cf_zone_id)
        cf_records = add_ids_to_records(
            cf_records, current_cf_dns_records["result"], app_args.domain_name
        )

    if verbose_mode:
        logger.info(f"Mailtrap records: {mt_records}")
        logger.info(f"Cloudflare records: {cf_records}")

    cf_response = batch_records_to_cloudflare(
        dns_action, cf_conn_info.auth_headers, cf_zone_id, cf_records
    )

    parse_cf_response(cf_response, dns_action)


if __name__ == "__main__":
    main()
