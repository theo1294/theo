#!/usr/bin/env python3
import threading
import requests
import sys
import os
import time
import subprocess
from typing import List, Optional, Dict
import json
from datetime import datetime, timedelta
from rich.console import Console
from rich import print
from rich.panel import Panel
import re
import pytz
from pathlib import Path

console = Console()
os.system('clear' if os.name == 'posix' else 'cls')

# File paths
COOKIE_PATH = '/storage/emulated/0/a/cookie.txt'

config = {
    'post': '',
    'cookies': [],
    'total_shares': 0,
    'target_shares': 0
}

def banner():
    os.system('clear' if os.name == 'posix' else 'cls')

    print(Panel(
        r"""[red]●[yellow] ●[green] ●
[cyan]██████╗░██╗░░░██╗░█████╗░
[cyan]██╔══██╗╚██╗░██╔╝██╔══██╗
[cyan]██████╔╝░╚████╔╝░██║░░██║
[cyan]██╔══██╗░░╚██╔╝░░██║░░██║
[cyan]██║░░██║░░░██║░░░╚█████╔╝
[cyan]╚═╝░░╚═╝░░░╚═╝░░░░╚════╝░""",
        title="[bright_white] SPAMSHARE [green]●[yellow] Active [/]",
        width=65,
        style="bold bright_white",
    ))
    
    print(Panel(
        """[yellow]⚡[cyan] Tool     : [green]SpamShare[/]
[yellow]⚡[cyan] Version  : [green]1.0.0[/]
[yellow]⚡[cyan] Dev      : [green]Ryo Evisu[/]
[yellow]⚡[cyan] Status   : [red]Cookie Mode[/]""",
        title="[white on red] INFORMATION [/]",
        width=65,
        style="bold bright_white",
    ))

def show_main_menu():
    print(Panel("""[1] Start Share Process
[2] Exit""",
        title="[bright_white]>> [Main Menu] <<",
        width=65,
        style="bold bright_white"
    ))
    
    choice = console.input("[bright_white]Enter choice (1-2): ")
    
    if choice == "2":
        return False
    return True

class ShareStats:
    def __init__(self):
        self.success_count = 0
        self.failed_count = 0
        self.lock = threading.Lock()
        self.cookie_stats = {}

    def update_success(self, cookie_index):
        with self.lock:
            self.success_count += 1
            if cookie_index not in self.cookie_stats:
                self.cookie_stats[cookie_index] = {"success": 0, "failed": 0}
            self.cookie_stats[cookie_index]["success"] += 1

    def update_failed(self, cookie_index):
        with self.lock:
            self.failed_count += 1
            if cookie_index not in self.cookie_stats:
                self.cookie_stats[cookie_index] = {"success": 0, "failed": 0}
            self.cookie_stats[cookie_index]["failed"] += 1

def load_cookies():
    try:
        cookie_file = Path(COOKIE_PATH)
        if cookie_file.exists():
            with open(cookie_file, 'r') as f:
                cookies = [line.strip() for line in f if line.strip()]
            console.print(f"[green]Successfully loaded {len(cookies)} cookies from {COOKIE_PATH}")
            return cookies
        else:
            console.print(Panel(
                f"[red]Cookie file not found at {COOKIE_PATH}\n\n[yellow]Creating directory structure...[/]",
                title="[bright_white on red] ERROR [/]",
                width=65,
                style="bold bright_white"
            ))
            os.makedirs(os.path.dirname(COOKIE_PATH), exist_ok=True)
            with open(cookie_file, 'w') as f:
                f.write("")
            console.print(Panel(
                f"[green]Created empty cookie file at {COOKIE_PATH}\n\n[yellow]Please add your cookies and restart the script.[/]",
                title="[bright_white on yellow] ACTION REQUIRED [/]",
                width=65,
                style="bold bright_white"
            ))
            return None
    except Exception as e:
        console.print(Panel(
            f"[red]Error loading cookies: {str(e)}",
            title="[bright_white on red] ERROR [/]",
            width=65,
            style="bold bright_white"
        ))
        return None

def main():
    try:
        banner()
        
        # Load cookies
        cookies = load_cookies()
        if not cookies:
            return
        
        while True:
            if not show_main_menu():
                break
            
            # Starting share process
            print("[yellow]Enter target post link to share: [/yellow]")
            post_link = console.input("[bright_white]Post Link: ")
            print("[yellow]Enter number of shares: [/yellow]")
            try:
                share_count = int(console.input("[bright_white]Number of Shares: "))
            except ValueError:
                print("[red]Please enter a valid number for share count!")
                continue

            stats = ShareStats()
            print("\n[green]Sharing process completed! Returning to menu...\n")
            
    except KeyboardInterrupt:
        console.print("\n[red]Exiting...")
        sys.exit(0)

if __name__ == '__main__':
    main()
