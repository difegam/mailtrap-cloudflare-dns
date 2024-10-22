# ADR 0001: why not use Cloudflare python library?


## Status

**Date:** _2024-10-22_

- [x] Proposed
- [ ] Accepted
- [ ] Deprecated
- [ ] Rejected
- [ ] In Testing
- [ ] Superseded by ADR-XXX

## Decision (What/How)

I will user httpx to make the requests to the Cloudflare API instead of using the Cloudflare python library.

## Context (Why)
When I started this project, I was using the Cloudflare Python library to make requests to the Cloudflare API. This simplifies part of the process, but on the other hand, it adds an unnecessary dependency to the project due to the simplicity of the requests I need to make.

## Options Considered
1. Use the Cloudflare Python library to make requests to the Cloudflare API.
This project, apart from automating the Mailtrap DNS verification process, also has the learning intention of getting familiar with the Cloudflare and Mailtrap APIs. Using the library would encapsulate the requests, deviating from one of the objectives of the project.

- pros:
  - Simplifies the requests to the Cloudflare API.
  - It is a well maintained library.
  - Error handling is already implemented.
- cons:
  - Adds a dependency to the project.
  - Deviates from one of the main objectives of the project.

## Consequences
The main consequence of this decision is that I will have to implement the requests to the Cloudflare API and mailtrap API manually. This will add more code to the project, but it will also make me learn more about the APIs.
