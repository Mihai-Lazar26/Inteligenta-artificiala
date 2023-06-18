import pygame
import sys
import math
import copy
import time
import statistics

ADANCIME_MAX = 6
INF = 99

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

    btn_dificultate = GrupButoane(
        top=240,
        left=30,
        listaButoane=[
            Buton(display=display, w=40, h=30, text="usor", valoare=2),
            Buton(display=display, w=40, h=30, text="mediu", valoare=3),
            Buton(display=display, w=40, h=30, text="greu", valoare=4)
        ],
        indiceSelectat=0
    )

    btn_variante = GrupButoane(
        top=310,
        left=30,
        listaButoane=[
            Buton(display=display, w=80, h=30, text="Estimare 1", valoare=1),
            Buton(display=display, w=80, h=30, text="Estimare 2", valoare=2)
        ],
        indiceSelectat=1
    )

    ok = Buton(display=display, top=380, left=30, w=40, h=30, text="ok", culoareFundal=(155, 0, 55))
    btn_alg.deseneaza()
    btn_juc.deseneaza()
    btn_rand.deseneaza()
    btn_dificultate.deseneaza()
    btn_variante.deseneaza()
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
                            if not btn_dificultate.selecteazaDupacoord(pos):
                                if not btn_variante.selecteazaDupacoord(pos):
                                    if ok.selecteazaDupacoord(pos):
                                        display.fill((0, 0, 0))  # stergere ecran
                                        tabla_curenta.deseneaza()
                                        return btn_juc.getValoare(), btn_alg.getValoare(), btn_rand.getValoare(), \
                                               btn_dificultate.getValoare(), btn_variante.getValoare()

        pygame.display.update()



def distEuclid(p0, p1):
    (x0, y0) = p0
    (x1, y1) = p1
    return math.sqrt((x0 - x1) ** 2 + (y0 - y1) ** 2)

class Graph:
    # coordonatele nodurilor ()
    # (coloana, linie)
    noduri = [(y, x) for x in range(10) for y in range(5) if (y, x) not in [(0, 1), (4, 1), (0, 8), (4, 8)]]

    muchii = [(0, 1), (1, 2), (2, 3), (3, 4), (5, 6), (6, 7), (0, 5), (1, 5), (2, 6), (3, 7), (4, 7),
              (5, 10), (6, 10), (7, 10), (38, 39), (39, 40), (41, 42), (42, 43), (43, 44), (44, 45), (38, 35),
              (39, 35), (40, 35), (41, 38), (42, 38), (43, 39), (44, 40), (45, 40)]
    for (inod, nod) in enumerate(noduri):
        if inod < 8:
            continue
        if inod > 37:
            break
        nextLinie = inod + 1
        nextColoana = inod + 5
        if (nextLinie - 3) % 5 != 0:
            muchii.append((inod, nextLinie))
        if nextColoana <= 37:
            muchii.append((inod, nextColoana))

class Joc:
    JMIN = None
    JMAX = None

    @classmethod
    def initializeaza(cls, display=pygame.display.set_mode(size=(250, 500)), scalare=50, translatie=20, razaPct=10,
                      razaPiesa=20, culoareEcran=(255, 255, 255), culoareLinii=(0, 0, 0)):
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
        cls.coordonateNoduri = [[cls.translatie + cls.scalare * x for x in nod] for nod in Graph.noduri]

    def deseneaza(self, marcaj=None):
        self.__class__.display.fill(self.__class__.culoareEcran)
        # for nod in coordonateNoduri:
        #     pygame.draw.circle(surface=ecran, color=culoareLinii, center=nod, radius=Graph.razaPct,
        #                        width=0)  # width=0 face un cerc plin

        for muchie in self.tabla.muchii:
            p0 = self.__class__.coordonateNoduri[muchie[0]]
            p1 = self.__class__.coordonateNoduri[muchie[1]]
            pygame.draw.line(surface=self.__class__.display, color=self.__class__.culoareLinii, start_pos=p0, end_pos=p1, width=5)
        if marcaj != 'alb':
            for nod in self.pieseAlbe:
                self.__class__.display.blit(self.__class__.piesaAlba, (nod[0] - self.__class__.razaPiesa, nod[1] - self.__class__.razaPiesa))
        else:
            for nod in self.pieseAlbe:
                self.__class__.display.blit(self.__class__.piesaSelectata,
                                            (nod[0] - self.__class__.razaPiesa, nod[1] - self.__class__.razaPiesa))
        if marcaj != 'negru':
            for nod in self.pieseNegre:
                self.__class__.display.blit(self.__class__.piesaNeagra, (nod[0] - self.__class__.razaPiesa, nod[1] - self.__class__.razaPiesa))
        else:
            for nod in self.pieseNegre:
                self.__class__.display.blit(self.__class__.piesaSelectata, (nod[0] - self.__class__.razaPiesa, nod[1] - self.__class__.razaPiesa))
        if self.__class__.nodPiesaSelectata:
            self.__class__.display.blit(self.__class__.piesaSelectata, (self.__class__.nodPiesaSelectata[0] -
                                self.__class__.razaPiesa, self.__class__.nodPiesaSelectata[1] - self.__class__.razaPiesa))
        pygame.display.update()

    @classmethod
    def setNodPiesaSelectata(cls, val=False):
        cls.nodPiesaSelectata = val

    def __init__(self, pieseAlbe = None, pieseNegre = None):
        self.tabla = Graph
        if pieseAlbe == None:
            self.pieseAlbe = [[self.__class__.translatie + self.__class__.scalare * x for x in nod] for nod in
                                       self.tabla.noduri[-17:]]
            self.pieseAlbe.remove(self.pieseAlbe[3])
        else:
            self.pieseAlbe = pieseAlbe

        if pieseNegre == None:
            self.pieseNegre = [[self.__class__.translatie + self.__class__.scalare * x for x in nod] for nod
                                         in self.tabla.noduri[:17]]
            self.pieseNegre.remove(self.pieseNegre[-4])
        else:
            self.pieseNegre = pieseNegre



        self.endAlbe = [[self.__class__.translatie + self.__class__.scalare * x for x in nod] for nod in
                        self.tabla.noduri[:11]]
        self.endAlbe.remove(self.endAlbe[8])
        self.endAlbe.remove(self.endAlbe[8])
        self.endAlbe.sort()

        self.endNegre = [[self.__class__.translatie + self.__class__.scalare * x for x in nod] for nod in
                         self.tabla.noduri[-11:]]
        self.endNegre.remove(self.endNegre[1])
        self.endNegre.remove(self.endNegre[1])
        self.endNegre.sort()

    @classmethod
    def jucator_opus(cls, jucator):
        return cls.JMAX if jucator == cls.JMIN else cls.JMIN

    def unTranslate(self, piesa):
        x = (piesa[0] - self.__class__.translatie) // self.__class__.scalare
        y = (piesa[1] - self.__class__.translatie) // self.__class__.scalare
        return [x, y]

    def translate(self, piesaN):
        return [self.__class__.translatie + self.__class__.scalare * piesaN[0],
                self.__class__.translatie + self.__class__.scalare * piesaN[1]]

    def culoare(self, piesa):
        if piesa in self.pieseAlbe:
            return 'alb'
        elif piesa in self.pieseNegre:
            return 'negru'
        elif piesa in self.__class__.coordonateNoduri:
            return 'gol'
        else:
            return None

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

    def mutare(self, piesa, sus = False, jos = False, stanga = False, dreapta = False):

        # functia returneaza o mutare valida in directiile alese de noi

        if piesa == None:
            return None

        untranslated = self.unTranslate(piesa)
        x = untranslated[0]
        y = untranslated[1]

        if sus:
            y -= 1
        elif jos:
            y += 1

        if stanga:
            x -= 1
        elif dreapta:
            x += 1

        mutare = self.translate([x,y])
        if mutare not in self.__class__.coordonateNoduri:
            return None

        p1 = self.__class__.coordonateNoduri.index(piesa)
        p2 = self.__class__.coordonateNoduri.index(mutare)

        if (p1, p2) not in self.tabla.muchii and (p2, p1) not in self.tabla.muchii:
            return None

        return mutare

    def capturariPiesa(self, piesa):

        # functia returneaza toate capturile pe care le poate face o piesa, structura returnata fiind de forma
        # [(captured, mutare)]

        if self.culoare(piesa) == 'gol':
            return []

        def valid(captured, mutare):
            if captured != None and mutare != None:
                if self.culoare(captured) in ['alb', 'negru'] and self.culoare(piesa) != self.culoare(captured):
                    if self.culoare(mutare) == 'gol':
                        return True
            return False

        l_capturari = []

        captured = self.mutare(piesa, stanga=True)
        mutare = self.mutare(captured, stanga=True)
        if valid(captured, mutare):
            l_capturari.append((captured, mutare))

        captured = self.mutare(piesa, dreapta=True)
        mutare = self.mutare(captured, dreapta=True)
        if valid(captured, mutare):
            l_capturari.append((captured, mutare))

        captured = self.mutare(piesa, jos=True)
        mutare = self.mutare(captured, jos=True)
        if valid(captured, mutare):
            l_capturari.append((captured, mutare))

        captured = self.mutare(piesa, sus=True)
        mutare = self.mutare(captured, sus=True)
        if valid(captured, mutare):
            l_capturari.append((captured, mutare))

        captured = self.mutare(piesa, dreapta=True, sus=True)
        mutare = self.mutare(captured, dreapta=True, sus=True)
        if valid(captured, mutare):
            l_capturari.append((captured, mutare))

        captured = self.mutare(piesa, dreapta=True, jos=True)
        mutare = self.mutare(captured, dreapta=True, jos=True)
        if valid(captured, mutare):
            l_capturari.append((captured, mutare))

        captured = self.mutare(piesa, stanga=True, sus=True)
        mutare = self.mutare(captured, stanga=True, sus=True)
        if valid(captured, mutare):
            l_capturari.append((captured, mutare))

        captured = self.mutare(piesa, stanga=True, jos=True)
        mutare = self.mutare(captured, stanga=True, jos=True)
        if valid(captured, mutare):
            l_capturari.append((captured, mutare))

        return l_capturari

    # directie = st, su, dr, jo, stsu, stjo, drsu, drjo
    def attackPower(self, piesa, directie = []):

        # Functia returneaza numarul maxim de capturi pe care le poate face o piesa intr-o mutare

        if self.culoare(piesa) == 'gol':
            return 0

        def valid(captured, mutare):
            if captured != None and mutare != None:
                if self.culoare(captured) in ['alb', 'negru'] and self.culoare(piesa) != self.culoare(captured):
                    if self.culoare(mutare) == 'gol':
                        return True
            return False

        def makeCapture(captured, mutare):
            copieAlbe = copy.deepcopy(self.pieseAlbe)
            copieNegre = copy.deepcopy(self.pieseNegre)

            if self.culoare(piesa) == 'alb':
                copieAlbe.remove(piesa)
                copieAlbe.append(mutare)
                copieNegre.remove(captured)
            elif self.culoare(piesa) == 'negru':
                copieNegre.remove(piesa)
                copieNegre.append(mutare)
                copieAlbe.remove(captured)

            joc = Joc(copieAlbe, copieNegre)
            return joc
        sum = 0
        if directie != []:
            if 'st' in directie:
                captured = self.mutare(piesa, stanga=True)
                mutare = self.mutare(captured, stanga=True)
                if valid(captured, mutare):
                    joc_nou = makeCapture(captured, mutare)
                    sum = max(sum, joc_nou.attackPower(mutare))
            if 'dr' in directie:
                captured = self.mutare(piesa, dreapta=True)
                mutare = self.mutare(captured, dreapta=True)
                if valid(captured, mutare):
                    joc_nou = makeCapture(captured, mutare)
                    sum = max(sum, joc_nou.attackPower(mutare))
            if 'su' in directie:
                captured = self.mutare(piesa, sus=True)
                mutare = self.mutare(captured, sus=True)
                if valid(captured, mutare):
                    joc_nou = makeCapture(captured, mutare)
                    sum = max(sum, joc_nou.attackPower(mutare))
            if 'jo' in directie:
                captured = self.mutare(piesa, jos=True)
                mutare = self.mutare(captured, jos=True)
                if valid(captured, mutare):
                    joc_nou = makeCapture(captured, mutare)
                    sum = max(sum, joc_nou.attackPower(mutare))
            if 'stsu' in directie:
                captured = self.mutare(piesa, stanga=True, sus=True)
                mutare = self.mutare(captured, stanga=True, sus=True)
                if valid(captured, mutare):
                    joc_nou = makeCapture(captured, mutare)
                    sum = max(sum, joc_nou.attackPower(mutare))
            if 'stjo' in directie:
                captured = self.mutare(piesa, stanga=True, jos=True)
                mutare = self.mutare(captured, stanga=True, jos=True)
                if valid(captured, mutare):
                    joc_nou = makeCapture(captured, mutare)
                    sum = max(sum, joc_nou.attackPower(mutare))
            if 'drsu' in directie:
                captured = self.mutare(piesa, dreapta=True, sus=True)
                mutare = self.mutare(captured, dreapta=True, sus=True)
                if valid(captured, mutare):
                    joc_nou = makeCapture(captured, mutare)
                    sum = max(sum, joc_nou.attackPower(mutare))
            if 'drjo' in directie:
                captured = self.mutare(piesa, dreapta=True, jos=True)
                mutare = self.mutare(captured, dreapta=True, jos=True)
                if valid(captured, mutare):
                    joc_nou = makeCapture(captured, mutare)
                    sum = max(sum, joc_nou.attackPower(mutare))
        else:
            capturari = self.capturariPiesa(piesa)
            if capturari == []:
                return 0
            for captured, mutare in capturari:
                copieAlbe = copy.deepcopy(self.pieseAlbe)
                copieNegre = copy.deepcopy(self.pieseNegre)

                if self.culoare(piesa) == 'alb':
                    copieAlbe.remove(piesa)
                    copieAlbe.append(mutare)
                    copieNegre.remove(captured)
                elif self.culoare(piesa) == 'negru':
                    copieNegre.remove(piesa)
                    copieNegre.append(mutare)
                    copieAlbe.remove(captured)

                joc = Joc(copieAlbe, copieNegre)
                sum = max(sum, joc.attackPower(mutare))
        return sum + 1




    def starePiesa(self, piesa, jucator):

        # Functia returneaza numarul maxim de piese pe care le poate captura jucatorul opus daca jucator = jucator opus
        # sau returneaza numarul maxim de capturi pe care le poate face piesa curenta

        if piesa == None or self.culoare(piesa) == 'gol':
            return 0


        if self.culoare(piesa) == jucator:
            stare = 0
            defense = self.mutare(piesa, stanga=True)
            attacker = self.mutare(piesa, dreapta=True)
            if defense == None or (self.culoare(defense) in ['alb', 'negru'] and self.culoare(defense) == self.culoare(piesa)):
                pass
            elif self.culoare(attacker) in ['alb', 'negru'] and self.culoare(attacker) != self.culoare(piesa):
                atac = self.attackPower(attacker, ['st'])
                stare = max(stare, atac)

            defense = self.mutare(piesa, dreapta=True)
            attacker = self.mutare(piesa, stanga=True)
            if defense == None or (
                    self.culoare(defense) in ['alb', 'negru'] and self.culoare(defense) == self.culoare(piesa)):
                pass
            elif self.culoare(attacker) in ['alb', 'negru'] and self.culoare(attacker) != self.culoare(piesa):
                atac = self.attackPower(attacker, ['dr'])
                stare = max(stare, atac)

            defense = self.mutare(piesa, sus=True)
            attacker = self.mutare(piesa, jos=True)
            if defense == None or (
                    self.culoare(defense) in ['alb', 'negru'] and self.culoare(defense) == self.culoare(piesa)):
                pass
            elif self.culoare(attacker) in ['alb', 'negru'] and self.culoare(attacker) != self.culoare(piesa):
                atac = self.attackPower(attacker, ['su'])
                stare = max(stare, atac)

            defense = self.mutare(piesa, jos=True)
            attacker = self.mutare(piesa, sus=True)
            if defense == None or (
                    self.culoare(defense) in ['alb', 'negru'] and self.culoare(defense) == self.culoare(piesa)):
                pass
            elif self.culoare(attacker) in ['alb', 'negru'] and self.culoare(attacker) != self.culoare(piesa):
                atac = self.attackPower(attacker, ['jo'])
                stare = max(stare, atac)

            defense = self.mutare(piesa, stanga=True, sus=True)
            attacker = self.mutare(piesa, dreapta=True, jos=True)
            if defense == None or (
                    self.culoare(defense) in ['alb', 'negru'] and self.culoare(defense) == self.culoare(piesa)):
                pass
            elif self.culoare(attacker) in ['alb', 'negru'] and self.culoare(attacker) != self.culoare(piesa):
                atac = self.attackPower(attacker, ['stsu'])
                stare = max(stare, atac)

            defense = self.mutare(piesa, stanga=True, jos=True)
            attacker = self.mutare(piesa, dreapta=True, sus=True)
            if defense == None or (
                    self.culoare(defense) in ['alb', 'negru'] and self.culoare(defense) == self.culoare(piesa)):
                pass
            elif self.culoare(attacker) in ['alb', 'negru'] and self.culoare(attacker) != self.culoare(piesa):
                atac = self.attackPower(attacker, ['stjo'])
                stare = max(stare, atac)

            defense = self.mutare(piesa, dreapta=True, sus=True)
            attacker = self.mutare(piesa, stanga=True, jos=True)
            if defense == None or (
                    self.culoare(defense) in ['alb', 'negru'] and self.culoare(defense) == self.culoare(piesa)):
                pass
            elif self.culoare(attacker) in ['alb', 'negru'] and self.culoare(attacker) != self.culoare(piesa):
                atac = self.attackPower(attacker, ['drsu'])
                stare = max(stare, atac)

            defense = self.mutare(piesa, dreapta=True, jos=True)
            attacker = self.mutare(piesa, stanga=True, sus=True)
            if defense == None or (
                    self.culoare(defense) in ['alb', 'negru'] and self.culoare(defense) == self.culoare(piesa)):
                pass
            elif self.culoare(attacker) in ['alb', 'negru'] and self.culoare(attacker) != self.culoare(piesa):
                atac = self.attackPower(attacker, ['drjo'])
                stare = max(stare, atac)
            return -stare
        else:
            stare = self.attackPower(piesa)
            return stare



    def mutariPiesa(self, piesa):

        # Functia returneaza valorile 'c', [(captured, mutare)] daca piesa are capturi altfel returneaza 'm', [mutare] daca nu are capturi posibile

        if self.culoare(piesa) == 'gol':
            return []

        l_mutari = self.capturariPiesa(piesa)

        if l_mutari != []:
            return 'c', l_mutari

        def valid(mutare):
            if mutare != None and self.culoare(mutare) == 'gol':
                return True
            return False

        mutare = self.mutare(piesa, stanga=True)
        if valid(mutare):
            l_mutari.append(mutare)

        mutare = self.mutare(piesa, dreapta=True)
        if valid(mutare):
            l_mutari.append(mutare)

        mutare = self.mutare(piesa, sus=True)
        if valid(mutare):
            l_mutari.append(mutare)

        mutare = self.mutare(piesa, jos=True)
        if valid(mutare):
            l_mutari.append(mutare)

        mutare = self.mutare(piesa, stanga=True, sus=True)
        if valid(mutare):
            l_mutari.append(mutare)

        mutare = self.mutare(piesa, stanga=True, jos=True)
        if valid(mutare):
            l_mutari.append(mutare)

        mutare = self.mutare(piesa, dreapta=True, sus=True)
        if valid(mutare):
            l_mutari.append(mutare)

        mutare = self.mutare(piesa, dreapta=True, jos=True)
        if valid(mutare):
            l_mutari.append(mutare)

        return 'm', l_mutari





    def frunzeMutarePiesa(self, piesa):

        # Functia returneaza starile finale ale jocului dupa efectuarea tuturor capturilor posibile

        frunze = []
        mutari = self.capturariPiesa(piesa)
        if mutari == []:
            return [self]
        for captured, mutare in mutari:
            copieAlbe = copy.deepcopy(self.pieseAlbe)
            copieNegre = copy.deepcopy(self.pieseNegre)
            if self.culoare(piesa) == 'alb':
                copieAlbe.remove(piesa)
                copieAlbe.append(mutare)
                copieNegre.remove(captured)
            elif self.culoare(piesa) == 'negru':
                copieNegre.remove(piesa)
                copieNegre.append(mutare)
                copieAlbe.remove(captured)

            joc_nou = Joc(copieAlbe, copieNegre)
            frunze.extend(joc_nou.frunzeMutarePiesa(mutare))
        return frunze




    def mutari(self, jucator, final = False):

        # Functia returneaza o lista de succesori posibili

        if jucator == 'alb':
            pieseSelectate = self.pieseAlbe
        elif jucator == 'negru':
            pieseSelectate = self.pieseNegre

        l_mutari = []

        ok = False

        for piesa in pieseSelectate:
            # Generez toate mutarile pentru fiecare piesa din piesele selectate
            type, mutari = self.mutariPiesa(piesa)
            if type == 'c':
                ok = True
                for captured, mutare in mutari:
                    copieAlbe = copy.deepcopy(self.pieseAlbe)
                    copieNegre = copy.deepcopy(self.pieseNegre)

                    if self.culoare(piesa) == 'alb':
                        copieAlbe.remove(piesa)
                        copieAlbe.append(mutare)
                        copieNegre.remove(captured)
                    elif self.culoare(piesa) == 'negru':
                        copieNegre.remove(piesa)
                        copieNegre.append(mutare)
                        copieAlbe.remove(captured)

                    joc_nou = Joc(copieAlbe, copieNegre)
                    # Daca pot face capturi cu o piesa si final == True o sa generez starile finale ale tablei dupa terminarea capturarilor
                    # Adica daca o piesa poate captura, capturez cu ea pana nu mai poate captura
                    if final == True:
                        frunze = self.frunzeMutarePiesa(piesa)
                        l_mutari.extend(frunze)
                    else:
                        l_mutari.append(joc_nou)

        if not ok:
            # Daca nu exista capturari pentru starea curenta a tablei de joc generez toate mutarile posibile
            for piesa in pieseSelectate:
                type, mutari = self.mutariPiesa(piesa)
                for mutare in mutari:
                    copieAlbe = copy.deepcopy(self.pieseAlbe)
                    copieNegre = copy.deepcopy(self.pieseNegre)

                    if self.culoare(piesa) == 'alb':
                        copieAlbe.remove(piesa)
                        copieAlbe.append(mutare)
                    elif self.culoare(piesa) == 'negru':
                        copieNegre.remove(piesa)
                        copieNegre.append(mutare)

                    joc_nou = Joc(copieAlbe, copieNegre)
                    l_mutari.append(joc_nou)

        return l_mutari

    def calculeazaScor(self, jucCurent, varianta = 1):

        jMin = self.__class__.JMIN
        jMax = self.__class__.JMAX

        score = 0
        if varianta == 1:

            # Tin cont de numarul de piese
            score += len(self.pieseAlbe)
            score -= len(self.pieseNegre)

            # Tin cont de numarul de mutari ale pieselor
            mutari = self.mutari('alb')
            score += len(mutari)

            mutari = self.mutari('negru')
            score -= len(mutari)

            # Tin cont de cate piese se afla in triunghiul adversarului
            if len(self.pieseAlbe) >= len(self.endAlbe):
                for piesa in self.endAlbe:
                    if piesa in self.pieseAlbe:
                        score += 1

            if len(self.pieseNegre) >= len(self.endNegre):
                for piesa in self.endNegre:
                    if piesa in self.pieseNegre:
                        score -= 1
        elif varianta == 2:
            score = 0
            def value(piesa):
                x, y = self.unTranslate(piesa)
                if self.culoare(piesa) == 'negru':
                    return y + 1
                else:
                    return 10 - y
            for piesa in self.pieseAlbe:
                x = self.starePiesa(piesa, jucCurent)

                # Tin cont de cat de puternica este o piesa adica daca am doua piese care se pot captura in functie de care e jucatorul curent
                # returnez numarul de atacuri ale adversarului sau ale jucatorului curent, daca nu am atacuri tin cont de cat de avansata este o piesa
                if x != 0:
                    score += self.starePiesa(piesa, jucCurent)
                else:
                    score += value(piesa)

            for piesa in self.pieseNegre:
                x = self.starePiesa(piesa, jucCurent)
                if x != 0:
                    score -= self.starePiesa(piesa, jucCurent)
                else:
                    score -= value(piesa)

        if jMax == 'alb':
            return score
        else:
            return -score

    def estimeaza_scor(self, adancime, jucCurent, varianta = 1):
        tFinal = self.final()
        if tFinal == self.__class__.JMAX:
            return INF + adancime
        elif tFinal == self.__class__.JMIN:
            return -INF - adancime
        else:
            return self.calculeazaScor(jucCurent, varianta)

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
    variantaEstimare = 1

    @classmethod
    def setEstimare(cls, estimare):
        cls.variantaEstimare = estimare

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
        l_mutari = self.tabla_joc.mutari(self.j_curent, True)
        juc_opus = Joc.jucator_opus(self.j_curent)
        l_stari_mutari = [Stare(mutare, juc_opus, self.adancime - 1, parinte=self) for mutare in l_mutari]

        return l_stari_mutari

    def __str__(self):
        sir = str(self.tabla_joc) + "(Juc curent:" + self.j_curent + ")\nScor(pentru calculator): " + \
              str(self.tabla_joc.estimeaza_scor(self.adancime, self.j_curent, self.__class__.variantaEstimare)) + '\n'
        return sir

def min_max(stare, varianta = 1):
    if stare.adancime == 0 or stare.tabla_joc.final():
        stare.estimare = stare.tabla_joc.estimeaza_scor(stare.adancime, stare.j_curent, varianta)
        return 0, stare

    # calculez toate mutarile posibile din starea curenta
    stare.mutari_posibile = stare.mutari()
    nrSucc = len(stare.mutari_posibile)

    # aplic algoritmul minimax pe toate mutarile posibile (calculand astfel subarborii lor)
    # mutariCuEstimare = [min_max(mutare) for mutare in stare.mutari_posibile]
    mutariCuEstimare = []
    for mutare in stare.mutari_posibile:
        newNrSucc, x = min_max(mutare, varianta)
        nrSucc += newNrSucc
        mutariCuEstimare.append(x)

    if stare.j_curent == Joc.JMAX:
        # daca jucatorul e JMAX aleg starea-fiica cu estimarea maxima
        stare.stare_aleasa = max(mutariCuEstimare, key=lambda x: x.estimare)
    else:
        # daca jucatorul e JMIN aleg starea-fiica cu estimarea minima
        stare.stare_aleasa = min(mutariCuEstimare, key=lambda x: x.estimare)
    stare.estimare = stare.stare_aleasa.estimare
    return nrSucc, stare


def alpha_beta(alpha, beta, stare, varianta = 1):
    if stare.adancime == 0 or stare.tabla_joc.final():
        stare.estimare = stare.tabla_joc.estimeaza_scor(stare.adancime, stare.j_curent, varianta)
        return 0, stare

    if alpha > beta:
        return 0, stare  # este intr-un interval invalid deci nu o mai procesez

    stare.mutari_posibile = stare.mutari()
    nrSucc = len(stare.mutari_posibile)

    if stare.j_curent == Joc.JMAX:
        estimare_curenta = float('-inf')

        for mutare in stare.mutari_posibile:
            # calculeaza estimarea pentru starea noua, realizand subarborele
            newSucc, stare_noua = alpha_beta(alpha, beta, mutare, varianta)
            nrSucc += newSucc

            if (estimare_curenta < stare_noua.estimare):
                stare.stare_aleasa = stare_noua
                estimare_curenta = stare_noua.estimare
            if (alpha < stare_noua.estimare):
                alpha = stare_noua.estimare
                if alpha >= beta:
                    break

    elif stare.j_curent == Joc.JMIN:
        estimare_curenta = float('inf')

        for mutare in stare.mutari_posibile:

            newSucc, stare_noua = alpha_beta(alpha, beta, mutare, varianta)
            nrSucc += newSucc

            if (estimare_curenta > stare_noua.estimare):
                stare.stare_aleasa = stare_noua
                estimare_curenta = stare_noua.estimare

            if (beta > stare_noua.estimare):
                beta = stare_noua.estimare
                if alpha >= beta:
                    break
    stare.estimare = stare.stare_aleasa.estimare

    return nrSucc, stare

def afis_daca_final(stare_curenta):
    final = stare_curenta.tabla_joc.final()
    if final:
        stare_curenta.tabla_joc.deseneaza(final)
        print("A castigat " + final)
        return True

    return False


def main():
    pygame.init()
    ecran = pygame.display.set_mode(size=(270, 510))
    Joc.initializeaza(ecran, translatie=35)

    tabla_curenta = Joc()
    Joc.JMIN, tip_algoritm, rand, adancime, varianta = deseneaza_alegeri(ecran, tabla_curenta)

    Joc.JMAX = 'alb' if Joc.JMIN == 'negru' else 'negru'
    jucator = Joc.JMIN if rand == 'player' else Joc.JMAX

    pygame.display.set_caption('Lazar Mihai Astar')
    tabla_curenta.deseneaza()

    stare_curenta = Stare(tabla_curenta, jucator, adancime)
    stare_curenta.setEstimare(varianta)

    print(str(stare_curenta))
    timpiList = []
    noduriGenerate = []
    tProgram_inainte = int(round(time.time() * 1000))
    nrMutari = 0
    while True:
        if (afis_daca_final(stare_curenta)):
            tProgram_dupa = int(round(time.time() * 1000))

            print('\n\nRulare program totala: ' + str(tProgram_dupa - tProgram_inainte) + ' milisecunde')
            print('Numar total mutari: ' + str(nrMutari))
            print('Timpi:')
            if timpiList != []:
                print(' min: ' + str(min(timpiList)))
                print(' max: ' + str(max(timpiList)))
                print(' media: ' + str(sum(timpiList) / len(timpiList)))
                print(' mediana: ' + str(statistics.median(timpiList)))
            else:
                print(' min: 0')
                print(' max: 0')
                print(' media: 0')
                print(' mediana: 0')

            print('Noduri Generate:')
            if noduriGenerate != []:
                print(' min: ' + str(min(noduriGenerate)))
                print(' max: ' + str(max(noduriGenerate)))
                print(' media: ' + str(sum(noduriGenerate) / len(noduriGenerate)))
                print(' mediana: ' + str(statistics.median(noduriGenerate)))
            else:
                print(' min: 0')
                print(' max: 0')
                print(' media: 0')
                print(' mediana: 0')
            break

        if stare_curenta.j_curent == Joc.JMIN:
            tu_inainte = int(round(time.time() * 1000))
            while stare_curenta.j_curent == Joc.JMIN:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        tProgram_dupa = int(round(time.time() * 1000))

                        print('\n\nRulare program totala: ' + str(tProgram_dupa - tProgram_inainte) + ' milisecunde')
                        print('Numar total mutari: ' + str(nrMutari))
                        print('Timpi:')
                        if timpiList != []:
                            print(' min: ' + str(min(timpiList)))
                            print(' max: ' + str(max(timpiList)))
                            print(' media: ' + str(sum(timpiList) / len(timpiList)))
                            print(' mediana: ' + str(statistics.median(timpiList)))
                        else:
                            print(' min: 0')
                            print(' max: 0')
                            print(' media: 0')
                            print(' mediana: 0')

                        print('Noduri Generate:')
                        if noduriGenerate != []:
                            print(' min: ' + str(min(noduriGenerate)))
                            print(' max: ' + str(max(noduriGenerate)))
                            print(' media: ' + str(sum(noduriGenerate) / len(noduriGenerate)))
                            print(' mediana: ' + str(statistics.median(noduriGenerate)))
                        else:
                            print(' min: 0')
                            print(' max: 0')
                            print(' media: 0')
                            print(' mediana: 0')

                        pygame.quit()  # inchide fereastra
                        sys.exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        pos = pygame.mouse.get_pos()
                        if stare_curenta.j_curent == 'alb':
                            pieseJucator = stare_curenta.tabla_joc.pieseAlbe
                        else:
                            pieseJucator = stare_curenta.tabla_joc.pieseNegre

                        pieseCapt = []
                        pieseMut = []

                        for piesa in pieseJucator:
                            type, mutari = stare_curenta.tabla_joc.mutariPiesa(piesa)
                            if type == 'c':
                                pieseCapt.append(piesa)
                            elif type == 'm' and mutari != []:
                                pieseMut.append(piesa)

                        if pieseCapt != []:
                            pieseJucator = pieseCapt
                        else:
                            pieseJucator = pieseMut


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
                                                    tabla_curenta = Joc(copieAlbe, copieNegre)
                                                    stare_curenta.tabla_joc = tabla_curenta

                                                    tip, capt = stare_curenta.tabla_joc.mutariPiesa(mutare)

                                                    if tip != 'c':
                                                        stare_curenta.j_curent = Joc.JMAX
                                                        nrMutari += 1
                                                    else:
                                                        stare_curenta.tabla_joc.setNodPiesaSelectata(mutare)

                                                    tu_dupa = int(round(time.time() * 1000))
                                                    print('Tabla dupa mutarea utilizatorului')
                                                    print(str(stare_curenta))
                                                    print('Utilizatorul a gandit ' + str(tu_dupa - tu_inainte) + ' milisecunde\n')

                                                    stare_curenta.tabla_joc.deseneaza()
                                        elif type == 'm':
                                            for mutare in mutariPiesa:
                                                if nod == mutare:
                                                    copieAlbe = copy.deepcopy(stare_curenta.tabla_joc.pieseAlbe)
                                                    copieNegre = copy.deepcopy(stare_curenta.tabla_joc.pieseNegre)

                                                    if stare_curenta.j_curent == 'alb':
                                                        copieAlbe.remove(piesaSelectata)
                                                        copieAlbe.append(mutare)

                                                    elif stare_curenta.j_curent == 'negru':
                                                        copieNegre.remove(piesaSelectata)
                                                        copieNegre.append(mutare)

                                                    stare_curenta.tabla_joc.setNodPiesaSelectata(False)
                                                    tabla_curenta = Joc(copieAlbe, copieNegre)
                                                    stare_curenta.tabla_joc = tabla_curenta
                                                    stare_curenta.j_curent = Joc.JMAX
                                                    nrMutari += 1

                                                    tu_dupa = int(round(time.time() * 1000))
                                                    print('Tabla dupa mutarea utilizatorului')
                                                    print(str(stare_curenta))
                                                    print('Utilizatorul a gandit ' + str(
                                                        tu_dupa - tu_inainte) + ' milisecunde\n')
                                                    stare_curenta.tabla_joc.deseneaza()
        else:
            t_inainte = int(round(time.time() * 1000))
            if tip_algoritm == '1':
                nrNoduri, stare_actualizata = min_max(stare_curenta, varianta)
            else:
                nrNoduri, stare_actualizata = alpha_beta(-500, 500, stare_curenta, varianta)

            stare_curenta.tabla_joc = stare_actualizata.stare_aleasa.tabla_joc
            print("Tabla dupa mutarea calculatorului")

            stare_curenta.j_curent = Joc.JMIN
            nrMutari += 1
            print(str(stare_curenta))

            stare_curenta.tabla_joc.deseneaza()
            # preiau timpul in milisecunde de dupa mutare
            t_dupa = int(round(time.time() * 1000))
            print("Calculatorul a \"gandit\" timp de " + str(t_dupa - t_inainte) + " milisecunde.")
            print("Au fost generate " + str(nrNoduri) + " noduri.")

            noduriGenerate.append(nrNoduri)
            timpiList.append(t_dupa - t_inainte)

            # S-a realizat o mutare. Schimb jucatorul cu cel opus

if __name__ == '__main__':

    main()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()