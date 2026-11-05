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
The header and footer are repeated in each page — update all six when changing them.

## Before going live — checklist

- [x] **Phone number** — (801) 678-0444.
- [ ] **Email** — confirm `danielle@daniellevaughns.com` is a working inbox.
- [x] **Brokerage name** — KW Utah Realtors Keller Williams (footer and contact page).
- [ ] **Contact form** — by default it opens the visitor's email app. To receive submissions directly, create a free form at a service such as Formspree and add `data-endpoint="https://formspree.io/f/XXXX"` to the `<form>` in `contact.html`.
- [ ] **Social links** — add real profile URLs (none are included yet).
- [ ] **Testimonials** — add real client reviews (with permission) when available.
- [ ] **Scheduling** — embed Danielle's Calendly on the contact page.
- [ ] **Listings** — add real listings, or connect an IDX/MLS provider.

## Hosting

Hosted on Vercel (config in `vercel.json`: clean URLs such as `/about`, asset caching). Every push to `main` redeploys the live site automatically; other branches get preview links.
