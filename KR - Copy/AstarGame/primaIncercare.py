import pygame
import sys
import math
import copy

ADANCIME_MAX = 6
INF = 100000

def distEuclid(p0, p1):
    (x0, y0) = p0
    (x1, y1) = p1
    return math.sqrt((x0 - x1) ** 2 + (y0 - y1) ** 2)

class Graph:
    # coordonatele nodurilor ()
    # (coloana, linie)
    def __init__(self):
        self.noduri = [(y, x) for x in range(10) for y in range(5) if (y, x) not in [(0, 1), (4, 1), (0, 8), (4, 8)]]

        self.muchii = [(0, 1), (1, 2), (2, 3), (3, 4), (5, 6), (6, 7), (0, 5), (1, 5), (2, 6), (3, 7), (4, 7),
                  (5, 10), (6, 10), (7, 10), (38, 39), (39, 40), (41, 42), (42, 43), (43, 44), (44, 45), (38, 35),
                  (39, 35), (40, 35), (41, 38), (42, 38), (43, 39), (44, 40), (45, 40)]
        for (inod, nod) in enumerate(self.noduri):
            if inod < 8:
                continue
            if inod > 37:
                break
            nextLinie = inod + 1
            nextColoana = inod + 5
            if (nextLinie - 3) % 5 != 0:
                self.muchii.append((inod, nextLinie))
            if nextColoana <= 37:
                self.muchii.append((inod, nextColoana))

class Joc:

    JMIN = None
    JMAX = None

    @classmethod
    def initializeaza(cls, display = pygame.display.set_mode(size=(250, 500)), scalare = 50, translatie = 20, razaPct = 10, razaPiesa = 20,
                      culoareEcran = (255, 255, 255), culoareLinii = (0, 0, 0)):
        cls.display = display
        cls.scalare = scalare
        cls.translatie = translatie
        cls.razaPct = razaPct
        cls.razaPiesa = razaPiesa

        cls.culoareEcran = culoareEcran
        cls.culoareLinii = culoareLinii

        cls.diametruPiesa = 2 * cls.razaPiesa
        cls.piesaAlba = pygame.image.load('piesa-alba.png')
        cls.piesaAlba = pygame.transform.scale(cls.piesaAlba, (cls.diametruPiesa, cls.diametruPiesa))
        cls.piesaNeagra = pygame.image.load('piesa-neagra.png')
        cls.piesaNeagra = pygame.transform.scale(cls.piesaNeagra, (cls.diametruPiesa, cls.diametruPiesa))
        cls.piesaSelectata = pygame.image.load('piesa-rosie.png')
        cls.piesaSelectata = pygame.transform.scale(cls.piesaSelectata, (cls.diametruPiesa, cls.diametruPiesa))
        cls.nodPiesaSelectata = False
        cls.coordonateNoduri = [[cls.translatie + cls.scalare * x for x in nod] for nod in Graph().noduri]

    @classmethod
    def setNodPiesaSelectata(cls, val = False):
        cls.nodPiesaSelectata = val

    def deseneaza(self, marcaj=None):
        self.__class__.display.fill(self.__class__.culoareEcran)
        # for nod in coordonateNoduri:
        #     pygame.draw.circle(surface=ecran, color=culoareLinii, center=nod, radius=Graph.razaPct,
        #                        width=0)  # width=0 face un cerc plin

        for muchie in self.tabla.muchii:
            p0 = self.__class__.coordonateNoduri[muchie[0]]
            p1 = self.__class__.coordonateNoduri[muchie[1]]
            pygame.draw.line(surface=self.__class__.display, color=self.__class__.culoareLinii, start_pos=p0, end_pos=p1, width=5)
        for nod in self.pieseAlbe:
            self.__class__.display.blit(self.__class__.piesaAlba, (nod[0] - self.__class__.razaPiesa, nod[1] - self.__class__.razaPiesa))
        for nod in self.pieseNegre:
            self.__class__.display.blit(self.__class__.piesaNeagra, (nod[0] - self.__class__.razaPiesa, nod[1] - self.__class__.razaPiesa))
        if self.__class__.nodPiesaSelectata:
            self.__class__.display.blit(self.__class__.piesaSelectata, (self.__class__.nodPiesaSelectata[0] -
                                self.__class__.razaPiesa, self.__class__.nodPiesaSelectata[1] - self.__class__.razaPiesa))
        pygame.display.update()

    def __init__(self, tabla=None, pieseAlbe = None, pieseNegre = None):
        self.tabla = tabla or Graph()
        self.pieseAlbe = pieseAlbe or [[self.__class__.translatie + self.__class__.scalare * x for x in nod] for nod in self.tabla.noduri[-17:]]
        self.pieseNegre = pieseNegre or [[self.__class__.translatie + self.__class__.scalare * x for x in nod] for nod in self.tabla.noduri[:17]]
        self.pieseAlbe.remove(self.pieseAlbe[3])
        self.pieseNegre.remove(self.pieseNegre[-4])

        self.endAlbe = [[self.__class__.translatie + self.__class__.scalare * x for x in nod] for nod in self.tabla.noduri[:11]]
        self.endAlbe.remove(self.endAlbe[8])
        self.endAlbe.remove(self.endAlbe[8])
        self.endAlbe.sort()

        self.endNegre = [[self.__class__.translatie + self.__class__.scalare * x for x in nod] for nod in self.tabla.noduri[-11:]]
        self.endNegre.remove(self.endNegre[1])
        self.endNegre.remove(self.endNegre[1])
        self.endNegre.sort()

    @classmethod
    def jucator_opus(cls, jucator):
        return cls.JMAX if jucator == cls.JMIN else cls.JMIN

    def final(self):
        if self.pieseAlbe == []:
            return 'negru'

        if self.pieseNegre == []:
            return 'alb'

        okA = True

        for nod in self.endAlbe:
            if nod not in self.pieseAlbe:
                okA = False
                break

        if okA:
            return 'alb'

        okB = True

        for nod in self.endNegre:
            if nod not in self.pieseNegre:
                okB = False
                break

        if okB:
            return 'negru'

        if self.mutari('alb') == []:
            return 'negru'

        if self.mutari('negru') == []:
            return 'alb'

        return False

    def culoare(self, piesa):
        if piesa in self.pieseAlbe:
            return 'alb'
        elif piesa in self.pieseNegre:
            return 'negru'
        elif piesa in self.__class__.coordonateNoduri:
            return 'gol'
        else:
            return None

    def unTranslate(self, piesa):
        x = (piesa[0] - self.__class__.translatie) // self.__class__.scalare
        y = (piesa[1] - self.__class__.translatie) // self.__class__.scalare
        return [x, y]

    def translate(self, piesaN):
        return [self.__class__.translatie + self.__class__.scalare * piesaN[0],
                self.__class__.translatie + self.__class__.scalare * piesaN[1]]

    def mutare(self, piesa, pas = 1, sus = False, jos = False, stanga = False, dreapta = False):

        x, y = self.unTranslate(piesa)

        if sus:
            y -= pas
        elif jos:
            y += pas

        if stanga:
            x -= pas
        elif dreapta:
            x += pas

        if x < 0 or x > 4:
            return None
        if y < 0 or y > 9:
            return None

        return self.translate([x, y])

    def capturariPosibile(self, piesa):

        graf = self.tabla
        def check(mutare, spatiu):

            if mutare != None and spatiu != None and mutare in self.__class__.coordonateNoduri and spatiu in self.__class__.coordonateNoduri:
                m1 = self.__class__.coordonateNoduri.index(piesa)
                m2 = self.__class__.coordonateNoduri.index(mutare)
                m3 = self.__class__.coordonateNoduri.index(spatiu)

                if ((m1, m2) in graf.muchii or (m2, m1) in graf.muchii) and (
                        (m2, m3) in graf.muchii or (m3, m2) in graf.muchii):
                    if self.culoare(spatiu) == 'gol':
                        if ((self.culoare(piesa) == 'alb' and self.culoare(mutare) == 'negru') or
                                (self.culoare(piesa) == 'negru' and self.culoare(mutare) == 'alb')):
                            return (mutare, spatiu)
            return None

        cList = []

        mutare = self.mutare(piesa, stanga= True)
        spatiu = self.mutare(piesa, 2, stanga= True)
        x = check(mutare, spatiu)
        if x != None:
            cList.append(x)

        mutare = self.mutare(piesa, dreapta=True)
        spatiu = self.mutare(piesa, 2, dreapta=True)
        x = check(mutare, spatiu)
        if x != None:
            cList.append(x)

        mutare = self.mutare(piesa, sus=True)
        spatiu = self.mutare(piesa, 2, sus=True)
        x = check(mutare, spatiu)
        if x != None:
            cList.append(x)

        mutare = self.mutare(piesa, jos=True)
        spatiu = self.mutare(piesa, 2, jos=True)
        x = check(mutare, spatiu)
        if x != None:
            cList.append(x)

        mutare = self.mutare(piesa, stanga=True, sus=True)
        spatiu = self.mutare(piesa, 2, stanga=True, sus=True)
        x = check(mutare, spatiu)
        if x != None:
            cList.append(x)

        mutare = self.mutare(piesa, stanga=True, jos=True)
        spatiu = self.mutare(piesa, 2, stanga=True, jos=True)
        x = check(mutare, spatiu)
        if x != None:
            cList.append(x)

        mutare = self.mutare(piesa, dreapta=True, sus=True)
        spatiu = self.mutare(piesa, 2, dreapta=True, sus=True)
        x = check(mutare, spatiu)
        if x != None:
            cList.append(x)

        mutare = self.mutare(piesa, dreapta=True, jos=True)
        spatiu = self.mutare(piesa, 2, dreapta=True, jos=True)
        x = check(mutare, spatiu)
        if x != None:
            cList.append(x)

        return cList


    def ocupat(self, piesa):
        return piesa in self.pieseAlbe or piesa in self.pieseNegre


    def mutariPiesa(self, piesa):

        graf = self.tabla
        def check(mutare):
            if mutare != None and mutare in self.__class__.coordonateNoduri :
                m1 = self.__class__.coordonateNoduri.index(piesa)
                m2 = self.__class__.coordonateNoduri.index(mutare)

                if (m1, m2) in graf.muchii or (m2, m1) in graf.muchii:
                    if self.culoare(mutare) == 'gol':
                        return mutare
            return None

        mutari = self.capturariPosibile(piesa)
        if mutari != []:
            return 'c', mutari

        mutare = self.mutare(piesa, stanga= True)
        if mutare != None and check(mutare) != None:
            mutari.append(mutare)

        mutare = self.mutare(piesa, dreapta=True)
        if mutare != None and check(mutare) != None:
            mutari.append(mutare)

        mutare = self.mutare(piesa, sus=True)
        if mutare != None and check(mutare) != None:
            mutari.append(mutare)

        mutare = self.mutare(piesa, jos=True)
        if mutare != None and check(mutare) != None:
            mutari.append(mutare)

        mutare = self.mutare(piesa, stanga=True, sus=True)
        if mutare != None and check(mutare) != None:
            mutari.append(mutare)

        mutare = self.mutare(piesa, stanga=True, jos=True)
        if mutare != None and check(mutare) != None:
            mutari.append(mutare)

        mutare = self.mutare(piesa, dreapta=True, sus=True)
        if mutare != None and check(mutare) != None:
            mutari.append(mutare)

        mutare = self.mutare(piesa, dreapta=True, jos=True)
        if mutare != None and check(mutare) != None:
            mutari.append(mutare)

        return 'm', mutari


    def mutari(self, jucator):
        l_mutari = []
        pieseSelectate = []
        if jucator == 'alb':
            pieseSelectate = self.pieseAlbe
        elif jucator == 'negru':
            pieseSelectate = self.pieseNegre

        mutari = {}
        captures = {}
        for piesa in pieseSelectate:
            type, mutariPiesa = self.mutariPiesa(piesa)
            if type == 'c':
                captures[piesa] = mutariPiesa
            elif type == 'm':
                mutari[piesa] = mutariPiesa

        if captures != {}:
            for piesa in captures:
                for mutare in captures[piesa]:
                    copieAlbe = copy.deepcopy(self.pieseAlbe)
                    copieNegre = copy.deepcopy(self.pieseNegre)

                    captured = mutare[0]
                    move = mutare[1]

                    if jucator == 'alb':
                        copieAlbe.remove(piesa)
                        copieAlbe.append(move)
                        copieNegre.remove(captured)

                    if jucator == 'negru':
                        copieNegre.remove(piesa)
                        copieNegre.append(move)
                        copieAlbe.remove(captured)

                    l_mutari.append(Joc(self.tabla, copieAlbe, copieNegre))
        else:
            for piesa in mutari:
                for mutare in mutari[piesa]:
                    copieAlbe = copy.deepcopy(self.pieseAlbe)
                    copieNegre = copy.deepcopy(self.pieseNegre)

                    if jucator == 'alb':
                        copieAlbe.remove(piesa)
                        copieAlbe.append(mutare)

                    if jucator == 'negru':
                        copieNegre.remove(piesa)
                        copieNegre.append(mutare)

                    l_mutari.append(Joc(self.tabla, copieAlbe, copieNegre))


        return l_mutari

    def calculeazaScor(self, varianta = 1):

        jMin = self.__class__.JMIN
        jMax = self.__class__.JMAX

        score = 0
        score += len(self.pieseAlbe)
        score -= len(self.pieseNegre)

        mutari = self.mutari('alb')
        score += len(mutari)

        mutari = self.mutari('negru')
        score -= len(mutari)

        for piesa in self.endAlbe:
            if piesa in self.pieseAlbe:
                score += 1

        for piesa in self.endNegre:
            if piesa in self.pieseNegre:
                score -= 1

        # v2: cat de avansata e o piesa?

        if jMax == 'alb':
            return score
        else:
            return -score

    def estimeazaScor(self, adancime, varianta = 1):
        tFinal = self.final()
        if tFinal == self.__class__.JMAX:
            return INF + adancime
        elif tFinal == self.__class__.JMIN:
            return -INF - adancime
        else:
            return self.calculeazaScor(varianta)

    def sirAfisare(self):

        sir = '   '
        for i in range(5):
            sir += str(i+1) + ' '
        sir += '\n'
        for y in range(10):
            if y < 9:
                sir += str(y+1) + '  '
            else:
                sir += str(y+1) + ' '
            for x in range(5):
                translate = self.translate([x, y])
                if translate in self.pieseAlbe:
                    sir += 'A '
                elif translate in self.pieseNegre:
                    sir += 'N '
                elif self.culoare(translate) == 'gol':
                    sir += '# '
                else:
                    sir += '  '
            sir += '\n'
        return sir

    def __str__(self):
        return self.sirAfisare()

    def __repr__(self):
        return self.sirAfisare()


class Stare:

    def __init__(self, tabla_joc, j_curent, adancime, parinte=None, estimare=None):
        self.tabla_joc = tabla_joc
        self.j_curent = j_curent

        # adancimea in arborele de stari
        self.adancime = adancime

        self.parinte = parinte

        # estimarea favorabilitatii starii (daca e finala) sau al celei mai bune stari-fiice (pentru jucatorul curent)
        self.estimare = estimare

        # lista de mutari posibile din starea curenta
        self.mutari_posibile = []

        # cea mai buna mutare din lista de mutari posibile pentru jucatorul curent
        self.stare_aleasa = None

    def mutari(self):
        l_mutari = self.tabla_joc.mutari(self.j_curent)
        juc_opus = Joc.jucator_opus(self.j_curent)
        l_stari_mutari = [Stare(mutare, juc_opus, self.adancime - 1, parinte=self) for mutare in l_mutari]

        return l_stari_mutari

    def __str__(self):
        sir = str(self.tabla_joc) + "(Juc curent:" + self.j_curent + ")\n"
        return sir

def min_max(stare):
    if stare.adancime == 0 or stare.tabla_joc.final():
        stare.estimare = stare.tabla_joc.estimeaza_scor(stare.adancime)
        return stare

    # calculez toate mutarile posibile din starea curenta
    stare.mutari_posibile = stare.mutari()

    # aplic algoritmul minimax pe toate mutarile posibile (calculand astfel subarborii lor)
    mutariCuEstimare = [min_max(mutare) for mutare in stare.mutari_posibile]

    if stare.j_curent == Joc.JMAX:
        # daca jucatorul e JMAX aleg starea-fiica cu estimarea maxima
        stare.stare_aleasa = max(mutariCuEstimare, key=lambda x: x.estimare)
    else:
        # daca jucatorul e JMIN aleg starea-fiica cu estimarea minima
        stare.stare_aleasa = min(mutariCuEstimare, key=lambda x: x.estimare)
    stare.estimare = stare.stare_aleasa.estimare
    return stare

class Buton:
    def __init__(self, display=None, left=0, top=0, w=0, h=0, culoareFundal=(53, 80, 115),
                 culoareFundalSel=(89, 134, 194), text="", font="arial", fontDimensiune=16, culoareText=(255, 255, 255),
                 valoare=""):
        self.display = display
        self.culoareFundal = culoareFundal
        self.culoareFundalSel = culoareFundalSel
        self.text = text
        self.font = font
        self.w = w
        self.h = h
        self.selectat = False
        self.fontDimensiune = fontDimensiune
        self.culoareText = culoareText
        # creez obiectul font
        fontObj = pygame.font.SysFont(self.font, self.fontDimensiune)
        self.textRandat = fontObj.render(self.text, True, self.culoareText)
        self.dreptunghi = pygame.Rect(left, top, w, h)
        # aici centram textul
        self.dreptunghiText = self.textRandat.get_rect(center=self.dreptunghi.center)
        self.valoare = valoare

    def selecteaza(self, sel):
        self.selectat = sel
        self.deseneaza()

    def selecteazaDupacoord(self, coord):
        if self.dreptunghi.collidepoint(coord):
            self.selecteaza(True)
            return True
        return False

    def updateDreptunghi(self):
        self.dreptunghi.left = self.left
        self.dreptunghi.top = self.top
        self.dreptunghiText = self.textRandat.get_rect(center=self.dreptunghi.center)

    def deseneaza(self):
        culoareF = self.culoareFundalSel if self.selectat else self.culoareFundal
        pygame.draw.rect(self.display, culoareF, self.dreptunghi)
        self.display.blit(self.textRandat, self.dreptunghiText)


class GrupButoane:
    def __init__(self, listaButoane=[], indiceSelectat=0, spatiuButoane=10, left=0, top=0):
        self.listaButoane = listaButoane
        self.indiceSelectat = indiceSelectat
        self.listaButoane[self.indiceSelectat].selectat = True
        self.top = top
        self.left = left
        leftCurent = self.left
        for b in self.listaButoane:
            b.top = self.top
            b.left = leftCurent
            b.updateDreptunghi()
            leftCurent += (spatiuButoane + b.w)

    def selecteazaDupacoord(self, coord):
        for ib, b in enumerate(self.listaButoane):
            if b.selecteazaDupacoord(coord):
                self.listaButoane[self.indiceSelectat].selecteaza(False)
                self.indiceSelectat = ib
                return True
        return False

    def deseneaza(self):
        # atentie, nu face wrap
        for b in self.listaButoane:
            b.deseneaza()

    def getValoare(self):
        return self.listaButoane[self.indiceSelectat].valoare


############# ecran initial ########################
def deseneaza_alegeri(display, tabla_curenta):
    btn_alg = GrupButoane(
        top=30,
        left=30,
        listaButoane=[
            Buton(display=display, w=80, h=30, text="minimax", valoare="minimax"),
            Buton(display=display, w=80, h=30, text="alphabeta", valoare="alphabeta")
        ],
        indiceSelectat=1)
    btn_juc = GrupButoane(
        top=100,
        left=30,
        listaButoane=[
            Buton(display=display, w=35, h=30, text="alb", valoare="alb"),
            Buton(display=display, w=35, h=30, text="negru", valoare="negru")
        ],
        indiceSelectat=0)

    btn_rand = GrupButoane(
        top=170,
        left=30,
        listaButoane=[
            Buton(display=display, w=40, h=30, text="player", valoare="player"),
            Buton(display=display, w=40, h=30, text="AI", valoare="ai")
        ],
        indiceSelectat=0
    )

    ok = Buton(display=display, top=240, left=30, w=40, h=30, text="ok", culoareFundal=(155, 0, 55))
    btn_alg.deseneaza()
    btn_juc.deseneaza()
    btn_rand.deseneaza()
    ok.deseneaza()
    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif ev.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if not btn_alg.selecteazaDupacoord(pos):
                    if not btn_juc.selecteazaDupacoord(pos):
                        if not btn_rand.selecteazaDupacoord(pos):
                            if ok.selecteazaDupacoord(pos):
                                display.fill((0, 0, 0))  # stergere ecran
                                tabla_curenta.deseneaza()
                                return btn_juc.getValoare(), btn_alg.getValoare(), btn_rand.getValoare()
        pygame.display.update()

def main():
    pygame.init()
    ecran = pygame.display.set_mode(size=(270, 510))
    Joc.initializeaza(ecran, translatie=35)

    tabla_curenta = Joc()
    Joc.JMIN, tip_algoritm, rand = deseneaza_alegeri(ecran, tabla_curenta)

    Joc.JMAX = 'alb' if Joc.JMIN == 'negru' else 'negru'
    jucator = Joc.JMIN if rand == 'player' else Joc.JMAX

    print('jmin: ', Joc.JMIN)
    print('jmax: ', Joc.JMAX)
    print('tip: ', tip_algoritm)
    print('rand: ', jucator)

    print(tabla_curenta)

    pygame.display.set_caption('Lazar Mihai Astar')
    tabla_curenta.deseneaza()

    adancime = ADANCIME_MAX

    stare_curenta = Stare(tabla_curenta, jucator, adancime)
    while True:
        if stare_curenta.j_curent == Joc.JMIN:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()  # inchide fereastra
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if stare_curenta.j_curent == 'alb':
                        pieseJucator = stare_curenta.tabla_joc.pieseAlbe
                    else:
                        pieseJucator = stare_curenta.tabla_joc.pieseNegre

                    for nod in stare_curenta.tabla_joc.coordonateNoduri:
                        if distEuclid(pos, nod) <= stare_curenta.tabla_joc.razaPiesa:
                            if nod in pieseJucator:
                                if stare_curenta.tabla_joc.nodPiesaSelectata == False:
                                    stare_curenta.tabla_joc.setNodPiesaSelectata(nod)
                                elif tabla_curenta.nodPiesaSelectata == nod:
                                    stare_curenta.tabla_joc.setNodPiesaSelectata(False)
                                stare_curenta.tabla_joc.deseneaza()
                            elif nod not in pieseJucator:
                                piesaSelectata = stare_curenta.tabla_joc.nodPiesaSelectata
                                if piesaSelectata:
                                    type, mutariPiesa = stare_curenta.tabla_joc.mutariPiesa(piesaSelectata)
                                    print(mutariPiesa)
                                    if type == 'c':
                                        for captured, mutare in mutariPiesa:
                                            if nod == mutare:
                                                copieAlbe = copy.deepcopy(stare_curenta.tabla_joc.pieseAlbe)
                                                copieNegre = copy.deepcopy(stare_curenta.tabla_joc.pieseNegre)

                                                if stare_curenta.j_curent == 'alb':
                                                    copieAlbe.remove(piesaSelectata)
                                                    copieAlbe.append(mutare)
                                                    copieNegre.remove(captured)
                                                elif stare_curenta.j_curent == 'negru':
                                                    copieNegre.remove(piesaSelectata)
                                                    copieNegre.append(mutare)
                                                    copieAlbe.remove(captured)

                                                stare_curenta.tabla_joc.setNodPiesaSelectata(False)
                                                tabla_curenta = Joc(stare_curenta.tabla_joc.tabla, copieAlbe, copieNegre)
                                                stare_curenta = Stare(tabla_curenta, Joc.JMAX, adancime)

                                                stare_curenta.tabla_joc.deseneaza()
                                    elif type == 'm':
                                        for mutare in mutariPiesa:
                                            if nod == mutare:
                                                copieAlbe = copy.deepcopy(stare_curenta.tabla_joc.pieseAlbe)
                                                copieNegre = copy.deepcopy(stare_curenta.tabla_joc.pieseNegre)

                                                print(copieAlbe)

                                                if stare_curenta.j_curent == 'alb':
                                                    copieAlbe.remove(piesaSelectata)
                                                    copieAlbe.append(mutare)

                                                elif stare_curenta.j_curent == 'negru':
                                                    copieNegre.remove(piesaSelectata)
                                                    copieNegre.append(mutare)

                                                print(copieAlbe)


                                                stare_curenta.tabla_joc.setNodPiesaSelectata(False)
                                                tabla_curenta = Joc(stare_curenta.tabla_joc.tabla, copieAlbe, copieNegre)
                                                stare_curenta = Stare(tabla_curenta, Joc.JMAX, adancime)

                                                stare_curenta.tabla_joc.deseneaza()




if __name__ == '__main__':

    main()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()