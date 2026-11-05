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
    {
        "status": "For Sale",
        "price": "$1,475,000",
        "address": "7450 S Enchanted Hills Dr",
        "city": "Cottonwood Heights, UT 84121",
        "beds": 5,
        "baths": 3,
        "sqft": "3,486",
        "image": "assets/img/listings/7450-s-enchanted-hills-dr.webp",
        "description": "A beautifully updated home in a secluded Cottonwood Heights neighborhood, with vaulted ceilings, two fireplaces, newly refinished hardwood floors and a remodeled primary bath. Outside, an oversized deck with unobstructed valley views overlooks a pool and a dedicated garden area.",
        "link": "https://www.zillow.com/homedetails/7450-S-Enchanted-Hills-Dr-Cottonwood-Heights-UT-84121/12875572_zpid/",
    },
    {
        "status": "For Sale",
        "price": "$1,399,000",
        "address": "1528 E Harvard Ave",
        "city": "Salt Lake City, UT 84105",
        "beds": 4,
        "baths": 3,
        "sqft": "2,914",
        "image": "assets/img/listings/1528-e-harvard-ave.webp",
        "description": "A fully renovated 1915 bungalow on one of Yalecrest's most distinguished tree-lined streets, with a Thermador kitchen, waterfall quartz countertops and a light-filled main-floor primary suite. Minutes to downtown SLC, the University of Utah, 15th & 15th and 9th & 9th.",
        "link": "https://daniellevaughns.kw.com/property/1528-E-HARVARD-AVE-Salt-Lake-City-UT-84105/2137842695522850",
    },
]
