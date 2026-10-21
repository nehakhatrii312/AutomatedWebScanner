"""A small, permission-based scanner for common website security headers."""

# Import tools from Python's standard library for web requests and URL checking.
import sys
import urllib.error
import urllib.parse
import urllib.request


# Keep redirects disabled so the scanner sends only one GET request.
class NoRedirectHandler(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


# Ask for permission first, then get and prepare the website address.
def get_website_url():
    permission = input("Do you have permission to scan this site? (yes/no) ")
    if permission.strip().lower() != "yes":
        print("Scan cancelled. Permission is required.")
        return None

    website_url = input("Enter a website URL: ").strip()
    if not website_url:
        print("Invalid URL: please enter a website address.")
        return None

    if "://" not in website_url:
        website_url = "https://" + website_url

    try:
        parsed_url = urllib.parse.urlsplit(website_url)
        if parsed_url.scheme not in ("http", "https") or not parsed_url.hostname:
            raise ValueError
        parsed_url.port
    except ValueError:
        print("Invalid URL: enter a valid address starting with http:// or https://.")
        return None

    return website_url


# Make one normal GET request and return its response headers.
def fetch_headers(website_url):
    request = urllib.request.Request(
        website_url,
        headers={"User-Agent": "AutomatedWebScanner/1.0"},
        method="GET",
    )
    opener = urllib.request.build_opener(NoRedirectHandler())

    try:
        with opener.open(request, timeout=10) as response:
            return response.status, response.headers
    except urllib.error.HTTPError as error:
        # An HTTP error, including a redirect, still contains response headers.
        return error.code, error.headers
    except urllib.error.URLError as error:
        if isinstance(error.reason, TimeoutError):
            print("The request timed out after 10 seconds. Please try again later.")
        else:
            print("Could not reach the website. Check your internet connection and URL.")
        return None, None
    except (TimeoutError, OSError):
        print("Could not connect to the website. Check your internet connection and try again.")
        return None, None


# Check the five requested security headers and the wildcard CORS setting.
def check_headers(response_headers):
    required_headers = [
        "Content-Security-Policy",
        "X-Frame-Options",
        "Strict-Transport-Security",
        "X-Content-Type-Options",
        "Referrer-Policy",
    ]
    results = []

    for header_name in required_headers:
        if response_headers.get(header_name):
            results.append((header_name, "PASS"))
        else:
            results.append((header_name, "FAIL"))

    cors_value = response_headers.get("Access-Control-Allow-Origin", "")
    if cors_value.strip() == "*":
        results.append(("Access-Control-Allow-Origin", "WARN"))
    else:
        results.append(("Access-Control-Allow-Origin", "PASS"))

    return results


# Print a readable report and calculate a score out of six checks.
def print_report(website_url, status_code, results):
    score = sum(1 for _, result in results if result == "PASS")

    print("\nAutomated Web Scanner Report")
    print("----------------------------")
    print("Website: " + website_url)
    print("HTTP status: " + str(status_code))
    print("\nHeader checks:")
    for header_name, result in results:
        print("- " + header_name + ": " + result)
    print("\nScore: " + str(score) + "/6")


# Run the scanner steps in order and stop safely if a step cannot continue.
def main():
    website_url = get_website_url()
    if website_url is None:
        return

    status_code, response_headers = fetch_headers(website_url)
    if response_headers is None:
        return

    results = check_headers(response_headers)
    print_report(website_url, status_code, results)


# Start the program when this file is run directly.
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nScan cancelled.")
        sys.exit(0)