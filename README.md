# SmuggleMyPayload
![Preview](Source/tool.png)
HTML smuggling tool for red team initial access operations. Generates pixel-perfect lure pages that embed a payload inside the HTML and deliver it client-side via JavaScript  no server-side hosting of the binary required.

Developed by **Maverick**

---

## How It Works

1. Your payload (any binary) is base64-encoded and embedded directly in the HTML file.
2. The base64 string is XOR-encrypted with a random single-byte key and split into shuffled chunks.
3. Junk code, decoy DOM elements, and randomized variable names are injected to defeat static analysis.
4. When the target opens the HTML file (via email, link, or QR code), JavaScript reassembles and decodes the payload in-browser, then triggers a download  the binary never touches the network as a file transfer.

This bypasses email gateways, web proxies, and network-level file inspection that look for known file signatures in transit.

---

## Features

| # | Feature | Description |
|---|---------|-------------|
| 1 | **11 Lure Templates + Custom** | Microsoft 365, DocuSign, SharePoint, OneDrive, Azure Portal, LinkedIn, Google Drive, Dropbox, WeTransfer, Zoom, Slack  each with accurate branding, fonts, logos, and layout. Plus a fully customizable template. |
| 2 | **Template-Specific Metadata** | Per-template fields populated from CLI  LinkedIn sender name/title/initials, Google Drive/Dropbox sharer name/email, Zoom meeting topic/duration, Slack channel name, etc. |
| 3 | **Multi-File Display** | Fake file list UI showing additional files alongside the primary payload. Template-aware rendering (Google Drive table rows, Dropbox file rows, Slack attachments, WeTransfer pills). |
| 4 | **Email-Safe HTML Wrapper** | Table-based HTML layout with no JavaScript and no external CSS. Compatible with Outlook, Gmail, and other email clients. Links to your hosted lure page. |
| 5 | **Dark Mode** | Per-template dark palettes. `auto` mode uses `@media (prefers-color-scheme: dark)`. `force` mode injects dark CSS directly. |
| 6 | **Expiry Countdown Timer** | Live countdown displayed on the lure page. Creates urgency. Configurable duration (default 7 days). |
| 7 | **File Size Spoofing** | Display any file size in the lure UI regardless of actual payload size. |
| 8 | **Preview Mode** | Render any template with a dummy payload for inspection without needing a real binary. |
| 9 | **QR Code Delivery** | Generate a QR code (PNG or SVG fallback) pointing to your hosted lure URL. For physical delivery or messaging apps. |
| 10 | **Payload Encryption at Rest (Fragment Key)** | Payload XOR key derived from the URL fragment (`#secret`). The key is never stored in the HTML. Without the correct fragment, `atob` fails and the page shows "Link Expired". |
| 11 | **Environment Keying** | JavaScript checks target's timezone, browser language, and/or screen dimensions before payload delivery. Mismatch shows "Page Not Available"  sandbox and analyst machines get nothing. |

### Obfuscation Layers

- **XOR encoding** of the base64 payload with a random single-byte key
- **Chunk shuffling** with forward permutation  chunks stored out of order, reassembled via index map
- **Adaptive chunk sizing**  scales 8K / 32K / 64K / 128K based on payload length
- **Comma-boundary splitting**  chunks split at CSV comma boundaries, never mid-number
- **Randomized variable names**  every JS variable is a unique random string per build
- **Junk code injection**  random whitespace and JavaScript comments between statements
- **Decoy DOM elements**  hidden divs with plausible CSS class names injected into the page

---

## Installation

```
pip install qrcode[pil]    # optional, for PNG QR codes (SVG fallback works without it)
```

No other dependencies. Python 3.8+.

## Files

```
smuggle_backend.py          # Core engine  templates, obfuscation, build logic, all feature functions
smugglemypayload.py         # Interactive CLI and argparse interface
test_smugglemypayload.py    # 105 tests covering all features
```

---

## Usage

### Interactive Mode

```bash
python3 smugglemypayload.py
```

Menu-driven interface:

```
[1] Set payload path
[2] Set output filename
[3] Select template (1-12)
[4] Delivery method (click / auto-download)
[5] Set redirect URL
[6] Set output path
[7] Custom logo
[8] Advanced options
[9] View current config
[B] Build lure
[P] Preview mode
[E] Email wrapper
[Q] QR code generator
[0] Exit
```

**Advanced options** (`[8]`) submenu:

```
[1] Dark mode (auto / force / off)
[2] Display file size
[3] Extra display files
[4] Countdown timer
[5] Fragment key (payload encryption)
[6] Environment keying (timezone / language / screen)
[0] Back
```

### CLI Mode

Basic build:

```bash
python3 smugglemypayload.py --payload beacon.exe --template 3 --output lure.html
```

With advanced features:

```bash
python3 smugglemypayload.py \
  --payload beacon.exe \
  --template 6 \
  --method 1 \
  --output lure.html \
  --dark auto \
  --display-size "2.4 MB" \
  --display-files "Q3_Report.xlsx:1.2 MB,Budget_2024.pdf:890 KB" \
  --countdown \
  --fragment-key "s3cr3t-k3y" \
  --env-tz "America/New_York" \
  --env-lang "en-US" \
  --env-screen "1920x1080"
```

Preview (no payload needed):

```bash
python3 smugglemypayload.py --preview --template 1 --filename "update.msi"
```

Email wrapper:

```bash
python3 smugglemypayload.py --email-wrapper https://your-server.com/lure.html --template 3
```

QR code:

```bash
python3 smugglemypayload.py --qr https://your-server.com/lure.html
```

---

## Templates

| # | Template | Brand Details |
|---|----------|---------------|
| 1 | Microsoft 365  Security Update | Segoe UI font, MS logo squares (#f25022, #7fba00, #00a4ef, #ffb900), accent #0078d4 |
| 2 | DocuSign  Document Ready | Helvetica font, Primary Cobalt #4C00FF, Inkwell #130032, Ecru #f8f3f0 |
| 3 | SharePoint  File Shared | Segoe UI, teal header #036367 |
| 4 | OneDrive  Secure Download | Segoe UI, blue accent #0078d4, cloud icon |
| 5 | Azure Portal  Security Alert | Segoe UI, dark sidebar, Azure blue #0078d4 |
| 6 | LinkedIn  Shared Document | System UI stack, LinkedIn blue #0a66c2, bg #f3f2ef |
| 7 | Google Drive  File Shared | Google Sans/Roboto, Google blue #1a73e8, multicolor dots (#4285F4, #EA4335, #FBBC05, #34A853) |
| 8 | Dropbox  File Transfer | System UI stack, Dropbox blue #0061FF, bg #f7f5f2 |
| 9 | WeTransfer  Download Ready | Gradient header #409FFF  #6366f1 |
| 10 | Zoom  Recording Available | System UI stack, Zoom blue #2D8CFF, recording badge |
| 11 | Slack  Shared File | Lato font, aubergine #4A154B, green #007a5a |
| 12 | Custom | Fully configurable  title, heading, body, button text, accent color, footer |

---

## Fragment Key Encryption

When a fragment key is set, the payload can only be decoded if the target opens the lure with the correct URL fragment:

```
https://your-server.com/lure.html#s3cr3t-k3y
```

The key derivation is: `sum of char codes of fragment string, mod 254, plus 1`  produces a value 1–255 used as an additional XOR key on the payload. The HTML file contains no trace of the key. Without the correct fragment, `atob()` fails on the corrupted base64 and the page displays "Link Expired".

## Environment Keying

Restricts payload delivery to targets matching specific environment fingerprints:

- **Timezone**: `Intl.DateTimeFormat().resolvedOptions().timeZone` (e.g., `America/New_York`)
- **Language**: `navigator.language` (e.g., `en-US`)
- **Screen**: `screen.width x screen.height` (e.g., `1920x1080`)

Any mismatch replaces the page body with a generic "Page Not Available" message. Sandboxes, analyst VMs, and automated scanners with default configurations will never see the payload.

---

## Operational Notes

- **Large payloads supported**  adaptive chunking scales up to 128K chunks for payloads over 2MB.
- **No external dependencies in generated HTML**  every lure is a single self-contained file. No CDN loads, no external fonts, no tracking pixels.
- **No comments in source**  the codebase is written clean with descriptive naming, no inline comments to strip.
- **Email wrapper** contains zero JavaScript  safe for email client delivery. It just links to your hosted lure page with template-matching branding.
- **QR codes** fall back to inline SVG generation if the `qrcode` Python library isn't installed.

---

## Running Tests

```bash
python3 -m pytest test_smugglemypayload.py -v
```

105 tests covering: obfuscation engine, XOR encoding, chunk shuffling, adaptive sizing, all 12 templates (both delivery methods), payload integrity roundtrip, fragment key encryption, dark mode, countdown timers, environment keying, file size spoofing, multi-file display, preview mode, email wrapper, QR code generation, and module imports.

---

## Legal

This tool is intended for authorized red team operations and security testing only. Unauthorized use against systems you do not own or have explicit permission to test is illegal. You are responsible for ensuring compliance with applicable laws and engagement rules.
