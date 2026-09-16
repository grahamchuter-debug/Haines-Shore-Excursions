#!/usr/bin/env python3
"""
Phase 3B: assemble clean public/ site with build-time HTML inlining.
Preserves existing content/partials; does not rewrite STRONG copy.
"""
from __future__ import annotations

import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "public"
DOMAIN = "https://hainesshoreexcursions.com"
SITE = "Haines Shore Excursions"
EMAIL = "hello@hainesshoreexcursions.com"
DATE = "2026-09-16"

# RED shared cruise-ship binary + Seward wildlife twin → verified Haines assets
IMAGE_REMAP: dict[str, tuple[str, str]] = {
    "/images/schedule.png": (
        "/images/hero-haines.png",
        "Scenic coastline near Haines, Alaska for cruise schedule planning",
    ),
    "/images/planner.png": (
        "/images/scenic-haines.png",
        "Lynn Canal scenery near Haines used for cruise day planning",
    ),
    "/images/enquire.png": (
        "/images/hero-haines.png",
        "Haines, Alaska scenery — enquire about shore excursions",
    ),
    "/images/faq.png": (
        "/images/scenic-haines.png",
        "Haines Alaska scenery for cruise excursion planning questions",
    ),
    "/images/best-time.png": (
        "/images/scenic-haines.png",
        "Seasonal scenery near Haines, Alaska",
    ),
    "/images/best-haines-excursions.png": (
        "/images/bald-eagles-haines.png",
        "Bald eagles near Haines, Alaska — top shore excursion theme",
    ),
    "/images/chilkat-preserve.png": (
        "/images/bald-eagles-haines.png",
        "Bald eagles associated with the Chilkat Bald Eagle Preserve near Haines",
    ),
    "/images/chilkoot-river.png": (
        "/images/chilkoot-lake.png",
        "Wildlife habitat near Chilkoot Lake and River, Haines Alaska",
    ),
    "/images/cultural.png": (
        "/images/scenic-haines.png",
        "Haines Alaska town and mountain setting for heritage tours",
    ),
    "/images/nature-walks.png": (
        "/images/scenic-haines.png",
        "Forest and mountain scenery near Haines for nature walks",
    ),
    "/images/photography.png": (
        "/images/bald-eagles-haines.png",
        "Bald eagles near Haines — photography tour subject",
    ),
    "/images/fort-seward.png": (
        "/images/scenic-haines.png",
        "Haines Alaska harbour and mountain scenery near Fort Seward",
    ),
    "/images/haines-cruise-port.png": (
        "/images/hero-haines.png",
        "Haines, Alaska coastal scenery near the cruise port",
    ),
    "/images/haines-wildlife.png": (
        "/images/chilkoot-lake.png",
        "Wildlife habitat at Chilkoot Lake near Haines, Alaska",
    ),
}

OK_IMAGES = {
    "hero-haines.png",
    "bald-eagles-haines.png",
    "intro.png",
    "chilkoot-lake.png",
    "eagle-closeup.png",
    "scenic-haines.png",
    "skagway-comparison.png",
    "ATTRIBUTION.md",
}

# Trailing-slash CTR title/description passes (slugs only — no renames)
CTR: dict[str, tuple[str, str]] = {
    "": (
        "Haines Shore Excursions | Bald Eagles & Cruise Port Wildlife",
        "Plan Haines shore excursions from the Portage Cove cruise pier — bald eagles, Chilkoot Lake wildlife and a quieter Alaska stop than Skagway.",
    ),
    "haines-cruise-ship-schedule": (
        "Haines Cruise Ship Schedule | Port Calls & Typical Hours",
        "When cruise ships visit Haines, Alaska: typical 6–10 hour dock calls, May–September season, and how to plan shore excursions early.",
    ),
    "haines-cruise-port-guide": (
        "Haines Cruise Port Guide | Pier, Pickup & Port Day Tips",
        "Haines cruise pier on Portage Cove — dock logistics, tour pickup, weather and how to plan 6–10 hours ashore.",
    ),
    "chilkat-bald-eagle-preserve-guide": (
        "Chilkat Bald Eagle Preserve Guide | From Haines Cruise Port",
        "Visit the Chilkat Bald Eagle Preserve from Haines — eagle viewing, river corridor tours and cruise-day timing tips.",
    ),
    "chilkoot-lake-guide": (
        "Chilkoot Lake Guide | Wildlife Near Haines Cruise Port",
        "Chilkoot Lake State Park from Haines — bears, eagles, glacier-fed scenery and typical shore excursion timing.",
    ),
    "haines-bald-eagle-guide": (
        "Haines Bald Eagle Guide | Chilkat & Cruise Season Viewing",
        "Where and when to see bald eagles from Haines — Chilkat Preserve peaks and summer cruise-call sightings.",
    ),
    "best-time-to-visit-haines": (
        "Best Time to Visit Haines | Cruise Season & Wildlife",
        "Best months to visit Haines, Alaska for cruise passengers — wildlife, weather and May–September port calls.",
    ),
    "haines-vs-skagway": (
        "Haines vs Skagway | Which Alaska Cruise Port Fits You?",
        "Haines vs Skagway for cruise passengers — wildlife and eagles versus White Pass railway and Gold Rush crowds.",
    ),
    "enquire": (
        "Enquire About Haines Shore Excursions",
        "Enquire about Haines shore excursions — share your ship, date and interests. Enquiry-only planning help, no online checkout.",
    ),
}

PAGES: list[dict] = [
    {"slug": "", "content": "home.html", "hero": "hero-home.html", "data_page": "home", "name": "Home", "trust": True},
    {"slug": "best-haines-shore-excursions", "content": "best-haines-shore-excursions.html", "hero": "hero-best.html", "data_page": "excursions", "name": "Best Excursions", "trust": True},
    {"slug": "haines-cruise-port-guide", "content": "haines-cruise-port-guide.html", "hero": "hero-port.html", "data_page": "port", "name": "Port Guide", "trust": True},
    {"slug": "things-to-do-in-haines-from-a-cruise-ship", "content": "things-to-do-in-haines-from-a-cruise-ship.html", "hero": "hero-things.html", "data_page": "port", "name": "Things To Do", "trust": True},
    {"slug": "haines-wildlife-guide", "content": "haines-wildlife-guide.html", "hero": "hero-wildlife.html", "data_page": "wildlife", "name": "Wildlife Guide", "trust": True},
    {"slug": "haines-bald-eagle-guide", "content": "haines-bald-eagle-guide.html", "hero": "hero-eagle_guide.html", "data_page": "eagles", "name": "Bald Eagle Guide", "trust": True},
    {"slug": "haines-vs-skagway", "content": "haines-vs-skagway.html", "hero": "hero-vs_skagway.html", "data_page": "port", "name": "Haines vs Skagway", "trust": True},
    {"slug": "chilkoot-lake-guide", "content": "chilkoot-lake-guide.html", "hero": "hero-chilkoot_lake.html", "data_page": "wildlife", "name": "Chilkoot Lake Guide", "trust": True},
    {"slug": "chilkat-bald-eagle-preserve-guide", "content": "chilkat-bald-eagle-preserve-guide.html", "hero": "hero-chilkat.html", "data_page": "eagles", "name": "Chilkat Preserve", "trust": True},
    {"slug": "best-time-to-visit-haines", "content": "best-time-to-visit-haines.html", "hero": "hero-best_time.html", "data_page": "port", "name": "Best Time To Visit", "trust": True},
    {"slug": "haines-cruise-ship-schedule", "content": "haines-cruise-ship-schedule.html", "hero": "hero-schedule.html", "data_page": "port", "name": "Cruise Schedule", "trust": True},
    {"slug": "haines-cruise-planner", "content": "haines-cruise-planner.html", "hero": "hero-planner.html", "data_page": "port", "name": "Cruise Planner", "trust": True},
    {"slug": "haines-faq", "content": "haines-faq.html", "hero": "hero-faq.html", "data_page": "faq", "name": "FAQ", "trust": True},
    {"slug": "enquire", "content": "enquire.html", "hero": "hero-enquire.html", "data_page": "enquire", "name": "Enquire", "trust": False},
    {"slug": "bald-eagle-viewing-tours", "content": "bald-eagle-viewing-tours.html", "hero": "hero-bald-eagle-viewing-tours.html", "data_page": "excursions", "name": "Bald Eagle Viewing", "trust": True},
    {"slug": "chilkoot-lake-wildlife-tour", "content": "chilkoot-lake-wildlife-tour.html", "hero": "hero-chilkoot-lake-wildlife-tour.html", "data_page": "excursions", "name": "Chilkoot Lake Wildlife", "trust": True},
    {"slug": "chilkoot-river-tour", "content": "chilkoot-river-tour.html", "hero": "hero-chilkoot-river-tour.html", "data_page": "excursions", "name": "Chilkoot River Tour", "trust": True},
    {"slug": "scenic-haines-tour", "content": "scenic-haines-tour.html", "hero": "hero-scenic-haines-tour.html", "data_page": "excursions", "name": "Scenic Haines Tour", "trust": True},
    {"slug": "fort-seward-tour", "content": "fort-seward-tour.html", "hero": "hero-fort-seward-tour.html", "data_page": "excursions", "name": "Fort Seward Tour", "trust": True},
    {"slug": "photography-tours", "content": "photography-tours.html", "hero": "hero-photography-tours.html", "data_page": "excursions", "name": "Photography Tours", "trust": True},
    {"slug": "cultural-heritage-tours", "content": "cultural-heritage-tours.html", "hero": "hero-cultural-heritage-tours.html", "data_page": "excursions", "name": "Cultural & Heritage", "trust": True},
    {"slug": "nature-walks", "content": "nature-walks.html", "hero": "hero-nature-walks.html", "data_page": "excursions", "name": "Nature Walks", "trust": True},
]


def slash(slug: str) -> str:
    return "/" if not slug else f"/{slug}/"


def canon(slug: str) -> str:
    return DOMAIN + ("/" if not slug else f"/{slug}/")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def remap_images(html: str) -> str:
    for old, (new, alt) in IMAGE_REMAP.items():
        if old not in html:
            continue
        # background url(...)
        html = html.replace(f"url('{old}')", f"url('{new}')")
        html = html.replace(f'url("{old}")', f'url("{new}")')
        html = html.replace(f"url({old})", f"url({new})")
        # src=
        html = html.replace(f'src="{old}"', f'src="{new}"')
        html = html.replace(f"src='{old}'", f"src='{new}'")
        # update aria-label on same hero block when old path was schedule-like misleading
        html = re.sub(
            rf'(url\([\'"]?{re.escape(new)}[\'"]?\)[^>]*)aria-label="[^"]*"',
            rf'\1aria-label="{alt}"',
            html,
            count=1,
        )
        # update nearby alt= for img tags pointing at new after remap
        html = re.sub(
            rf'(src="{re.escape(new)}"[^>]*alt=")[^"]*(")',
            rf"\1{alt}\2",
            html,
        )
        html = re.sub(
            rf'(alt=")[^"]*("[^>]*src="{re.escape(new)}")',
            rf"\1{alt}\2",
            html,
        )
    return html


def fix_internal_links(html: str) -> str:
    """Convert bare internal page links to trailing-slash form."""
    slugs = [p["slug"] for p in PAGES if p["slug"]]

    def repl(m: re.Match[str]) -> str:
        quote = m.group(1)
        path = m.group(2)
        # already slash-terminated directory or asset
        if path.startswith(("/", "http", "mailto", "#", "tel")) is False:
            return m.group(0)
        if any(path.startswith(ext) for ext in ("/images/", "/css/", "/js/", "/fonts/")):
            return m.group(0)
        if path in ("/", ""):
            return f"href={quote}/{quote}"
        # strip .html
        clean = path
        if clean.endswith(".html"):
            clean = clean[: -5]
        clean = clean.rstrip("/")
        leaf = clean.lstrip("/")
        if leaf in slugs:
            return f"href={quote}/{leaf}/{quote}"
        return m.group(0)

    return re.sub(r'href=(["\'])(/[^"\']*)\1', repl, html)


def extract_head_field(shell: str, name: str) -> str | None:
    m = re.search(
        rf'<meta[^>]+name=["\']{name}["\'][^>]+content=["\']([^"\']*)["\']',
        shell,
        re.I,
    )
    if m:
        return m.group(1)
    m = re.search(
        rf'<meta[^>]+content=["\']([^"\']*)["\'][^>]+name=["\']{name}["\']',
        shell,
        re.I,
    )
    return m.group(1) if m else None


def extract_title(shell: str) -> str:
    m = re.search(r"<title>(.*?)</title>", shell, re.I | re.S)
    return re.sub(r"\s+", " ", m.group(1)).strip() if m else SITE


def extract_og_image(shell: str) -> str:
    m = re.search(
        r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\']([^"\']+)["\']',
        shell,
        re.I,
    )
    if m:
        return m.group(1)
    m = re.search(r'<link[^>]+rel=["\']preload["\'][^>]+href=["\']([^"\']+)["\']', shell, re.I)
    return m.group(1) if m else "/images/hero-haines.png"


def extract_jsonld(shell: str) -> list[dict]:
    blocks = re.findall(
        r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>([\s\S]*?)</script>',
        shell,
        re.I,
    )
    out: list[dict] = []
    for b in blocks:
        try:
            data = json.loads(b)
            if isinstance(data, list):
                out.extend(data)
            else:
                out.append(data)
        except json.JSONDecodeError:
            pass
    return out


def organization_schema() -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": SITE,
        "url": f"{DOMAIN}/",
        "email": EMAIL,
        "description": "Independent Haines Alaska shore excursion planning guide for cruise passengers.",
        "areaServed": {"@type": "Place", "name": "Haines, Alaska"},
        "contactPoint": {
            "@type": "ContactPoint",
            "contactType": "customer enquiry",
            "email": EMAIL,
            "url": f"{DOMAIN}/enquire/",
        },
    }


def website_schema() -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": SITE,
        "url": f"{DOMAIN}/",
        "description": "Independent Haines Alaska shore excursion planning guide",
    }


def webpage_schema(title: str, description: str, slug: str) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "name": title,
        "description": description,
        "url": canon(slug),
        "isPartOf": {"@type": "WebSite", "name": SITE, "url": f"{DOMAIN}/"},
    }


def breadcrumb_schema(slug: str, name: str) -> dict:
    items = [
        {
            "@type": "ListItem",
            "position": 1,
            "name": "Home",
            "item": f"{DOMAIN}/",
        }
    ]
    if slug:
        items.append(
            {
                "@type": "ListItem",
                "position": 2,
                "name": name,
                "item": canon(slug),
            }
        )
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": items,
    }


def set_active_nav(nav: str, data_page: str) -> str:
    # mark matching data-nav
    def repl(m: re.Match[str]) -> str:
        full = m.group(0)
        nav_key = m.group(1)
        if nav_key == data_page:
            full = re.sub(
                r'class="([^"]*)"',
                r'class="\1 text-ocean-600 font-semibold"',
                full,
                count=1,
            )
            if "aria-current" not in full:
                full = full.replace(">", ' aria-current="page">', 1)
        return full

    return re.sub(
        r'<a[^>]+data-nav="([^"]+)"[^>]*>',
        repl,
        nav,
    )


def clean_enquire_hero(hero: str) -> str:
    hero = hero.replace("Book &amp; Enquire", "Enquire")
    hero = hero.replace("Book & Enquire", "Enquire")
    return hero


def assemble_page(page: dict) -> str:
    slug = page["slug"]
    shell_path = ROOT / ("index.html" if not slug else f"{slug}/index.html")
    shell = read(shell_path)

    title = extract_title(shell)
    description = extract_head_field(shell, "description") or ""
    keywords = extract_head_field(shell, "keywords") or ""
    if slug in CTR:
        title, description = CTR[slug]
    elif slug == "" and "" in CTR:
        title, description = CTR[""]

    og_image = extract_og_image(shell)
    # remap og image if RED
    for old, (new, _) in IMAGE_REMAP.items():
        if old in og_image or old.lstrip("/") in og_image:
            og_image = DOMAIN + new if new.startswith("/") else new
            if not og_image.startswith("http"):
                og_image = DOMAIN + new
            break
    if og_image.startswith("/"):
        og_image = DOMAIN + og_image

    preload = extract_og_image(shell)
    if preload.startswith("http"):
        preload = preload.replace(DOMAIN, "")
    for old, (new, _) in IMAGE_REMAP.items():
        if old in preload:
            preload = new
            break

    nav = fix_internal_links(remap_images(read(ROOT / "partials/nav.html")))
    nav = set_active_nav(nav, page["data_page"])
    footer = fix_internal_links(remap_images(read(ROOT / "partials/footer.html")))
    # ensure hello@ visible
    if EMAIL not in footer:
        footer = footer.replace(
            '<div class="border-t border-gray-800 pt-8 text-xs text-center sm:text-left">',
            f'<div class="border-t border-gray-800 pt-8 text-xs text-center sm:text-left">\n'
            f'      <p>Planning questions: <a href="mailto:{EMAIL}" class="text-white hover:underline">{EMAIL}</a>. '
            f"We reply when we can — not a 24/7 desk.</p>",
            1,
        )

    hero = fix_internal_links(remap_images(read(ROOT / "partials" / page["hero"])))
    if slug == "enquire":
        hero = clean_enquire_hero(hero)
    content = fix_internal_links(remap_images(read(ROOT / "content" / page["content"])))
    trust = ""
    if page.get("trust"):
        trust = fix_internal_links(
            remap_images(read(ROOT / "partials/trust-strip.html"))
        )

    schemas = extract_jsonld(shell)
    # Drop Product/Offer if any
    schemas = [
        s
        for s in schemas
        if s.get("@type") not in ("Product", "Offer")
        and "InStock" not in json.dumps(s)
    ]
    # Ensure core schemas
    types = {s.get("@type") for s in schemas}
    if "Organization" not in types:
        schemas.insert(0, organization_schema())
    if "WebSite" not in types:
        schemas.insert(0, website_schema())
    if "WebPage" not in types:
        schemas.append(webpage_schema(title, description, slug))
    if "BreadcrumbList" not in types:
        schemas.append(breadcrumb_schema(slug, page["name"]))
    # Fix breadcrumb/website URLs to trailing slash
    for s in schemas:
        if s.get("@type") == "WebSite":
            s["url"] = f"{DOMAIN}/"
        if s.get("@type") == "WebPage":
            s["url"] = canon(slug)
            s["name"] = title
            s["description"] = description
        if s.get("@type") == "BreadcrumbList":
            for item in s.get("itemListElement", []):
                if item.get("position") == 1:
                    item["item"] = f"{DOMAIN}/"
                elif item.get("position") == 2 and slug:
                    item["item"] = canon(slug)
                    item["name"] = page["name"]

    schema_html = "".join(
        f'  <script type="application/ld+json">\n{json.dumps(s, indent=2)}\n  </script>\n'
        for s in schemas
    )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title}</title>
  <meta name="description" content="{description}" />
  <meta name="keywords" content="{keywords}" />
  <link rel="canonical" href="{canon(slug)}" />
  <link rel="preload" as="image" href="{preload}" fetchpriority="high" />
  <meta property="og:type" content="website" />
  <meta property="og:url" content="{canon(slug)}" />
  <meta property="og:title" content="{title}" />
  <meta property="og:description" content="{description}" />
  <meta property="og:image" content="{og_image}" />
  <meta property="og:site_name" content="{SITE}" />
  <meta name="twitter:card" content="summary_large_image" />
{schema_html}  <script src="https://cdn.tailwindcss.com"></script>
  <script src="/js/tailwind-config.js"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;600;700&family=DM+Sans:wght@400;500;600;700&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="/css/site.css" />
</head>
<body class="bg-white text-gray-800 antialiased" data-page="{page["data_page"]}">
{nav}
{hero}
{trust}
<main id="page-content">
{content}
</main>
{footer}
</body>
</html>
"""


def write_404() -> None:
    nav = fix_internal_links(read(ROOT / "partials/nav.html"))
    footer = fix_internal_links(read(ROOT / "partials/footer.html"))
    if EMAIL not in footer:
        footer = footer.replace(
            '<div class="border-t border-gray-800 pt-8 text-xs text-center sm:text-left">',
            f'<div class="border-t border-gray-800 pt-8 text-xs text-center sm:text-left">\n'
            f'      <p>Planning questions: <a href="mailto:{EMAIL}" class="text-white hover:underline">{EMAIL}</a>.</p>',
            1,
        )
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Page not found | {SITE}</title>
  <meta name="robots" content="noindex,follow" />
  <meta name="description" content="This page was not found on Haines Shore Excursions." />
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="/js/tailwind-config.js"></script>
  <link rel="stylesheet" href="/css/site.css" />
  <link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;600;700&family=DM+Sans:wght@400;500;600;700&display=swap" rel="stylesheet" />
</head>
<body class="bg-white text-gray-800 antialiased">
{nav}
<main class="max-w-3xl mx-auto px-4 py-24 text-center">
  <h1 class="text-4xl font-display font-bold text-gray-900 mb-4">Page not found</h1>
  <p class="text-gray-600 mb-8">This page does not exist on Haines Shore Excursions. Try one of these guides instead.</p>
  <div class="flex flex-wrap justify-center gap-3 text-sm">
    <a href="/" class="btn-ocean text-white font-semibold px-5 py-2.5 rounded-full">Homepage</a>
    <a href="/best-haines-shore-excursions/" class="border border-slate-300 font-semibold px-5 py-2.5 rounded-full">Excursions</a>
    <a href="/haines-cruise-port-guide/" class="border border-slate-300 font-semibold px-5 py-2.5 rounded-full">Port Guide</a>
    <a href="/haines-cruise-ship-schedule/" class="border border-slate-300 font-semibold px-5 py-2.5 rounded-full">Cruise Schedule</a>
    <a href="/enquire/" class="border border-slate-300 font-semibold px-5 py-2.5 rounded-full">Enquire</a>
  </div>
  <p class="mt-10 text-sm text-gray-500">Questions: <a class="text-ocean-600 underline" href="mailto:{EMAIL}">{EMAIL}</a></p>
</main>
{footer}
</body>
</html>
"""
    (OUT / "404.html").write_text(html, encoding="utf-8")


def write_sitemap() -> None:
    urls = []
    for p in PAGES:
        loc = canon(p["slug"])
        priority = "1.0" if not p["slug"] else "0.8"
        if p["slug"] == "haines-cruise-ship-schedule":
            priority = "0.9"
        urls.append(
            f"""  <url>
    <loc>{loc}</loc>
    <lastmod>{DATE}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>{priority}</priority>
  </url>"""
        )
    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(urls)
        + "\n</urlset>\n"
    )
    (OUT / "sitemap.xml").write_text(xml, encoding="utf-8")


def write_robots() -> None:
    (OUT / "robots.txt").write_text(
        f"User-Agent: *\nAllow: /\n\nSitemap: {DOMAIN}/sitemap.xml\n",
        encoding="utf-8",
    )


def copy_assets() -> None:
    css_dst = OUT / "css"
    css_dst.mkdir(parents=True, exist_ok=True)
    shutil.copy2(ROOT / "css/site.css", css_dst / "site.css")

    js_dst = OUT / "js"
    js_dst.mkdir(parents=True, exist_ok=True)
    shutil.copy2(ROOT / "js/tailwind-config.js", js_dst / "tailwind-config.js")
    # Do NOT copy site.js — no client content fetch

    img_dst = OUT / "images"
    img_dst.mkdir(parents=True, exist_ok=True)
    for name in OK_IMAGES:
        src = ROOT / "images" / name
        if src.exists():
            shutil.copy2(src, img_dst / name)
    # Update attribution
    (img_dst / "ATTRIBUTION.md").write_text(
        "# Image attribution\n\n"
        "Verified Haines-area photography assets only. "
        "Shared multi-destination cruise-ship placeholders were removed in World 2.0 Phase 3B.\n",
        encoding="utf-8",
    )


def main() -> None:
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)

    print("Assembling Haines public/ (build-time HTML inlining)…")
    for page in PAGES:
        html = assemble_page(page)
        if page["slug"]:
            dest = OUT / page["slug"] / "index.html"
            dest.parent.mkdir(parents=True, exist_ok=True)
        else:
            dest = OUT / "index.html"
        dest.write_text(html, encoding="utf-8")
        print(f"  wrote {dest.relative_to(OUT)}")

    write_404()
    write_sitemap()
    write_robots()
    copy_assets()
    print(f"Done. Output: {OUT}")


if __name__ == "__main__":
    main()
