# DV Realty — Danielle Vaughns

Website for Danielle Vaughns, Utah REALTOR® and relocation specialist.

Plain HTML, CSS and JavaScript — no build step, no framework. Open `index.html` in a browser, or serve the folder locally:

```bash
python3 -m http.server 8000
```

then visit http://localhost:8000.

## Pages

| File | Page |
| --- | --- |
| `index.html` | Home |
| `about.html` | About Danielle |
| `relocate.html` | Relocation process & medical professionals |
| `communities.html` | Utah community guide |
| `listings.html` | Curated search / off-market access (ready for real listings) |
| `contact.html` | Contact & consultation request form |

Shared styles live in `assets/css/style.css` and shared behavior in `assets/js/main.js`.

The HTML pages are generated from `build/` so the header, footer and contact details stay identical everywhere:

- `build/shared.py` — phone, email, brokerage, Calendly and KW links, header, footer
- `build/pages.py` — page content
- `build/listings.py` — featured listings

After editing any of these, regenerate the pages from the repo root:

```bash
python3 build/pages.py
```

## Before going live — checklist

- [x] **Phone number** — (801) 678-0444.
- [x] **Email** — dvrealtyut@gmail.com.
- [x] **Brokerage name** — KW Utah Realtors Keller Williams (footer and contact page).
- [ ] **Contact form** — by default it opens the visitor's email app. To receive submissions directly, create a free form at a service such as Formspree and add `data-endpoint="https://formspree.io/f/XXXX"` to the `<form>` in `contact.html`.
- [ ] **Social links** — add real profile URLs (none are included yet).
- [ ] **Testimonials** — add real client reviews (with permission) when available.
- [x] **Scheduling** — Calendly (calendly.com/dvrealtyut/30min) embedded on the contact page (`#schedule`).
- [x] **Listings search** — "Search All Utah Homes" links to daniellevaughns.kw.com.
- [ ] **Featured listings** — add Danielle's listings in `build/listings.py`.

## Photos

Photos of Danielle live in `assets/img/` as WebP at two widths (800 and 1400px). Originals (DSC_*.jpg, ~20 MB each) are kept in Google Drive, not in this repo — they're too large to serve on a website. To add a new photo, ask Claude to optimize it, or export it as WebP at 800px and 1400px wide.

`og-image.jpg` (1200×630) is the preview image shown when the site is shared on social media or in texts.

## Hosting

Hosted on Vercel (config in `vercel.json`: clean URLs such as `/about`, asset caching). Every push to `main` redeploys the live site automatically; other branches get preview links.
