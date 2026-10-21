# Automated Web Scanner

A simple, safe command-line tool written in Python that audits a website's **security headers** and **CORS setting**, then prints an easy-to-read report with a score out of 6.

> **Project for:** IBM SkillsBuild National Cybersecurity Bootcamp (BharatCares, CSRBOX Group, in collaboration with IBM), October 2026
> **Author:** Neha Khatri, BCA 2nd Year (3rd Semester), Vision College of Commerce

---

## Overview

When a browser opens a website, the server sends back the page along with response headers. Some of these headers are security instructions for the browser. If a site leaves them out, attacks such as clickjacking or cross-site scripting become easier.

This scanner sends **one normal GET request**, checks the important headers, and reports each result as **PASS**, **FAIL** or **WARN**.

## Features

- Asks for permission before every scan
- Sends only a single, normal GET request (like a browser opening a page)
- Checks 5 security headers and the CORS header
- Clear PASS / FAIL / WARN report with a final score out of 6
- Automatically adds `https://` if the address has no scheme
- 10-second timeout and friendly error messages, so it never hangs or crashes
- **Zero dependencies**: uses only Python's standard library

## Security Checks

| Check | Purpose | Result |
| --- | --- | --- |
| `Content-Security-Policy` | Limits where a page may load scripts and content from; helps reduce cross-site scripting | PASS if present, FAIL if missing |
| `X-Frame-Options` | Stops the page from being shown inside another site's frame; protects against clickjacking | PASS if present, FAIL if missing |
| `Strict-Transport-Security` | Tells the browser to use HTTPS only for this site | PASS if present, FAIL if missing |
| `X-Content-Type-Options` | Prevents the browser from guessing file types (MIME sniffing) | PASS if present, FAIL if missing |
| `Referrer-Policy` | Controls how much page address information is shared with other sites | PASS if present, FAIL if missing |
| `Access-Control-Allow-Origin` (CORS) | Shows which other websites may read responses from this site | WARN if the value is `*`, otherwise PASS |

**Scoring:** each PASS = 1 point. FAIL and WARN = 0. Maximum score = **6**.

## How It Works

1. The program asks: *"Do you have permission to scan this site? (yes/no)"*. If the answer is not `yes`, it stops.
2. You enter a website address. If it has no `http://` or `https://`, `https://` is added automatically.
3. The address is validated (must start with http/https and contain a valid hostname).
4. One GET request is sent with a 10-second timeout. Redirects are deliberately **not** followed.
5. The response headers are read and each required security header is checked.
6. `Access-Control-Allow-Origin` is checked for the value `*` (any origin).
7. A report is printed with PASS / FAIL / WARN for each check and the final score.

## Requirements

- **Python 3**
- No external packages. Nothing needs to be installed with `pip`.

The project uses only these standard library modules:

- `urllib.request`
- `urllib.parse`
- `urllib.error`
- `sys`

## Usage

```bash
py Neha_AutomatedWebScanner.py
```

Then follow the prompts: confirm permission, then enter the website address.

> On Windows, `py` is the Python launcher. On Linux/macOS, use `python3 Neha_AutomatedWebScanner.py` instead.

## Sample Output

Scan of `https://github.com`:

```
Automated Web Scanner Report
---------------------------
Website: https://github.com
HTTP status: 200

Header checks:
- Content-Security-Policy: PASS
- X-Frame-Options: PASS
- Strict-Transport-Security: PASS
- X-Content-Type-Options: PASS
- Referrer-Policy: PASS
- Access-Control-Allow-Origin: PASS

Score: 6/6
```

## Test Results

| Website | Score | Observation |
| --- | --- | --- |
| https://github.com | 6/6 | All five security headers present and no wildcard CORS; a well-secured site |
| https://example.com | 1/6 | None of the five security headers present; passes only the CORS check |
| https://httpbin.org | 0/6 | No security headers; CORS allows all origins (`*`), so a WARN was shown |

**Notes**

- The WARN for `httpbin.org` is expected: allowing all origins is intentional for a public testing service, but it would be a concern for a site that handles private data.
- When a test site was slow and did not respond, the scanner timed out after 10 seconds and showed a clear message instead of crashing.

## Code Structure

All code is in a single file, `Neha_AutomatedWebScanner.py`:

| Part | What it does |
| --- | --- |
| `NoRedirectHandler` | Blocks redirects so only one request is made |
| `get_website_url()` | Asks for permission, takes the address, adds `https://` if needed and validates it |
| `fetch_headers()` | Sends the single GET request (10-second timeout), returns status code and headers, prints friendly messages on errors |
| `check_headers()` | Checks the five security headers and the CORS header and records PASS, FAIL or WARN |
| `print_report()` | Counts the passes, calculates the score and prints the report |
| `main()` | Runs the steps in order and stops safely if any step cannot continue |

## Safety and Ethical Use

- **Permission prompt:** confirmation is required before every scan.
- **Single request:** only one normal GET request is sent per run.
- **No redirect following:** the scanner never makes a second request.
- **Timeout:** requests give up after 10 seconds.
- **Passive only:** no crawling, brute-forcing, injection or attacks.
- **Responsible use:** scan only websites that you own or that are intended for testing.

## Limitations

- Checks response headers only; it does not find vulnerabilities inside page content.
- Redirects are not followed, so a redirecting site shows the headers of the redirect response (for example status 301).
- Scans one website per run.
- Checks whether a header is present, not whether its value is strong enough.
- The report is printed on screen and not saved to a file.

## Future Scope

- Colored output for easier reading
- Option to save the report to a file
- Scanning a user-provided list of sites
- A carefully limited option to follow redirects
- Checking the strength of header values, not only their presence

## References

- IBM SkillsBuild National Cybersecurity Bootcamp, BharatCares (CSRBOX Group) in collaboration with IBM, October 2026
- [OWASP Secure Headers Project](https://owasp.org/www-project-secure-headers)
- [MDN Web Docs: HTTP headers and CORS](https://developer.mozilla.org)
- [Python documentation: urllib](https://docs.python.org/3/library/urllib.html)

## Author

**Neha Khatri**
BCA, Vision College of Commerce
IBM SkillsBuild National Cybersecurity Bootcamp
