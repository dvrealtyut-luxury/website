# Featured listings shown on the Listings page (all) and the Home page (first 2).
# Leave the list empty to hide the Featured section entirely.
#
# To add a listing:
#   1. Save a landscape photo (ideally 1600px wide or more) into assets/img/listings/
#      and convert it to .webp — or ask Claude to do it.
#   2. Copy the example below into LISTINGS and fill it in.
#   3. Regenerate the pages from the repo root:  python3 build/pages.py
#
# Example:
# {
#     "status": "For Sale",            # e.g. For Sale, New Listing, Under Contract, Sold
#     "price": "$1,250,000",
#     "address": "123 Example Dr",
#     "city": "Park City, UT 84060",
#     "beds": 4,
#     "baths": 3.5,
#     "sqft": "3,800",
#     "image": "assets/img/listings/123-example-dr.webp",
#     "description": "One or two sentences about the home.",
#     "link": "https://daniellevaughns.kw.com/...",   # the listing's page on her KW site
# },

LISTINGS = [
]
