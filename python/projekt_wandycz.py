# zaimportowanie potrzebnych bibliotek
import pygame, random, sys, time
from pygame.locals import *

# inicjalizacja wszysktich modułów biblioteki pygame
pygame.init()

# załadowanie obrazków
student = pygame.image.load('student.png')
piec = pygame.image.load('5.png')
dwa = pygame.image.load('2.png')
trzy = pygame.image.load('3.png')
cztery = pygame.image.load('4.png')
tlo = pygame.image.load('tlo.png')
tlo_game_over = pygame.image.load('tloover.png')

# kilka kolorów w rgb
czarny = (0, 0, 0)
bialy = (255, 255, 255)
jaskrawy_czerwony = (255, 0, 0)
ladny_niebieski = (206, 238, 255)
ladny_zielony = (108, 153, 142)
guzikowy_niebieski = (6, 146, 221)
ruby = (191, 59, 101)

# stworzenie okna i podstawowych parametrów
szerokosc = 1000
wysokosc = 600
okno = pygame.display.set_mode((szerokosc, wysokosc)) # otworzenie okna, w którym będzie gra
zegar = pygame.time.Clock() # ile razy na sekundę gra się odświeża
pygame.display.set_caption('Symulacja studenta') # tytul okna
# pygame.mouse.set_visible(False) # ukrycie kursora

# stworzenie klasy gracza
class Gracz:
    def __init__(self, postac, szybkosc, px, py, hitbox_x, hitbox_y):

        '''
        Klasa Gracz przechowuje informacje o parametrach postaci, którą gramy.

        :param postac: obraz, jakim będziemy sterować
        :param szybkosc: prędkość przemieszczania się
        :param px: współrzędna położenia postaci w poziomie względem okna gry
        :param py: współrzędna położenia postaci w pionie względem okna gry
        :param hitbox_x: obszar poziomy, w którym po uderzeniu w inny obiekt zachodzi interakcja
        :param hitbox_y: obszar pionowy, w którym po uderzeniu w inny obiekt zachodzi interakcja
        '''

        self.szybkosc = szybkosc
        self.postac = postac
        self.px = px
        self.py = py
        self.hitbox_x = hitbox_x
        self.hitbox_y = hitbox_y

# stworzenie klasy obiektów
class Obiekt:
    def __init__(self, rzecz, spadanie, x, y, hitbox_x, hitbox_y):

        '''
        Klasa Obiekt przechowuje informacje o obiektach, które wchodzą w interakcje z naszą postacią.

        :param rzecz: obraz, który się pojawia
        :param spadanie: prędkość, z jaką dany obiekt spada
        :param x: współrzędna położenia obiektu w poziomie względem okna gry
        :param y: współrzędna położenia obiektu w pionie względem okna gry
        :param hitbox_x: obszar poziomy, w którym po uderzeniu w inny obiekt zachodzi interakcja
        :param hitbox_y: obszar pionowy, w którym po uderzeniu w inny obiekt zachodzi interakcja
        '''

        self.rzecz = rzecz
        self.spadanie = spadanie
        self.x = x
        self.y = y
        self.hitbox_x = hitbox_x
        self.hitbox_y = hitbox_y

class Przycisk:
    def __init__(self, napis, x, y, w, h, akcja=None):

        '''
        Klasa Przycisk przechowuje informacje o przyciskach, które pojawiają się na ekranie startowym.

        :param napis: tekst, który pojawi się na przycisku
        :param x: górna krawędź przycisku
        :param y: lewa krawędź przycisku
        :param w: szerokość
        :param h: wyskość
        :param akcja: jaka akcja następuje po naciśnięciu przycisku
        '''

        mysz = pygame.mouse.get_pos() # pobiera aktualną pozycję kursora
        klik = pygame.mouse.get_pressed() # czy mysz została przyciśnięta
        print(klik)

        # jeśli najedziemy myszą w odpowiednie miejsce pojawia się przycisk w kolorze czerwonym, w przeciwnym razie przycisk ma kolor niebieski
        if x+w > mysz[0] > x and y+h > mysz[1] > y:
            pygame.draw.rect(okno, jaskrawy_czerwony, (x, y, w, h))
            if klik[0] == 1 and akcja != None:
                # time.sleep() # można użyć opóźnienia, z jakim po kliknięciu dzieje się akcja
                akcja()
        else:
            pygame.draw.rect(okno, guzikowy_niebieski, (x, y, w, h))

        # dodaje tekst na przyciskach
        tekst = pygame.font.Font(None, 25)
        teskt_p, tekst_r = wiadomosc(napis, tekst)
        tekst_r.center = ( (x + (w/2)), (y + (h/2)))
        okno.blit(teskt_p, tekst_r)


# punktacja
def licznik_punktów(licz):

    '''
    Funkcja oblicza punktację.

    :param licz: string z wynikiem na dany moment
    :return: funkcja zwraca napis Wynik: ~obecna ilość punktów~
    '''

    czcionka = pygame.font.SysFont(None, 30)
    tekst = czcionka.render("Średnia:" + str(licz),True, czarny)
    okno.blit(tekst, (0, 0))

# wyświetlanie wiadomości
def wiadomosc(tekst, czcionka):

    '''
    Funkcja przygotowuje tekst.

    :param tekst: tekst, który chcemy wyświetlić
    :param czcionka: wygląd tekstu
    '''

    napis = czcionka.render(tekst, True, ladny_niebieski)
    return napis, napis.get_rect()

def wyswietlanie_wiadomosci(tekst):

    '''
    Funkcja wyświetla tekst na 3 sekundy, po czym powraca do gry

    :param tekst: teskt, który zostaje wyświetlony
    '''

    font = pygame.font.Font(None, 45)
    tekst_p, tekst_r = wiadomosc(tekst, font)
    tekst_r.center = ((szerokosc / 3), (wysokosc /3))
    okno.blit(tekst_p, tekst_r)
    pygame.display.update()
    time.sleep(3)
    gra()

def game_over():

    '''
    Funkcja określa co dzieje się na ekranie końca gry.
    '''

    pygame.mixer.music.load('koniec.mp3')
    pygame.mixer.music.play(-1)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                koniec()

        okno.fill(ruby)
        okno.blit(tlo_game_over, (0, 0))

        font = pygame.font.Font(None, 80)
        tekst_p, tekst_r = wiadomosc('O nie! Przedmiot niezaliczony :(', font)
        tekst_r.center = ((490, 60))
        okno.blit(tekst_p, tekst_r)

        zagraj_znow = Przycisk('Zagraj jeszcze raz', 240, 500, 220, 60, gra)
        wyjdz = Przycisk('Wyjdź z gry', 575, 500, 220, 60, koniec)

        pygame.display.update()
        zegar.tick(20)

def menu_poczatkowe():

    '''
    Funkcja zapętla ekran początkowy aż do momentu, kiedy nie zostanie wybrany następny stan: gra lub wyjście z niej.
    '''

    pygame.mixer.music.load('menu.mp3')
    pygame.mixer.music.play(-1)

    menu = True

    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                koniec()

        okno.fill(bialy)
        okno.blit(tlo, (0, 0))

        font = pygame.font.Font(None, 120)
        tekst_p, tekst_r = wiadomosc('Symulator studenta', font)
        tekst_r.center = ((470, 100))
        okno.blit(tekst_p, tekst_r)

        start_przycisk = Przycisk('Start!', 240, 200, 120, 60, gra)
        stop_przycisk = Przycisk('Zamknij', 575, 200, 120, 60, koniec)


        pygame.display.update()
        zegar.tick(20) # odświeżanie z częstością 20 razy na sekundę



def gra():

    '''
    Funkcja służy do obsługi głównego okna gry. Najpierw Przypisuje konkretne klasy pojawiającym się obiektom, a następnie zapętla grę.
    '''

    gracz = Gracz(student, 7, 200, 400, 120, 100)
    dwoja = Obiekt(dwa, 4, random.randrange(0, szerokosc - 70), -600, 49, 73)
    piatka = Obiekt(piec, 5, random.randrange(0, szerokosc - 70), -600, 49, 73)
    troja = Obiekt(trzy, 4, random.randrange(0, szerokosc - 70), -600, 49, 73)
    czwora = Obiekt(cztery, 4, random.randrange(0, szerokosc - 70), -600, 49, 73)

    pygame.mixer.music.load('muzyka.mp3')
    pygame.mixer.music.play(-1)

    # zainicjowanie zmiennych
    wynik = 0
    ilosc = 0

    def srednia(wynik, ilosc):
        try:
            return wynik / ilosc
        except:
            return int(0)

    x_zmienna = 0

    koniec_gry = False

    while not koniec_gry:
        if koniec_gry:
            game_over()
        else:
            okno.fill(ladny_zielony)  # tło

            # rysowanie obiektów
            okno.blit(dwoja.rzecz, (dwoja.x, dwoja.y))
            okno.blit(piatka.rzecz, (piatka.x, piatka.y))
            okno.blit(troja.rzecz, (troja.x, troja.y))
            okno.blit(czwora.rzecz, (czwora.x, czwora.y))

            # rysowanie postaci gracza
            okno.blit(gracz.postac, (gracz.px, gracz.py))

            # obsługa klawiatury, ustalenie prędkości poruszania się gracza
            for event in pygame.event.get():
                if event.type == QUIT:
                    koniec()
                if event.type == KEYDOWN:
                    if event.key == K_LEFT and gracz.px > 0:
                        x_zmienna = gracz.szybkosc * -1 + -1 * 0.5 * srednia(wynik, ilosc)
                    elif event.key == K_RIGHT and gracz.px < szerokosc - 45:
                        x_zmienna = gracz.szybkosc + 0.5 * srednia(wynik, ilosc)
                if event.type == KEYUP:
                    if event.key == K_LEFT or event.key == K_RIGHT:
                        x_zmienna = 0

            gracz.px += x_zmienna

            # ustalenie granic, za które postać gracza nie może wyjść
            if gracz.px > szerokosc - gracz.hitbox_x or gracz.px < 0:
                x_zmienna = 0

            # ustalenie przeliczników spadania ocen
            piatka.y += piatka.spadanie + 0.1 * srednia(wynik, ilosc)
            dwoja.y += dwoja.spadanie + 1.5 * srednia(wynik, ilosc)
            troja.y += troja.spadanie
            czwora.y += czwora.spadanie + 0.05 * srednia(wynik, ilosc)

            # "zapętlenie" spadania ocen; jeśli wyjdzie poza ekran - powraca do góry
            if piatka.y > wysokosc:
                piatka.y = -10
                piatka.x = random.randrange(0, szerokosc - 70)
            if dwoja.y > wysokosc:
                dwoja.y = -410
                dwoja.x = random.randrange(0, szerokosc - 70)
            if troja.y > wysokosc:
                troja.y = -10
                troja.x = random.randrange(0, szerokosc - 70)
            if czwora.y > wysokosc:
                czwora.y = -10
                czwora.x = random.randrange(0, szerokosc - 70)

            licznik_punktów(round(srednia(wynik, ilosc),2))

            # ustalenie reguł, które mówią, kiedy "dostaje się" daną ocenę
            if gracz.py < dwoja.y + dwoja.hitbox_y:
                if (dwoja.x < gracz.px and dwoja.x + dwoja.hitbox_x > gracz.px) or (dwoja.x > gracz.px and dwoja.x < gracz.px + gracz.hitbox_x) or (dwoja.x > gracz.px and dwoja.x < gracz.px + gracz.hitbox_x):
                    dwoja.y = -100
                    dwoja.x = random.randrange(0, szerokosc - 70)
                    wynik += 2
                    ilosc += 1
                    # efekt_d = pygame.mixer.Sound('dwa_m.wav')
                    # efekt_d.play()

            if gracz.py < troja.y + troja.hitbox_y and gracz.py > troja.y or gracz.py + gracz.hitbox_y > troja.y and gracz.py + gracz.hitbox_y < troja.y + troja.hitbox_y:
                if (troja.x < gracz.px and troja.x + troja.hitbox_x > gracz.px) or (troja.x > gracz.px and troja.x < gracz.px + gracz.hitbox_x) or (troja.x > gracz.px and troja.x < gracz.px + gracz.hitbox_x):
                    troja.y = -100
                    troja.x = random.randrange(0, szerokosc - 70)
                    wynik += 3
                    ilosc += 1

            if gracz.py < czwora.y + czwora.hitbox_y and gracz.py > czwora.y or gracz.py + gracz.hitbox_y > czwora.y and gracz.py + gracz.hitbox_y < czwora.y + czwora.hitbox_y:
                if (czwora.x < gracz.px and czwora.x + czwora.hitbox_x > gracz.px) or (czwora.x > gracz.px and czwora.x < gracz.px + gracz.hitbox_x) or (czwora.x > gracz.px and czwora.x < gracz.px + gracz.hitbox_x):
                    czwora.y = -100
                    czwora.x = random.randrange(0, szerokosc - 70)
                    wynik += 4
                    ilosc += 1

            if gracz.py < piatka.y + piatka.hitbox_y and gracz.py > piatka.y or gracz.py + gracz.hitbox_y > piatka.y and gracz.py + gracz.hitbox_y < piatka.y + piatka.hitbox_y:
                if (piatka.x < gracz.px and piatka.x + piatka.hitbox_x > gracz.px) or (piatka.x > gracz.px and piatka.x < gracz.px + gracz.hitbox_x) or (piatka.x > gracz.px and piatka.x < gracz.px + gracz.hitbox_x):
                    piatka.y = -100
                    piatka.x = random.randrange(0, szerokosc - 70)
                    wynik += 5
                    ilosc += 1
                    print(srednia(wynik, ilosc))

            if srednia(wynik, ilosc) < 3.0 and ilosc > 1:
                koniec_gry = True
                game_over()

            pygame.display.update()  # dzięki display.update gra się odświeża na ekranie
            zegar.tick(60)  # 60 odświeżeń na sekundę


def koniec():

    '''
    Funkcja łączy ze sobą dwie funkcje potrzebne do zamknięcia okna z grą.
    '''
    pygame.quit()
    quit()


menu_poczatkowe()
gra()
koniec()