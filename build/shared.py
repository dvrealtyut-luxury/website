PHONE = "(801) 678-0444"
PHONE_TEL = "+18016780444"
EMAIL = "dvrealtyut@gmail.com"
KW_SEARCH = "https://daniellevaughns.kw.com"
CALENDLY = "https://calendly.com/dvrealtyut/30min"
# Update when the custom domain is connected (used for social share previews)
SITE_URL = "https://dv-realty.vercel.app"
BROKERAGE = "KW Utah Realtors Keller Williams"
LUXURY = "KW Utah Realtors Luxury"

# Short fingerprint of a file, added to its URL so browsers fetch the new copy
# whenever it changes (instead of reusing an old saved one).
import hashlib as _hashlib, os as _os
_ROOT = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
def asset_version(path):
    with open(_os.path.join(_ROOT, path), "rb") as f:
        return _hashlib.md5(f.read()).hexdigest()[:8]

ARROW = '<svg class="arrow" viewBox="0 0 18 10" aria-hidden="true"><path d="M0 5h16M12 1l4 4-4 4" fill="none" stroke="currentColor"/></svg>'

NAV = [
    ("index.html", "Home"),
    ("about.html", "About"),
    ("relocate.html", "Relocate"),
    ("communities.html", "Communities"),
    ("listings.html", "Listings"),
    ("contact.html", "Contact"),
]

# Layered Wasatch-style ridgeline used at the base of dark bands
RIDGE = """<svg class="{cls}" viewBox="0 0 1440 220" preserveAspectRatio="none" aria-hidden="true">
  <path d="M0 220V150l90-38 70 26 110-74 80 40 60-22 120 70 90-52 70 30 130-96 90 58 70-20 110 66 100-48 80 30 170-70v170z" fill="rgba(255,255,255,0.035)"/>
  <path d="M0 220v-44l120-30 90 20 140-58 110 46 90-18 140 52 120-62 100 34 130-44 120 50 90-22 90 30 100-26v122z" fill="rgba(255,255,255,0.05)"/>
  <path d="M0 150l90-38 70 26 110-74 80 40 60-22 120 70 90-52 70 30 130-96 90 58 70-20 110 66 100-48 80 30 170-70" fill="none" stroke="rgba(226,201,147,0.45)" stroke-width="1" vector-effect="non-scaling-stroke"/>
</svg>"""

MOUNTAIN_ART = [
    "M0 190l60-40 40 18 70-70 50 44 40-20 70 58 60-30 50 40",
    "M0 200l50-30 60 20 80-100 40 40 30-16 60 60 50-24 70 50",
    "M0 180l70-50 30 12 60-48 70 56 40-12 50 30 50-50 70 62",
    "M0 196l40-22 70 10 50-60 60 48 50-80 60 70 40-14 70 48",
    "M0 186l80-36 50 26 60-44 40 20 60-70 50 54 60-16 40 46",
    "M0 194l60-30 40 14 60-30 50-60 50 40 40-10 70 46 70-20",
]


def mountain_art(i):
    d = MOUNTAIN_ART[i % len(MOUNTAIN_ART)]
    return (f'<svg class="community__art" viewBox="0 0 440 220" preserveAspectRatio="none" aria-hidden="true">'
            f'<path d="{d}"/><path d="{d}" transform="translate(0 14)" opacity=".45"/></svg>')


def header(active, light=False):
    links = "\n".join(
        f'        <a href="{href}"{" aria-current=\"page\"" if href == active else ""}>{label}</a>'
        for href, label in NAV[1:]
    )
    mlinks = "\n".join(
        f'    <a class="mm-link" href="{href}"{" aria-current=\"page\"" if href == active else ""}>{label}</a>'
        for href, label in NAV
    )
    return f"""<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header{' header-light' if light else ''}">
  <div class="wrap">
    <a class="brand" href="index.html" aria-label="DV Realty — home">
      <img src="assets/img/logo-dv-realty.png" alt="DV Realty" width="664" height="199">
    </a>
    <nav class="nav" aria-label="Primary">
{links}
        <a class="btn btn--gold" href="contact.html#schedule">Schedule a Call</a>
    </nav>
    <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="mobile-menu" aria-label="Open menu"><span></span><span></span></button>
  </div>
</header>
<div class="mobile-menu" id="mobile-menu" aria-hidden="true">
{mlinks}
  <div class="mm-foot">
    <a class="btn btn--gold" href="contact.html#schedule" style="margin-bottom:24px">Schedule a Call</a>
    <a href="tel:{PHONE_TEL}">{PHONE}</a>
    <a href="mailto:{EMAIL}">{EMAIL}</a>
  </div>
</div>"""


def cta(title="Ready to call <em>Utah</em> home?", lede="Schedule a free, no-pressure consultation and let Danielle guide you through every step of your move."):
    return f"""<section class="cta">
  <div class="wrap wrap--narrow">
    <span class="eyebrow eyebrow--center reveal">Begin the conversation</span>
    <h2 class="display reveal reveal-d1">{title}</h2>
    <p class="lede reveal reveal-d2">{lede}</p>
    <div class="btn-row reveal reveal-d3">
      <a class="btn btn--gold" href="contact.html#schedule">Book Your Free Call {ARROW}</a>
      <a class="btn btn--ghost-light" href="tel:{PHONE_TEL}">{PHONE}</a>
    </div>
    <div class="cta__assure reveal reveal-d4"><span>Free consultation</span><span>No obligation</span><span>Licensed Utah REALTOR®</span></div>
  </div>
  {RIDGE.format(cls="cta__ridge")}
</section>"""


EHO = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2 1 10h3v12h16V10h3L12 2zm5 17H7v-8l5-3.6 5 3.6v8zM9 13h6v1.6H9zm0 2.8h6v1.6H9z"/></svg>'


def footer():
    return f"""<footer class="site-footer">
  <div class="wrap">
    <div class="footer-top">
      <div class="footer-brand">
        <img src="assets/img/logo-dv-realty.png" alt="DV Realty" width="664" height="199" loading="lazy">
        <p>Utah's relocation specialist — helping individuals, families and medical professionals find their home and build their new life in Utah.</p>
      </div>
      <div>
        <h4>Explore</h4>
        <ul>
          <li><a href="about.html">About Danielle</a></li>
          <li><a href="relocate.html">Relocate to Utah</a></li>
          <li><a href="communities.html">Utah Communities</a></li>
          <li><a href="listings.html">Listings</a></li>
          <li><a href="{KW_SEARCH}" target="_blank" rel="noopener">Search All Homes ↗</a></li>
        </ul>
      </div>
      <div>
        <h4>Services</h4>
        <ul>
          <li><a href="relocate.html">Relocation Services</a></li>
          <li><a href="relocate.html#medical">Medical Professionals</a></li>
          <li><a href="listings.html">Buy a Home</a></li>
          <li><a href="contact.html#message">Sell Your Home</a></li>
        </ul>
      </div>
      <div class="footer-contact">
        <h4>Contact</h4>
        <ul>
          <li><a href="tel:{PHONE_TEL}">{PHONE}</a></li>
          <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
          <li>Salt Lake City, Utah</li>
          <li>{BROKERAGE}<br>{LUXURY}</li>
        </ul>
      </div>
    </div>
    <div class="footer-big" aria-hidden="true">Danielle Vaughns</div>
    <div class="footer-bottom">
      <span>© <span data-year>2026</span> DV Realty · Danielle Vaughns, Licensed Utah REALTOR®. Brokered by {BROKERAGE} · {LUXURY}. All rights reserved.</span>
      <span class="eho">{EHO} Equal Housing Opportunity</span>
    </div>
  </div>
</footer>"""


def page(filename, title, description, body, light_header=False):
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<meta name="theme-color" content="#1b1222">
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:image" content="{SITE_URL}/assets/img/og-image.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" type="image/png" sizes="32x32" href="assets/img/favicon-32.png">
<link rel="apple-touch-icon" href="assets/img/favicon-180.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;1,300;1,400&family=Jost:wght@300;400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/style.css?v={asset_version('assets/css/style.css')}">
</head>
<body>
{header(filename, light_header)}
<main id="main">
{body}
</main>
{footer()}
<script src="assets/js/main.js?v={asset_version('assets/js/main.js')}" defer></script>
</body>
</html>
"""
