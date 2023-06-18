import pygame
import sys
import math


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
        print(inod, nod)
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

    scalare = 50
    translatie = 20
    razaPct = 10
    razaPiesa = 20


pygame.init()
culoareEcran = (255, 255, 255)
culoareLinii = (0, 0, 0)

ecran = pygame.display.set_mode(size=(250, 500))

piesaAlba = pygame.image.load('piesa-alba.png')
diametruPiesa = 2 * Graph.razaPiesa
piesaAlba = pygame.transform.scale(piesaAlba, (diametruPiesa, diametruPiesa))
piesaNeagra = pygame.image.load('piesa-neagra.png')
piesaNeagra = pygame.transform.scale(piesaNeagra, (diametruPiesa, diametruPiesa))
piesaSelectata = pygame.image.load('piesa-rosie.png')
piesaSelectata = pygame.transform.scale(piesaSelectata, (diametruPiesa, diametruPiesa))
nodPiesaSelectata = False
coordonateNoduri = [[Graph.translatie + Graph.scalare * x for x in nod] for nod in Graph.noduri]
print('coordonateNoduri: ', coordonateNoduri)
pieseAlbe = []
nodPiesaSelectata = None
pieseNegre = []


def deseneazaEcranJoc():
    ecran.fill(culoareEcran)
    # for nod in coordonateNoduri:
    #     pygame.draw.circle(surface=ecran, color=culoareLinii, center=nod, radius=Graph.razaPct,
    #                        width=0)  # width=0 face un cerc plin

    print("Albe: ", pieseAlbe)
    print("Negre: ",pieseNegre)
    for muchie in Graph.muchii:
        p0 = coordonateNoduri[muchie[0]]
        p1 = coordonateNoduri[muchie[1]]
        pygame.draw.line(surface=ecran, color=culoareLinii, start_pos=p0, end_pos=p1, width=5)
    for nod in pieseAlbe:
        ecran.blit(piesaAlba, (nod[0] - Graph.razaPiesa, nod[1] - Graph.razaPiesa))
    for nod in pieseNegre:
        ecran.blit(piesaNeagra, (nod[0] - Graph.razaPiesa, nod[1] - Graph.razaPiesa))
    if nodPiesaSelectata:
        ecran.blit(piesaSelectata, (nodPiesaSelectata[0] - Graph.razaPiesa, nodPiesaSelectata[1] - Graph.razaPiesa))
    pygame.display.update()


deseneazaEcranJoc()
rand = 0

print("Muta " + ("negru" if rand else "alb"))
while True:

    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if ev.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            for nod in coordonateNoduri:
                if distEuclid(pos, nod) <= Graph.razaPct:
                    if rand == 1:
                        piesa = piesaNeagra
                        pieseCurente = pieseNegre
                    else:
                        piesa = piesaAlba
                        pieseCurente = pieseAlbe

                    if nod not in pieseAlbe + pieseNegre:

                        if nodPiesaSelectata:

                            n0 = coordonateNoduri.index(nod)
                            n1 = coordonateNoduri.index(nodPiesaSelectata)
                            if ((n0, n1) in Graph.muchii or (n1, n0) in Graph.muchii):
                                pieseCurente.remove(nodPiesaSelectata)
                                pieseCurente.append(nod)
                                rand = 1 - rand
                                print("Muta " + ("negru" if rand else "alb"))
                                nodPiesaSelectata = False
                        else:
                            pieseCurente.append(nod)
                            rand = 1 - rand
                            print("Muta " + ("negru" if rand else "alb"))
                    else:
                        if nod in pieseCurente:
                            if nodPiesaSelectata == nod:
                                nodPiesaSelectata = False
                            else:
                                nodPiesaSelectata = nod

                    deseneazaEcranJoc()
                    break

if __name__ == '__main__':
    exit(0)