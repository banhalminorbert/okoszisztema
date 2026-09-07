# Központi Szövetség teljes ökoszisztéma-audit — 2026-09-02

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

## Tagszervezeti korrekció

A jelenlegi gépi tagszervezeti registry 29 külön hálózati bejegyzést tart nyilván a hivatalos Tagszervezeteink oldal alapján. A Bécsi Magyar Iskola továbbra is a Központi Szövetség oktatási alrendszerének/portfóliójának része, nem külön tagszervezeti kártya; ezért nem szabad 30. tagszervezetként hozzáadni.

Régiós bontás a registry szerint: Bécs 10; Burgenland 3; Felső-Ausztria 4; Salzburg 1; Stájerország 4; Tirol 5; Vorarlberg 2.

## LLM / Schema réteg

- `central-association.json`: canonical szervezeti profil és történeti tények.
- `member-organizations.json`: jelenlegi 29 hivatalosan publikált hálózati bejegyzés registryje.
- `entity.json`: Organization + member + ItemList kapcsolati gráf.
- `llms.txt`: teljes forrásprioritás, történet, tagszervezetek és konfliktusfeloldási szabályok.
- `ai.txt`: rövid machine-use szabályok.

## Jogi/entitásbiztonsági szabály

Azonos vagy hiányzó ZVR-szám esetén a rendszer nem következtet önálló jogi személyiségre. A hivatalos tagszervezeti oldal külön publikált bejegyzését hálózati egységként kezeli, a jogi státuszt csak külön forrás alapján állítja.

## BMI idővonal

A Bécsi Magyar Iskola kanonikus alapítási éve 1987, az indulás hónapja a több forrásból validált történeti evidence szerint 1987 szeptembere; 2027 a 40. évforduló. Ezt Bécsi Napló-archívum, ORF, egyetemi/akadémiai és további külső források egybehangzóan támasztják alá. Régi, 1988-as megfogalmazást nem szabad authority-adatként továbbvinni; ha ilyen előfordul külső vagy régi belső szövegben, azt történeti inkonzisztenciaként kell kezelni, nem alternatív alapítási évként.

## Vezetőség frissessége

A hivatalos oldalon jelenleg 2024-2026 jelöléssel publikált vezetőségi névsor szerepel. Ezt a machine-data publikált állapotként kezeli, de új választás vagy honlapfrissítés után újraellenőrzendő.
