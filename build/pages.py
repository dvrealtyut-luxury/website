import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from shared import *
from listings import LISTINGS
from team import TEAM
from reviews import REVIEWS, GOOGLE_REVIEWS_URL
import html as _html

# Output to the repo root by default: python3 build/pages.py
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")


def img(name, alt, sizes="(max-width: 900px) 100vw, 50vw", eager=False, w=1400, h=2100, pos=None):
    style = f' style="object-position:{pos}"' if pos else ""
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    return (f'<img src="assets/img/{name}-1400.webp" srcset="assets/img/{name}-800.webp 800w, assets/img/{name}-1400.webp 1400w" '
            f'sizes="{sizes}" width="{w}" height="{h}" alt="{alt}" {load} decoding="async"{style}>')



COMMUNITIES = [
    ("park", "Park City", "Old Town · Deer Valley · Kimball Junction",
     "Three major ski areas, world-class mountain biking and a storied Main Street, a short drive up Parley's Canyon."),
    ("yalecrest", "Yalecrest", "Historic homes · Tree-lined streets",
     "One of Salt Lake City's most beloved historic neighborhoods, minutes from the University of Utah and downtown."),
    ("millcreek", "Millcreek & Holladay", "Mature trees · Larger lots",
     "Established, gracious neighborhoods on Salt Lake's east side, with Millcreek Canyon close by."),
    ("cottonwoods", "The Cottonwoods & Sandy", "Cottonwood Heights · Sandy",
     "Neighborhoods at the doorstep of Big and Little Cottonwood Canyons and four world-class ski resorts."),
    ("draper", "Draper & South Jordan", "Corner Canyon · Daybreak",
     "Newer homes, top-rated trail systems and an easy commute in either direction along the I-15 corridor."),
    ("utah-county", "Utah County", "Lehi · Silicon Slopes · Provo",
     "The heart of Utah's tech corridor — new construction, two major universities and a growing medical community."),
]

# Featured listings are edited in build/listings.py.
def listing_card(i, l):
    specs = f"<span>{l['beds']} Beds</span><span>{l['baths']} Baths</span><span>{l['sqft']} Sq Ft</span>"
    link = l.get("link") or "contact.html"
    ext = ' target="_blank" rel="noopener"' if link.startswith("http") else ""
    return f"""      <article class="listing reveal reveal-d{i % 2}">
        <a class="listing__media" href="{link}"{ext}>
          <img src="{l['image']}" alt="{l['address']}, {l['city']}" width="1200" height="800" loading="lazy" decoding="async">
          <span class="listing__badge">{l['status']}</span>
        </a>
        <div class="listing__body">
          <div class="listing__price">{l['price']}</div>
          <div class="listing__addr">{l['address']} · {l['city']}</div>
          <p class="listing__desc">{l.get('description', '')}</p>
          <div class="listing__specs">{specs}</div>
          <a class="link-arrow listing__cta" href="{link}"{ext}>View Details {ARROW}</a>
        </div>
      </article>"""


def featured_section(limit=None, head=True, sand=False):
    if not LISTINGS:
        return ""
    items = LISTINGS[:limit] if limit else LISTINGS
    cards = "\n".join(listing_card(i, l) for i, l in enumerate(items))
    more = (f'\n    <div class="center reveal" style="margin-top:64px"><a class="btn btn--ghost" href="listings.html">View All Listings {ARROW}</a></div>'
            if limit and len(LISTINGS) > limit else "")
    return f"""<section class="section{' section--sand' if sand else ''}" id="featured">
  <div class="wrap">
    <div class="section-head section-head--split">
      <div>
        <span class="eyebrow reveal">Featured properties</span>
        <h2 class="h2 reveal reveal-d1">Homes you'll <em>love in Utah.</em></h2>
      </div>
      <p class="lede reveal reveal-d2">A curated selection of Danielle's current listings across Utah's most sought-after communities.</p>
    </div>
    <div class="listings">
{cards}
    </div>{more}
  </div>
</section>"""


# --------------------------------------------------------------------------- GOOGLE REVIEWS
GOOGLE_G = ('<svg class="gr-g" viewBox="0 0 48 48" aria-hidden="true">'
    '<path fill="#FFC107" d="M43.611 20.083H42V20H24v8h11.303c-1.649 4.657-6.08 8-11.303 8-6.627 0-12-5.373-12-12s5.373-12 12-12c3.059 0 5.842 1.154 7.961 3.039l5.657-5.657C34.046 6.053 29.268 4 24 4 12.955 4 4 12.955 4 24s8.955 20 20 20 20-8.955 20-20c0-1.341-.138-2.65-.389-3.917z"/>'
    '<path fill="#FF3D00" d="M6.306 14.691l6.571 4.819C14.655 15.108 18.961 12 24 12c3.059 0 5.842 1.154 7.961 3.039l5.657-5.657C34.046 6.053 29.268 4 24 4 16.318 4 9.656 8.337 6.306 14.691z"/>'
    '<path fill="#4CAF50" d="M24 44c5.166 0 9.86-1.977 13.409-5.192l-6.19-5.238A11.91 11.91 0 0 1 24 36c-5.202 0-9.619-3.317-11.283-7.946l-6.522 5.025C9.505 39.556 16.227 44 24 44z"/>'
    '<path fill="#1976D2" d="M43.611 20.083H42V20H24v8h11.303a12.04 12.04 0 0 1-4.087 5.571l.003-.002 6.19 5.238C36.971 39.205 44 34 44 24c0-1.341-.138-2.65-.389-3.917z"/>'
    '</svg>')
STAR = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 17.27 18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"/></svg>'


def review_card(i, r):
    text = _html.escape(r["text"].strip()).replace("\n\n", "<br><br>").replace("\n", "<br>")
    return f"""      <article class="gr-card reveal reveal-d{i % 3}">
        <header class="gr-card__head">
          <span class="gr-avatar" style="background:{r.get('color', '#1a73e8')}" aria-hidden="true">{_html.escape(r['name'][0])}</span>
          <span class="gr-name">{_html.escape(r['name'])}</span>
          {GOOGLE_G}
        </header>
        <div class="gr-stars" role="img" aria-label="Rated 5 out of 5 stars">{STAR * 5}</div>
        <p class="gr-text">{text}</p>
        <button class="gr-more" type="button" aria-expanded="false" hidden>Read more</button>
      </article>"""


def reviews_section(sand=False):
    if not REVIEWS:
        return ""
    cards = "\n".join(review_card(i, r) for i, r in enumerate(REVIEWS))
    return f"""<section class="section{' section--sand' if sand else ''}" id="reviews">
  <div class="wrap">
    <div class="section-head section-head--split">
      <div>
        <span class="eyebrow reveal">Client reviews</span>
        <h2 class="h2 reveal reveal-d1">In their <em>own words.</em></h2>
      </div>
      <p class="lede reveal reveal-d2">Real reviews from Danielle's clients on Google.</p>
    </div>
    <div class="gr reveal">
      <div class="gr-bar">
        <div class="gr-brand">{GOOGLE_G}<span>Google Reviews</span></div>
        <a class="gr-btn" href="{GOOGLE_REVIEWS_URL}" target="_blank" rel="noopener">See all reviews</a>
      </div>
      <div class="gr-track">
{cards}
      </div>
    </div>
  </div>
</section>"""


# --------------------------------------------------------------------------- HOME
marquee_items = "".join(f"<span>{c[1]}</span>" for c in COMMUNITIES)
community_cards = "\n".join(f"""      <a class="community reveal reveal-d{i % 3}" href="communities.html#{c[0]}">
        {mountain_art(i)}
        <span class="community__idx">0{i+1}</span>
        <h3>{c[1].replace("&", "&amp;")}</h3>
        <p>{c[3]}</p>
        <span class="tags">{c[2]}</span>
      </a>""" for i, c in enumerate(COMMUNITIES))

home = f"""<section class="hero">
  <div class="hero__copy">
    <span class="eyebrow fade-up">Utah Luxury Real Estate · Relocation Specialist</span>
    <h1 class="display">
      <span class="line-reveal"><span>Your next</span></span>
      <span class="line-reveal"><span>chapter starts</span></span>
      <span class="line-reveal"><span><em>in Utah.</em></span></span>
    </h1>
    <p class="lede fade-up">Luxury real estate and relocation for C-suite executives, physicians and medical professionals — discreet, seamless and stress-free.</p>
    <div class="btn-row fade-up">
      <a class="btn" href="contact.html#schedule">Schedule a Consultation {ARROW}</a>
      <a class="btn btn--ghost" href="communities.html">Explore Communities</a>
    </div>
    <div class="scroll-cue fade-up"><i></i>Scroll</div>
  </div>
  <div class="hero__media">
    <div class="hero__img">{img("danielle-kitchen-walk", "Danielle Vaughns walking through a bright, modern Utah kitchen", eager=True, pos="50% 30%")}</div>
    <div class="hero__badge" aria-hidden="true">
      <svg viewBox="0 0 168 168"><defs><path id="circ" d="M84 84m-64 0a64 64 0 1 1 128 0a64 64 0 1 1-128 0"/></defs>
        <text><textPath href="#circ">Utah Relocation Specialist · DV Realty · </textPath></text></svg>
      <img src="assets/img/monogram.png" alt="" width="199" height="199">
    </div>
    <div class="hero__meta">Salt Lake City · Park City · Northern Utah</div>
  </div>
</section>

<div class="marquee" aria-hidden="true"><div class="marquee__track">{marquee_items}{marquee_items}{marquee_items}{marquee_items}</div></div>

{featured_section(limit=2, sand=True)}

<section class="section">
  <div class="wrap">
    <div class="split">
      <div class="frame reveal">
        <div class="frame__img mask">{img("danielle-smile", "Danielle Vaughns smiling, resting her chin on her hand at a kitchen table", sizes="(max-width: 900px) 100vw, 45vw")}</div>
        <div class="frame__tag"><small>KW Utah</small><strong>Top 10 Individual Producer</strong></div>
      </div>
      <div>
        <span class="eyebrow reveal">Meet your agent</span>
        <h2 class="h2 reveal reveal-d1">A personal guide for <em>one of life's biggest moves.</em></h2>
        <p class="lede reveal reveal-d2">Danielle moved 12 times as an Air Force family, so she knows firsthand what relocation really takes. Today she guides executives, physicians and their families through their own moves with local expertise, genuine care and complete discretion. Whether you're moving across the country or across the valley, she makes the journey feel effortless.</p>
        <ul class="checklist reveal reveal-d3">
          <li>Licensed Utah REALTOR®</li>
          <li>{LUXURY} · Luxury Market Center Liaison</li>
          <li>Member, Utah Board of REALTORS® &amp; Park City Board of REALTORS®</li>
          <li>Medical &amp; C-Suite Relocation Specialist</li>
        </ul>
        <p class="signature reveal reveal-d3">Danielle Vaughns</p>
        <a class="link-arrow reveal reveal-d4" href="about.html">Meet Danielle {ARROW}</a>
      </div>
    </div>
  </div>
</section>

<section class="section section--dark">
  <div class="wrap">
    <div class="section-head section-head--split">
      <div>
        <span class="eyebrow reveal">Relocation services</span>
        <h2 class="h2 reveal reveal-d1">Your relocation, <em>handled with expertise.</em></h2>
      </div>
      <p class="lede reveal reveal-d2">From your first search to closing day and beyond, Danielle provides end-to-end support tailored to your move, your family and your timeline.</p>
    </div>
    <div class="services">
      <article class="service reveal">
        <span class="service__num">01</span>
        <h3>Personalized Home Search</h3>
        <p>A curated shortlist of homes matched to your lifestyle, budget and vision — saving you time and eliminating the guesswork.</p>
      </article>
      <article class="service reveal reveal-d1">
        <span class="service__num">02</span>
        <h3>Virtual Tours &amp; Neighborhood Guidance</h3>
        <p>Can't visit yet? Live virtual tours and in-depth neighborhood walkthroughs let you decide with confidence from anywhere.</p>
      </article>
      <article class="service reveal reveal-d2">
        <span class="service__num">03</span>
        <h3>End-to-End Relocation Support</h3>
        <p>School research, commutes, utilities and trusted local resources — Danielle guides you through every step of the move.</p>
      </article>
    </div>
    <div class="reveal" style="margin-top:64px"><a class="link-arrow" href="services.html">Explore all services {ARROW}</a></div>
  </div>
</section>

<section class="feature on-dark" id="medical">
  <div class="feature__media mask">
    {img("danielle-desk-blazer", "Danielle Vaughns at her desk in a navy blazer, looking out the window", sizes="(max-width: 900px) 100vw, 45vw", pos="50% 35%")}
  </div>
  <div class="feature__copy">
    <span class="eyebrow reveal">For medical &amp; C-suite professionals</span>
    <h2 class="h2 reveal reveal-d1">Your schedule is demanding. <em>Your move shouldn't be.</em></h2>
    <p class="lede reveal reveal-d2">Danielle specializes in helping physicians, medical professionals and executives relocate to Utah — on a real timeline, with as little of your time as possible.</p>
    <ul class="feature__list reveal reveal-d3">
      <li><b>i.</b>Introductions to lenders who understand physician and jumbo loans</li>
      <li><b>ii.</b>Neighborhoods mapped to your hospital commute</li>
      <li><b>iii.</b>Mid- to long-term luxury rentals while you find the right home</li>
      <li><b>iv.</b>Personalized area tours — in person or virtual</li>
    </ul>
    <div class="reveal reveal-d4"><a class="btn btn--gold" href="relocate.html#medical">Plan Your Relocation {ARROW}</a></div>
  </div>
</section>

{reviews_section(sand=True)}

<section class="section">
  <div class="wrap">
    <div class="section-head section-head--split">
      <div>
        <span class="eyebrow reveal">Utah communities</span>
        <h2 class="h2 reveal reveal-d1">Find the place your family <em>will thrive.</em></h2>
      </div>
      <p class="lede reveal reveal-d2">From Yalecrest's historic streets to the mountain calm of Park City — Danielle knows Northern Utah's communities, the commutes, the schools and the little details that make each one feel like home.</p>
    </div>
    <div class="communities">
{community_cards}
    </div>
  </div>
</section>

<section class="section section--sand">
  <div class="wrap">
    <figure class="quote reveal">
      <span class="quote__mark" aria-hidden="true">“</span>
      <blockquote>Moving isn't just about square footage or zip codes. It's about finding the community where your family will thrive — where your mornings feel right, and where you can truly put down roots.</blockquote>
      <figcaption><cite>Danielle Vaughns</cite></figcaption>
    </figure>
  </div>
</section>

{cta()}"""

# --------------------------------------------------------------------------- ABOUT
def team_card(i, m):
    initials = "".join(w[0] for w in m["name"].split()[:2])
    photo = (f'<img src="{m["image"]}" alt="{m["name"]}, {m["role"]}" width="960" height="1200" loading="lazy" decoding="async">'
             if m.get("image") else f'<span class="member__initials" aria-hidden="true">{initials}</span>')
    bio = f'\n        <p>{m["bio"]}</p>' if m.get("bio") else ""
    return f"""      <article class="member reveal reveal-d{i % 3}">
        <div class="member__photo">{photo}</div>
        <h3>{m["name"]}</h3>
        <span class="member__role">{m["role"]}</span>{bio}
      </article>"""

team_cards = "\n".join(team_card(i, m) for i, m in enumerate(TEAM))

ICON = {
    "badge": '<svg viewBox="0 0 36 36"><circle cx="18" cy="14" r="9"/><path d="M12 21l-3 12 9-4 9 4-3-12"/></svg>',
    "star": '<svg viewBox="0 0 36 36"><path d="M18 3l4.4 9.6L33 14l-7.8 7.2L27.2 32 18 26.8 8.8 32l2-10.8L3 14l10.6-1.4z"/></svg>',
    "cross": '<svg viewBox="0 0 36 36"><rect x="4" y="4" width="28" height="28" rx="14"/><path d="M18 11v14M11 18h14"/></svg>',
    "key": '<svg viewBox="0 0 36 36"><circle cx="12" cy="18" r="7"/><path d="M19 18h14M28 18v6M32 18v4"/></svg>',
    "mountain": '<svg viewBox="0 0 36 36"><path d="M2 30l11-17 6 9 4-5 11 13z"/><path d="M10 17.5l3 2 3-2"/></svg>',
    "diamond": '<svg viewBox="0 0 36 36"><path d="M9 6h18l6 8-15 17L3 14z"/><path d="M3 14h30M13 6l5 25 5-25"/></svg>',
}

about = f"""<section class="page-hero">
  <div class="page-hero__glow"></div>
  <div class="wrap">
    <div class="crumbs fade-up"><a href="index.html">Home</a><span>/</span>About</div>
    <h1 class="h1">
      <span class="line-reveal"><span>Danielle Vaughns</span></span>
      <span class="line-reveal"><span><em>Utah REALTOR® &amp; Relocation Specialist</em></span></span>
    </h1>
  </div>
  {RIDGE.format(cls="page-hero__ridge")}
</section>

<section class="section">
  <div class="wrap">
    <div class="split split--reverse">
      <div class="frame frame--left reveal">
        <div class="frame__img mask">{img("danielle-blazer", "Danielle Vaughns in a navy blazer, smiling in a modern kitchen", sizes="(max-width: 900px) 100vw, 45vw", pos="50% 25%")}</div>
        <div class="frame__tag"><small>Serving</small><strong>Northern Utah</strong></div>
      </div>
      <div>
        <span class="eyebrow reveal">A personal welcome</span>
        <h2 class="h2 reveal reveal-d1">Your move to Utah deserves <em>an expert by your side.</em></h2>
        <p class="lede reveal reveal-d2">Welcome — I'm so glad you're here. Whether you're relocating from across the country or searching for your forever home right here in Utah, I want you to know this journey matters to me.</p>
        <p class="reveal reveal-d2">I specialize in helping medical professionals, executives and their families make the move to Utah. I know your schedule is demanding and your timeline is real, so I make the process as simple and stress-free as possible — from personalized area tours to connecting you with lenders who understand physician and jumbo loans. And because privacy matters in luxury real estate, every client can count on my complete discretion.</p>
        <p class="reveal reveal-d3">Moving isn't just about square footage or zip codes. It's about finding the community where your family will thrive, where your mornings feel right, and where you can truly put down roots.</p>
        <p class="signature reveal reveal-d3">Danielle</p>
        <div class="btn-row reveal reveal-d4">
          <a class="btn" href="contact.html#schedule">Schedule a Call {ARROW}</a>
          <a class="btn btn--ghost" href="mailto:{EMAIL}">Send a Message</a>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section section--sand" id="story">
  <div class="wrap">
    <div class="story">
      <div>
        <span class="eyebrow reveal">Her story</span>
        <h2 class="h2 reveal reveal-d1">Twelve moves taught her <em>what home really means.</em></h2>
        <dl class="story-stats reveal reveal-d2">
          <div><dt>Moves as an Air Force family</dt><dd>12</dd></div>
          <div><dt>Born in</dt><dd>Virginia</dd></div>
          <div><dt>Gives back</dt><dd>Non-profit board member</dd></div>
        </dl>
      </div>
      <div class="story__text">
        <p class="lede reveal">Danielle was born in Virginia and spent her childhood on the East Coast before her family moved to Olympia, Washington, when her dad retired from the Air Force.</p>
        <p class="reveal">Moving would continue to be a theme throughout her life. She married her college sweetheart, a newly commissioned Air Force officer, and over his career they lived throughout the country and moved 12 times. Danielle became all too familiar with the process of moving and relocation — and that experience shapes how she guides every client today.</p>
        <p class="reveal">Before real estate, Danielle spent several years in non-profit development and marketing. She now uses those skills to help clients buy, sell and invest in property. Her compassionate heart keeps her involved in serving the underprivileged in her community, through volunteer work and as a board member of a local non-profit.</p>
        <p class="reveal">Multiple moves aside, Danielle has always been passionate about travel and has explored much of Europe. She loves the thrill of adventure while also having a deep appreciation for settling down. When she isn't busy with real estate or serving the community, you'll find her skiing, discovering new restaurants and coffee shops, or enjoying time with her family. Her charisma is infectious and overflows into every part of her life.</p>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head center">
      <span class="eyebrow eyebrow--center reveal">Qualifications</span>
      <h2 class="h2 reveal reveal-d1">Credentials &amp; <em>designations</em></h2>
    </div>
    <div class="creds">
      <div class="cred reveal">{ICON['badge']}<strong>Licensed Utah REALTOR®</strong></div>
      <div class="cred reveal reveal-d1">{ICON['star']}<strong>KW Utah Top 10 Individual Producer</strong></div>
      <div class="cred reveal reveal-d2">{ICON['cross']}<strong>Medical &amp; C-Suite Relocation Specialist</strong></div>
      <div class="cred reveal">{ICON['diamond']}<strong>{LUXURY} Agent &amp; Luxury Market Center Liaison</strong></div>
      <div class="cred reveal reveal-d1">{ICON['mountain']}<strong>Member, Utah Board of REALTORS® &amp; Park City Board of REALTORS®</strong></div>
      <div class="cred reveal reveal-d2">{ICON['key']}<strong>Buyer &amp; Seller Representation</strong></div>
    </div>
  </div>
</section>

<section class="section section--sand">
  <div class="wrap">
    <div class="split">
      <div class="frame reveal">
        <div class="frame__img mask">{img("danielle-book", "Danielle Vaughns holding a book beside a round mirror in a bright home", sizes="(max-width: 900px) 100vw, 45vw")}</div>
        <div class="frame__tag"><small>Experience</small><strong>Utah Expert</strong></div>
      </div>
      <div>
        <span class="eyebrow reveal">Local expertise</span>
        <h2 class="h2 reveal reveal-d1">At home in Utah's <em>most sought-after communities.</em></h2>
        <p class="lede reveal reveal-d2">From the historic streets of Yalecrest to the mountain charm of Park City, I know Northern Utah's most desirable communities inside and out — the commutes to major hospitals, the schools, the lifestyle, and the little details that make each area feel like home.</p>
        <ul class="checklist checklist--cols reveal reveal-d3">
          <li>Salt Lake City &amp; Yalecrest</li>
          <li>Park City &amp; Summit County</li>
          <li>Millcreek &amp; Holladay</li>
          <li>Cottonwood Heights &amp; Sandy</li>
          <li>Draper &amp; South Jordan</li>
          <li>Utah County</li>
          <li>Physician &amp; jumbo loan guidance</li>
          <li>Luxury rentals &amp; corporate housing</li>
        </ul>
        <a class="link-arrow reveal reveal-d4" href="communities.html">Explore communities {ARROW}</a>
      </div>
    </div>
  </div>
</section>

<section class="triptych" aria-label="Photos of Danielle">
  <div class="triptych__item mask">{img("danielle-kitchen", "Danielle Vaughns standing at a kitchen island", sizes="(max-width: 900px) 33vw, 380px", pos="50% 8%")}</div>
  <div class="triptych__item mask">{img("danielle-sofa-2", "Danielle Vaughns seated on a leather sofa in a sunlit living room", sizes="(max-width: 900px) 33vw, 380px", pos="70% 50%")}</div>
  <div class="triptych__item mask">{img("danielle-living-room", "Danielle Vaughns walking through a living room with a marble fireplace", sizes="(max-width: 900px) 33vw, 380px", pos="50% 25%")}</div>
</section>

<section class="section section--dark">
  <div class="wrap">
    <div class="section-head center">
      <span class="eyebrow eyebrow--center reveal">What I stand for</span>
      <h2 class="h2 reveal reveal-d1">My core <em>values</em></h2>
    </div>
    <div class="values">
      <div class="value reveal"><h3>Integrity First</h3><p>Every client deserves honest, transparent guidance. No pressure, no shortcuts — I represent your best interests at every step.</p></div>
      <div class="value reveal reveal-d1"><h3>Complete Discretion</h3><p>Privacy matters, especially in luxury real estate. Your search, your sale and your plans stay confidential, shared only with the people who need to know.</p></div>
      <div class="value reveal reveal-d2"><h3>White-Glove Service</h3><p>From your first call to closing day and beyond, a concierge-level experience tailored to your life and your timeline.</p></div>
    </div>
  </div>
</section>

{reviews_section()}

<section class="section section--sand" id="team">
  <div class="wrap">
    <div class="section-head center">
      <span class="eyebrow eyebrow--center reveal">Behind every move</span>
      <h2 class="h2 reveal reveal-d1">Meet the <em>team</em></h2>
    </div>
    <div class="team">
{team_cards}
    </div>
  </div>
</section>

{cta(title="Let's find your <em>Utah home.</em>", lede="Luxury service. Lasting relationships. Whether you're relocating from out of state or searching locally, let's start with a conversation.")}"""

# --------------------------------------------------------------------------- SERVICES
SERVICES = [
    ("buying", "Buying a Home", "Primary homes · Second homes · Luxury properties",
     "From the first conversation to the day you get your keys, Danielle guides your purchase with local insight, sharp negotiation and complete discretion.",
     ["A hand-curated shortlist matched to your lifestyle and budget",
      "Access to off-market and coming-soon homes",
      "In-person and live virtual tours",
      "Introductions to trusted lenders, including physician and jumbo loans",
      "Strategic offers and skilled negotiation",
      "Inspection, appraisal and closing, coordinated around your schedule"],
     ("listings.html", "View current listings")),
    ("selling", "Selling a Home", "Pricing · Preparation · Marketing · Negotiation",
     "Danielle positions your home to attract qualified buyers and the strongest possible offer — backed by Keller Williams Luxury and handled with discretion from listing to closing.",
     ["A pricing strategy grounded in current market data",
      "Guidance on preparing and presenting your home",
      "Marketing that reaches qualified local and out-of-state buyers",
      "Private, discreet showings when you need them",
      "Skilled negotiation on every offer",
      "Steady communication through closing"],
     ("contact.html#message", "Talk about selling")),
    ("relocation", "Relocation", "Out-of-state moves · Buying from afar · Settling in",
     "Danielle moved 12 times as an Air Force family, so she knows what relocation really takes. Her six-step process takes you from wherever you are today to settled in Northern Utah.",
     ["A discovery call about your timeline, budget, commute and lifestyle",
      "A neighborhood shortlist with honest notes on the trade-offs",
      "Area tours in person or by live video",
      "A clear rent-first or buy-now strategy",
      "Coordination with a trusted agent in your current city",
      "Local recommendations to help you settle in"],
     ("relocate.html", "See the relocation process")),
    ("medical", "Medical &amp; C-Suite Relocation", "Physicians · Residents · Executives",
     "A residency match, a new attending role, a C-suite appointment — these moves come with fixed dates and very little free time. Danielle builds your move around your schedule, with complete discretion.",
     ["Neighborhoods mapped to your hospital or office commute",
      "Lenders experienced with physician and jumbo loans",
      "Luxury rentals while you find the right home",
      "Virtual tours and remote signing so you can buy from anywhere",
      "Confidential representation for high-profile clients"],
     ("relocate.html#medical", "Medical &amp; executive relocation")),
    ("rentals", "Luxury Rentals &amp; Corporate Housing", "Mid- to long-term · Corporate · Medical stays",
     "Not every move starts with a purchase. Danielle arranges high-end rentals and corporate housing for executives, medical professionals and their families — handled with the same care and discretion as a luxury sale.",
     ["Mid- to long-term luxury rentals",
      "Corporate housing for relocating executives and their families",
      "Short-term stays in high-end homes for medical professionals and families",
      "Homes matched to your dates, budget and lifestyle",
      "A smooth path to buying when you're ready"],
     ("relocate.html#luxury-services", "More about luxury services")),
    ("investment", "Investment Properties", "Buy · Sell · Grow your portfolio",
     "Whether you're adding a rental, a second home or your first investment property, Danielle helps you evaluate opportunities and buy or sell with a clear plan.",
     ["Help finding properties that fit your goals",
      "Guidance on neighborhoods across Northern Utah",
      "Representation when buying or selling investment properties",
      "Introductions to trusted lenders and local resources"],
     ("contact.html#message", "Talk about investing")),
]

SERVICE_SUMMARY = {
    "buying": "Find the right home with local insight, off-market access and skilled negotiation.",
    "selling": "Price, present and market your home to reach qualified buyers — with discretion.",
    "relocation": "A calm, six-step move to Northern Utah from wherever you are today.",
    "medical": "Moves built around fixed start dates for physicians and executives.",
    "rentals": "Mid- to long-term luxury rentals, corporate housing and medical stays.",
    "investment": "Buy or sell rentals, second homes and investment properties with a clear plan.",
}

service_overview = "\n".join(f"""      <a class="svc-card reveal reveal-d{i % 3}" href="#{sid}">
        <span class="service__num">0{i+1}</span>
        <h3>{name}</h3>
        <p>{SERVICE_SUMMARY[sid]}</p>
      </a>""" for i, (sid, name, tags, lede, items, link) in enumerate(SERVICES))

service_details = "\n".join(f"""    <article class="area" id="{sid}">
      <div class="area__head reveal">
        <span class="area__num">No. 0{i+1}</span>
        <h2 class="h2">{name}</h2>
        <div class="tags">{tags}</div>
      </div>
      <div class="area__body reveal reveal-d1">
        <p class="lede">{lede}</p>
        <ul class="checklist checklist--cols">
{chr(10).join(f"          <li>{x}</li>" for x in items)}
        </ul>
        <a class="link-arrow" href="{link[0]}">{link[1]} {ARROW}</a>
      </div>
    </article>""" for i, (sid, name, tags, lede, items, link) in enumerate(SERVICES))

services = f"""<section class="page-hero">
  <div class="page-hero__glow"></div>
  <div class="wrap">
    <div class="crumbs fade-up"><a href="index.html">Home</a><span>/</span>Services</div>
    <h1 class="h1">
      <span class="line-reveal"><span>Every service,</span></span>
      <span class="line-reveal"><span><em>one trusted advisor.</em></span></span>
    </h1>
    <p class="lede fade-up">Buying, selling, relocating, renting or investing — Danielle guides every step with local expertise, white-glove service and complete discretion.</p>
  </div>
  {RIDGE.format(cls="page-hero__ridge")}
</section>

<section class="section section--sand">
  <div class="wrap">
    <div class="svc-grid">
{service_overview}
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
{service_details}
  </div>
</section>

{cta(title="Not sure where <em>to start?</em>", lede="Tell Danielle about your plans and she'll recommend the right next step — no pressure, no obligation.")}"""

# --------------------------------------------------------------------------- RELOCATE
STEPS = [
    ("Discovery call", "We talk through your move — timeline, budget, commute, schools, lifestyle — and what home needs to feel like for your family."),
    ("Your Utah shortlist", "Danielle narrows the map to the communities that fit, with honest notes on the trade-offs of each one."),
    ("Tour — in person or virtual", "A personalized area tour when you're in town, or live video walkthroughs of homes and neighborhoods when you can't be."),
    ("Financing &amp; strategy", "Introductions to trusted lenders, including those who understand physician and jumbo loans, plus a clear plan for renting first or buying now."),
    ("Offer to closing", "Strategic negotiation and steady communication through inspection, appraisal and closing — coordinated around your schedule."),
    ("Settling in", "Utilities, local services and recommendations from people who live here. Danielle's support doesn't stop at the keys."),
]
steps = "\n".join(f"""      <div class="step reveal">
        <span class="step__num">0{i+1}</span>
        <h3>{t}</h3>
        <p>{d}</p>
      </div>""" for i, (t, d) in enumerate(STEPS))

relocate = f"""<section class="page-hero">
  <div class="page-hero__glow"></div>
  <div class="wrap">
    <div class="crumbs fade-up"><a href="index.html">Home</a><span>/</span>Relocate</div>
    <h1 class="h1">
      <span class="line-reveal"><span>Relocating to Utah,</span></span>
      <span class="line-reveal"><span><em>beautifully handled.</em></span></span>
    </h1>
    <p class="lede fade-up">A calm, well-run process from the first phone call to the day you get your keys — designed for people moving from out of state, on a real timeline.</p>
  </div>
  {RIDGE.format(cls="page-hero__ridge")}
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head section-head--split">
      <div>
        <span class="eyebrow reveal">The process</span>
        <h2 class="h2 reveal reveal-d1">Six steps to <em>home.</em></h2>
      </div>
      <p class="lede reveal reveal-d2">Every move is different, but the best ones share a clear plan. Here's how Danielle guides you from wherever you are today to settled in Utah.</p>
    </div>
    <div class="steps">
{steps}
    </div>
  </div>
</section>

<section class="feature on-dark" id="medical">
  <div class="feature__media mask">
    {img("danielle-sofa", "Danielle Vaughns relaxing on a tufted leather sofa", sizes="(max-width: 900px) 100vw, 45vw", pos="62% 50%")}
  </div>
  <div class="feature__copy">
    <span class="eyebrow reveal">Medical &amp; executive relocation</span>
    <h2 class="h2 reveal reveal-d1">Built around <em>your start date.</em></h2>
    <p class="lede reveal reveal-d2">A residency match, a new attending role, a C-suite appointment — these moves come with fixed dates and very little free time. Danielle specializes in exactly this, with complete discretion.</p>
    <ul class="feature__list reveal reveal-d3">
      <li><b>i.</b>Neighborhoods mapped to your hospital and call-schedule commute</li>
      <li><b>ii.</b>Introductions to lenders experienced with physician and jumbo loans</li>
      <li><b>iii.</b>Rent-first options when buying before you arrive doesn't make sense</li>
      <li><b>iv.</b>Virtual tours and remote signing so you can buy from anywhere</li>
    </ul>
    <div class="reveal reveal-d4"><a class="btn btn--gold" href="contact.html#schedule">Plan Your Move {ARROW}</a></div>
  </div>
</section>

<section class="section" id="luxury-services">
  <div class="wrap">
    <div class="section-head section-head--split">
      <div>
        <span class="eyebrow reveal">Luxury services</span>
        <h2 class="h2 reveal reveal-d1">Luxury rentals &amp; <em>corporate housing.</em></h2>
      </div>
      <p class="lede reveal reveal-d2">Not every move starts with a purchase. Danielle arranges high-end rentals and corporate housing for executives, medical professionals and their families — handled with the same care and discretion as a luxury sale.</p>
    </div>
    <div class="services services--light">
      <article class="service reveal">
        <span class="service__num">01</span>
        <h3>Mid- to long-term luxury rentals</h3>
        <p>High-end homes for a season, a contract term or a trial run in a new community — so you can live like a local before you commit to buying.</p>
      </article>
      <article class="service reveal reveal-d1">
        <span class="service__num">02</span>
        <h3>Corporate housing</h3>
        <p>Move-in-ready homes for relocating executives and their families, coordinated around your start date and your company's relocation plans.</p>
      </article>
      <article class="service reveal reveal-d2">
        <span class="service__num">03</span>
        <h3>Medical moves &amp; stays</h3>
        <p>Short-term stays in high-end homes for medical professionals and families who need to be in Utah for a set time — arranged around your dates.</p>
      </article>
    </div>
    <div class="reveal" style="margin-top:56px"><a class="link-arrow" href="contact.html#message">Ask about luxury rentals {ARROW}</a></div>
  </div>
</section>

<section class="section section--sand">
  <div class="wrap">
    <div class="section-head center">
      <span class="eyebrow eyebrow--center reveal">Two paths</span>
      <h2 class="h2 reveal reveal-d1">Rent first, <em>or buy now?</em></h2>
      <p class="lede reveal reveal-d2">There's no single right answer — Danielle will help you weigh it honestly for your situation.</p>
    </div>
    <div class="services services--light">
      <article class="service reveal">
        <span class="service__num">A</span>
        <h3>Rent first</h3>
        <p>Live in Utah for a season, learn the commutes and neighborhoods first-hand, then buy with total confidence. Ideal when your timeline is tight or the area is brand new to you.</p>
      </article>
      <article class="service reveal reveal-d1">
        <span class="service__num">B</span>
        <h3>Buy now</h3>
        <p>Move once and start building equity on day one. With virtual tours and a trusted local advocate, many clients buy before they ever arrive.</p>
      </article>
      <article class="service reveal reveal-d2">
        <span class="service__num">C</span>
        <h3>Sell where you are</h3>
        <p>Need to sell before you move? Danielle can coordinate with a trusted agent in your current city so both sides of the move stay in sync.</p>
      </article>
    </div>
  </div>
</section>

{cta()}"""

# --------------------------------------------------------------------------- COMMUNITIES
AREAS = [
    ("salt", "Salt Lake City", "The Avenues · Sugar House · Federal Heights · East Bench",
     "Utah's capital pairs historic tree-lined neighborhoods with a growing downtown, a major international airport and the state's largest academic medical campus at the University of Utah — all with mountain canyons just minutes from the city.",
     [("Lifestyle", "Walkable historic districts, dining, arts and professional sports"),
      ("Outdoors", "Red Butte, City Creek and Emigration canyons close by"),
      ("Good to know", "Close to University of Utah Health, Huntsman Cancer Institute and the VA")]),
    ("yalecrest", "Yalecrest", "East side Salt Lake City · Historic homes · Tree-lined streets",
     "One of Salt Lake City's most beloved historic neighborhoods. Yalecrest is known for its tree-lined streets — many named for universities like Yale, Harvard and Princeton — and character-rich bungalows, English cottages and period-revival homes from the early twentieth century.",
     [("Lifestyle", "Minutes to the shops and dining of 15th &amp; 15th and 9th &amp; 9th"),
      ("Outdoors", "Neighborhood parks and quick access to the foothill trails"),
      ("Good to know", "Minutes to the University of Utah and downtown Salt Lake City")]),
    ("park", "Park City &amp; Summit County", "Old Town · Deer Valley · Kimball Junction · Jeremy Ranch",
     "A historic mining town turned world-class mountain resort, and the longtime home of the Sundance Film Festival. Park City offers three major ski areas, including Deer Valley, a lively Main Street and year-round trails, a short drive from Salt Lake via Parley's Canyon.",
     [("Lifestyle", "Main Street dining, galleries and a true four-season mountain town"),
      ("Outdoors", "Three major ski areas and world-class mountain biking on hundreds of miles of trails"),
      ("Good to know", "Roughly 35–45 minutes to Salt Lake City International, depending on traffic")]),
    ("millcreek", "Millcreek &amp; Holladay", "Millcreek · Holladay · Mature trees · Larger lots",
     "Gracious, established neighborhoods on Salt Lake's east side. Holladay is known for mature landscaping, larger lots and its village-style center; Millcreek offers a mix of classic and newer homes at the foot of Millcreek Canyon.",
     [("Lifestyle", "Quiet, tree-lined streets, Holladay Village and Millcreek Common"),
      ("Outdoors", "Millcreek Canyon's trails close by, with the Cottonwood canyons a short drive away"),
      ("Good to know", "Convenient to Intermountain Medical Center in Murray")]),
    ("cottonwoods", "The Cottonwoods &amp; Sandy", "Cottonwood Heights · Sandy · Canyon access",
     "Neighborhoods at the mouths of Big and Little Cottonwood Canyons, with some of the closest access in the valley to Brighton, Solitude, Alta and Snowbird.",
     [("Lifestyle", "Established neighborhoods, larger lots and easy freeway access"),
      ("Outdoors", "Brighton, Solitude, Alta and Snowbird up the Cottonwood canyons"),
      ("Good to know", "An easy commute to downtown Salt Lake City via I-215 and I-15")]),
    ("draper", "Draper &amp; South Jordan", "Draper · South Jordan · Corner Canyon · Daybreak",
     "Newer homes, strong amenities and some of the valley's best trail systems, with an easy commute north to Salt Lake or south to Utah County.",
     [("Lifestyle", "Family-friendly neighborhoods, newer construction and master-planned Daybreak"),
      ("Outdoors", "Corner Canyon's trail network and quick access to the Cottonwood canyons"),
      ("Good to know", "Central to both Salt Lake and Utah County employers")]),
    ("utah-county", "Utah County", "Lehi · Silicon Slopes · Provo · Orem",
     "The heart of Utah's tech corridor, known as Silicon Slopes — the community behind the annual Silicon Slopes Summit, which draws innovators from around the world. Lehi and its neighbors offer abundant new construction and a younger community, with BYU and Utah Valley University to the south.",
     [("Lifestyle", "Thanksgiving Point, new town centers and a fast-growing restaurant scene"),
      ("Outdoors", "American Fork Canyon, Utah Lake and Provo Canyon nearby"),
      ("Good to know", "Intermountain Primary Children's Lehi campus, and BYU's new School of Medicine in Provo opening to its first class in July 2027")]),
    ("heber", "Heber Valley &amp; Midway", "Midway · Heber City · Jordanelle",
     "Wide pastoral valleys framed by the Wasatch, just over the ridge from Park City.",
     [("Lifestyle", "Small-town pace and open views"),
      ("Outdoors", "Jordanelle and Deer Creek reservoirs"),
      ("Good to know", "About 20 minutes to Park City")]),
]

areas = "\n".join(f"""    <article class="area" id="{aid}">
      <div class="area__head reveal">
        <span class="area__num">No. 0{i+1}</span>
        <h2 class="h2">{name}</h2>
        <div class="tags">{tags}</div>
      </div>
      <div class="area__body reveal reveal-d1">
        <p class="lede">{desc}</p>
        <dl class="facts">
{''.join(f'          <div><dt>{k}</dt><dd>{v}</dd></div>' + chr(10) for k, v in facts)}        </dl>
      </div>
    </article>""" for i, (aid, name, tags, desc, facts) in enumerate(AREAS))

communities = f"""<section class="page-hero">
  <div class="page-hero__glow"></div>
  <div class="wrap">
    <div class="crumbs fade-up"><a href="index.html">Home</a><span>/</span>Communities</div>
    <h1 class="h1">
      <span class="line-reveal"><span>Utah's most</span></span>
      <span class="line-reveal"><span><em>sought-after communities.</em></span></span>
    </h1>
    <p class="lede fade-up">An insider's introduction to the places Danielle's clients call home — the lifestyle, the commute and what makes each one special.</p>
  </div>
  {RIDGE.format(cls="page-hero__ridge")}
</section>

<section class="section">
  <div class="wrap">
{areas}
  </div>
</section>

<section class="section section--sand">
  <div class="wrap">
    <figure class="quote reveal">
      <span class="quote__mark" aria-hidden="true">“</span>
      <blockquote>Not sure which community is right for you? That's exactly what our first conversation is for.</blockquote>
      <figcaption><cite>Danielle Vaughns</cite></figcaption>
    </figure>
  </div>
</section>

{cta()}"""

# --------------------------------------------------------------------------- LISTINGS
listings = f"""<section class="page-hero">
  <div class="page-hero__glow"></div>
  <div class="wrap">
    <div class="crumbs fade-up"><a href="index.html">Home</a><span>/</span>Listings</div>
    <h1 class="h1">
      <span class="line-reveal"><span>Find your</span></span>
      <span class="line-reveal"><span><em>Utah home.</em></span></span>
    </h1>
    <p class="lede fade-up">Handpicked properties across Northern Utah's most sought-after communities — from Yalecrest to Park City, the Cottonwoods to Utah County.</p>
    <div class="btn-row fade-up" style="margin-top:40px">
      <a class="btn btn--gold" href="{KW_SEARCH}" target="_blank" rel="noopener">Search All Utah Homes {ARROW}</a>
    </div>
  </div>
  {RIDGE.format(cls="page-hero__ridge")}
</section>

{featured_section()}

<section class="section{' section--sand' if LISTINGS else ''}">
  <div class="wrap">
    <div class="search-panel reveal">
      <div>
        <span class="eyebrow">Search every listing</span>
        <h2 class="h2" style="margin-bottom:24px">Every home on the market, <em>updated live.</em></h2>
        <p class="lede">Browse every active listing across Utah — with photos, maps and saved searches — on Danielle's Keller Williams home search.</p>
        <div class="btn-row" style="margin-top:36px"><a class="btn" href="{KW_SEARCH}" target="_blank" rel="noopener">Search All Utah Homes {ARROW}</a></div>
      </div>
      <div>
        <span class="eyebrow">Private access</span>
        <h3 class="h3" style="margin-bottom:20px">A shortlist made for you</h3>
        <p>Tell Danielle what home looks like for your family and she'll send a hand-curated list — including off-market and coming-soon homes that never appear on public search sites.</p>
        <ul class="checklist" style="margin-top:28px">
          <li>Luxury &amp; move-up properties</li>
          <li>Mountain &amp; ski-area homes</li>
          <li>New construction</li>
          <li>First homes &amp; investment properties</li>
        </ul>
        <a class="link-arrow" href="contact.html#message">Request a Custom Search {ARROW}</a>
      </div>
    </div>
  </div>
</section>

<section class="section{'' if LISTINGS else ' section--sand'}">
  <div class="wrap">
    <div class="section-head section-head--split">
      <div>
        <span class="eyebrow reveal">Search by community</span>
        <h2 class="h2 reveal reveal-d1">Where would you <em>like to live?</em></h2>
      </div>
      <p class="lede reveal reveal-d2">Start with the lifestyle you want — Danielle will find the homes.</p>
    </div>
    <div class="communities">
{community_cards}
    </div>
  </div>
</section>

{cta()}"""

# --------------------------------------------------------------------------- CONTACT
contact = f"""<section class="page-hero">
  <div class="page-hero__glow"></div>
  <div class="wrap">
    <div class="crumbs fade-up"><a href="index.html">Home</a><span>/</span>Contact</div>
    <h1 class="h1">
      <span class="line-reveal"><span>Let's talk about</span></span>
      <span class="line-reveal"><span><em>your move.</em></span></span>
    </h1>
    <p class="lede fade-up">Book a free, no-obligation consultation. Danielle personally responds to every inquiry, usually within one business day.</p>
  </div>
  {RIDGE.format(cls="page-hero__ridge")}
</section>

<section class="section" id="schedule">
  <div class="wrap">
    <div class="contact-grid">
      <div class="contact-info">
        <div class="frame frame--left reveal" style="max-width:360px">
          <div class="frame__img mask">{img("danielle-smile-2", "Danielle Vaughns smiling warmly at a kitchen table", sizes="(max-width: 900px) 100vw, 360px")}</div>
        </div>
        <dl class="reveal reveal-d1">
          <div><dt>Call or text</dt><dd><a href="tel:{PHONE_TEL}">{PHONE}</a></dd></div>
          <div><dt>Email</dt><dd><a href="mailto:{EMAIL}">{EMAIL}</a></dd></div>
          <div><dt>Based in</dt><dd>Salt Lake City, Utah<br>Serving Northern Utah</dd></div>
          <div><dt>Brokerage</dt><dd>{BROKERAGE}<br>{LUXURY}<img class="brokerage-kw" src="assets/img/kw-luxury-ink.png" alt="Keller Williams Luxury" width="560" height="170" loading="lazy"></dd></div>
        </dl>
      </div>

      <div class="scheduler reveal reveal-d1">
        <span class="eyebrow">Free 30-minute consultation</span>
        <h2 class="h2">Book a time</h2>
        <p>Choose a time that works for you. Danielle will call to talk through your move — timeline, neighborhoods, financing and next steps.</p>
        <iframe class="scheduler__frame" src="{CALENDLY}?embed_type=Inline&amp;embed_domain={SITE_URL.split("//", 1)[1]}&amp;hide_gdpr_banner=1&amp;background_color=ffffff&amp;text_color=1b1222&amp;primary_color=b8924f" title="Book a free consultation with Danielle Vaughns" width="100%" height="760" frameborder="0"></iframe>
        <p class="scheduler__alt">Calendar not loading? <a href="{CALENDLY}" target="_blank" rel="noopener">Open the scheduler in a new tab ↗</a></p>
      </div>
    </div>
  </div>
</section>

<section class="section section--sand" id="message">
  <div class="wrap wrap--narrow">
    <form class="form reveal" data-contact data-email="{EMAIL}" novalidate>
      <span class="eyebrow">Prefer to write?</span>
      <h2 class="h2">Send a message</h2>
      <p>Share a little about your move or your home and Danielle will be in touch, usually within one business day.</p>
        <div class="form-grid">
          <div class="field"><label for="f-name">Full name</label><input id="f-name" name="name" autocomplete="name" required></div>
          <div class="field"><label for="f-email">Email</label><input id="f-email" name="email" type="email" autocomplete="email" required></div>
          <div class="field"><label for="f-phone">Phone</label><input id="f-phone" name="phone" type="tel" autocomplete="tel"></div>
          <div class="field"><label for="f-from">Moving from</label><input id="f-from" name="from" placeholder="City, State"></div>
          <div class="field field--full">
            <label for="f-timeline">Timeline</label>
            <select id="f-timeline" name="timeline">
              <option value="">Select one</option>
              <option>Within 3 months</option>
              <option>3–6 months</option>
              <option>6–12 months</option>
              <option>Just exploring</option>
            </select>
          </div>
          <div class="field field--full">
            <label for="f-source">How did you hear about Danielle?</label>
            <select id="f-source" name="source">
              <option value="">Select one</option>
              <option>Google search</option>
              <option>Google reviews / Google Maps</option>
              <option>ChatGPT or another AI assistant</option>
              <option>Zillow or Realtor.com</option>
              <option>Keller Williams</option>
              <option>Referral from a friend or client</option>
              <option>Social media</option>
              <option>Other</option>
            </select>
          </div>
          <fieldset class="field field--full">
            <legend>I'm interested in</legend>
            <div class="chips">
              <label class="chip"><input type="checkbox" name="interest" value="Buying"><span>Buying</span></label>
              <label class="chip"><input type="checkbox" name="interest" value="Selling"><span>Selling</span></label>
              <label class="chip"><input type="checkbox" name="interest" value="Relocating"><span>Relocating</span></label>
              <label class="chip"><input type="checkbox" name="interest" value="Medical professional relocation"><span>Medical relocation</span></label>
              <label class="chip"><input type="checkbox" name="interest" value="Renting first"><span>Renting first</span></label>
              <label class="chip"><input type="checkbox" name="interest" value="Luxury rental or corporate housing"><span>Luxury rental / corporate housing</span></label>
            </div>
          </fieldset>
          <div class="field field--full"><label for="f-msg">Tell me about your move</label><textarea id="f-msg" name="message" rows="4"></textarea></div>
        </div>
        <div class="form-foot">
          <small>Your information is kept private and used only to respond to your inquiry.</small>
          <button class="btn" type="submit">Send Request {ARROW}</button>
        </div>
        <p class="form-status" role="status" aria-live="polite"></p>
      </form>
  </div>
</section>"""

PAGES = [
    ("index.html", "Danielle Vaughns | Utah Luxury Real Estate & Relocation · DV Realty",
     "Danielle Vaughns is a Utah luxury REALTOR® and relocation specialist for C-suite executives, physicians and medical professionals, serving Salt Lake City, Park City and Northern Utah.", home),
    ("about.html", "About Danielle Vaughns | DV Realty",
     "Meet Danielle Vaughns — Utah luxury REALTOR®, KW Utah Top 10 Individual Producer and relocation specialist for medical and C-suite professionals — and her team.", about),
    ("services.html", "Services | DV Realty",
     "Buying, selling, relocation, medical and C-suite moves, luxury rentals, corporate housing and investment properties with Danielle Vaughns, Utah luxury REALTOR®.", services),
    ("relocate.html", "Relocate to Utah | DV Realty",
     "A calm, expert-led relocation to Utah, from discovery call to keys — with specialized support for physicians and executives, plus luxury rentals and corporate housing.", relocate),
    ("communities.html", "Utah Communities | DV Realty",
     "An insider's guide to Salt Lake City, Yalecrest, Park City, Millcreek, Holladay, Cottonwood Heights, Sandy, Draper, South Jordan and Utah County.", communities),
    ("listings.html", "Utah Homes for Sale | DV Realty",
     "Curated Utah home searches and off-market access with Danielle Vaughns, Utah relocation specialist.", listings),
    ("contact.html", "Contact & Schedule a Call | DV Realty",
     "Schedule a free consultation with Danielle Vaughns, Utah REALTOR® and relocation specialist.", contact),
]

for fn, title, desc, body in PAGES:
    with open(f"{OUT}/{fn}", "w") as f:
        f.write(page(fn, title, desc, body, light_header=fn != "index.html"))
    print("wrote", fn)

# Sitemap and robots.txt so Google, Bing and AI assistants can find every page.
urls = "\n".join(f"  <url><loc>{SITE_URL}/{canonical_path(fn)}</loc></url>" for fn, *_ in PAGES)
with open(f"{OUT}/sitemap.xml", "w") as f:
    f.write(f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{urls}
</urlset>
""")
with open(f"{OUT}/robots.txt", "w") as f:
    f.write(f"""# Every search engine and AI assistant is welcome to read this site.
User-agent: *
Allow: /

Sitemap: {SITE_URL}/sitemap.xml
""")
print("wrote sitemap.xml, robots.txt")
