import requests
import time
import sys
import os

BASE_URL = "http://localhost:8000"
HEADERS = {
    "Content-Type": "application/json",
    "User-Agent": "NX-TRACE-Scanner/1.0"
}

def print_banner():
    """Print NX ASCII art banner with eye theme"""
    banner = """
\033[95m
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢘⡆⢇⠀⢀⠀⠀⠀⠀⢰⠀⠀⢀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣤⣠⣴⣛⣯⣿⢿⣿⣿⠤⣼⣦⣤⣄⠀⣸⡄⠀⢸⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡰⠀⣰⡖⢺⡇⢠⣿⣏⢹⣷⣺⣿⣿⢀⣯⣿⣹⠉⣽⣿⣷⢤⣿⣿⣞⣀⣠⠆⠀⠀⠀⣠⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠰⣧⣾⡿⣿⢿⣷⣜⣿⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣞⣿⣿⣷⡟⠷⣤⣀⢀⣼⠃⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢠⠀⢣⣤⣶⠻⣧⣤⣿⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⣹⣿⣁⣼⠟⠑⣤⠞⠀⠀⠀⠀⠀
⠀⠀⠀⠀⢠⠀⢣⣠⡟⣿⣷⣾⣿⣿⣿⠿⢛⣿⣿⣿⠿⠟⠛⠋⠙⠛⠛⠻⢿⣿⣿⣿⣿⣿⣿⣿⣥⣶⣿⣿⣦⢞⡟⣲⠇⢠⠆⢰⠀
⠀⠀⠀⠀⠘⣦⠞⣩⣿⣿⣿⣿⡿⠟⠁⣰⣿⡿⠋⠁⠀⢀⣠⣤⣤⣤⣀⡀⠀⠈⠙⢿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣿⣿⣷⣶⠟⣱⡯⠀
⠀⠀⠀⠈⣰⣻⣿⣿⣿⣿⣿⡿⠁⠀⢰⣿⡟⠀⠀⢀⣴⣿⠿⠛⠛⠻⢿⣿⣶⡀⠀⠀⠹⣿⣯⡿⣿⣿⣿⣿⣿⣯⣟⣿⣿⡶⣋⣴⠋
⠀⢀⡀⣰⣿⣿⣷⠿⠟⢸⣿⡇⠀⠀⣾⣿⡃⠀⠀⢸⣿⣇⣀⣤⣄⠀⠀⠙⢿⣿⡄⠀⠀⢹⣿⡍⣆⠹⢿⣿⣿⣿⣿⢿⣿⡿⠛⠁⠀
⠀⠀⣹⣿⣿⣿⢣⣦⠀⢸⣿⣇⠀⠀⠸⣿⣧⡀⠀⠈⠻⠿⠛⢻⣿⣧⠀⠀⠘⣿⣧⠀⠀⢸⣿⣧⠇⠀⠀⣺⡿⣿⣿⣿⣷⣶⣾⠟⠁
⢀⣴⣿⣿⡞⢡⣇⢧⠀⠀⢿⣿⡄⠀⠀⠙⣿⣷⣤⣀⣀⣀⣤⣾⣿⠃⠀⠀⣸⣿⡇⠀⠀⣸⣿⠏⠀⠀⣰⣿⣷⣮⣿⠙⣯⡯⠀⠀⠀
⠙⠛⢡⡟⢹⡀⢻⡛⣄⠀⠈⢻⣿⣦⡀⠀⠀⠙⠛⠿⠿⠿⠟⠋⠁⠀⢀⣴⣿⡟⠁⠀⣴⡿⠁⠀⢀⣰⣿⣯⣿⢻⡛⣿⡟⠀⠀⠀⠀
⠀⠀⡞⢧⣘⣳⠤⣏⡙⠳⠤⢄⣙⣿⣿⣶⣤⣄⣀⣀⣀⣀⣀⣀⣤⣶⣿⡿⠋⢀⣠⠞⠉⠀⣠⣶⣿⡿⢿⠿⣷⣰⠃⣿⠀⠀⠀⠀⠀
⠀⠀⠘⠲⣤⣤⣶⠃⢉⡷⠶⣤⣤⣉⣉⡛⠛⠿⠿⡿⢿⣿⠿⠿⠛⠋⠁⠀⠒⢋⣤⣤⡶⣾⣿⢿⡗⣍⠈⠇⢹⠇⣸⠇⠀⠀⠀⠀⠀
⠀⠀⠀⠀⢠⣤⣬⣟⡻⢄⠀⡴⠋⢉⢟⡿⢿⣿⡷⢷⣶⡿⢷⣼⣾⣶⡾⢷⢾⣿⠙⣿⡓⣄⢻⣎⠛⠈⠁⣠⠊⣰⠏⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠺⠋⠙⠿⣯⡓⢾⣃⠀⠸⡏⠀⠸⠱⠁⠀⢻⠃⢸⡾⣞⡆⢻⠀⢿⣟⣷⠘⠗⠈⢻⠟⠀⣠⠞⠁⡴⠋⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⠦⠈⠑⠲⢅⣀⠀⠀⠀⠀⠸⠀⠹⡇⠛⠃⠀⠀⠈⠉⢻⠀⠀⠀⠠⠗⠊⠀⠀⠊⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠒⠢⠄⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠉⠒⠒⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
\033[0m
\033[94m╔═══════════════════════════════════════════════════════════════════════════════════════════════════════╗\033[0m
\033[94m║                                                                                                       ║\033[0m
\033[94m║                                   ███╗   ██╗██╗  ██╗                                                  ║\033[0m
\033[94m║                                   ████╗  ██║╚██╗██╔╝                                                  ║\033[0m
\033[94m║                                   ██╔██╗ ██║ ╚███╔╝                                                   ║\033[0m
\033[94m║                                   ██║╚██╗██║ ██╔██╗                                                   ║\033[0m
\033[94m║                                   ██║ ╚████║██╔╝ ██╗                                                  ║\033[0m
\033[94m║                                   ╚═╝  ╚═══╝╚═╝  ╚═╝                                                  ║\033[0m
\033[94m║                                                                                                       ║\033[0m
\033[94m║                                 👁️  N X - T R A C E  👁️                                                 ║\033[0m
\033[94m║                               Network Security Scanner v1.0                                           ║\033[0m
\033[94m║                                                                                                       ║\033[0m
\033[94m╚═══════════════════════════════════════════════════════════════════════════════════════════════════════╝\033[0m
"""
    print(banner)

def print_separator():
    """Print a separator line"""
    print("\033[90m" + "─" * 60 + "\033[0m")

def print_header(text):
    """Print a section header"""
    print(f"\n\033[1m\033[94m[ {text} ]\033[0m")
    print_separator()

def print_success(text):
    """Print success message"""
    print(f"\033[92m[✓]\033[0m {text}")

def print_error(text):
    """Print error message"""
    print(f"\033[91m[✗]\033[0m {text}")

def print_info(text):
    """Print info message"""
    print(f"\033[94m[i]\033[0m {text}")

def print_warning(text):
    """Print warning message"""
    print(f"\033[93m[!]\033[0m {text}")

def load_endpoints():
    """Load endpoints from file"""
    try:
        with open("endpoints.txt", "r") as file:
            endpoints = [line.strip() for line in file if line.strip()]
            return endpoints
    except FileNotFoundError:
        print_error("endpoints.txt not found!")
        sys.exit(1)
    
def test_endpoint(endpoint):
    """Test a single endpoint"""
    url = f"{BASE_URL}{endpoint}"
    start = time.time()

    result = {
        "endpoint": endpoint,
        "status_code": None,
        "response_time": None,
        "content_length": None,
        "auth_required": False,  # Default to False
        "error": None
    }

    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        elapsed = time.time() - start
        
        result["status_code"] = response.status_code
        result["response_time"] = round(elapsed, 3)
        result["content_length"] = len(response.content)

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
        result["error"] = "Timeout after 10 seconds"
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
    print("\033[97m" + "─" * 70 + "\033[0m")
    print("\033[97mEndpoint              Status    Time       Size        Auth     \033[0m")
    print("\033[97m" + "─" * 70 + "\033[0m")

    for r in results:
        if r["error"]:
            status = "\033[91mERROR\033[0m"
            time_str = "─"
            size_str = "─"
            auth_str = "─"
        else:
            # Color code based on status
            if r["status_code"] == 200:
                status = f"\033[92m{r['status_code']}\033[0m"
            elif r["status_code"] in [401, 403]:
                status = f"\033[91m🔒 {r['status_code']}\033[0m"
            elif r["status_code"] == 404:
                status = f"\033[93m{r['status_code']}\033[0m"
            elif r["status_code"] >= 400:
                status = f"\033[93m{r['status_code']}\033[0m"
            else:
                status = f"\033[94m{r['status_code']}\033[0m"

            time_str = f"{r['response_time']:5.3f}s"
            
            # Format size with KB/MB if large
            if r['content_length'] > 1024*1024:
                size_str = f"{r['content_length']/(1024*1024):5.1f} MB"
            elif r['content_length'] > 1024:
                size_str = f"{r['content_length']/1024:5.1f} KB"
            else:
                size_str = f"{r['content_length']:5} B"

            auth_str = "\033[91m🔒 YES\033[0m" if r['auth_required'] else "\033[92m🔓 NO\033[0m"

        endpoint_display = r['endpoint'][:20] + "..." if len(r['endpoint']) > 20 else r['endpoint']
        print(f"{endpoint_display:23} {status:10} {time_str:10} {size_str:11} {auth_str:10}")

    print("\033[97m" + "─" * 70 + "\033[0m")

def main():
    #Clear screen and print banner
    if os.name == 'posix': #Linux/Mac
        os.system('clear')
    elif os.name == 'nt':  #Windows
        os.system('cls')

    print_banner()

    print_info(f"TARGET: {BASE_URL}")

    endpoints = load_endpoints()
    print_success(f"Loaded {len(endpoints)} endpoints from endpoints.txt")
    
    print_header("STARTING SCAN")
    
    results = []
    successful = 0
    failed = 0

    print("\n\033[93m[▶] Scanning endpoints...\033[0m\n")

    for i, ep in enumerate(endpoints, 1):
        # Print scanning animation
        animation = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        print(f"\r\033[94m{animation[i % len(animation)]} Scanning {ep}...\033[0m", end="", flush=True)


        result = test_endpoint(ep)
        results.append(result)

        if result["error"]:
            failed += 1
        else:
            successful += 1

         # Clear line and print result
        print(f"\r{' ' * 60}", end="")
        if result["error"]:
            print_error(f"{ep}: {result['error']}")
        else:
            # Determine icon and color
            if result['status_code'] == 200:
                icon = "✅"
                color = "\033[92m"
            elif result['status_code'] in [401, 403]:
                icon = "🔒"
                color = "\033[91m"
            elif result['status_code'] == 404:
                icon = "❓"
                color = "\033[93m"
            else:
                icon = "⚠️"
                color = "\033[93m"
                
            auth_text = "(Auth)" if result['auth_required'] else ""
            print_success(f"{icon} {ep}: {color}{result['status_code']}\033[0m | {result['response_time']:5.3f}s {auth_text}")
        
    print() # New line after scan

        #Print summary
    print_header("SCAN SUMMARY")

    if successful == len(endpoints):
        print_success(f"All {successful} endpoints scanned successfully")
    else:
        print_success(f"Successful: {successful}/{len(endpoints)}")
        if failed > 0:
            print_error(f"Failed: {failed}/{len(endpoints)}")
    
        # Calculate statistics
    successful_results = [r for r in results if not r.get("error")]
    if successful_results:
        avg_time = sum(r['response_time'] for r in successful_results) / len(successful_results)
        print_info(f"Average response time: {avg_time:.3f}s")
        
        auth_required = len([r for r in successful_results if r['auth_required']])
        print_info(f"Endpoints requiring auth: {auth_required}/{len(successful_results)}")

    #Print result table
    print_result_table(results)

    #Generate report
    print_header("GENERATING REPORT")

    try:
        with open("report.txt", "w") as report:
            report.write("=" * 70 + "\n")
            report.write("                     NX-TRACE SCAN REPORT\n")
            report.write("=" * 70 + "\n\n")
            
            report.write(f"Scan Date: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            report.write(f"Target URL: {BASE_URL}\n")
            report.write(f"Endpoints Scanned: {len(endpoints)}\n")
            report.write(f"Successful: {successful}\n")
            report.write(f"Failed: {failed}\n")

            if successful_results:
                avg_time = sum(r['response_time'] for r in successful_results) / len(successful_results)
                report.write(f"Average Response Time: {avg_time:.3f} seconds\n")
            
            report.write("\n" + "-" * 70 + "\n\n")


        for r in results:
                report.write(f"ENDPOINT: {r['endpoint']}\n")
                if r["error"]:
                    report.write(f"  Status: ERROR\n")
                    report.write(f"  Error: {r['error']}\n")
                else:
                    report.write(f"  Status Code: {r['status_code']}\n")
                    report.write(f"  Response Time: {r['response_time']} seconds\n")
                    report.write(f"  Content Length: {r['content_length']} bytes\n")
                    report.write(f"  Authentication Required: {'YES' if r['auth_required'] else 'NO'}\n")
                report.write("-" * 40 + "\n")

        print_success("Report saved to report.txt")

    except Exception as e:
        print_error(f"Failed to write report: {str(e)}")

    # Print exit banner
    print("\n" + "=" * 70)
    print("\033[1m\033[95m[👁️] SCAN COMPLETE - NX-TRACE Security Scanner [👁️]\033[0m")
    print("=" * 70)
    print("\033[90mReport saved to: report.txt\033[0m")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n\033[91m[✗] Scan interrupted by user\033[0m")
        sys.exit(1)