import os

__author__ = 'Mark Weinreuter'
__ordner_pfad = os.path.dirname(__file__)


def liste_ausgeben(liste):
    for l in liste:
        print(l)


def ordner_pfad():
    return __ordner_pfad


def kombiniere_pfad(*pfade):
    return os.path.join(*pfade)


def existiert_datei(pfad):
    return os.path.exists(pfad)


def existiert_datei_fehler(pfad):
    ex = existiert_datei(pfad)
    if not ex:
        print("Die Datei: '%s' existiert nicht." % pfad)

    return ex


def lese_datei(dateipfad, start_ordner="", modus="r", encoding="utf-8"):
    pfad = os.path.join(start_ordner, dateipfad)

    if not existiert_datei(pfad):
        print("Die Datei: '%s' existiert nicht!" % pfad)
        return None

    try:
        with open(pfad, mode=modus, encoding=encoding) as datei:
            inhalt = datei.read()
            return inhalt

    except IOError as e:
        print("Es ist ein Fehler beim Laden der Datei aufgetreten: ", e)

    return None


def liste_dateien_rekursiv(pfad, endungen=(), start_ordner="", ergebnis_liste=None):
    kompletter_pfad = kombiniere_pfad(start_ordner, pfad)

    if not existiert_datei(kompletter_pfad) or not os.path.isdir(kompletter_pfad):
        print("Der Pfad '%s' existiert nicht oder ist kein Ordner!" % kompletter_pfad)
        return []

    dateien = os.listdir(kompletter_pfad)

    if isinstance(endungen, str):
        endungen = (endungen)

    if ergebnis_liste is None:
        ergebnis_liste = []

    for datei in dateien:

        neuer_pfad = os.path.join(kompletter_pfad, datei)

        if os.path.isdir(neuer_pfad):
            liste_dateien_rekursiv(neuer_pfad, endungen, ergebnis_liste=ergebnis_liste)
            continue

        pos = datei.rfind(".")
        if len(endungen) == 0 or (pos > -1 and datei[pos + 1:] in endungen):
            ergebnis_liste.append(neuer_pfad)

    return ergebnis_liste


def pfade_und_schluessel(pfade, schluessel):
    if isinstance(pfade, str) and isinstance(schluessel, str):
        pfade = [pfade]
        schluessel = [schluessel]

    elif isinstance(schluessel, str):
        if len(pfade) > 1:
            schluessel = [schluessel + "_%d" % i for i in range(0, len(pfade))]
        else:
            schluessel = [schluessel]

    elif isinstance(pfade, str) and not isinstance(schluessel, str):
        print("Ungültige Anzahl von Pfaden und Schlüsseln! Gib entweder ein Bild und Schlüssel,"
              " einen Liste von Bilder und einen Schlüssel oder eine Liste von Bildern und Schlüsseln an")
        return None

    if len(schluessel) != len(pfade):
        print("Die Anzahl an Pfaden und Schlüssel muss gleich sein.")
        return None

    return zip(pfade, schluessel)


if __name__ == "__main__":
    l = liste_dateien_rekursiv("resourcen", ("png"))
    pus = list(pfade_und_schluessel(["a", "c"], "b"))
    print(pus)
