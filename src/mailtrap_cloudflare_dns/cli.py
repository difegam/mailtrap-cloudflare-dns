import argparse


def cli() -> argparse.Namespace:
    cli = argparse.ArgumentParser(description="Mailtrap to Cloudflare DNS records migration")
    cli.add_argument(
        "-d",
        "--domain-name",
        help="Domain name",
        required=False,
    )
    cli.add_argument(
        "-cf",
        "--cloudflare-api-token",
        help="Cloudflare API token",
        required=False,
    )
    cli.add_argument(
        "-mt",
        "--mailtrap-api-token",
        help="Mailtrap API token",
        required=False,
    )
    cli.add_argument(
        "-c",
        "--comment",
        help="Comment or note for the DNS records.",
        default="mailtrap domain verification record",
    )

    # Options
    cli.add_argument(
        "-a",
        "--action",
        help="Action to Perform, default is [create] records in Cloudflare",
        choices=[
            "create",
            "overwrite",
            "delete",
        ],
        default="create",
    )
    cli.add_argument("--load-env", action="store_true", help="Load environment variables")
    cli.add_argument("-v", "--verbose", action="store_true", help="Verbose mode")
    return cli.parse_args()
