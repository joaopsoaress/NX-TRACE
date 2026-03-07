"""Report generation module"""

import json
from datetime import datetime
from typing import List
from pathlib import Path

from nx_trace.utils.colors import print_success, print_error


class Reporter:
    """Handles report generation in various formats"""

    def __init__(self, results: List, target: str, args):
        self.results = results
        self.target = target
        self.args = args
        self.timestamp = datetime.now()

    def generate(self) -> str:
        """Generates report in specified format"""
        if self.args.format == "json":
            return self._generate_text()
        else:
            return self._generate_text()
        
    def _generate_text(self) -> str:
        """Generate text report"""
        lines = []
        lines.append("=" * 70)
        lines.append("                    NX-TRACE SCAN REPORT")
        lines.append("=" * 70)
        lines.append("")
        lines.append(f"Scan Date: {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"Target: {self.target}")
        lines.append(f"Endpoints Scanned: {len(self.results)}")
        lines.append("")

        # Summary
        successful = [r for r in self.results if not r.error]
        failed = [r for r in self.results if r.error]

        lines.append("SUMMARY")
        lines.append("-" * 40)
        lines.append(f"Successful: {len(successful)}")
        lines.append(f"Failed: {len(failed)}")

        if successful:
            avg_time = sum(r.response_time for r in successful if r.response_time) / len(successful)
            lines.append(f"Average Response Time: {avg_time:.3f}s")

        lines.append("")

        # Details
        lines.append("DETAILS")
        lines.append("-" * 40)
        
        for result in self.results:
            lines.append(f"Endpoint: {result.endpoint}")
            lines.append(f"  Method: {result.method}")
            
            if result.error:
                lines.append(f"  Status: ERROR")
                lines.append(f"  Error: {result.error}")
            else:
                lines.append(f"  Status Code: {result.status_code}")
                lines.append(f"  Response Time: {result.response_time}s")
                lines.append(f"  Content Length: {result.content_length} bytes")
                lines.append(f"  Auth Required: {'YES' if result.auth_required else 'NO'}")
            
            lines.append("")
        
        return "\n".join(lines)

    def _generate_json(self) -> str:
        """Generate JSON report"""
        report = {
            "scan_info": {
                "timestamp": self.timestamp.isoformat(),
                "target": self.target,
                "version": "2.0.0"
            },
            "summary": {
                "total": len(self.results),
                "successful": len([r for r in self.results if not r.error]),
                "failed": len([r for r in self.results if r.error])
            },
            "results": [r.to_dict() for r in self.results]
        }
        
        return json.dumps(report, indent=2)
    
    def save(self, filepath: str):
        """Save report to file"""
        try:
            # Create directory if it doesn't exist
            Path(filepath).parent.mkdir(parents=True, exist_ok=True)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(self.generate())
            
            print_success(f"Report saved to {filepath}")
            
        except Exception as e:
            print_error(f"Failed to save report: {str(e)}")