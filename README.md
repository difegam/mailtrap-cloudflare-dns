# Mailtrap Cloudflare DNS

## Table of Contents

- [Mailtrap Cloudflare DNS](#mailtrap-cloudflare-dns)
  - [Table of Contents](#table-of-contents)
  - [About ](#about-)
  - [Getting Started ](#getting-started-)
    - [Prerequisites](#prerequisites)
    - [Creating a Cloudflare API token](#creating-a-cloudflare-api-token)
    - [Creating a Mailtrap API token](#creating-a-mailtrap-api-token)
    - [Installing](#installing)
      - [Using `uv`](#using-uv)
  - [Usage ](#usage-)
  - [Nice to have](#nice-to-have)

## About <a name = "about"></a>

A simple tool to add, update and delete Mailtrap DNS verification records in Cloudflare DNS.


## Getting Started <a name = "getting_started"></a>

### Prerequisites
- Python 3.12*
- [Cloudflare API token](#creating-a-cloudflare-api-token)
- [Mailtrap API token](#creating-a-mailtrap-api-token)
- [`uv`](https://docs.astral.sh/uv/) Python package and project manager (`optional`)

### Creating a Cloudflare API token
To create a Cloudflare API token follow these steps:

1. Go to https://dash.cloudflare.com/profile/api-tokens
2. Click Create Token
3. Click Create Custom Token at the bottom of the page
- Give your API token a descriptive name `mailtrap-verification-dns`
- Select the following permissions:
  - Zone - Zone - Read
  - Zone - DNS - Edit
- Zone Resources
  - specific zone - select the zone you want to add the DNS record to
4. Click Continue to Summary
5. Click Create Token
6. Copy the generated token
7. Save the token in a secure place. You won't be able to see it again.


### Creating a Mailtrap API token
To create a Mailtrap API token follow these steps:
1. Go to https://mailtrap.io/api-tokens
2. Copy the API token from the domain you want verification for.

### Installing

Clone the repository and install the dependencies.

```bash
git clone git@github.com:difegam/mailtrap-cloudflare-dns.git
cd mailtrap-cloudflare-dns
```

#### Using `uv`
`uv` makes it easy to run the application. [Install `uv`](https://docs.astral.sh/uv/getting-started/installation/) and run the following command. Can it be any simpler?

```bash
uv run app --help
```
The previous command will create a virtual environment, install Python version required for the project (Python 3.12) and the dependencies, and show the help message of the application.

Create a `.env` file in the root of the project with the following variables:

```bash
CLOUDFLARE_API_TOKEN=your-cloudflare-api-token
MAILTRAP_API_TOKEN=your-mailtrap-api-token
DOMAIN_NAME=example.com
```

If you don't want uv you can install the dependencies manually.

> You must have Python 3.12 installed in your system.

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
Activate the virtual environment and run the application.

```bash
source venv/bin/activate
python src/mailtrap_cloudflare_dns/main.py --help
```

## Usage <a name = "usage"></a>

Using the tool is simple.

```bash
uv run app --load-env --action {create, overwrite, delete}
```
use the `--load-env` flag to load the environment variables from the `.env` file. You can also use the `--cloudflare-api-token`, `--mailtrap-api-token`, and `--domain-name` flags to pass the values directly.

By default, the tool add a comment to all dns records to easily identify them on the Cloudflare dashboard. If you want to remove the comment, use the `--comment ""` to pass an empty string.


## Nice to have<a name = "todo"></a>
- [ ] Add tests
- [ ] Create a Docker image
- [ ] Better error handling
- [ ] Add more DNS providers