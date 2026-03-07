import argparse
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
import requests
import time
import sys
import os
import json

# Import my modules
from nx_trace.utils.colors import (
    print_banner, print_success, print_error,
    print_info, print_warning, print_header
)
from nx_trace.utils.http import HTTPClient, HTTPResponse
from nx_trace.utils.validators import validate_target

# Constants
BASE_URL = "http://127.0.0.1:8000"
HEADERS = {
    "Content-Type": "application/json",
    "User-Agent": "NX-TRACE-Scanner/2.0.0"
}


class ScanResult:
    """Represents the result of a scan for a single endpoint."""
    
    def __init__(self, endpoint: str):
        self.endpoint = endpoint
        self.status_code: Optional[int] = None
        self.response_time: Optional[float] = None
        self.content_length: Optional[int] = None
        self.auth_required: bool = False
        self.response_data: Optional[Dict] = None
        self.error: Optional[str] = None
        self.method: str = "GET"

    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            "endpoint": self.endpoint,
            "method": self.method,
            "status_code": self.status_code,
            "response_time": self.response_time,
            "content_length": self.content_length,
            "auth_required": self.auth_required,
            "error": self.error
        }
    
class EndpointScanner:
    """Scans individual endpoints"""

    def __init__(self, http_client: HTTPClient):
        self.http_client = http_client
    
    def scan(self, target: str, endpoint: str, method: str = "GET") -> ScanResult:
        """Scan a single endpoint"""
        result = ScanResult(endpoint)
        result.method = method

        url = f"{target}{endpoint}"
        start = time.time()

        try:
            response = self.http_client.request(method, url)

            if response is None:
                result.error = "Request failed (timeout or connection error)"
                return result
            
            result.status_code = response.status_code
            result.response_time = round(time.time() - start, 3)
            result.content_length = len(response.content)

            # Parse JSON if applicable
            if 'application/json' in response.headers.get('Content-Type', ''):
                try:
                    result.response_data = json.loads(response.text)
                except:
                    pass

            # Detects auth requirements
            result.auth_required = self._detect_auth(response)

        except Exception as e:
            result.error = str(e)

        return result
    
    def _detect_auth(self, response: HTTPResponse) -> bool:
        """Detect if endpoint requires authentication"""
        # Check status codes
        if response.status_code in [401, 403]:
            return True
        
        # Check headers
        if 'WWW-Authenticate' in response.headers:
            return True
        
        # Check content
        text = response.text.lower()
        auth_keywords = ["login", "sign in", "authenticate", "authorization", 
                        "access denied", "forbidden", "auth", "unauthorized"]
 
        return any(keyword in text for keyword in auth_keywords)

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="NX-TRACE - REST API Security Scanner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  nx-trace --target http://localhost:8000
  nx-trace --target https://api.example.com --methods GET,POST --timeout 15
  nx-trace --target http://test.com --output report.json --format json
        """
    )
    
    # Target (required)
    parser.add_argument(
        "--target", "-t",
        required=True,
        help="Target URL to scan (e.g., http://localhost:8000)"
    )

    # Output options
    parser.add_argument(
        "--output", "-o",
        help="Output file for results"
    )

    parser.add_argument(
        "--format", "-f",
        choices=["txt", "json"],
        default="txt",
        help="Output format (default: txt)"
    )

    # Scan options
    parser.add_argument(
        "--methods",
        default="GET",
        help="HTTP methods to test (comma-separated, default: GET)"
    )

    parser.add_argument(
        "--timeout",
        type=int,
        default=10,
        help="Request timeout in seconds (default: 10)"
    )

    parser.add_argument(
        "--user-agent",
        help="Custom User-Agent string"
    )

    parser.add_argument(
        "--no-color",
        action="store_true",
        help="Disable colored output"
    )

    # Discovery options
    parser.add_argument(
        "--discovery",
        action="store_true",
        help="Enable automatic endpoint discovery"
    )    

    parser.add_argument(
        "--wordlist",
        help="Custom wordlist file for discovery"
    )

    parser.add_argument(
        "--endpoints-file",
        default="endpoints.txt",
        help="File containing endpoints to scan (default: endpoints.txt)"
    )
    
    # Other options
    parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="Suppress output (only show results)"
    )

    parser.add_argument(
        "--version",
        action="version",
        version="NX-TRACE 2.0.0"
    )

    return parser.parse_args()

def load_endpoints(filepath: str) -> List[str]:
    """Load endpoints from file - checks multiple possible locations"""
    
    # Possible locations for endpoints.txt
    possible_paths = [
        filepath,  # Specified file path
        os.path.join(os.path.dirname(__file__), "../data/endpoints.txt"),  # Package data
        os.path.join(os.getcwd(), "src", "nx_trace", "data", "endpoints.txt"),
        os.path.join(os.getcwd(), "endpoints.txt"),  # Current directory
        os.path.join(os.path.dirname(__file__), "endpoints.txt")  # Same as script
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    endpoints = [
                        line.strip() for line in f 
                        if line.strip() and not line.startswith('#')
                    ]
                    if endpoints:
                        print_info(f"Loaded {len(endpoints)} endpoints from: {path}")
                        return endpoints
            except Exception as e:
                print_warning(f"Error reading {path}: {str(e)}")
                continue
    
    # If we get here, no file was found
    print_error(f"Endpoints file not found: {filepath}")
    print_info("Please create an endpoints.txt file or run with --discovery")
    return []

def test_endpoint(target, endpoint, timeout=10):
    """Test a single endpoint"""
    url = f"{target}{endpoint}"
    start = time.time()

    result = {
        "endpoint": endpoint,
        "status_code": None,
        "response_time": None,
        "content_length": None,
        "auth_required": False,  # Default to False
        "response_data": None,
        "error": None
    }

    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        elapsed = time.time() - start
        
        result["status_code"] = response.status_code
        result["response_time"] = round(elapsed, 3)
        result["content_length"] = len(response.content)

        if 'application/json' in response.headers.get('Content-Type', ''):
            try:
                result["response_data"] = response.json()
            except:
                result["response_data"] = {"error": "Failed to parse JSON"}

        auth_detected = False
        
        # Check status codes
        if response.status_code in [401, 403]:
            auth_detected = True
        
        # Check response headers
        if 'WWW-Authenticate' in response.headers:
            auth_detected = True

        # Check response content for auth keywords
        response_text = response.text.lower()
        auth_keywords = ["login", "sign in", "authenticate", "authorization", "access denied", "forbidden", "auth", "unauthorized"]
        if any(keyword in response_text for keyword in auth_keywords):
            auth_detected = True

        result["auth_required"] = auth_detected


    except requests.exceptions.Timeout:
        result["error"] = f"Timeout after {timeout} seconds"
    except requests.exceptions.ConnectionError:
        result["error"] = "Connection refused - is the server running?"
    except requests.exceptions.RequestException as e:
        result["error"] = f"Request error: {str(e)}"
    except Exception as e:
        result["error"] = f"Unexpected error: {str(e)}"

    return result

def print_result_table(results):
    """Print results in a formatted table"""
    print_header("SCAN RESULTS")
    print("─" * 80)
    print(f"{'Endpoint':<30} {'Method':<8} {'Status':<8} {'Time':<10} {'Size':<12} {'Auth':<8}")
    print("─" * 80)

    for r in results:
        if r.error:
            status = "ERROR"
            time_str = "─"
            size_str = "─"
            auth_str = "─"
            method = r.method
        else:
            # Status code
            if r.status_code == 200:
                status = f"\033[92m{r.status_code}\033[0m"
            elif r.status_code in [401, 403]:
                status = f"\033[91m🔒{r.status_code}\033[0m"
            elif r.status_code == 404:
                status = f"\033[93m{r.status_code}\033[0m"
            elif r.status_code >= 400:
                status = f"\033[93m{r.status_code}\033[0m"
            else:
                status = f"\033[94m{r.status_code}\033[0m"

            # Response time
            time_str = f"{r.response_time:.3f}s"
            
            # Format size
            if r.content_length > 1024*1024:
                size_str = f"{r.content_length/(1024*1024):.1f} MB"
            elif r.content_length > 1024:
                size_str = f"{r.content_length/1024:.1f} KB"
            else:
                size_str = f"{r.content_length} B"

            # Auth
            auth_str = "🔒 YES" if r.auth_required else "🔓 NO"
            method = r.method

        endpoint_display = r.endpoint[:28] + ".." if len(r.endpoint) > 28 else r.endpoint
        print(f"{endpoint_display:<30} {method:<8} {status:<8} {time_str:<10} {size_str:<12} {auth_str:<8}")

    print("─" * 80)

def process_results(results: List[ScanResult], args):
    """Process and display results"""
    
    # Calculate statistics
    successful = [r for r in results if not r.error]
    failed = [r for r in results if r.error]
    
    # Display summary
    print_header("SCAN SUMMARY")
    
    if len(successful) == len(results):
        print_success(f"All {len(successful)} endpoints scanned successfully")
    else:
        print_success(f"Successful: {len(successful)}/{len(results)}")
        if failed:
            print_error(f"Failed: {len(failed)}/{len(results)}")
    
    if successful:
        avg_time = sum(r.response_time for r in successful if r.response_time) / len(successful)
        print_info(f"Average response time: {avg_time:.3f}s")
        
        auth_count = len([r for r in successful if r.auth_required])
        print_info(f"Endpoints requiring auth: {auth_count}/{len(successful)}")
    
    print()
    
    # Display results table
    print_result_table(results)
    
    # Generate report
    if args.output:
        # If user specify a path, uses it
        output_path = args.output
    else:
        # Create output folder if it does not exists
        output_dir = Path.cwd() / "output"
        output_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = output_dir / f"report_{timestamp}.txt"
    
    from nx_trace.core.reporter import Reporter
    reporter = Reporter(results, args.target, args)
    reporter.save(str(output_path))

def discover_endpoints(target, wordlist=None):
    """Discover endpoints by brute-forcing common paths"""
    
    print_header("ENDPOINT DISCOVERY")
    print_info("Starting endpoint discovery...")

    # Default wordlist if none provided
    if not wordlist:
        wordlist = [
            "admin", "dashboard", "manager", "management",
            "api", "v1", "v2", "v3", "rest", "graphql",
            "login", "logout", "register", "auth",
            "users", "user", "accounts", "profile",
            "products", "orders", "payments", "cart",
            "health", "status", "ping", "metrics",
            "docs", "swagger", "openapi", "redoc",
            "backup", "temp", "logs", "config",
            ".env", ".git", "test", "dev",
            "public", "private", "internal",
            "webhook", "callback", "hooks",
            "db", "database", "search", "query",
            "reports", "export", "import", "download"
        ]
    
    discovered = []
    discovered_only = []

    print(f"\n Testing {len(wordlist)} words...")
    print("(This can take a while)\n")

    for i, word in enumerate(wordlist, 1):
        # Create endpoint variations
        variations = [
            f"/{word}",
            f"/api/{word}",
            f"/rest/{word}",
            f"/v1/{word}",
            f"/{word}/v1",
            f"/{word}/api"
        ]

        # Visual progress
        progress = f"[{i}/{len(wordlist)}]"
        print(f"\r{progress} Testing: {word:<20}", end="", flush=True)

        for endpoint in variations:
            url = f"{target}{endpoint}"

            try:
                # Short timeout to not lag
                response = requests.get(url, timeout=2, allow_redirects=False)

                # If it isn't 404, consider found
                if response.status_code != 404:
                    discovered.append({
                        "endpoint": endpoint,
                        "status": response.status_code,
                        "content_type": response.headers.get('Content-Type', 'unknown')
                    })

                    discovered_only.append(endpoint)

                    # Immediately show when found
                    status_color = "\033[92m" if response.status_code == 200 else "\033[93m"
                    print(f"\n  ✅ Found: {endpoint:<30} {status_color}[{response.status_code}]\033[0m")
            
            except requests.exceptions.Timeout:
                # Timeout is expected, just ignore it
                pass
            except requests.exceptions.ConnectionError:
                # If it doesn't connect, everything stops
                print_error(f"\nConnection failed to {target}")
                return [], []
            except:
                # Ignore other errors
                pass

    print("\n")

    # Discovery Statistics
    if discovered:
        print_success(f"Discovered {len(discovered)} new endpoints!")

        # Show summary by status code
        status_count = {}
        for d in discovered:
            status_count[d['status']] = status_count.get(d['status'], 0) + 1
        
        print_info("Summary by status:")
        for status, count in sorted(status_count.items()):
            color = "\033[92m" if status == 200 else "\033[93m" if status < 400 else "\033[91m"
            print(f"  {color}{status}\033[0m: {count} endpoints")
    else:
        print_warning("No new endpoints found :(")

    return discovered, discovered_only

def update_endpoints_file(discovered_endpoints, original_file="endpoints.txt"):
    """Update the endpoint file with the newly discovered endpoints"""
    
    print_header("UPDATING ENDPOINTS FILE") 

    # Load existing endpoints
    existing_endpoints = []
    try:
        with open(original_file, "r") as f:
            existing_endpoints = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        print_info(f"Existing endpoints: {len(existing_endpoints)}")
    except FileNotFoundError:
        print_warning("endpoints.txt not found. Creating new file...")
        existing_endpoints = []

    # Extract only the endpoints from the discovered results
    new_endpoints = discovered_endpoints

    # Combine and remove duplicates (while preserving order)
    all_endpoints = []
    seen = set()

    # Add existing ones
    for ep in existing_endpoints:
        if ep not in seen:
            all_endpoints.append(ep)
            seen.add(ep)
            
    # Add new ones
    new_count = 0
    for ep in new_endpoints:
        if ep not in seen:
            all_endpoints.append(ep)
            seen.add(ep)
            new_count += 1

    # Create a backup for the original file
    if os.path.exists(original_file):
        backup_name = f"endpoints_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        os.rename(original_file, backup_name)
        print_info(f"Backup created: {backup_name}")

    # Write new file
    with open(original_file, "w") as f:
        # Explanatory header
        f.write("# NX-TRACE Endpoints File\n")
        f.write(f"# Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("# " + "="*50 + "\n\n")
        f.write("# ========== ENDPOINTS FOUND ==========\n\n")

        for endpoint in sorted(all_endpoints):  # Sort alphabetically
            f.write(f"{endpoint}\n")

    print_success(f"{original_file} file updated!")
    print_info(f"Total endpoints: {len(all_endpoints)}")
    print_info(f"   |- Existing: {len(existing_endpoints)}")
    print_info(f"   L- New added: {new_count}")

    if new_count > 0:
        print_info("New endpoints added:")
        for ep in new_endpoints:
            if ep not in existing_endpoints:
                print(f"   + {ep}")

    return all_endpoints

def main():
    """Main entry point"""
    args = parse_arguments()

    # Clear screen and print banner
    if not args.quiet:
        if os.name == 'posix':  # Linux/Mac
            os.system('clear')
        elif os.name == 'nt':   # Windows
            os.system('cls')
        print_banner()

    try:
        # Validate target
        target = validate_target(args.target)

        if not args.quiet:
            print_info(f"Target: {target}")
            print_info(f"Methods: {args.methods}")
            print_info(f"Timeout: {args.timeout}s")
            print()

        # Initialize HTTP client
        headers = {}
        if args.user_agent:
            headers["User-Agent"] = args.user_agent

        http_client = HTTPClient(
            timeout=args.timeout,
            headers=headers
        )

        # Handle discovery if requested
        endpoints = []
        
        if args.discovery:
            discovered, discovered_only = discover_endpoints(target, args.wordlist)
            if discovered:
                endpoints = update_endpoints_file(discovered_only, args.endpoints_file)
            else:
                print_warning("No endpoints discovered.")
                # Try to load from file as fallback
                endpoints = load_endpoints(args.endpoints_file)
        else:
            # Load endpoints from file
            endpoints = load_endpoints(args.endpoints_file)

        if not endpoints:
            print_error("No endpoints to scan!")
            sys.exit(1)

        if not args.quiet:
            print_success(f"Loaded {len(endpoints)} endpoints to scan")
            print_header("STARTING SCAN")

        # Initialize scanner
        scanner = EndpointScanner(http_client)
        results = []
        methods = [m.strip() for m in args.methods.split(',')]

        # Scan each endpoint
        total_scans = len(endpoints) * len(methods)
        scan_count = 0

        for i, ep in enumerate(endpoints, 1):
            if not args.quiet:
                # Show progress
                print(f"\rProgress: [{i}/{len(endpoints)}] Scanning {ep[:30]:30}", end="", flush=True)

            # Scan with each method
            for method in methods:
                result = scanner.scan(target, ep, method)
                results.append(result)
                scan_count += 1

        if not args.quiet:
            print("\n")

        # Process results
        process_results(results, args)

    except KeyboardInterrupt:
        print("\n")
        print_warning("Scan interrupted by user")
        sys.exit(130)
    except Exception as e:
        print_error(f"Scan failed: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n\033[91m[✗] Scan interrupted by user\033[0m")
        sys.exit(1)