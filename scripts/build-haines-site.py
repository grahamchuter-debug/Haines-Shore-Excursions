#!/usr/bin/env python3
"""Generate Haines Shore Excursions static site with clean URLs."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOMAIN = "https://hainesshoreexcursions.com"
SITE = "Haines Shore Excursions"
DATE = "2026-06-24"
FONTS = (
    "https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;600;700"
    "&family=DM+Sans:wght@400;500;600;700&display=swap"
)
HERO_GRADIENT = (
    "linear-gradient(135deg, rgba(12, 74, 110, 0.75) 0%, "
    "rgba(22, 101, 52, 0.65) 50%, rgba(20, 83, 45, 0.55) 100%)"
)
ACCENT = "text-teal-400"

IMG = {
    "home": ("images/hero-haines.png", "Bald eagle landing at the Chilkat Bald Eagle Preserve near Haines Alaska"),
    "best": ("images/best-haines-excursions.png", "Best Haines shore excursions for Alaska cruise passengers"),
    "port": ("images/haines-cruise-port.png", "Haines Alaska cruise port and ferry dock on Lynn Canal"),
    "wildlife": ("images/haines-wildlife.png", "Whale watching and wildlife viewing near Haines Alaska"),
    "eagles": ("images/bald-eagles-haines.png", "Two bald eagles fighting over salmon on a snowy riverbank at the Chilkat Bald Eagle Preserve, Haines Alaska"),
    "eagle_close": ("images/eagle-closeup.png", "Bald eagle perched in southeast Alaska near Haines"),
    "chilkoot_lake": ("images/chilkoot-lake.png", "Brown bear carrying a salmon at Chilkoot Lake State Park near Haines Alaska"),
    "chilkat": ("images/chilkat-preserve.png", "Chilkat Bald Eagle Preserve river valley near Haines"),
    "scenic": ("images/scenic-haines.png", "Calm Alaskan fjord near Haines with snow-capped mountains and evergreen forests framed by tree branches"),
    "fort_seward": ("images/fort-seward.png", "Historic Fort William H Seward in Haines Alaska"),
    "photography": ("images/photography.png", "Nature photography tour in the Chilkat Valley Haines"),
    "cultural": ("images/cultural.png", "Cultural and heritage experiences in Haines Alaska"),
    "nature": ("images/nature-walks.png", "Guided nature walk in the forests near Haines Alaska"),
    "chilkoot_river": ("images/chilkoot-river.png", "Chilkoot River salmon run and wildlife viewing Haines"),
    "skagway": ("images/skagway-comparison.png", "Skagway Alaska cruise port compared with Haines"),
    "intro": ("images/intro.png", "Two bald eagles in mid-air confrontation on a snowy riverbank near Haines Alaska"),
    "faq": ("images/faq.png", "Cruise passengers planning Haines shore excursions"),
    "planner": ("images/planner.png", "Haines Alaska cruise day planner for shore excursions"),
    "enquire": ("images/enquire.png", "Enquire about Haines shore excursions for cruise passengers"),
    "schedule": ("images/schedule.png", "Haines Alaska cruise ship schedule and port calls"),
    "best_time": ("images/best-time.png", "Best time to visit Haines Alaska for wildlife and bald eagles"),
    "things": ("images/intro.png", "Things to do in Haines from a cruise ship"),
}


def u(slug: str = "") -> str:
    return "/" if not slug else f"/{slug}"


def write(path: str, content: str) -> None:
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")
    print(f"  wrote {path}")


def breadcrumb_schema(slug: str, name: str) -> dict:
    items = [{"@type": "ListItem", "position": 1, "name": "Home", "item": f"{DOMAIN}/"}]
    if slug:
        items.append({"@type": "ListItem", "position": 2, "name": name, "item": f"{DOMAIN}/{slug}"})
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": items}


def faq_schema(qa: list[tuple[str, str]]) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in qa
        ],
    }


def page_shell(
    *,
    title: str,
    description: str,
    keywords: str,
    slug: str,
    data_page: str,
    hero: str,
    content: str,
    preload: str,
    schema: dict | None = None,
    trust: bool = True,
) -> str:
    canon = f"{DOMAIN}/" if not slug else f"{DOMAIN}/{slug}"
    schema_block = ""
    if schema:
        schema_block = f'  <script type="application/ld+json">\n{json.dumps(schema, indent=2)}\n  </script>\n'
    trust_attr = '\n  data-trust-strip="/partials/trust-strip.html"' if trust else ""
    content_file = content if content.startswith("/content/") else f"/content/{content}"
    hero_path = hero if hero.startswith("/") else f"/{hero}"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title}</title>
  <meta name="description" content="{description}" />
  <meta name="keywords" content="{keywords}" />
  <link rel="canonical" href="{canon}" />
  <link rel="preload" as="image" href="/{preload}" fetchpriority="high" />
  <meta property="og:type" content="website" />
  <meta property="og:url" content="{canon}" />
  <meta property="og:title" content="{title}" />
  <meta property="og:description" content="{description}" />
  <meta property="og:image" content="{DOMAIN}/{preload}" />
  <meta property="og:site_name" content="{SITE}" />
  <meta name="twitter:card" content="summary_large_image" />
{schema_block}  <script src="https://cdn.tailwindcss.com"></script>
  <script src="/js/tailwind-config.js"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="{FONTS}" rel="stylesheet" />
  <link rel="stylesheet" href="/css/site.css" />
</head>
<body class="bg-white text-gray-800 antialiased" data-page="{data_page}" data-hero="{hero_path}" data-content="{content_file}"{trust_attr}>
  <div id="site-nav"></div>
  <div id="page-hero"></div>
  <div id="page-trust-strip"></div>
  <main id="page-content"></main>
  <div id="site-footer"></div>
  <script src="/js/site.js"></script>
</body>
</html>
"""


def write_page(slug: str, html: str) -> None:
    path = "index.html" if not slug else f"{slug}/index.html"
    write(path, html)


def _wave() -> str:
    return '<div class="absolute bottom-0 left-0 right-0"><svg viewBox="0 0 1440 48" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="none" class="site-hero__wave" aria-hidden="true"><path d="M0 24 C360 48 1080 0 1440 24 L1440 48 L0 48 Z" fill="white"/></svg></div>'


def hero(
    eyebrow: str,
    title: str,
    lead: str,
    image_key: str,
    breadcrumb: str = "",
    cta: tuple[str, str] | None = None,
    tags: list[str] | None = None,
) -> str:
    image, aria = IMG[image_key]
    bc = ""
    if breadcrumb:
        bc = f"""<nav class="site-hero__breadcrumb flex items-center gap-2 mb-4 text-xs text-white/60" aria-label="Breadcrumb">
        <a href="/" class="hover:text-white transition-colors">Home</a>
        <svg class="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>
        <span class="text-white/80">{breadcrumb}</span>
      </nav>"""
    cta_html = f'<a href="{u(cta[0])}" class="btn-ocean inline-flex items-center justify-center gap-2 text-white font-semibold px-7 py-3 rounded-full text-sm shadow-xl">{cta[1]}</a>' if cta else ""
    tags_html = ""
    if tags:
        tags_html = '<div class="site-hero__tags flex flex-wrap gap-2 mt-5 pt-4 border-t border-white/20">' + "".join(
            f'<span class="inline-flex items-center bg-white/10 border border-white/25 rounded-full px-3.5 py-1.5 text-xs font-semibold text-white">{t}</span>'
            for t in tags
        ) + "</div>"
    return f"""<section class="site-hero">
  <div class="absolute inset-0 hero-bg-custom" style="background-image: {HERO_GRADIENT}, url('/{image}');" role="img" aria-label="{aria}"></div>
  <div class="site-hero__inner max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
    <div class="max-w-3xl">{bc}
      <div class="site-hero__eyebrow inline-flex items-center gap-2 bg-white/15 backdrop-blur-sm border border-white/30 rounded-full px-4 py-1.5 mb-3">
        <span class="w-2 h-2 rounded-full bg-teal-400 animate-pulse"></span>
        <span class="text-white/90 text-xs font-semibold tracking-widest uppercase">{eyebrow}</span>
      </div>
      <h1 class="site-hero__title text-4xl sm:text-5xl lg:text-[3.25rem] font-display font-bold text-white leading-tight mb-3">{title}</h1>
      <p class="site-hero__lead text-base sm:text-lg text-white/85 font-light leading-relaxed mb-5 max-w-2xl">{lead}</p>
      <div class="site-hero__actions flex flex-col sm:flex-row gap-3">{cta_html}</div>
      {tags_html}
    </div>
  </div>
  {_wave()}
</section>"""


def internal_links() -> str:
    links = [
        ("haines-cruise-port-guide", "Port Guide"),
        ("best-haines-shore-excursions", "Best Excursions"),
        ("haines-wildlife-guide", "Wildlife Guide"),
        ("haines-bald-eagle-guide", "Bald Eagle Guide"),
        ("things-to-do-in-haines-from-a-cruise-ship", "Things To Do"),
        ("haines-vs-skagway", "Haines vs Skagway"),
        ("haines-faq", "FAQ"),
        ("enquire", "Enquire"),
    ]
    parts = []
    for i, (slug, label) in enumerate(links):
        if i:
            parts.append('<span class="text-gray-300">·</span>')
        parts.append(f'<a href="{u(slug)}" class="text-ocean-600 hover:text-ocean-800 font-medium">{label}</a>')
    return f"""<nav class="mt-10 pt-8 border-t border-gray-100" aria-label="Related Haines guides">
  <p class="text-sm font-semibold text-gray-900 mb-3">Plan your Haines port day</p>
  <div class="flex flex-wrap gap-3 text-sm">{"".join(parts)}</div>
</nav>"""


def help_cta() -> str:
    return f"""<div class="text-center mt-8 p-6 bg-alpine-50 rounded-2xl border border-alpine-100">
  <p class="text-gray-700 font-medium mb-3">Need help choosing the right Haines excursion?</p>
  <a href="{u('enquire')}" class="btn-ocean inline-flex items-center justify-center text-white text-sm font-semibold px-6 py-3 rounded-full">Get personalised advice →</a>
</div>"""


def commercial_strip(
    best_for: str,
    wildlife: str,
    return_ship: str,
) -> str:
    return f"""<aside class="commercial-strip" aria-label="Cruise passenger highlights">
  <h3>Why cruise passengers choose this</h3>
  <ul>
    <li><strong>Best for cruise passengers:</strong> {best_for}</li>
    <li><strong>Wildlife opportunities:</strong> {wildlife}</li>
    <li><strong>Return-to-ship timing:</strong> {return_ship}</li>
  </ul>
  {help_cta()}
</aside>"""


def cruise_snapshot(**kw: str) -> str:
    defaults = dict(
        time_in_port="6–10 hours (typical Haines call)",
        best_for="Wildlife, eagles, scenic wilderness",
        activity_level="Varies by tour",
        family="Good with age-appropriate tour choice",
        return_ship="Operators plan 60–90 min pier buffer",
        popular="Eagle viewing, Chilkoot Lake, river tours",
    )
    defaults.update(kw)
    rows = "".join(
        f'<div class="cruise-snapshot__item"><dt>{k}</dt><dd>{v}</dd></div>'
        for k, v in [
            ("Typical Time In Port", defaults["time_in_port"]),
            ("Best For", defaults["best_for"]),
            ("Activity Level", defaults["activity_level"]),
            ("Family Friendly", defaults["family"]),
            ("Return To Ship Friendly", defaults["return_ship"]),
            ("Popular Excursion Types", defaults["popular"]),
        ]
    )
    return f"""<aside class="cruise-snapshot mb-10 px-4 sm:px-0" aria-label="Cruise passenger snapshot">
  <h3 class="font-display font-bold text-lg text-gray-900 mb-4">Cruise Passenger Snapshot</h3>
  <dl class="cruise-snapshot__grid">{rows}</dl>
</aside>"""


def excursion_meta(
    duration: str,
    fitness: str,
    wildlife: str,
    photography: str,
    best_for: str,
    return_ship: str,
) -> str:
    cards = [
        ("Duration", duration),
        ("Fitness Level", fitness),
        ("Wildlife Opportunities", wildlife),
        ("Photography Opportunities", photography),
        ("Best For", best_for),
        ("Return-To-Ship Confidence", return_ship),
    ]
    body = "".join(
        f'<div class="excursion-meta__card"><h4>{h}</h4><p>{p}</p></div>' for h, p in cards
    )
    return f'<div class="excursion-meta max-w-5xl mx-auto px-4">{body}</div>'


def faq_block(items: list[tuple[str, str]]) -> str:
  body = "".join(
      f'<details class="faq-item rounded-2xl border border-alpine-100 p-5"><summary class="font-semibold text-gray-900 cursor-pointer">{q}</summary><p class="mt-4 text-sm text-gray-500">{a}</p></details>'
      for q, a in items
  )
  return f'<section class="py-8"><div class="max-w-3xl mx-auto px-4 space-y-4"><h2 class="text-2xl font-display font-bold text-gray-900 mb-6">Frequently Asked Questions</h2>{body}</div></section>'


def card_grid(cards: list[tuple[str, str, str, str, str, str]]) -> str:
    items = []
    for img_key, title, desc, slug, label in [(c[0], c[1], c[2], c[3], c[4]) for c in cards]:
        img, alt = IMG[img_key]
        items.append(f"""<div class="card-hover bg-white rounded-3xl overflow-hidden shadow-md border border-alpine-50 flex flex-col">
      <div class="card-media h-44 relative overflow-hidden"><img src="/{img}" alt="{alt}" width="600" height="352" loading="lazy" decoding="async" /></div>
      <div class="p-6 flex flex-col flex-1">
        <h3 class="text-lg font-display font-semibold text-gray-900 mb-2">{title}</h3>
        <p class="text-sm text-gray-500 leading-relaxed flex-1">{desc}</p>
        <a href="{u(slug)}" class="mt-5 btn-ocean inline-flex items-center justify-center text-white text-xs font-semibold px-5 py-2.5 rounded-full">{label}</a>
      </div>
    </div>""")
    return '<div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-6">' + "".join(items) + "</div>"


def comparison_table() -> str:
    rows = [
        ("Bald Eagle Viewing", "2.5–4 hrs", "Eagle enthusiasts", "Easy to moderate", "bald-eagle-viewing-tours"),
        ("Chilkoot Lake Wildlife", "2.5–4 hrs", "Bears, eagles, lake scenery", "Easy to moderate", "chilkoot-lake-wildlife-tour"),
        ("Chilkoot River Tour", "2.5–3 hrs", "Salmon runs &amp; bears", "Easy", "chilkoot-river-tour"),
        ("Scenic Haines Tour", "3–4 hrs", "Mountains &amp; Lynn Canal", "Easy", "scenic-haines-tour"),
        ("Fort Seward Tour", "2–3 hrs", "History &amp; culture", "Easy", "fort-seward-tour"),
        ("Photography Tours", "4 hrs", "Eagles, bears, landscapes", "Moderate", "photography-tours"),
        ("Cultural &amp; Heritage", "2–3 hrs", "Tlingit &amp; army history", "Easy", "cultural-heritage-tours"),
        ("Nature Walks", "2–3 hrs", "Forest mindfulness", "Easy", "nature-walks"),
    ]
    body = "".join(
        f"""<tr class="border-b border-alpine-50 hover:bg-sand-50/80">
      <td class="py-4 pr-4 font-semibold text-gray-900"><a href="{u(link)}" class="text-ocean-600 hover:text-ocean-800">{name}</a></td>
      <td class="py-4 px-3 text-gray-600">{dur}</td>
      <td class="py-4 px-3 text-gray-600">{best}</td>
      <td class="py-4 px-3 text-gray-600">{act}</td>
      <td class="py-4 pl-3"><a href="{u(link)}" class="text-teal-600 font-medium text-xs whitespace-nowrap">Guide →</a></td>
    </tr>"""
        for name, dur, best, act, link in rows
    )
    return f"""<section class="py-16 bg-sand-50"><div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
  <h2 class="text-3xl sm:text-4xl font-display font-bold text-gray-900 text-center mb-4">Which Haines Excursion Is Right for Me?</h2>
  <p class="text-center text-gray-600 text-sm max-w-2xl mx-auto mb-10">Match your port day to eagles, Chilkoot Lake wildlife, river viewing or Fort Seward — all timed for typical Alaska cruise schedules.</p>
  <div class="overflow-x-auto rounded-3xl border border-alpine-100 shadow-sm">
    <table class="w-full text-sm text-left min-w-[720px]">
      <thead class="bg-ocean-800 text-white"><tr>
        <th class="py-4 px-4 font-semibold rounded-tl-3xl">Excursion</th>
        <th class="py-4 px-3 font-semibold">Duration</th>
        <th class="py-4 px-3 font-semibold">Best For</th>
        <th class="py-4 px-3 font-semibold">Fitness Level</th>
        <th class="py-4 px-4 font-semibold rounded-tr-3xl">Details</th>
      </tr></thead>
      <tbody class="bg-white">{body}</tbody>
    </table>
  </div>
</div></section>"""


def excursion_page(
    intro: str,
    bullets: list[str],
    image_key: str,
    duration: str,
    fitness: str,
    wildlife: str,
    photography: str,
    best_for: str,
    return_ship: str,
    faq: list[tuple[str, str]],
    snapshot_kw: dict | None = None,
) -> str:
    img, alt = IMG[image_key]
    bl = "".join(f'<li class="flex gap-2 text-sm text-gray-600"><span class="text-ocean-500">✓</span>{b}</li>' for b in bullets)
    snap = cruise_snapshot(**(snapshot_kw or {}))
    return f"""<section class="pt-8 pb-4 bg-white"><div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8"><div class="grid lg:grid-cols-2 gap-12 items-start">
  <div><p class="text-gray-600 leading-relaxed mb-6">{intro}</p><ul class="space-y-3 mb-6">{bl}</ul></div>
  <div class="card-media rounded-3xl overflow-hidden aspect-[4/3] shadow-lg"><img src="/{img}" alt="{alt}" width="600" height="450" loading="lazy" decoding="async" /></div>
</div></div></section>
<section class="pb-4 bg-white">{excursion_meta(duration, fitness, wildlife, photography, best_for, return_ship)}</section>
<section class="pb-8 bg-white"><div class="max-w-7xl mx-auto px-4">{snap}</div></section>
<section class="pb-8 bg-white"><div class="max-w-3xl mx-auto px-4">{commercial_strip(best_for, wildlife, return_ship)}</div></section>
{faq_block(faq)}
<section class="pb-16 bg-white"><div class="max-w-3xl mx-auto px-4 text-center">
  <a href="{u('enquire')}" class="btn-ocean inline-flex items-center justify-center text-white font-semibold px-8 py-4 rounded-full shadow-lg">Enquire about this tour →</a>
  {internal_links()}
</div></section>"""


def content_home() -> str:
    cards = card_grid([
        ("eagles", "Bald Eagle Viewing", "World-class eagle concentrations at the Chilkat Bald Eagle Preserve.", "bald-eagle-viewing-tours", "Eagle Tours"),
        ("chilkoot_lake", "Chilkoot Lake Wildlife", "Bears, eagles and mountain scenery at Chilkoot Lake State Park.", "chilkoot-lake-wildlife-tour", "Lake Tour"),
        ("scenic", "Scenic Haines Tour", "Lynn Canal, fjords and authentic small-town Alaska.", "scenic-haines-tour", "Scenic Tour"),
        ("fort_seward", "Fort Seward Heritage", "Historic barracks, art and Tlingit culture in downtown Haines.", "fort-seward-tour", "Fort Seward"),
    ])
    return f"""<section class="pt-8 pb-8 bg-white"><div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8"><div class="grid lg:grid-cols-2 gap-12 items-center">
  <div>
    <div class="inline-flex items-center gap-2 text-ocean-600 text-xs font-semibold tracking-widest uppercase mb-3"><div class="w-8 h-px bg-ocean-400"></div>Haines · Lynn Canal</div>
    <h2 class="text-3xl sm:text-4xl font-display font-bold text-gray-900 mb-5">Quieter Alaska.<br/><span class="text-ocean-600">Exceptional Wildlife.</span></h2>
    <p class="text-gray-600 leading-relaxed mb-5">Haines offers a more authentic southeast Alaska experience than busier ports — bald eagles, Chilkoot Lake bears, salmon rivers and Fort William H. Seward heritage on a typical <strong>6–10 hour</strong> cruise call.</p>
    <a href="{u('best-haines-shore-excursions')}" class="btn-ocean inline-flex items-center gap-2 text-white font-semibold px-7 py-3.5 rounded-full text-sm shadow-lg">Browse All Excursions</a>
  </div>
  <div class="info-image rounded-3xl aspect-[4/3] shadow-2xl overflow-hidden"><img src="/{IMG['intro'][0]}" alt="{IMG['intro'][1]}" width="800" height="600" loading="lazy" decoding="async" /></div>
</div></div></section>
<section class="pb-8 bg-white"><div class="max-w-7xl mx-auto px-4">{cruise_snapshot()}</div></section>
<section class="py-16 bg-sand-50"><div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
  <div class="text-center mb-12"><h2 class="text-3xl font-display font-bold text-gray-900">Top Haines Experiences</h2></div>
  {cards}
</div></section>
{comparison_table()}
<section class="py-16 cta-gradient"><div class="max-w-3xl mx-auto px-4 text-center">
  <h2 class="text-3xl font-display font-bold text-white mb-4">Plan Your Haines Port Day</h2>
  <div class="flex flex-col sm:flex-row gap-4 justify-center">
    <a href="{u('haines-cruise-port-guide')}" class="btn-primary inline-flex items-center justify-center text-white font-semibold px-8 py-4 rounded-full">Port Guide</a>
    <a href="{u('haines-cruise-planner')}" class="btn-outline inline-flex items-center justify-center text-white font-semibold px-8 py-4 rounded-full">Cruise Planner</a>
  </div>
</div></section>"""


def content_best() -> str:
    cards = card_grid([
        ("eagles", "Bald Eagle Viewing", "Chilkat Preserve and river corridors with naturalist guides.", "bald-eagle-viewing-tours", "Eagle Tours"),
        ("chilkoot_lake", "Chilkoot Lake", "Small-group wildlife viewing at Alaska's scenic lake park.", "chilkoot-lake-wildlife-tour", "Lake Tour"),
        ("chilkoot_river", "Chilkoot River", "Salmon runs attract bears and eagles in season.", "chilkoot-river-tour", "River Tour"),
        ("photography", "Photography", "Guided shoots for eagles, bears and valley landscapes.", "photography-tours", "Photo Tours"),
    ])
    return f"""<section class="pt-8 pb-4 bg-white"><div class="max-w-3xl mx-auto px-4 text-center">
  <h2 class="text-3xl font-display font-bold text-gray-900 mb-4">Best Haines Shore Excursions</h2>
  <p class="text-gray-600 leading-relaxed text-sm">Independent guide to the excursions cruise passengers book most — timed for Haines pier schedules with return-to-ship confidence.</p>
</div></section>
<section class="pb-8 bg-white"><div class="max-w-3xl mx-auto px-4">{commercial_strip('Comparing all Haines tour types for your ship schedule', 'Bald eagles, bears, moose, seals and salmon depending on season', 'Reputable operators allow 60–90 minutes before all-aboard')}</div></section>
{comparison_table()}
<section class="py-16 bg-white"><div class="max-w-7xl mx-auto px-4">
  <h2 class="text-2xl font-display font-bold text-center mb-8">Excursion Guides</h2>
  {cards}
  <div class="mt-12 max-w-3xl mx-auto">{internal_links()}</div>
</div></section>"""


def content_port() -> str:
    return f"""<section class="pt-8 pb-4 bg-white"><div class="max-w-3xl mx-auto px-4 text-center">
  <p class="text-gray-600 leading-relaxed text-sm">Ships dock at the <strong>Haines cruise pier</strong> on Portage Cove — downtown, tour pickups and the ferry terminal are minutes away on a typical <strong>6–10 hour</strong> call.</p>
</div></section>
<section class="pb-8 bg-white"><div class="max-w-7xl mx-auto px-4">{cruise_snapshot(activity_level='Low at pier; moderate on wildlife tours', popular='Eagle tours, Chilkoot Lake, scenic drives')}</div></section>
<section class="py-12 bg-sand-50"><div class="max-w-7xl mx-auto px-4">
  <div class="info-image rounded-3xl aspect-[21/9] shadow-xl overflow-hidden mb-8 max-w-5xl mx-auto"><img src="/{IMG['port'][0]}" alt="{IMG['port'][1]}" width="1200" height="514" loading="lazy" decoding="async" /></div>
  <div class="grid lg:grid-cols-2 gap-6 text-sm">
    <div class="bg-white rounded-3xl p-6 border border-alpine-100"><h3 class="font-display font-bold text-lg mb-2">Where Ships Dock</h3><p class="text-gray-600">The main pier sits beside Portage Cove in downtown Haines. No tender required — you walk straight into a walkable, low-key port town.</p></div>
    <div class="bg-white rounded-3xl p-6 border border-alpine-100"><h3 class="font-display font-bold text-lg mb-2">Getting To Tours</h3><p class="text-gray-600">Wildlife tours to Chilkoot Lake and the Chilkat Valley typically include pier pickup. Allow 15–30 minutes drive to lake and river trailheads.</p></div>
  </div>
</div></section>
<section class="py-12 bg-white"><div class="max-w-7xl mx-auto px-4">
  <div class="grid sm:grid-cols-3 gap-6 text-sm">
    <div class="bg-sand-50 rounded-2xl p-6"><strong class="text-gray-900">Currency</strong><p class="mt-2 text-gray-600">US dollars. Cards accepted; carry cash for small vendors.</p></div>
    <div class="bg-ocean-50 rounded-2xl p-6"><strong class="text-gray-900">Weather</strong><p class="mt-2 text-gray-600">Layer up — southeast Alaska is cool and changeable even in summer. Rain gear helps.</p></div>
    <div class="bg-sand-50 rounded-2xl p-6"><strong class="text-gray-900">Wildlife Season</strong><p class="mt-2 text-gray-600">Salmon runs peak late summer–fall for bears and eagles. Eagles concentrate Oct–Feb at Chilkat.</p></div>
  </div>
  <p class="text-center mt-8"><a href="{u('things-to-do-in-haines-from-a-cruise-ship')}" class="text-ocean-600 font-semibold text-sm">Things to do from your ship →</a></p>
  <div class="mt-10 max-w-3xl mx-auto">{internal_links()}</div>
</div></section>"""


def content_things() -> str:
    return f"""<section class="pt-8 pb-8 bg-white"><div class="max-w-3xl mx-auto px-4">
  <p class="text-gray-600 text-sm text-center mb-8">Sample timeline for a <strong>6–10 hour</strong> Haines call. Adjust for your ship's actual times.</p>
  <ol class="space-y-4 text-sm">
    <li class="flex gap-4 bg-white rounded-2xl p-5 border border-alpine-100"><span class="font-bold text-ocean-600 shrink-0">07:30</span><div><strong>Depart pier</strong><p class="text-gray-600 mt-1">Meet Chilkoot Lake or eagle tour — morning light is best for photography.</p></div></li>
    <li class="flex gap-4 bg-white rounded-2xl p-5 border border-alpine-100"><span class="font-bold text-ocean-600 shrink-0">08:00</span><div><strong>Chilkoot Lake wildlife</strong><p class="text-gray-600 mt-1">Naturalist-guided viewing for bears, eagles and mountain scenery.</p></div></li>
    <li class="flex gap-4 bg-white rounded-2xl p-5 border border-alpine-100"><span class="font-bold text-ocean-600 shrink-0">12:00</span><div><strong>Fort Seward stroll</strong><p class="text-gray-600 mt-1">Historic barracks, local galleries and lunch in downtown Haines.</p></div></li>
    <li class="flex gap-4 bg-white rounded-2xl p-5 border border-alpine-100"><span class="font-bold text-ocean-600 shrink-0">14:00</span><div><strong>Scenic drive or nature walk</strong><p class="text-gray-600 mt-1">Short afternoon tour if energy and schedule allow.</p></div></li>
    <li class="flex gap-4 bg-white rounded-2xl p-5 border border-alpine-100"><span class="font-bold text-ocean-600 shrink-0">16:30</span><div><strong>Return to pier</strong><p class="text-gray-600 mt-1">Allow margin before published all-aboard.</p></div></li>
  </ol>
  <div class="mt-10">{commercial_strip('One-day Haines itineraries from the cruise pier', 'Morning wildlife tours maximise bear and eagle sightings', 'Finish downtown tours by mid-afternoon on standard schedules')}</div>
  <div class="mt-8">{internal_links()}</div>
</div></section>"""


def content_wildlife() -> str:
    return f"""<section class="pt-8 pb-8 bg-white"><div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8"><div class="grid lg:grid-cols-2 gap-12 items-start">
  <div>
    <p class="text-gray-600 leading-relaxed mb-6">Haines sits at the heart of some of southeast Alaska's richest wildlife habitat — the <strong>Chilkat Bald Eagle Preserve</strong>, Chilkoot Lake salmon streams and Lynn Canal marine life reward patient observers.</p>
    <ul class="space-y-3 mb-6 text-sm text-gray-600">
      <li class="flex gap-2"><span class="text-ocean-500">✓</span><strong>Bald eagles</strong> — world's largest seasonal gathering at Chilkat (Oct–Feb peak).</li>
      <li class="flex gap-2"><span class="text-ocean-500">✓</span><strong>Brown bears</strong> — Chilkoot River and lake shores during salmon runs.</li>
      <li class="flex gap-2"><span class="text-ocean-500">✓</span><strong>Marine life</strong> — seals, porpoises and occasional whales in Lynn Canal.</li>
      <li class="flex gap-2"><span class="text-ocean-500">✓</span><strong>Moose</strong> — meadow edges near lake and river corridors.</li>
    </ul>
    <a href="{u('haines-bald-eagle-guide')}" class="text-ocean-600 font-semibold text-sm">Bald eagle guide →</a>
  </div>
  <div class="card-media rounded-3xl overflow-hidden aspect-[4/3] shadow-lg"><img src="/{IMG['wildlife'][0]}" alt="{IMG['wildlife'][1]}" width="600" height="450" loading="lazy" decoding="async" /></div>
</div></div></section>
<section class="pb-8 bg-white"><div class="max-w-3xl mx-auto px-4">{commercial_strip('Wildlife-first port days away from cruise crowds', 'Eagles, bears, moose, seals and salmon by season', 'Morning wildlife tours typically return by early afternoon')}</div></section>
<section class="pb-16 bg-white"><div class="max-w-3xl mx-auto px-4">{internal_links()}</div></section>"""


def content_eagle_guide() -> str:
    return f"""<section class="pt-8 pb-8 bg-white"><div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8"><div class="grid lg:grid-cols-2 gap-12 items-start">
  <div>
    <p class="text-gray-600 leading-relaxed mb-6">The <strong>Chilkat Bald Eagle Preserve</strong> hosts one of the world's largest concentrations of bald eagles when salmon run in the Chilkat River. Summer cruise calls still yield sightings along rivers, lakes and estuaries with expert naturalist guides.</p>
    <ul class="space-y-3 mb-6 text-sm text-gray-600">
      <li class="flex gap-2"><span class="text-ocean-500">✓</span>Peak eagle numbers: <strong>October–February</strong> (fewer cruise ships).</li>
      <li class="flex gap-2"><span class="text-ocean-500">✓</span>Summer calls: eagles nest and fish throughout the Chilkoot and Chilkat valleys.</li>
      <li class="flex gap-2"><span class="text-ocean-500">✓</span>Bring binoculars and a telephoto lens — guides know active perches.</li>
    </ul>
    <a href="{u('chilkat-bald-eagle-preserve-guide')}" class="text-ocean-600 font-semibold text-sm">Chilkat Preserve guide →</a> · <a href="{u('bald-eagle-viewing-tours')}" class="text-ocean-600 font-semibold text-sm">Eagle viewing tours →</a>
  </div>
  <div class="card-media rounded-3xl overflow-hidden aspect-[4/3] shadow-lg"><img src="/{IMG['eagles'][0]}" alt="{IMG['eagles'][1]}" width="600" height="450" loading="lazy" decoding="async" /></div>
</div></div></section>
<section class="pb-16 bg-white"><div class="max-w-3xl mx-auto px-4">{internal_links()}</div></section>"""


def content_vs_skagway() -> str:
    return f"""<section class="pt-8 pb-8 bg-white"><div class="max-w-3xl mx-auto px-4">
  <p class="text-gray-600 leading-relaxed mb-8">Both Haines and Skagway sit on the Inside Passage, but they offer fundamentally different cruise port experiences. This guide helps you choose — or appreciate what makes each stop unique on an Alaska itinerary.</p>
  <div class="info-image rounded-3xl aspect-[21/9] shadow-xl overflow-hidden mb-10"><img src="/{IMG['skagway'][0]}" alt="{IMG['skagway'][1]}" width="1200" height="514" loading="lazy" decoding="async" /></div>
  <div class="overflow-x-auto rounded-3xl border border-alpine-100 shadow-sm mb-10">
    <table class="w-full text-sm text-left min-w-[640px]">
      <thead class="bg-ocean-800 text-white"><tr>
        <th class="py-4 px-4 font-semibold">Factor</th>
        <th class="py-4 px-4 font-semibold">Haines</th>
        <th class="py-4 px-4 font-semibold">Skagway</th>
      </tr></thead>
      <tbody class="bg-white">
        <tr class="border-b border-alpine-50"><td class="py-4 px-4 font-semibold">Crowd level</td><td class="py-4 px-4 text-gray-600">Quiet, authentic small town</td><td class="py-4 px-4 text-gray-600">Busier, more tourist-focused</td></tr>
        <tr class="border-b border-alpine-50"><td class="py-4 px-4 font-semibold">Top draw</td><td class="py-4 px-4 text-gray-600">Wildlife, eagles, wilderness</td><td class="py-4 px-4 text-gray-600">Gold Rush history, White Pass Railway</td></tr>
        <tr class="border-b border-alpine-50"><td class="py-4 px-4 font-semibold">Excursion style</td><td class="py-4 px-4 text-gray-600">Nature, photography, culture</td><td class="py-4 px-4 text-gray-600">Railway, hiking, historic tours</td></tr>
        <tr class="border-b border-alpine-50"><td class="py-4 px-4 font-semibold">Best for</td><td class="py-4 px-4 text-gray-600">Wildlife lovers &amp; photographers</td><td class="py-4 px-4 text-gray-600">History buffs &amp; scenic railway fans</td></tr>
        <tr><td class="py-4 px-4 font-semibold">Port feel</td><td class="py-4 px-4 text-gray-600">Independent, local, uncrowded</td><td class="py-4 px-4 text-gray-600">Frontier theme-park atmosphere</td></tr>
      </tbody>
    </table>
  </div>
  <h2 class="text-2xl font-display font-bold text-gray-900 mb-4">Which port is better for you?</h2>
  <p class="text-gray-600 text-sm mb-4"><strong>Choose Haines</strong> if bald eagles, bear viewing, Chilkoot Lake scenery and a genuine Alaska town matter more than railway nostalgia. Haines is Skagway's quieter, more wilderness-focused neighbour.</p>
  <p class="text-gray-600 text-sm mb-8"><strong>Choose Skagway</strong> if the White Pass &amp; Yukon Route railway, Gold Rush walking tours and high-energy historic excursions are your priority.</p>
  <p class="text-gray-600 text-sm mb-8">Many Alaska itineraries visit both ports on different days — use Haines for wildlife and Skagway for railway history.</p>
  {commercial_strip('Wildlife-first travellers who want fewer crowds', 'Haines: eagles, bears, marine life; Skagway: mountain goats, historic sites', 'Both ports suit standard 6–10 hour calls with local operator buffers')}
  <div class="mt-8">{internal_links()}</div>
</div></section>"""


def content_chilkoot_lake_guide() -> str:
    return f"""<section class="pt-8 pb-8 bg-white"><div class="max-w-3xl mx-auto px-4">
  <p class="text-gray-600 leading-relaxed mb-6"><strong>Chilkoot Lake State Park</strong> combines glacier-fed water, rainforest mountains and reliable wildlife viewing — bears fishing for salmon, bald eagles overhead and seals in the lake. It is the signature Haines shore excursion for cruise passengers who want pristine Alaska without Skagway-scale crowds.</p>
  <p class="text-gray-600 text-sm mb-8">Most tours run 2.5–4 hours with naturalist guides in groups of 14 or fewer. Pier pickup is standard; the drive from downtown Haines takes roughly 30 minutes.</p>
  <a href="{u('chilkoot-lake-wildlife-tour')}" class="btn-ocean inline-flex items-center justify-center text-white text-sm font-semibold px-6 py-3 rounded-full">Chilkoot Lake wildlife tour →</a>
  <div class="mt-10">{internal_links()}</div>
</div></section>"""


def content_chilkat_guide() -> str:
    return f"""<section class="pt-8 pb-8 bg-white"><div class="max-w-3xl mx-auto px-4">
  <p class="text-gray-600 leading-relaxed mb-6">The <strong>Chilkat Bald Eagle Preserve</strong> protects 48,000 acres along the Chilkat, Chilkoot and Tsirku rivers — hosting up to 4,000 bald eagles when late-run salmon attract birds from across the region. Rafting, jet-boat and guided viewing tours access the river corridor with expert interpretation.</p>
  <p class="text-gray-600 text-sm mb-8">Even on summer cruise calls, eagles nest and hunt throughout the preserve. Photography tours target active perches, waterfalls and salmon-catching bears where conditions allow.</p>
  <a href="{u('bald-eagle-viewing-tours')}" class="btn-ocean inline-flex items-center justify-center text-white text-sm font-semibold px-6 py-3 rounded-full">Bald eagle viewing tours →</a>
  <div class="mt-10">{internal_links()}</div>
</div></section>"""


def content_best_time() -> str:
    return f"""<section class="pt-8 pb-8 bg-white"><div class="max-w-3xl mx-auto px-4">
  <p class="text-gray-600 leading-relaxed mb-8">Haines cruise season runs <strong>May through September</strong>, with peak Inside Passage sailings in June–August. Each month offers different wildlife and weather trade-offs.</p>
  <div class="space-y-4 text-sm mb-8">
    <div class="bg-sand-50 rounded-2xl p-5 border border-alpine-100"><strong class="text-gray-900">May–June</strong><p class="mt-2 text-gray-600">Longer daylight, fewer crowds, bears emerging. Cooler temperatures — dress in layers.</p></div>
    <div class="bg-ocean-50 rounded-2xl p-5 border border-alpine-100"><strong class="text-gray-900">July–August</strong><p class="mt-2 text-gray-600">Peak cruise season. Salmon runs begin; bear viewing improves at Chilkoot River. Warmest weather (relative).</p></div>
    <div class="bg-sand-50 rounded-2xl p-5 border border-alpine-100"><strong class="text-gray-900">September</strong><p class="mt-2 text-gray-600">Salmon peak for bears and eagles. Fewer ships, autumn colours. Shorter days.</p></div>
    <div class="bg-alpine-50 rounded-2xl p-5 border border-alpine-100"><strong class="text-gray-900">October–February (off-season)</strong><p class="mt-2 text-gray-600">Maximum bald eagle concentrations at Chilkat — fewer cruise calls but world-class eagle photography for land-based visitors.</p></div>
  </div>
  <p class="text-sm text-gray-600 mb-8">See our <a href="{u('haines-cruise-ship-schedule')}" class="text-ocean-600 font-semibold">cruise ship schedule</a> for typical port call months.</p>
  {internal_links()}
</div></section>"""


def content_schedule() -> str:
    return f"""<section class="pt-8 pb-8 bg-white"><div class="max-w-3xl mx-auto px-4">
  <p class="text-gray-600 leading-relaxed mb-6">Major Alaska cruise lines call at Haines on select Inside Passage itineraries — often paired with Skagway, Juneau and Glacier Bay. Schedules vary by year; always confirm with your cruise line.</p>
  <p class="text-gray-600 text-sm mb-6"><strong>Typical pattern:</strong> ships arrive morning to midday and depart late afternoon, giving 6–10 hours ashore. Haines is a <strong>dock port</strong> — no tender required.</p>
  <ul class="space-y-3 text-sm text-gray-600 mb-8">
    <li class="flex gap-2"><span class="text-ocean-500">✓</span>Princess, Holland America, Norwegian and Viking commonly include Haines on some sailings.</li>
    <li class="flex gap-2"><span class="text-ocean-500">✓</span>Port calls concentrate May–September; exact dates publish 12–18 months ahead.</li>
    <li class="flex gap-2"><span class="text-ocean-500">✓</span>Book wildlife tours early on popular ship days — Chilkoot Lake groups are small.</li>
  </ul>
  <a href="{u('haines-cruise-planner')}" class="text-ocean-600 font-semibold text-sm">Use our cruise planner →</a>
  <div class="mt-10">{internal_links()}</div>
</div></section>"""


def content_planner() -> str:
    return f"""<section class="pt-8 pb-8 bg-white"><div class="max-w-3xl mx-auto px-4">
  <p class="text-gray-600 text-sm text-center mb-8">Check off priorities for your Haines port day, then match tours on our <a href="{u('best-haines-shore-excursions')}" class="text-ocean-600 font-semibold">excursions hub</a>.</p>
  <div class="planner-checklist space-y-3 mb-10">
    <label><input type="checkbox" /> I want bald eagle viewing</label>
    <label><input type="checkbox" /> Bear and wildlife photography is a priority</label>
    <label><input type="checkbox" /> I'd like Chilkoot Lake scenery</label>
    <label><input type="checkbox" /> I'm interested in Fort Seward history</label>
    <label><input type="checkbox" /> I prefer easy fitness / minimal walking</label>
    <label><input type="checkbox" /> I need a guaranteed afternoon return to ship</label>
    <label><input type="checkbox" /> I'm comparing Haines with Skagway</label>
  </div>
  {help_cta()}
  <div class="mt-10">{internal_links()}</div>
</div></section>"""


def content_enquire() -> str:
    return f"""<section class="pt-8 pb-16 bg-white"><div class="max-w-xl mx-auto px-4">
  <p class="text-gray-600 text-sm text-center mb-8">Tell us your ship, date and interests — we'll suggest Haines shore excursions matched to your schedule.</p>
  <form class="enquire-form" action="mailto:enquiries@hainesshoreexcursions.com" method="post" enctype="text/plain">
    <label for="name">Your name</label>
    <input id="name" name="name" type="text" required />
    <label for="email">Email</label>
    <input id="email" name="email" type="email" required />
    <label for="ship">Cruise ship &amp; date</label>
    <input id="ship" name="ship" type="text" placeholder="e.g. Ship name, 15 July 2026" required />
    <label for="interest">Interested in</label>
    <select id="interest" name="interest">
      <option>Bald eagle viewing</option>
      <option>Chilkoot Lake wildlife</option>
      <option>Chilkoot River tour</option>
      <option>Scenic Haines tour</option>
      <option>Fort Seward tour</option>
      <option>Photography tour</option>
      <option>Cultural &amp; heritage tour</option>
      <option>Nature walk</option>
      <option>Not sure — help me choose</option>
    </select>
    <label for="message">Message</label>
    <textarea id="message" name="message" rows="4" placeholder="Group size, mobility needs, timing concerns…"></textarea>
    <button type="submit" class="btn-ocean w-full text-white font-semibold py-3 rounded-full">Send enquiry</button>
  </form>
  <p class="text-xs text-gray-400 text-center mt-6">We respond within 1–2 business days. Not affiliated with any cruise line.</p>
</div></section>"""


def content_faq() -> str:
    qa = [
        ("How long do cruise ships stay in Haines?", "Most calls are 6 to 10 hours. Morning wildlife tours and an afternoon downtown visit fit comfortably with return buffer."),
        ("Is Haines a tender port?", "No — ships dock at the Haines pier. You walk straight into downtown."),
        ("When is best for bald eagles?", "Maximum concentrations are October–February at the Chilkat Preserve. Summer cruise calls still see eagles at lakes and rivers."),
        ("Can I see bears on a port day?", "Yes during salmon season (roughly July–September) at Chilkoot River and lake shores with guided tours."),
        ("Haines or Skagway for wildlife?", "Haines is the stronger wildlife port — eagles, bears and Chilkoot Lake. Skagway excels at Gold Rush history and the White Pass Railway."),
        ("Should I book ship excursions or independently?", "Ship tours guarantee the vessel waits if the operator is late. Reputable Haines operators plan 60–90 minute pier buffers — confirm policies when booking."),
    ]
    return f"""<section class="pb-8 bg-white"><div class="max-w-7xl mx-auto px-4">{cruise_snapshot(best_for='Quick planning answers')}</div></section>
{faq_block(qa)}
<section class="pb-16 bg-white"><div class="max-w-3xl mx-auto px-4">{internal_links()}</div></section>"""


EXCURSIONS = [
    dict(
        slug="bald-eagle-viewing-tours",
        hero_title=f"Bald Eagle Viewing<br/><span class=\"{ACCENT}\">Tours</span>",
        hero_lead="Expert-guided eagle viewing at the Chilkat Bald Eagle Preserve and river corridors — Haines' signature wildlife experience.",
        image="eagles",
        intro="Haines hosts one of the world's great bald eagle gatherings. Guided viewing tours access the Chilkat Bald Eagle Preserve and river corridors where naturalists know active perches, feeding patterns and photography angles.",
        bullets=["Small groups (often 14 or fewer) with expert naturalist guides", "Binoculars and spotting scopes typically provided", "Summer nest sites and fishing eagles; winter peak concentrations Oct–Feb", "Combine with Chilkat Preserve context for deeper interpretation"],
        duration="2.5–4 hours", fitness="Easy to moderate — short walks at viewing stops",
        wildlife="Bald eagles primary; bears, seals and salmon possible by season",
        photography="Excellent — telephoto lens recommended; guides know best angles",
        best_for="Birders, photographers and first-time Alaska visitors",
        return_ship="High confidence — standard half-day tours return by early afternoon",
        faq=[("How many eagles will I see?", "Summer calls typically yield multiple sightings; winter peaks can reach thousands along the Chilkat."), ("Is this suitable for children?", "Yes — easy viewing from vehicles and short walks; bring layers for cool weather."), ("Do I need my own binoculars?", "Helpful but most tours provide scopes and spare binoculars.")],
        snapshot=dict(best_for="Eagle enthusiasts and photographers", popular="Chilkat Preserve viewing, river corridor tours"),
    ),
    dict(
        slug="chilkoot-lake-wildlife-tour",
        hero_title=f"Chilkoot Lake<br/><span class=\"{ACCENT}\">Wildlife Tour</span>",
        hero_lead="Glacier-fed lake, mountain scenery and bears, eagles and seals at Chilkoot Lake State Park.",
        image="chilkoot_lake",
        intro="Chilkoot Lake State Park is Haines' premier wildlife destination — a naturalist-guided tour through rainforest mountains to glacier-fed water where bears fish for salmon, eagles perch overhead and seals surface in the lake.",
        bullets=["Express (2.5 hr) and full (4 hr) options with lunch on longer tours", "Groups capped around 14 guests for intimate viewing", "Pier pickup included on most operators", "Peak bear activity during salmon runs July–September"],
        duration="2.5–4 hours", fitness="Easy to moderate — uneven ground at lake shore possible",
        wildlife="Brown bears, bald eagles, seals, salmon; occasional moose",
        photography="Strong — mountain reflections, wildlife action shots",
        best_for="Wildlife lovers wanting Haines' signature experience",
        return_ship="High confidence — designed for standard port schedules",
        faq=[("When are bears most active?", "During salmon runs, roughly July through September at the lake outlet."), ("What is the drive time?", "About 30 minutes from downtown Haines to the lake."), ("Express or full tour?", "Express fits tighter schedules; full tour adds lunch and more viewing time.")],
        snapshot=dict(best_for="Bear and eagle wildlife viewing", popular="Chilkoot Lake State Park naturalist tours"),
    ),
    dict(
        slug="chilkoot-river-tour",
        hero_title=f"Chilkoot River<br/><span class=\"{ACCENT}\">Tour</span>",
        hero_lead="Salmon runs, bear viewing and eagle activity along the Chilkoot River corridor.",
        image="chilkoot_river",
        intro="The Chilkoot River connects Chilkoot Lake to Lynn Canal — during salmon season bears fish the shallows while bald eagles wait in the trees. Guided tours manage safe viewing distances with expert interpretation.",
        bullets=["Best bear viewing July–September during salmon runs", "Naturalist guides enforce wildlife-safe distances", "Often paired with lake or scenic stops on longer itineraries", "Photography opportunities at river overlooks"],
        duration="2.5–3 hours", fitness="Easy — short walks to viewing platforms",
        wildlife="Brown bears, bald eagles, salmon; seals possible near mouth",
        photography="Excellent during salmon season — bears and eagles action",
        best_for="Bear watchers and wildlife photographers",
        return_ship="High confidence on dedicated half-day tours",
        faq=[("Is bear viewing guaranteed?", "Never guaranteed in the wild, but salmon season offers very strong odds with guides who know daily patterns."), ("How close do we get to bears?", "Guides maintain safe, legal distances — bring a telephoto lens for close-up photos."), ("Can this combine with Chilkoot Lake?", "Some operators offer combined lake and river itineraries — ask when enquiring.")],
        snapshot=dict(best_for="Salmon-season bear viewing", popular="Chilkoot River wildlife corridors"),
    ),
    dict(
        slug="scenic-haines-tour",
        hero_title=f"Scenic Haines<br/><span class=\"{ACCENT}\">Tour</span>",
        hero_lead="Lynn Canal vistas, fjord scenery and authentic small-town Alaska beyond the cruise pier.",
        image="scenic",
        intro="A scenic Haines tour reveals what makes this port special — dramatic Lynn Canal, Chilkat Valley lookouts, rainforest drives and a downtown that feels genuinely Alaskan rather than theme-park frontier.",
        bullets=["Air-conditioned van or small bus with narration", "Photo stops at mountain and water viewpoints", "Less physically demanding than hiking or rafting tours", "Ideal for guests who want overview before choosing deeper excursions"],
        duration="3–4 hours", fitness="Easy — minimal walking, mostly scenic drives",
        wildlife="Eagle and wildlife sightings possible; not the primary focus",
        photography="Landscape and scenic photography at designated stops",
        best_for="First-time visitors and guests preferring low activity",
        return_ship="Very high confidence — flexible timing",
        faq=[("Does this include Chilkoot Lake?", "Some scenic tours include a lake photo stop; wildlife-focused lake tours are separate."), ("Is this good for limited mobility?", "Yes — mostly vehicle-based with optional short stops."), ("How does this compare to Skagway railway tours?", "Haines scenic tours emphasise wilderness and Lynn Canal rather than Gold Rush railway history.")],
        snapshot=dict(best_for="Scenic overview and photography", popular="Valley drives, Lynn Canal lookouts"),
    ),
    dict(
        slug="fort-seward-tour",
        hero_title=f"Fort Seward<br/><span class=\"{ACCENT}\">Tour</span>",
        hero_lead="Historic Fort William H. Seward — army barracks, local art and Tlingit heritage in downtown Haines.",
        image="fort_seward",
        intro="Fort William H. Seward is a decommissioned army post now home to inns, galleries and cultural spaces. Walking tours explore barracks architecture, local history and the Tlingit heritage that predates the fort by millennia.",
        bullets=["Walking distance from the cruise pier", "Combines with downtown lunch and shopping", "Lower physical demand than valley wildlife tours", "Cultural complement to morning Chilkoot Lake excursions"],
        duration="2–3 hours", fitness="Easy — paved and gravel paths in downtown Haines",
        wildlife="Limited — occasional bald eagle overhead",
        photography="Architecture, harbour views and cultural details",
        best_for="History buffs and guests wanting a relaxed port afternoon",
        return_ship="Very high confidence — downtown proximity to pier",
        faq=[("How far is Fort Seward from the pier?", "Roughly 10–15 minutes on foot along the waterfront."), ("Can I do this after a morning wildlife tour?", "Yes — a common pattern is Chilkoot Lake morning, Fort Seward afternoon."), ("Is Tlingit culture included?", "Quality tours reference Tlingit heritage alongside army history — ask operators for cultural depth.")],
        snapshot=dict(best_for="History and cultural heritage", popular="Fort Seward walking tours, gallery visits"),
    ),
    dict(
        slug="photography-tours",
        hero_title=f"Haines<br/><span class=\"{ACCENT}\">Photography Tours</span>",
        hero_lead="Small-group photo expeditions for eagles, bears, waterfalls and Chilkat Valley landscapes.",
        image="photography",
        intro="Haines photography tours are built for serious shooters — guides who understand light, positioning and wildlife behaviour take small groups to eagles, bear-fishing spots, waterfalls and mountain vistas across the Chilkat Valley.",
        bullets=["Small groups with photography-focused pacing", "Tripods welcome at designated stops", "Longer itineraries (often 4 hours) with lunch on some tours", "Private photography charters available for custom routes"],
        duration="4 hours (typical)", fitness="Moderate — some uneven terrain at river and lake stops",
        wildlife="Bald eagles, bears during salmon season, landscapes throughout",
        photography="Primary focus — guides assist with positioning and timing",
        best_for="Dedicated photographers with DSLR or mirrorless gear",
        return_ship="High confidence — confirm end time when booking",
        faq=[("What lens should I bring?", "200–600mm telephoto ideal for eagles and bears; wide-angle for landscapes."), ("Are tripods allowed?", "Yes at most designated viewing stops — confirm with your operator."), ("Private options?", "Private photography expeditions are available for custom pacing and locations.")],
        snapshot=dict(best_for="Serious nature photographers", popular="Chilkat Valley photo expeditions"),
    ),
    dict(
        slug="cultural-heritage-tours",
        hero_title=f"Cultural &amp;<br/><span class=\"{ACCENT}\">Heritage Tours</span>",
        hero_lead="Tlingit traditions, Fort Seward history and the authentic community behind Haines' quiet port.",
        image="cultural",
        intro="Beyond wildlife, Haines has deep cultural layers — Tlingit heritage spanning thousands of years, army history at Fort Seward and a thriving local arts community. Heritage tours connect cruise guests with the people and stories behind the scenery.",
        bullets=["Tlingit cultural context alongside fort and town history", "Gallery and carving studio visits where available", "Easy pacing suitable for all ages", "Pairs well with eagle or lake tours on split port days"],
        duration="2–3 hours", fitness="Easy — walking tours in downtown and fort grounds",
        wildlife="Not the focus — occasional eagle sightings",
        photography="Cultural subjects, harbour and architecture",
        best_for="Guests seeking authentic Alaska beyond wildlife checklist",
        return_ship="Very high confidence",
        faq=[("Is this different from Fort Seward alone?", "Heritage tours typically weave Tlingit culture, fort history and contemporary arts into one narrative."), ("Suitable for families?", "Yes — engaging storytelling for school-age children and adults."), ("When to schedule?", "Afternoon slot after a morning wildlife tour works well.")],
        snapshot=dict(best_for="Culture and history enthusiasts", popular="Tlingit heritage, Fort Seward walks"),
    ),
    dict(
        slug="nature-walks",
        hero_title=f"Haines<br/><span class=\"{ACCENT}\">Nature Walks</span>",
        hero_lead="Mindful forest walks and guided nature therapy in the rainforests and coves near Haines.",
        image="nature",
        intro="Not every Haines excursion needs adrenaline — guided nature walks and forest therapy experiences in Portage Cove State Park and nearby trails offer peaceful immersion in southeast Alaska's temperate rainforest.",
        bullets=["Easy pace with guided mindfulness and naturalist interpretation", "Snack or beverage often included", "Small groups in quiet forest settings", "Ideal contrast to high-energy wildlife drives"],
        duration="2–3 hours", fitness="Easy — gentle forest paths",
        wildlife="Birdsong, forest ecology; occasional eagle overhead",
        photography="Forest details, moss, light through canopy",
        best_for="Guests wanting calm, restorative time in nature",
        return_ship="Very high confidence",
        faq=[("What is forest walk therapy?", "A guided mindful walking practice combining meditation, sensory awareness and nature — originated in Japan as shinrin-yoku."), ("Is this physically demanding?", "No — gentle paths suitable for most mobility levels."), ("Good for a second port day?", "Excellent if you have already done Chilkoot Lake on a previous Alaska itinerary.")],
        snapshot=dict(best_for="Relaxation and forest immersion", popular="Portage Cove walks, mindfulness nature tours"),
    ),
]

EXC_NAV = {
    "bald-eagle-viewing-tours": "Bald Eagle Viewing",
    "chilkoot-lake-wildlife-tour": "Chilkoot Lake",
    "chilkoot-river-tour": "Chilkoot River",
    "scenic-haines-tour": "Scenic Haines",
    "fort-seward-tour": "Fort Seward",
    "photography-tours": "Photography",
    "cultural-heritage-tours": "Cultural & Heritage",
    "nature-walks": "Nature Walks",
}


def inject_schemas(html: str, schemas: list[dict]) -> str:
    block = "".join(
        f'  <script type="application/ld+json">\n{json.dumps(s, indent=2)}\n  </script>\n'
        for s in schemas
    )
    return html.replace("  <meta name=\"twitter:card\"", block + "  <meta name=\"twitter:card\"", 1)


def main() -> None:
    print("Building Haines Shore Excursions site…")

    write("partials/nav.html", f"""<nav class="fixed top-0 left-0 right-0 z-50 bg-white/90 border-b border-alpine-100 shadow-sm">
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
    <div class="flex items-center justify-between h-12">
      <a href="/" class="flex items-center gap-2">
        <div class="w-7 h-7 rounded-full btn-ocean flex items-center justify-center">
          <svg class="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2C8 2 4 5 4 9c0 5 4 9 8 13 4-4 8-8 8-13 0-4-4-7-8-7z"/></svg>
        </div>
        <span class="font-display font-semibold text-ocean-800 text-base leading-tight">Haines<br/><span class="text-[10px] font-body font-normal text-teal-600 tracking-widest uppercase">Shore Excursions</span></span>
      </a>
      <div class="hidden lg:flex items-center gap-4 text-sm font-medium">
        <a href="/" data-nav="home" class="text-gray-600 hover:text-ocean-600 transition-colors">Home</a>
        <a href="{u('best-haines-shore-excursions')}" data-nav="excursions" class="text-gray-600 hover:text-ocean-600 transition-colors">Excursions</a>
        <a href="{u('haines-wildlife-guide')}" data-nav="wildlife" class="text-gray-600 hover:text-ocean-600 transition-colors">Wildlife</a>
        <a href="{u('haines-bald-eagle-guide')}" data-nav="eagles" class="text-gray-600 hover:text-ocean-600 transition-colors">Eagles</a>
        <a href="{u('haines-cruise-port-guide')}" data-nav="port" class="text-gray-600 hover:text-ocean-600 transition-colors">Port Guide</a>
        <a href="{u('haines-faq')}" data-nav="faq" class="text-gray-600 hover:text-ocean-600 transition-colors">FAQ</a>
      </div>
      <a href="{u('enquire')}" class="hidden md:inline-flex items-center gap-2 btn-ocean text-white text-sm font-semibold px-4 py-2 rounded-full shadow-md">Enquire</a>
      <button type="button" class="lg:hidden p-2 rounded-lg text-gray-600 hover:bg-sand-50" aria-label="Open menu">
        <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/></svg>
      </button>
    </div>
  </div>
</nav>""")

    exc_links = "".join(f'<li><a href="{u(s)}" class="hover:text-white transition-colors">{lbl}</a></li>' for s, lbl in EXC_NAV.items())
    write("partials/footer.html", f"""<footer class="bg-gray-900 text-gray-400 py-14">
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
    <div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-10 mb-12">
      <div class="sm:col-span-2 lg:col-span-1">
        <a href="/" class="font-display font-semibold text-white text-lg">{SITE}</a>
        <p class="mt-3 text-sm leading-relaxed">Independent planning guide for cruise visitors to Haines, Alaska. Bald eagles, Chilkoot Lake wildlife and authentic wilderness — not affiliated with any cruise line.</p>
      </div>
      <div>
        <h3 class="text-white text-sm font-semibold uppercase tracking-wider mb-4">Excursions</h3>
        <ul class="space-y-2 text-sm">
          <li><a href="{u('best-haines-shore-excursions')}" class="hover:text-white transition-colors">All Excursions</a></li>
          {exc_links}
        </ul>
      </div>
      <div>
        <h3 class="text-white text-sm font-semibold uppercase tracking-wider mb-4">Resources</h3>
        <ul class="space-y-2 text-sm">
          <li><a href="{u('haines-cruise-port-guide')}" class="hover:text-white transition-colors">Port Guide</a></li>
          <li><a href="{u('things-to-do-in-haines-from-a-cruise-ship')}" class="hover:text-white transition-colors">Things To Do</a></li>
          <li><a href="{u('haines-wildlife-guide')}" class="hover:text-white transition-colors">Wildlife Guide</a></li>
          <li><a href="{u('haines-bald-eagle-guide')}" class="hover:text-white transition-colors">Bald Eagle Guide</a></li>
          <li><a href="{u('chilkoot-lake-guide')}" class="hover:text-white transition-colors">Chilkoot Lake Guide</a></li>
          <li><a href="{u('chilkat-bald-eagle-preserve-guide')}" class="hover:text-white transition-colors">Chilkat Preserve</a></li>
          <li><a href="{u('haines-vs-skagway')}" class="hover:text-white transition-colors">Haines vs Skagway</a></li>
          <li><a href="{u('best-time-to-visit-haines')}" class="hover:text-white transition-colors">Best Time To Visit</a></li>
          <li><a href="{u('haines-cruise-ship-schedule')}" class="hover:text-white transition-colors">Cruise Schedule</a></li>
          <li><a href="{u('haines-cruise-planner')}" class="hover:text-white transition-colors">Cruise Planner</a></li>
          <li><a href="{u('haines-faq')}" class="hover:text-white transition-colors">FAQ</a></li>
          <li><a href="{u('enquire')}" class="hover:text-white transition-colors">Enquire</a></li>
        </ul>
      </div>
    </div>
    <div class="border-t border-gray-800 pt-8 text-xs text-center sm:text-left">
      <p>&copy; 2026 {SITE}. Verify times and prices with operators before booking.</p>
    </div>
  </div>
</footer>""")

    write("partials/trust-strip.html", """<section class="trust-strip" aria-label="Haines shore excursion highlights">
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
    <ul class="trust-strip__list">
      <li class="trust-strip__item"><span class="trust-strip__check" aria-hidden="true">✔</span> Bald Eagles</li>
      <li class="trust-strip__item"><span class="trust-strip__check" aria-hidden="true">✔</span> Chilkoot Lake Wildlife</li>
      <li class="trust-strip__item"><span class="trust-strip__check" aria-hidden="true">✔</span> Authentic Alaska</li>
      <li class="trust-strip__item"><span class="trust-strip__check" aria-hidden="true">✔</span> Return-To-Ship Confidence</li>
    </ul>
  </div>
</section>""")

    heroes = {
        "home": hero("Lynn Canal · Alaska", f"Haines Shore<br/><span class=\"{ACCENT}\">Excursions</span><br/>from the Cruise Port", "Bald eagles, Chilkoot Lake wildlife, Fort Seward heritage and scenic wilderness — the quieter, more authentic Alaska port.", "home", cta=("best-haines-shore-excursions", "Compare Excursions"), tags=["🦅 Bald Eagles", "🐻 Wildlife", "🏔️ Chilkoot Lake", "🏛️ Fort Seward"]),
        "best": hero("Independent Guide", f"Best Haines<br/><span class=\"{ACCENT}\">Shore Excursions</span>", "Compare eagle viewing, Chilkoot Lake, river tours, photography and heritage experiences for your ship schedule.", "best", breadcrumb="Best Excursions", cta=("enquire", "Need help choosing? →")),
        "port": hero("Cruise Passenger Guide", f"Haines<br/><span class=\"{ACCENT}\">Cruise Port Guide</span>", "Pier location, pickup logistics, weather and how to plan shore time in downtown Haines.", "port", breadcrumb="Port Guide", cta=("best-haines-shore-excursions", "View Excursions →")),
        "things": hero("Port Day Timeline", f"Things To Do in<br/><span class=\"{ACCENT}\">Haines</span> from a Cruise Ship", "Hour-by-hour plan from gangway to departure — wildlife morning, Fort Seward afternoon.", "things", breadcrumb="Things To Do"),
        "wildlife": hero("Wildlife · Haines", f"Haines<br/><span class=\"{ACCENT}\">Wildlife Guide</span>", "Eagles, bears, moose, seals and salmon — what to expect by season on a Haines port day.", "wildlife", breadcrumb="Wildlife Guide"),
        "eagle_guide": hero("Chilkat &amp; Beyond", f"Haines<br/><span class=\"{ACCENT}\">Bald Eagle Guide</span>", "When and where to see bald eagles — from summer cruise calls to winter concentrations at Chilkat.", "eagles", breadcrumb="Bald Eagle Guide"),
        "vs_skagway": hero("Alaska Port Comparison", "Haines vs Skagway:<br/><span class=\"text-teal-400\">Which Alaska Cruise Port<br/>Is Better?</span>", "Wildlife and authenticity versus Gold Rush railway history — an honest comparison for cruise passengers.", "skagway", breadcrumb="Haines vs Skagway"),
        "chilkoot_lake": hero("State Park · Haines", f"Chilkoot Lake<br/><span class=\"{ACCENT}\">Guide</span>", "Glacier-fed lake, bear viewing and mountain scenery — Haines' essential shore excursion destination.", "chilkoot_lake", breadcrumb="Chilkoot Lake Guide"),
        "chilkat": hero("Eagle Preserve", f"Chilkat Bald Eagle<br/><span class=\"{ACCENT}\">Preserve Guide</span>", "48,000 acres protecting the world's largest seasonal bald eagle gathering.", "chilkat", breadcrumb="Chilkat Preserve"),
        "best_time": hero("Seasonal Planning", f"Best Time To Visit<br/><span class=\"{ACCENT}\">Haines</span>", "Wildlife, weather and cruise season month-by-month for planning your Alaska itinerary.", "best_time", breadcrumb="Best Time To Visit"),
        "schedule": hero("Port Calls · Alaska", f"Haines Cruise<br/><span class=\"{ACCENT}\">Ship Schedule</span>", "When cruise ships visit Haines, typical port hours and how to book excursions early.", "schedule", breadcrumb="Cruise Schedule"),
        "planner": hero("Plan Your Day", f"Haines<br/><span class=\"{ACCENT}\">Cruise Planner</span>", "Checklist your priorities and match the right shore excursions to your ship schedule.", "planner", breadcrumb="Cruise Planner"),
        "faq": hero("Cruise Planning Answers", f"Haines<br/><span class=\"{ACCENT}\">Excursions FAQ</span>", "Port timing, eagles, bears, Skagway comparison and booking independent vs ship tours.", "faq", breadcrumb="FAQ"),
        "enquire": hero("Book &amp; Enquire", f"Enquire About<br/><span class=\"{ACCENT}\">Haines Tours</span>", "Tell us your ship, date and interests — personalised excursion recommendations for your port day.", "enquire", breadcrumb="Enquire"),
    }
    for key, html in heroes.items():
        write(f"partials/hero-{key}.html", html)

    for ex in EXCURSIONS:
        slug = ex["slug"]
        write(f"partials/hero-{slug}.html", hero("Haines Shore Excursion", ex["hero_title"], ex["hero_lead"], ex["image"], breadcrumb=EXC_NAV.get(slug, slug), cta=("enquire", "Enquire about this tour →")))
        write(f"content/{slug}.html", excursion_page(ex["intro"], ex["bullets"], ex["image"], ex["duration"], ex["fitness"], ex["wildlife"], ex["photography"], ex["best_for"], ex["return_ship"], ex["faq"], ex.get("snapshot")))

    contents = {
        "home.html": content_home(),
        "best-haines-shore-excursions.html": content_best(),
        "haines-cruise-port-guide.html": content_port(),
        "things-to-do-in-haines-from-a-cruise-ship.html": content_things(),
        "haines-wildlife-guide.html": content_wildlife(),
        "haines-bald-eagle-guide.html": content_eagle_guide(),
        "haines-vs-skagway.html": content_vs_skagway(),
        "chilkoot-lake-guide.html": content_chilkoot_lake_guide(),
        "chilkat-bald-eagle-preserve-guide.html": content_chilkat_guide(),
        "best-time-to-visit-haines.html": content_best_time(),
        "haines-cruise-ship-schedule.html": content_schedule(),
        "haines-cruise-planner.html": content_planner(),
        "haines-faq.html": content_faq(),
        "enquire.html": content_enquire(),
    }
    for name, html in contents.items():
        write(f"content/{name}", html)

    faq_qa = [
        ("How long do cruise ships stay in Haines?", "Most calls are 6 to 10 hours."),
        ("Is Haines a tender port?", "No — ships dock at the Haines pier."),
        ("When is best for bald eagles?", "Peak Oct–Feb at Chilkat; summer calls still see eagles."),
        ("Can I see bears on a port day?", "Yes during salmon season with guided Chilkoot tours."),
        ("Haines or Skagway for wildlife?", "Haines for eagles and bears; Skagway for railway history."),
        ("Ship excursion or book independently?", "Ship tours guarantee wait-if-late; reputable locals plan buffer returns."),
    ]

    pages = [
        dict(slug="", file_content="home.html", title=f"{SITE} | Bald Eagles, Chilkoot Lake &amp; Wildlife Tours from Haines Cruise Port", description="Plan Haines shore excursions for Alaska cruise passengers — bald eagle viewing, Chilkoot Lake wildlife, Fort Seward tours and scenic wilderness from the Haines cruise pier.", keywords="Haines shore excursions, Haines Alaska cruise excursions, bald eagle tours Haines, Chilkoot Lake wildlife cruise", data_page="home", hero="partials/hero-home.html", preload=IMG["home"][0], extra_schema=[{"@context": "https://schema.org", "@type": "WebSite", "name": SITE, "url": f"{DOMAIN}/", "description": "Independent Haines Alaska shore excursion planning guide"}]),
        dict(slug="best-haines-shore-excursions", file_content="best-haines-shore-excursions.html", title="Best Haines Shore Excursions | Compare Alaska Cruise Tours", description="Compare the best Haines shore excursions — bald eagle viewing, Chilkoot Lake wildlife, river tours, photography and Fort Seward with cruise timing.", keywords="best Haines shore excursions, Haines cruise port tours, compare Haines excursions", data_page="excursions", hero="partials/hero-best.html", preload=IMG["best"][0]),
        dict(slug="haines-cruise-port-guide", file_content="haines-cruise-port-guide.html", title="Haines Cruise Port Guide | Alaska Cruise Passenger Guide", description="Haines cruise port guide — pier location, pickup logistics, weather, wildlife seasons and top shore excursions for your ship schedule.", keywords="Haines cruise port guide, Haines Alaska cruise port, Haines port day", data_page="port", hero="partials/hero-port.html", preload=IMG["port"][0]),
        dict(slug="things-to-do-in-haines-from-a-cruise-ship", file_content="things-to-do-in-haines-from-a-cruise-ship.html", title="Things To Do In Haines From A Cruise Ship | Port Day Guide", description="How to spend your Haines port day from a cruise ship — wildlife morning, Fort Seward afternoon and sample timeline with return buffer.", keywords="things to do Haines cruise ship, Haines port day itinerary, one day Haines Alaska", data_page="port", hero="partials/hero-things.html", preload=IMG["things"][0]),
        dict(slug="haines-wildlife-guide", file_content="haines-wildlife-guide.html", title="Haines Wildlife Guide | Eagles, Bears &amp; Marine Life for Cruise Guests", description="Haines wildlife guide for cruise passengers — bald eagles, brown bears, moose, seals and salmon by season at Chilkoot and Chilkat.", keywords="Haines wildlife guide, bear viewing Haines cruise, Alaska wildlife shore excursion", data_page="wildlife", hero="partials/hero-wildlife.html", preload=IMG["wildlife"][0]),
        dict(slug="haines-bald-eagle-guide", file_content="haines-bald-eagle-guide.html", title="Haines Bald Eagle Guide | Chilkat Preserve &amp; Eagle Viewing Tips", description="Haines bald eagle guide — Chilkat Bald Eagle Preserve seasons, summer cruise sightings and photography tips for eagle viewing tours.", keywords="Haines bald eagle guide, Chilkat eagle preserve cruise, bald eagle tours Haines Alaska", data_page="eagles", hero="partials/hero-eagle_guide.html", preload=IMG["eagles"][0]),
        dict(slug="haines-vs-skagway", file_content="haines-vs-skagway.html", title="Haines vs Skagway: Which Alaska Cruise Port Is Better?", description="Haines vs Skagway compared for cruise passengers — wildlife and authentic Alaska versus Gold Rush railway history and crowds.", keywords="Haines vs Skagway, which Alaska cruise port better, Haines or Skagway wildlife", data_page="port", hero="partials/hero-vs_skagway.html", preload=IMG["skagway"][0]),
        dict(slug="chilkoot-lake-guide", file_content="chilkoot-lake-guide.html", title="Chilkoot Lake Guide | Haines Wildlife &amp; Scenery for Cruise Guests", description="Chilkoot Lake State Park guide — bears, eagles, glacier-fed water and shore excursions from Haines cruise port.", keywords="Chilkoot Lake guide Haines, Chilkoot Lake wildlife cruise, Haines lake tour", data_page="wildlife", hero="partials/hero-chilkoot_lake.html", preload=IMG["chilkoot_lake"][0]),
        dict(slug="chilkat-bald-eagle-preserve-guide", file_content="chilkat-bald-eagle-preserve-guide.html", title="Chilkat Bald Eagle Preserve Guide | Haines Eagle Viewing", description="Chilkat Bald Eagle Preserve guide — world's largest eagle gathering, seasons and tours from Haines Alaska cruise port.", keywords="Chilkat Bald Eagle Preserve guide, Chilkat eagle preserve Haines, eagle preserve Alaska cruise", data_page="eagles", hero="partials/hero-chilkat.html", preload=IMG["chilkat"][0]),
        dict(slug="best-time-to-visit-haines", file_content="best-time-to-visit-haines.html", title="Best Time To Visit Haines | Alaska Cruise &amp; Wildlife Seasons", description="Best time to visit Haines — cruise season months, salmon runs, bear viewing and peak bald eagle concentrations by season.", keywords="best time visit Haines Alaska, Haines cruise season, Haines wildlife season", data_page="port", hero="partials/hero-best_time.html", preload=IMG["best_time"][0]),
        dict(slug="haines-cruise-ship-schedule", file_content="haines-cruise-ship-schedule.html", title="Haines Cruise Ship Schedule | Alaska Port Call Planning", description="Haines cruise ship schedule — when ships visit, typical port hours and how to book shore excursions early.", keywords="Haines cruise ship schedule, Haines port calls, Alaska cruise Haines dates", data_page="port", hero="partials/hero-schedule.html", preload=IMG["schedule"][0]),
        dict(slug="haines-cruise-planner", file_content="haines-cruise-planner.html", title="Haines Cruise Planner | Shore Excursion Checklist", description="Interactive Haines cruise planner — checklist your priorities and match shore excursions to your Alaska port day.", keywords="Haines cruise planner, plan Haines port day, Haines excursion checklist", data_page="port", hero="partials/hero-planner.html", preload=IMG["planner"][0], trust=False),
        dict(slug="haines-faq", file_content="haines-faq.html", title="Haines Shore Excursions FAQ | Alaska Cruise Planning", description="FAQ for Haines shore excursions — port hours, eagles, bears, Skagway comparison and independent vs ship booking.", keywords="Haines shore excursions FAQ, Haines cruise port questions, Haines Alaska FAQ", data_page="faq", hero="partials/hero-faq.html", preload=IMG["faq"][0], extra_schema=[faq_schema(faq_qa)]),
        dict(slug="enquire", file_content="enquire.html", title="Enquire | Book Haines Shore Excursions for Cruise Passengers", description="Enquire about Haines shore excursions — tell us your ship, date and interests for personalised tour recommendations.", keywords="book Haines shore excursions, enquire Haines cruise tours, Haines excursion enquiry", data_page="excursions", hero="partials/hero-enquire.html", preload=IMG["enquire"][0], trust=False),
    ]

    for ex in EXCURSIONS:
        slug = ex["slug"]
        pages.append(dict(slug=slug, file_content=f"{slug}.html", title=f"{EXC_NAV[slug]} | Haines Shore Excursion for Cruise Passengers", description=ex["intro"].split(". ")[0] + ".", keywords=f"Haines {slug.replace('-', ' ')}, Haines cruise excursion, Alaska shore tour Haines", data_page="excursions", hero=f"partials/hero-{slug}.html", preload=IMG[ex["image"]][0], extra_schema=[faq_schema(ex["faq"])]))

    for p in pages:
        slug = p["slug"]
        name = p["title"].split("|")[0].strip()
        schemas = [breadcrumb_schema(slug, name)] + p.get("extra_schema", [])
        html = page_shell(title=p["title"], description=p["description"], keywords=p["keywords"], slug=slug, data_page=p["data_page"], hero=p["hero"], content=p["file_content"], preload=p["preload"], trust=p.get("trust", True))
        html = inject_schemas(html, schemas)
        write_page(slug, html)

    write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {DOMAIN}/sitemap.xml\n")
    sitemap_slugs = [p["slug"] for p in pages]
    lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    priorities = {"": "1.0", "best-haines-shore-excursions": "0.9", "haines-cruise-port-guide": "0.8"}
    for slug in sitemap_slugs:
        loc = f"{DOMAIN}/" if not slug else f"{DOMAIN}/{slug}"
        lines += ["  <url>", f"    <loc>{loc}</loc>", f"    <lastmod>{DATE}</lastmod>", "    <changefreq>monthly</changefreq>", f"    <priority>{priorities.get(slug, '0.7')}</priority>", "  </url>"]
    lines.append("</urlset>")
    write("sitemap.xml", "\n".join(lines) + "\n")

    write("package.json", '{\n  "name": "haines-shore-excursions",\n  "private": true,\n  "scripts": {\n    "build": "python3 scripts/build-haines-site.py",\n    "deploy": "wrangler deploy",\n    "preview": "python3 -m http.server 8903"\n  },\n  "devDependencies": {\n    "wrangler": "^4.94.0"\n  }\n}\n')
    write("wrangler.jsonc", '{\n  "$schema": "node_modules/wrangler/config-schema.json",\n  "name": "haines-shore-excursions",\n  "compatibility_date": "2026-06-24",\n  "observability": { "enabled": true },\n  "assets": {\n    "directory": ".",\n    "html_handling": "auto-trailing-slash"\n  },\n  "routes": [\n    {\n      "pattern": "hainesshoreexcursions.com",\n      "custom_domain": true\n    }\n  ]\n}\n')
    write("deploy.sh", f"#!/bin/bash\nset -euo pipefail\ncd \"$(dirname \"$0\")\"\nif [[ ! -f node_modules/.bin/wrangler ]]; then npm install; fi\necho \"Deploying {SITE} to Cloudflare...\"\nnpx wrangler deploy\necho \"Done. Check {DOMAIN}/ shortly.\"\n")
    (ROOT / "deploy.sh").chmod(0o755)
    write("images/ATTRIBUTION.md", "# Image attribution\n\nLocal Alaska photography assets for Haines Shore Excursions.\n")
    print("Done.")


if __name__ == "__main__":
    main()
