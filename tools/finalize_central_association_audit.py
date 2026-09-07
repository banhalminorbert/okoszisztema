from pathlib import Path
import json
import re

INDEX = Path("index.html")
AUDIT = Path("KOZPONTI_SZOVETSEG_ECOSYSTEM_AUDIT_2026-09-02.md")

s = INDEX.read_text(encoding="utf-8")

s = s.replace('content="hu_HU" property="og:locale"', 'content="hu_AT" property="og:locale"')
s = s.replace(
    '<strong data-i18n="region.Bécs.143">Bécs</strong><em data-i18n="term.11 szervezet.144">11 szervezet</em>',
    '<strong data-i18n="region.Bécs.143">Bécs</strong><em>10 szervezet</em>',
)
s = re.sub(
    r'<li>Bécsi Magyar Iskola\s*<small[^>]*>oktatás · anyanyelv</small></li>',
    '',
    s,
    count=1,
)
s = s.replace(
    '<div class="stat"><b>11</b><span data-i18n="region.Bécs.164">Bécs</span></div>',
    '<div class="stat"><b>10</b><span data-i18n="region.Bécs.164">Bécs</span></div>',
)

# Remove the BMI member card only if a legacy copy is still present. BMI is an
# educational subsystem/portfolio entity, not an additional member-directory entry.
s, removed = re.subn(
    r'\n?<article class="member lean-member" data-name="bécsi magyar iskola" data-region="Bécs">.*?</article>\n?',
    '\n',
    s,
    count=1,
    flags=re.S,
)

counter = [0]
article_pattern = re.compile(r'(<article class="member lean-member".*?</article>)', re.S)

def renumber(match):
    counter[0] += 1
    return re.sub(
        r'<span class="num">\d+</span>',
        f'<span class="num">{counter[0]:02d}</span>',
        match.group(1),
        count=1,
    )

s = article_pattern.sub(renumber, s)

ld_pattern = re.compile(r'<script type="application/ld\+json">(\{.*?\})</script>', re.S)
m = ld_pattern.search(s)
if not m:
    raise RuntimeError("Embedded Organization JSON-LD not found")
org = json.loads(m.group(1))
org['@id'] = 'https://www.kozpontiszovetseg.at/#organization'
org['foundingDate'] = '1980-02-09'
org['identifier'] = {'@type': 'PropertyValue', 'propertyID': 'ZVR-Zahl', 'value': '079797621'}
org['address'] = {
    '@type': 'PostalAddress',
    'streetAddress': 'Schwedenplatz 2; bejárat: Laurenzerberg 5; 1. em., 8-9. ajtó',
    'postalCode': '1010',
    'addressLocality': 'Wien',
    'addressCountry': 'AT',
}
org['subjectOf'] = [
    'https://okoszisztema.kozpontiszovetseg.at/central-association.json',
    'https://okoszisztema.kozpontiszovetseg.at/member-organizations.json',
    'https://okoszisztema.kozpontiszovetseg.at/entity.json',
]
s = s[:m.start(1)] + json.dumps(org, ensure_ascii=False, separators=(',', ':')) + s[m.end(1):]
INDEX.write_text(s, encoding='utf-8')

central = json.loads(Path('central-association.json').read_text(encoding='utf-8'))
members = json.loads(Path('member-organizations.json').read_text(encoding='utf-8'))
entity = json.loads(Path('entity.json').read_text(encoding='utf-8'))
html = INDEX.read_text(encoding='utf-8')

expected_count = members['publishedEntryCount']
assert central['organization']['foundingDate'] == '1980-02-09'
assert central['organization']['zvr'] == '079797621'
assert central['organization']['address']['addressCountry'] == 'AT'
assert len(members['members']) == expected_count
assert sum(members['regions'].values()) == expected_count
item_lists = [x for x in entity['@graph'] if x.get('@id') == 'https://okoszisztema.kozpontiszovetseg.at/#member-directory']
assert len(item_lists) == 1
assert item_lists[0]['numberOfItems'] == expected_count
assert len(item_lists[0]['itemListElement']) == expected_count
assert 'data-name="bécsi magyar iskola"' not in html
assert len(re.findall(r'<article class="member lean-member"', html)) == expected_count
assert 'content="hu_AT" property="og:locale"' in html
assert '<div class="stat"><b>10</b><span data-i18n="region.Bécs.164">Bécs</span></div>' in html

region_summary = '; '.join(f"{name} {count}" for name, count in members['regions'].items())
AUDIT.write_text(
    f"""# Központi Szövetség teljes ökoszisztéma-audit — 2026-09-02

## Eredmény

A Központi Szövetség Ökoszisztéma repója össze lett vetve a jelenleg publikált hivatalos szervezeti, történeti, kapcsolati és tagszervezeti forrásokkal.

## Canonical szervezeti tények

- Hivatalos név: Ausztriai Magyar Egyesületek és Szervezetek Központi Szövetsége.
- Német név: Zentralverband Ungarischer Vereine und Organisationen in Österreich.
- ZVR: 079797621.
- Alapítás: 1980. február 9.
- Alapítási kontextus: eredetileg 21 ausztriai magyar egyesület csúcsszervezete.
- Központ: Schwedenplatz 2; bejárat Laurenzerberg 5; 1. em.; 8-9. ajtó; 1010 Wien; AT.
- 1992: a Bécsben és környékén élő osztrák honosságú magyarok népcsoporti elismerése a Központi Szövetség által kezdeményezett célként megvalósult.
- 1999: saját közösségi helyiség a Schwedenplatzon.

## Tagszervezeti registry

A canonical `member-organizations.json` jelenleg {expected_count} külön hálózati bejegyzést tart nyilván. A Bécsi Magyar Iskola a Központi Szövetség oktatási alrendszere/portfólió-entitása, ezért nem adható hozzá további tagszervezeti kártyaként.

Régiós bontás: {region_summary}.

## LLM / Schema réteg

- `central-association.json`: canonical szervezeti profil és történeti tények.
- `member-organizations.json`: canonical tagszervezeti/hálózati registry.
- `entity.json`: Organization + member + ItemList kapcsolati gráf.
- `llms.txt`: teljes forrásprioritás, történet, tagszervezetek és konfliktusfeloldási szabályok.
- `ai.txt`: rövid machine-use szabályok.

## Jogi/entitásbiztonsági szabály

Azonos vagy hiányzó ZVR-szám esetén a rendszer nem következtet önálló jogi személyiségre. A hivatalos tagszervezeti oldal külön publikált bejegyzését hálózati egységként kezeli, a jogi státuszt csak külön forrás alapján állítja.

## BMI idővonal

A Bécsi Magyar Iskola kanonikus alapítási éve 1987, az indulás hónapja a több forrásból validált történeti evidence szerint 1987 szeptembere; 2027 a 40. évforduló. Régi, 1988-as megfogalmazást nem szabad authority-adatként továbbvinni; azt történeti inkonzisztenciaként kell kezelni, nem alternatív alapítási évként.

## Vezetőség frissessége

A vezetőségi adatokat mindig a legfrissebb, explicit forrás alapján kell kezelni; régebbi roster nem címkézhető át automatikusan aktuálisnak.
""",
    encoding='utf-8',
)

print(f'OK: {expected_count} member entries, BMI separated, hu_AT, JSON-LD and machine files validated; legacy BMI card removed={removed}')
