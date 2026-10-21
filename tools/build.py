"""Builds site/index.html for the Waste Wearable Art website.

Piece data lives in pieces_src.py (shared with the portfolio artifact).
Run: python3 build.py
"""
import html, os
E = html.escape
HERE = os.path.dirname(os.path.abspath(__file__))
ns = {}
exec(open(os.path.join(HERE, "pieces_src.py")).read(), ns)
P = ns["P"]

# Photos matched from the "single Images for posters" folder (by semester in filename + description).
EXTRA = {
    ("Fall 2025", "Group 19"): [("f25-g19.jpg", "A model in a white dress of layered, fan-folded newspaper tiers raises a paper wand and holds a pleated paper fan, walking a runway between rows of seated audience.")],
    ("Spring 2025", "Group 20"): [("s25-g20.jpg", "A model poses on stage in a teal satin wrap over a dress covered in clear, curling plastic ribbons and sparkling scales that catch the blue stage light.")],
    ("Spring 2024", "Group 9"): [("s24-g9.jpg", "A model stands on a dark stage in a strapless gown with a full skirt of clear, shimmering plastic over ruffled red coral-like layers, lit in blue and pink.")],
}
# Upcycle, recycle or repurpose: how the waste was transformed.
CAT = {
    ("Spring 2026", "Group 1"): "upcycle", ("Spring 2026", "Group 16"): "upcycle",
    ("Fall 2025", "Group 19"): "upcycle", ("Spring 2025", "Group 20"): "upcycle",
    ("Spring 2024", "Group 9"): "upcycle",
    ("Spring 2026", "Group 12"): "recycle", ("Spring 2025", "Group 13"): "recycle",
    ("Spring 2023", "Group 21"): "recycle", ("Spring 2023", "Group 22"): "recycle",
    ("Spring 2026", "Group 5"): "repurpose", ("Spring 2026", "Group 19"): "repurpose",
    ("Fall 2025", "Group 18"): "repurpose", ("Spring 2025", "Group 8"): "repurpose",
    ("Fall 2023", "Honors project"): "repurpose",
}
CATS = {
    "upcycle": dict(name="Upcycle", line="Waste, elevated.",
        lede="Upcycling turns something discarded into something worth more than it ever was. Newspaper becomes a gala gown. Shower curtains become a coral reef.",
        img="upcycle-hero.jpg"),
    "recycle": dict(name="Recycle", line="Single use. Second life.",
        lede="Recycling takes throwaway plastics such as shopping bags, bottles, straws and caps, and puts them back into the cycle as yarn, scales and sea foam.",
        img="recycle-hero.jpg"),
    "repurpose": dict(name="Repurpose", line="Same object. New job.",
        lede="Repurposing gives a thing a new role without breaking it down. A thrifted jacket, a vinyl record, a deck of playing cards or a pair of old jeans becomes part of a look.",
        img="repurpose-hero.jpg"),
}
FAM = {"plastic": "Plastic", "paper": "Paper", "fabric": "Fabric and denim", "mixed": "Mixed materials"}
SHOW = [
    ("hero.jpg", "Fall 2025", "A runway walk through the audience in a fan-folded newspaper gown.", "A model in a white newspaper gown walks between rows of seated students, arm raised."),
    ("show-f25-train.jpg", "Ocean in Distress.", "A trash-bag gown with a long train sweeps across the floor.", "A model in a blue and white plastic gown with a long train stands in front of a seated audience."),
    ("show-s24-hat.jpg", "Spring 2024", "A red top hat and a sash of reused material take the stage.", "A performer in a red top hat, red sleeves and white trousers with a sash of crumpled material strikes a pose on stage."),
    ("show-s24-group.jpg", "Spring 2024", "The whole class on stage after the show.", "Students and their instructor gather on stage in their finished garments beneath a projected runway show poster."),
]

from PIL import Image
IMG = os.path.join(HERE, "..", "img") if os.path.basename(HERE) == "tools" else os.path.join(HERE, "site", "img")
def SIZE(f): return Image.open(os.path.join(IMG, f)).size

def key(p): return (p["sem"], p["grp"])
for p in P:
    if key(p) in EXTRA and not p["imgs"]:
        p["imgs"] = EXTRA[key(p)]
    p["cat"] = CAT[key(p)]
    p["id"] = (p["sem"] + "-" + p["grp"]).lower().replace(" ", "-")
    p["year"], p["term"] = p["sem"].split()[1], p["sem"].split()[0]

def media(p, cls="", eager=False):
    if p["imgs"]:
        f, a = p["imgs"][0]
        lz = "" if eager else ' loading="lazy"'
        w, h = SIZE(f)
        return f'<img class="{cls}" src="img/{f}" alt="{E(a)}" width="{w}" height="{h}"{lz} decoding="async">'
    return (f'<div class="ph {cls}" data-fam="{p["fam"]}" role="img" aria-label="Photo coming soon">'
            f'<span>{E(FAM[p["fam"]])}</span><small>Runway photo coming soon</small></div>')

def chips(p): return "".join(f"<li>{E(m)}</li>" for m in p["mats"])

def feature(p, i):
    side = "flip" if i % 2 else ""
    return f'''<article class="feature {side} reveal" id="{p["id"]}" aria-labelledby="{p["id"]}-t">
<button class="feature-media" type="button" data-open="{p["id"]}" aria-label="Open {E(p["title"])}">{media(p)}</button>
<div class="feature-text">
<p class="credit">{E(p["grp"])} · {E(p["sem"])}</p>
<h3 id="{p["id"]}-t">{E(p["title"])}</h3>
<p class="blurb">{E(p["blurb"])}</p>
<ul class="mats" aria-label="Materials">{chips(p)}</ul>
<button class="more" type="button" data-open="{p["id"]}">Read the design concept <span aria-hidden="true">›</span></button>
</div></article>'''

def tile(p):
    return f'''<li class="tile reveal"><button type="button" data-open="{p["id"]}">
{media(p)}<span class="tile-cap"><span class="cat-tag" data-cat="{p["cat"]}">{CATS[p["cat"]]["name"]}</span>
<strong>{E(p["title"])}</strong><span class="credit">{E(p["grp"])}</span></span></button></li>'''

# Category views
cat_views = ""
for c, d in CATS.items():
    items = [p for p in P if p["cat"] == c]
    rows = "".join(feature(p, i) for i, p in enumerate(items))
    cat_views += f'''<section class="view" data-view="{c}" aria-labelledby="{c}-h" hidden>
<header class="cat-hero" data-cat="{c}">
<div class="wrap cat-hero-in"><div>
<p class="eyebrow">{len(items)} pieces</p>
<h1 id="{c}-h" tabindex="-1"><span class="grad">{d["name"]}.</span> {d["line"]}</h1>
<p class="lede">{d["lede"]}</p>
</div><div class="cat-hero-img" aria-hidden="true"><img src="img/{d["img"]}" alt="" width="{SIZE(d["img"])[0]}" height="{SIZE(d["img"])[1]}"></div></div></header>
<div class="wrap features">{rows}</div>
</section>'''

# Semester view: year switcher, then term switcher within the year
years = []
for p in P:
    if p["year"] not in years: years.append(p["year"])
years.sort(reverse=True)
terms = {y: [] for y in years}
for p in P:
    if p["term"] not in terms[p["year"]]: terms[p["year"]].append(p["term"])
ORDER = {"Fall": 0, "Spring": 1}
for y in terms: terms[y].sort(key=lambda t: ORDER[t])
year_btns = "".join(f'<button type="button" role="tab" data-year="{y}" aria-selected="false">{y}</button>' for y in years)
panels = ""
for y in years:
    tb = "".join(f'<button type="button" data-term="{t}" aria-pressed="false">{t} {y}</button>' for t in terms[y])
    grids = ""
    for t in terms[y]:
        ps = [p for p in P if p["year"] == y and p["term"] == t]
        n = len(ps)
        grids += (f'<div class="term" data-term="{t}" hidden><p class="term-head"><strong>{t} {y}</strong> '
                  f'<span>{n} piece{"s" if n > 1 else ""} on the runway</span></p>'
                  f'<ul class="tiles">{"".join(tile(p) for p in ps)}</ul></div>')
    panels += f'<div class="year" role="tabpanel" data-year="{y}" aria-label="{y}" hidden><div class="terms" role="group" aria-label="Semester">{tb}</div>{grids}</div>'

# Overview pillars and gallery
pillars = ""
for c, d in CATS.items():
    n = sum(1 for p in P if p["cat"] == c)
    pillars += f'''<a class="pillar reveal" href="#{c}" data-cat="{c}">
<img src="img/{d["img"]}" alt="" width="880" height="1100" loading="lazy">
<span class="pillar-text"><span class="pillar-name">{d["name"]}</span><span class="pillar-line">{d["line"]}</span>
<span class="pillar-link">{n} pieces <span aria-hidden="true">›</span></span></span></a>'''
gallery = "".join(f'''<li><figure><img src="img/{f}" alt="{E(a)}" loading="lazy" width="1200" height="900">
<figcaption><strong>{s}</strong> {E(cap)}</figcaption></figure></li>''' for f, s, cap, a in SHOW[1:])

# Data for the detail sheet
import json
DATA = {p["id"]: dict(t=p["title"], c=f'{p["grp"]} · {p["sem"]}', cat=CATS[p["cat"]]["name"], k=p["cat"],
        b=p["blurb"], x=p["concept"], m=p["mats"], f=FAM[p["fam"]], fam=p["fam"],
        i=[dict(s="img/" + f, a=a, w=SIZE(f)[0], h=SIZE(f)[1]) for f, a in p["imgs"]]) for p in P}

tpl = open(os.path.join(HERE, "template.html")).read()
out = (tpl.replace("%%CATVIEWS%%", cat_views).replace("%%YEARBTNS%%", year_btns).replace("%%YEARS%%", panels)
       .replace("%%PILLARS%%", pillars).replace("%%GALLERY%%", gallery).replace("%%N%%", str(len(P)))
       .replace("%%NS%%", str(sum(len(v) for v in terms.values())))
       .replace("%%DATA%%", json.dumps(DATA, ensure_ascii=False).replace("</", "<\\/")))
open(os.path.join(HERE, "..", "index.html"), "w").write(out)
print("built", len(out), "bytes,", len(P), "pieces")
