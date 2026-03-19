#!/usr/bin/env python3
import os
import sys
import argparse

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from classify_evidence import scan_directory

# ANSI colors for rich output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_banner():
    banner = r"""%s%s
    ___             ___ __  __                    
   /   | __  ______/ (_) /_/ /   ___  ____  _____ 
  / /| |/ / / / __  / / __/ /   / _ \/ __ \/ ___/ 
 / ___ / /_/ / /_/ / / /_/ /___/  __/ / / (__  )  
/_/  |_\__,_/\__,_/_/\__/_____/\___/_/ /_/____/   
%s
The Impeccable, Agentic Compliance Engine.
""" % (Colors.OKBLUE, Colors.BOLD, Colors.ENDC)
    print(banner)

def main():
    parser = argparse.ArgumentParser(description="AuditLens CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    scan_parser = subparsers.add_parser("scan", help="Scan evidence and generate an audit workspace")
    scan_parser.add_argument("input_dir", help="Directory containing evidence documents")
    scan_parser.add_argument("--framework", default="iso27001", choices=["iso27001", "soc2"], help="Compliance framework")

    args = parser.parse_args()

    if args.command == "scan":
        print_banner()
        print(f"{Colors.OKCYAN}Scanning directory: {args.input_dir} using {args.framework.upper()}...{Colors.ENDC}")
        
        try:
            catalog = scan_directory(args.input_dir, args.framework)
            stats = catalog['statistics']
            
            print(f"\n{Colors.OKGREEN}✓ Scan completed successfully!{Colors.ENDC}")
            print(f"{Colors.BOLD}Results (Compliance Delta):{Colors.ENDC}")
            print(f"  Files scanned:   {stats['total_files_scanned']}")
            print(f"  Mapped coverage: {stats['coverage_pct']}%  ({stats['evidenced_domains']} of {stats['total_control_domains']} domains)")
            
            if stats.get('missing_domains'):
                print(f"\n{Colors.WARNING}⚠️ Critical Gaps Detected:{Colors.ENDC}")
                for gap in stats['missing_domains']:
                    print(f"  - {gap['domain_id']}: {gap['domain_name']}")
            else:
                print(f"\n{Colors.OKGREEN}✓ No critical gaps detected!{Colors.ENDC}")
                
            print(f"\n{Colors.OKCYAN}Use the included 'Interactive Workspace' HTML template to view full results.{Colors.ENDC}")
            
        except Exception as e:
            print(f"\n{Colors.FAIL}✖ Scan failed: {str(e)}{Colors.ENDC}")
            sys.exit(1)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
