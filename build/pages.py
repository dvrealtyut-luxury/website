import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from shared import *
from listings import LISTINGS

# Output to the repo root by default: python3 build/pages.py
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")


def img(name, alt, sizes="(max-width: 900px) 100vw, 50vw", eager=False, w=1400, h=2100, pos=None):
    style = f' style="object-position:{pos}"' if pos else ""
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    return (f'<img src="assets/img/{name}-1400.webp" srcset="assets/img/{name}-800.webp 800w, assets/img/{name}-1400.webp 1400w" '
            f'sizes="{sizes}" width="{w}" height="{h}" alt="{alt}" {load} decoding="async"{style}>')



COMMUNITIES = [
    ("Salt Lake City", "The Avenues · Sugar House · East Bench",
     "Historic neighborhoods, a revitalized downtown and Utah's major academic medical centers — with the canyons minutes away."),
    ("Park City", "Old Town · Deer Valley · Kimball Junction",
     "World-class skiing, a storied Main Street and true mountain living, a short drive up Parley's Canyon from Salt Lake."),
    ("Heber Valley & Midway", "Midway · Heber City · Jordanelle",
     "Wide-open pastoral views, Swiss-inspired charm and room to breathe, just over the ridge from Park City."),
    ("Holladay & Cottonwood Heights", "Mature trees · Canyon access",
     "Established, gracious neighborhoods with larger lots, at the doorstep of Big and Little Cottonwood Canyons."),
    ("Draper & the South Valley", "Corner Canyon · Sandy · South Jordan",
     "Newer homes, top-rated trail systems and an easy commute in either direction along the I-15 corridor."),
    ("Lehi & Utah County", "Silicon Slopes · Provo · Orem",
     "The heart of Utah's tech corridor — new construction, young families and two major universities nearby."),
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


# --------------------------------------------------------------------------- HOME
marquee_items = "".join(f"<span>{c[0]}</span>" for c in COMMUNITIES)
community_cards = "\n".join(f"""      <a class="community reveal reveal-d{i % 3}" href="communities.html#{c[0].split(' ')[0].lower()}">
        {mountain_art(i)}
        <span class="community__idx">0{i+1}</span>
        <h3>{c[0]}</h3>
        <p>{c[2]}</p>
        <span class="tags">{c[1]}</span>
      </a>""" for i, c in enumerate(COMMUNITIES))

home = f"""<section class="hero">
  <div class="hero__copy">
    <span class="eyebrow fade-up">Utah Real Estate · Relocation Specialist</span>
    <h1 class="display">
      <span class="line-reveal"><span>Your next</span></span>
      <span class="line-reveal"><span>chapter starts</span></span>
      <span class="line-reveal"><span><em>in Utah.</em></span></span>
    </h1>
    <p class="lede fade-up">Relocating to Utah? Danielle Vaughns makes finding your home — and settling into your new community — simple, exciting and stress-free.</p>
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
    <div class="hero__meta">Salt Lake City · Park City · Heber</div>
  </div>
</section>

<div class="marquee" aria-hidden="true"><div class="marquee__track">{marquee_items}{marquee_items}{marquee_items}{marquee_items}</div></div>

{featured_section(limit=2, sand=True)}

<section class="section">
  <div class="wrap">
    <div class="split">
      <div class="frame reveal">
        <div class="frame__img mask">{img("danielle-smile", "Danielle Vaughns smiling, resting her chin on her hand at a kitchen table", sizes="(max-width: 900px) 100vw, 45vw")}</div>
        <div class="frame__tag"><small>KW Utah</small><strong>#8 Individual Producer</strong></div>
      </div>
      <div>
        <span class="eyebrow reveal">Meet your agent</span>
        <h2 class="h2 reveal reveal-d1">A personal guide for <em>one of life's biggest moves.</em></h2>
        <p class="lede reveal reveal-d2">With deep roots in Utah and years of experience guiding families through relocation, Danielle brings local expertise and genuine care to every client relationship. Whether you're moving across the country or across the valley, she makes the journey feel effortless.</p>
        <ul class="checklist reveal reveal-d3">
          <li>Licensed Utah REALTOR®</li>
          <li>{LUXURY} · Luxury Market Center Liaison</li>
          <li>Member, Park City Board of Realtors®</li>
          <li>Medical Professional Relocation Specialist</li>
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
    <div class="reveal" style="margin-top:64px"><a class="link-arrow" href="relocate.html">Start your Utah journey {ARROW}</a></div>
  </div>
</section>

<section class="feature on-dark" id="medical">
  <div class="feature__media mask">
    {img("danielle-desk-blazer", "Danielle Vaughns at her desk in a navy blazer, looking out the window", sizes="(max-width: 900px) 100vw, 45vw", pos="50% 35%")}
  </div>
  <div class="feature__copy">
    <span class="eyebrow reveal">For medical professionals</span>
    <h2 class="h2 reveal reveal-d1">Your schedule is demanding. <em>Your move shouldn't be.</em></h2>
    <p class="lede reveal reveal-d2">Danielle specializes in helping physicians, residents and medical professionals relocate to Utah — on a real timeline, with as little of your time as possible.</p>
    <ul class="feature__list reveal reveal-d3">
      <li><b>i.</b>Introductions to lenders who understand physician loans</li>
      <li><b>ii.</b>Neighborhoods mapped to your hospital commute</li>
      <li><b>iii.</b>Rent-first or buy-now strategies around your start date</li>
      <li><b>iv.</b>Personalized area tours — in person or virtual</li>
    </ul>
    <div class="reveal reveal-d4"><a class="btn btn--gold" href="relocate.html#medical">Relocating for Medicine {ARROW}</a></div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head section-head--split">
      <div>
        <span class="eyebrow reveal">Utah communities</span>
        <h2 class="h2 reveal reveal-d1">Find the place your family <em>will thrive.</em></h2>
      </div>
      <p class="lede reveal reveal-d2">From the energy of Salt Lake City to the mountain calm of Park City, Heber and Midway — Danielle knows the commutes, the schools and the little details that make each community feel like home.</p>
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
        <div class="frame__tag"><small>Serving</small><strong>All of Utah</strong></div>
      </div>
      <div>
        <span class="eyebrow reveal">A personal welcome</span>
        <h2 class="h2 reveal reveal-d1">Your move to Utah deserves <em>an expert by your side.</em></h2>
        <p class="lede reveal reveal-d2">Welcome — I'm so glad you're here. Whether you're relocating from across the country or searching for your forever home right here in Utah, I want you to know this journey matters to me.</p>
        <p class="reveal reveal-d2">I specialize in helping medical professionals and their families make the move to Utah. I know your schedule is demanding and your timeline is real, so I make the process as simple and stress-free as possible — from personalized area tours to connecting you with lenders who understand physician loans.</p>
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

<section class="section section--sand">
  <div class="wrap">
    <div class="section-head center">
      <span class="eyebrow eyebrow--center reveal">Qualifications</span>
      <h2 class="h2 reveal reveal-d1">Credentials &amp; <em>designations</em></h2>
    </div>
    <div class="creds">
      <div class="cred reveal">{ICON['badge']}<strong>Licensed Utah REALTOR®</strong></div>
      <div class="cred reveal reveal-d1">{ICON['star']}<strong>KW Utah #8 Individual Producer</strong></div>
      <div class="cred reveal reveal-d2">{ICON['cross']}<strong>Medical Professional Relocation Specialist</strong></div>
      <div class="cred reveal">{ICON['diamond']}<strong>{LUXURY} Agent &amp; Luxury Market Center Liaison</strong></div>
      <div class="cred reveal reveal-d1">{ICON['mountain']}<strong>Member, Park City Board of Realtors®</strong></div>
      <div class="cred reveal reveal-d2">{ICON['key']}<strong>Buyer &amp; Seller Representation</strong></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="split">
      <div class="frame reveal">
        <div class="frame__img mask">{img("danielle-book", "Danielle Vaughns holding a book beside a round mirror in a bright home", sizes="(max-width: 900px) 100vw, 45vw")}</div>
        <div class="frame__tag"><small>Experience</small><strong>Utah Expert</strong></div>
      </div>
      <div>
        <span class="eyebrow reveal">Local expertise</span>
        <h2 class="h2 reveal reveal-d1">Deep roots in Utah's <em>most sought-after communities.</em></h2>
        <p class="lede reveal reveal-d2">From the vibrant energy of Salt Lake City to the mountain charm of Park City, Heber and Midway, I know Utah's most desirable communities inside and out — the commutes to major hospitals, the schools, the lifestyle, and the little details that make each area feel like home.</p>
        <ul class="checklist checklist--cols reveal reveal-d3">
          <li>Salt Lake City &amp; surrounding areas</li>
          <li>Park City &amp; Summit County</li>
          <li>Heber Valley &amp; Midway</li>
          <li>Holladay &amp; Cottonwood Heights</li>
          <li>Physician loan guidance</li>
          <li>Rent-first or buy options</li>
          <li>Luxury &amp; move-up properties</li>
          <li>First-time homebuyers</li>
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
      <div class="value reveal reveal-d1"><h3>Local Expertise</h3><p>Utah is my home. I know the neighborhoods, the schools, the commutes, and the hidden gems that make each community unique.</p></div>
      <div class="value reveal reveal-d2"><h3>White-Glove Service</h3><p>From your first call to closing day and beyond, a concierge-level experience tailored to your life and your timeline.</p></div>
    </div>
  </div>
</section>

{cta(title="Let's find your <em>Utah home.</em>", lede="Luxury service. Lasting relationships. Whether you're relocating from out of state or searching locally, let's start with a conversation.")}"""

# --------------------------------------------------------------------------- RELOCATE
STEPS = [
    ("Discovery call", "We talk through your move — timeline, budget, commute, schools, lifestyle — and what home needs to feel like for your family."),
    ("Your Utah shortlist", "Danielle narrows the map to the communities that fit, with honest notes on the trade-offs of each one."),
    ("Tour — in person or virtual", "A personalized area tour when you're in town, or live video walkthroughs of homes and neighborhoods when you can't be."),
    ("Financing &amp; strategy", "Introductions to trusted lenders, including those who understand physician loans, plus a clear plan for renting first or buying now."),
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
    <span class="eyebrow reveal">Medical professional relocation</span>
    <h2 class="h2 reveal reveal-d1">Built around <em>your start date.</em></h2>
    <p class="lede reveal reveal-d2">Residency match, a new attending role, a fellowship — medical moves come with fixed dates and very little free time. Danielle specializes in exactly this.</p>
    <ul class="feature__list reveal reveal-d3">
      <li><b>i.</b>Neighborhoods mapped to your hospital and call-schedule commute</li>
      <li><b>ii.</b>Introductions to lenders experienced with physician loan programs</li>
      <li><b>iii.</b>Rent-first options when buying before you arrive doesn't make sense</li>
      <li><b>iv.</b>Virtual tours and remote signing so you can buy from anywhere</li>
    </ul>
    <div class="reveal reveal-d4"><a class="btn btn--gold" href="contact.html#schedule">Plan Your Move {ARROW}</a></div>
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
    ("holladay", "Holladay &amp; Cottonwood Heights", "Mature trees · Larger lots · Canyon access",
     "Gracious, established neighborhoods on Salt Lake's east side. Holladay is known for mature landscaping and larger lots; Cottonwood Heights sits at the mouths of Big and Little Cottonwood Canyons.",
     [("Lifestyle", "Quiet streets, a village-style city center and easy freeway access"),
      ("Outdoors", "Brighton, Solitude, Alta and Snowbird up the Cottonwood canyons"),
      ("Good to know", "Convenient to Intermountain Medical Center in Murray")]),
    ("park", "Park City &amp; Summit County", "Old Town · Deer Valley · Kimball Junction · Jeremy Ranch",
     "A historic mining town turned world-class mountain resort. Park City offers two major ski areas, a lively Main Street and year-round trails, a short drive from Salt Lake via Parley's Canyon.",
     [("Lifestyle", "Main Street dining, galleries and a true four-season mountain town"),
      ("Outdoors", "Deer Valley and Park City Mountain, plus hundreds of miles of trails"),
      ("Good to know", "Roughly 35–45 minutes to Salt Lake City International, depending on traffic")]),
    ("heber", "Heber Valley &amp; Midway", "Midway · Heber City · Jordanelle",
     "Wide pastoral valleys framed by the Wasatch. Midway is known for its Swiss-inspired character, while Heber City offers more space and newer neighborhoods — just over the ridge from Park City.",
     [("Lifestyle", "Small-town pace, open views and a growing local dining scene"),
      ("Outdoors", "Jordanelle and Deer Creek reservoirs, Soldier Hollow and Wasatch Mountain State Park"),
      ("Good to know", "About 20 minutes to Park City; under an hour to Salt Lake in most conditions")]),
    ("draper", "Draper &amp; the South Valley", "Draper · Sandy · South Jordan",
     "Newer homes, strong amenities and some of the valley's best trail systems, with an easy commute north to Salt Lake or south to Utah County.",
     [("Lifestyle", "Family-friendly neighborhoods, newer construction and shopping close by"),
      ("Outdoors", "Corner Canyon's trail network and quick access to the Cottonwood canyons"),
      ("Good to know", "Central to both Salt Lake and Utah County employers")]),
    ("lehi", "Lehi &amp; Utah County", "Silicon Slopes · Provo · Orem",
     "The heart of Utah's tech corridor. Lehi and its neighbors offer abundant new construction and a younger community, with BYU and Utah Valley University to the south.",
     [("Lifestyle", "Thanksgiving Point, new town centers and a fast-growing restaurant scene"),
      ("Outdoors", "American Fork Canyon, Utah Lake and Provo Canyon nearby"),
      ("Good to know", "Home to Intermountain Primary Children's Hospital's Lehi campus")]),
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
    <p class="lede fade-up">Handpicked properties across Utah's most sought-after communities — from Salt Lake City to Park City, Heber Valley to Cottonwood Heights.</p>
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
          <div><dt>Based in</dt><dd>Salt Lake City, Utah<br>Serving all of Utah</dd></div>
          <div><dt>Brokerage</dt><dd>{BROKERAGE}<br>{LUXURY}</dd></div>
        </dl>
      </div>

      <div class="scheduler reveal reveal-d1">
        <span class="eyebrow">Free 30-minute consultation</span>
        <h2 class="h2">Book a time</h2>
        <p>Choose a time that works for you. Danielle will call to talk through your move — timeline, neighborhoods, financing and next steps.</p>
        <div class="calendly-inline-widget" data-url="{CALENDLY}?hide_gdpr_banner=1&amp;background_color=ffffff&amp;text_color=1b1222&amp;primary_color=b8924f"></div>
        <p class="scheduler__alt">Calendar not loading? <a href="{CALENDLY}" target="_blank" rel="noopener">Open the scheduler in a new tab ↗</a></p>
      </div>
    </div>
  </div>
</section>
<script src="https://assets.calendly.com/assets/external/widget.js" async></script>

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
          <fieldset class="field field--full">
            <legend>I'm interested in</legend>
            <div class="chips">
              <label class="chip"><input type="checkbox" name="interest" value="Buying"><span>Buying</span></label>
              <label class="chip"><input type="checkbox" name="interest" value="Selling"><span>Selling</span></label>
              <label class="chip"><input type="checkbox" name="interest" value="Relocating"><span>Relocating</span></label>
              <label class="chip"><input type="checkbox" name="interest" value="Medical professional relocation"><span>Medical relocation</span></label>
              <label class="chip"><input type="checkbox" name="interest" value="Renting first"><span>Renting first</span></label>
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
    ("index.html", "Danielle Vaughns | Utah Relocation Specialist · DV Realty",
     "Relocating to Utah? Danielle Vaughns is a Utah REALTOR® and relocation specialist helping families and medical professionals find home in Salt Lake City, Park City, Heber and beyond.", home),
    ("about.html", "About Danielle Vaughns | DV Realty",
     "Meet Danielle Vaughns — Utah REALTOR®, KW Utah #8 Individual Producer and medical professional relocation specialist.", about),
    ("relocate.html", "Relocate to Utah | DV Realty",
     "A calm, expert-led relocation to Utah, from discovery call to keys — including specialized support for physicians and medical professionals.", relocate),
    ("communities.html", "Utah Communities | DV Realty",
     "An insider's guide to Salt Lake City, Park City, Heber Valley & Midway, Holladay, Cottonwood Heights, Draper and Lehi.", communities),
    ("listings.html", "Utah Homes for Sale | DV Realty",
     "Curated Utah home searches and off-market access with Danielle Vaughns, Utah relocation specialist.", listings),
    ("contact.html", "Contact & Schedule a Call | DV Realty",
     "Schedule a free consultation with Danielle Vaughns, Utah REALTOR® and relocation specialist.", contact),
]

for fn, title, desc, body in PAGES:
    with open(f"{OUT}/{fn}", "w") as f:
        f.write(page(fn, title, desc, body, light_header=fn != "index.html"))
    print("wrote", fn)
