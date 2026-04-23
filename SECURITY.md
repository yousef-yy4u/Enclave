# Security Policy

## Reporting a Vulnerability

**Do not open a public issue for security vulnerabilities.**

If you discover a security vulnerability in Enclave, please report it responsibly using one of the following methods:

1. **GitHub Private Security Advisory** (preferred):
   [https://github.com/yousef-yy4u/enclave/security/advisories/new](https://github.com/yousef-yy4u/enclave/security/advisories/new)

2. **Direct contact**: Reach out via the maintainer's [GitHub profile](https://github.com/yousef-yy4u).

## What to Include

- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

## Scope

The following are in scope for security reports:

- Authentication bypass or privilege escalation
- Data leakage across module boundaries (RBAC bypass)
- SQL injection or other injection vulnerabilities
- Path traversal in file serving or document storage
- Secrets exposure in logs, error messages, or API responses
- Cross-site scripting (XSS) or cross-site request forgery (CSRF)

## Response Timeline

We will acknowledge your report within **one week** and aim to provide a fix or mitigation plan as soon as possible after that.

## Disclosure

We follow coordinated disclosure. We ask that you do not publicly disclose the vulnerability until we have had a reasonable opportunity to address it.

## Supported Versions

| Version | Supported |
|---|---|
| Latest on `main` | ✅ |
| Older releases | ❌ |
