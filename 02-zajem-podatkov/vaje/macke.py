
import csv
import os
import requests
import re

############################################################################
# 1.a preberi spletno stran
# 1.b shrani spletnostran
# 1.c prečekiri če spletna stran res obstaja
#################
# 2.a preberi fajl
# 2.b napiš seznam oglasov
# 
############################################################################


###############################################################################
# Najprej definirajmo nekaj pomožnih orodij za pridobivanje podatkov s spleta.
###############################################################################

# definiratje URL glavne strani bolhe za oglase z maĝkami
cats_frontpage_url = 'http://www.bolha.com/zivali/male-zivali/macke/'
# mapa, v katero bomo shranili podatke
cat_directory = 'macke'
# ime datoteke v katero bomo shranili glavno stran
frontpage_filename = 'frontpage.html'
# ime CSV datoteke v katero bomo shranili podatke
csv_filename = 'TODO'


def download_url_to_string(url):
    """Funkcija kot argument sprejme niz in puskuša vrniti vsebino te spletne
    strani kot niz. V primeru, da med izvajanje pride do napake vrne None.
    """
    try:
        # del kode, ki morda sproži napako
        page_content = requests.get(url).text
    except requests.exeptions.RequestException as e:
        # koda, ki se izvede pri napaki
        print (e)
        page_content = ''
        # dovolj je ĝe izpišemo opozorilo in prekinemo izvajanje funkcije
        raise NotImplementedError()
    # nadaljujemo s kodo ĝe ni prišlo do napake
    return page_content                             #raise vrne error


def save_string_to_file(text, directory, filename):
    """Funkcija zapiše vrednost parametra "text" v novo ustvarjeno datoteko
    locirano v "directory"/"filename", ali povozi obstojeĝo. V primeru, da je
    niz "directory" prazen datoteko ustvari v trenutni mapi.
    """
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, filename)
    with open(path, 'w', encoding='utf-8') as file_out:
        file_out.write(text)
    return None


# Definirajte funkcijo, ki prenese glavno stran in jo shrani v datoteko.


def save_frontpage(page, directory, filename):
    """Funkcija shrani vsebino spletne strani na naslovu "page" v datoteko
    "directory"/"filename"."""
    content = download_url_to_string(page)
    save_string_to_file(content, directory, filename)
    return


###############################################################################
# Po pridobitvi podatkov jih želimo obdelati.
###############################################################################


def read_file_to_string(directory, filename):
    """Funkcija vrne celotno vsebino datoteke "directory"/"filename" kot niz"""
    path = os.path.join(directory, filename)
    with open(path, 'r') as d:
        vsebina = d.read()
    return vsebina


# Definirajte funkcijo, ki sprejme niz, ki predstavlja vsebino spletne strani,
# in ga razdeli na dele, kjer vsak del predstavlja en oglas. To storite s
# pomoĝjo regularnih izrazov, ki oznaĝujejo zaĝetek in konec posameznega
# oglasa. Funkcija naj vrne seznam nizov.

vzorec = (
    r'<h3><a title="(?P<Naslov>.*?)'
    r'" href="(?P<Povezava>.*?)"'
    r'>.*?</h3>\n\n(\s*(?P<Opis>.*?)\\?\s{3,}.*?)'
    r'(\n\n.*?)*?'
    r'<div class="price">'
    r'(?P<Cena>.*?)\\?'
    r'</div>'
)

def page_to_ads_moja(directory, filename):
    """Funkcija poišĝe posamezne ogllase, ki se nahajajo v spletni strani in
    vrne njih seznam"""
    seznam = []
    vsebina = read_file_to_string(directory, filename)
    for zadetek in re.finditer(vzorec, vsebina):
        seznam.append(zadetek.groupdict())
    return seznam

def page_to_ads(page_content):

    exp = r'<div class="ad">(.*?)<div class="cleas"></div>'
    expp = re.compile(exp, re.DOTALL)

    return re.findall(exp, page_content)   #ta zadeva ti naredi seznam

#.*<a title="(?P<naslov>.*)" href".*</h3>\s*(?P<vsebina>.*?)<div .*?<b>(?P<rodovnik>.*?)</b>
# Definirajte funkcijo, ki sprejme niz, ki predstavlja oglas, in izlušĝi
# podatke o imenu, ceni in opisu v oglasu.


def get_dict_from_ad_block(directory, filename):
    """Funkcija iz niza za posamezen oglasni blok izlušĝi podatke o imenu, ceni
    in opisu ter vrne slovar, ki vsebuje ustrezne podatke
    """
    seznam = page_to_ads(directory, filename)
    slovar = {}
    for i in range( len(seznam)):
        slovar[f'oglas_{i}'] = {}
        print(slovar)
        podseznam = seznam[i]
        print(podseznam)
        for j in ('Naslov', 'Cena', 'Opis'):
            slovar[f'oglas_{i}'][j] = podseznam[j]

    return slovar

# Definirajte funkcijo, ki sprejme ime in lokacijo datoteke, ki vsebuje
# besedilo spletne strani, in vrne seznam slovarjev, ki vsebujejo podatke o
# vseh oglasih strani.


def ads_from_file(directory, filename):
    """Funkcija prebere podatke v datoteki "directory"/"filename" in jih
    pretvori (razĝleni) v pripadajoĝ seznam slovarjev za vsak oglas posebej."""
    return get_dict_from_ad_block(directory, filename)


###############################################################################
# Obdelane podatke želimo sedaj shraniti.
###############################################################################


def write_csv(fieldnames, rows, directory, filename):
    """
    Funkcija v csv datoteko podano s parametroma "directory"/"filename" zapiše
    vrednosti v parametru "rows" pripadajoĝe kljuĝem podanim v "fieldnames"
    """
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, filename)
    with open(path, 'w') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
    return


# Definirajte funkcijo, ki sprejme neprazen seznam slovarjev, ki predstavljajo
# podatke iz oglasa maĝke, in zapiše vse podatke v csv datoteko. Imena za
# stolpce [fieldnames] pridobite iz slovarjev.


def write_cat_ads_to_csv(ads, directory, filename):
    """Funkcija vse podatke iz parametra "ads" zapiše v csv datoteko podano s
    parametroma "directory"/"filename". Funkcija predpostavi, da sa kljuĝi vseh
    sloverjev parametra ads enaki in je seznam ads neprazen.

    """
    # Stavek assert preveri da zahteva velja
    # Če drži se program normalno izvaja, drugaĝe pa sproži napako
    # Prednost je v tem, da ga lahko pod doloĝenimi pogoji izklopimo v
    # produkcijskem okolju
    assert ads and (all(j.keys() == ads[0].keys() for j in ads))
    raise NotImplementedError()


# Celoten program poženemo v glavni funkciji

def main(redownload=True, reparse=True):
    """Funkcija izvede celoten del pridobivanja podatkov:
    1. Oglase prenese iz bolhe
    2. Lokalno html datoteko pretvori v lepšo predstavitev podatkov
    3. Podatke shrani v csv datoteko
    """
    # Najprej v lokalno datoteko shranimo glavno stran

    # Iz lokalne (html) datoteke preberemo podatke

    # Podatke prebermo v lepšo obliko (seznam slovarjev)

    # Podatke shranimo v csv datoteko

    # Dodatno: S pomoĝjo parameteov funkcije main omogoĝi nadzor, ali se
    # celotna spletna stran ob vsakem zagon prense (ĝetudi že obstaja)
    # in enako za pretvorbo

    raise NotImplementedError()


#if __name__ == '__main__':
#    main()
