import sys, os, stopit, time
class NodParcurgere:
    # (raza, Broaste{Mormo : (gr, id)}, Frunze{ id : (x, y, m, max)})
    def __init__(self, info, parinte, cost = 0, h = 0):
        '''
        :param info (tuple): informatiile nodului
        :param parinte (NodParcurgere): adresa parintelui nodului curent
        :param cost (float): costul drumului de la starea initiala pana la nodul curent (self)
        :param h (float): euristica
        '''
        self.info = info
        self.parinte = parinte
        self.g = cost
        self.h = h
        self.f = self.g + self.h

    def obtineDrum(self):
        '''
        :return:
            list: lista nodurilor care se afla in drum
        '''
        l = [self]
        nod = self
        while nod.parinte is not None:
            l.insert(0, nod.parinte)
            nod = nod.parinte
        return l

    def contineInDrum(self, infoNodNou):
        '''

        :param infoNodNou (tuple): are valoarea informatiilor unui obiect de tip NodParcurgere
        :return:
            bool: True daca infoNodNou se afla in drum altfel False
        '''
        nodDrum = self
        while nodDrum is not None:
            if nodDrum.info == infoNodNou:
                return True
            nodDrum = nodDrum.parinte
        return False

    def istoricBroasca(self, broasca):
        '''

        :param broasca (str): id-ul broastei careia ii cautam lista de frunze vizitate in ordine inversa
        :return:
            list: lista frunzelor vizitate de broasca in ordine inversa
        '''
        nodCurent = self
        l = []
        while nodCurent != None:
            frunza = nodCurent.info[1][broasca][1]
            l.append(frunza)
            nodCurent = nodCurent.parinte
        return l

    def afisDrum(self, output, afisCost = False, afisLung=False):
        '''
            Scrie drumul in fisierul de output

        :param output (_io.TextIOWrapper): fisierul de output
        :param afisCost (bool): True daca frem sa afosam costul drumului
        :param afisLung (bool): True daca vrem sa afisam lungimea drumului
        '''
        l = self.obtineDrum()
        for (i, nod) in enumerate(l):
            output.write(str(i+1) + ')\n')
            broaste = nod.info[1]
            frunze = nod.info[2]
            for key in broaste:
                fr = broaste[key][1]
                if i == 0:
                    if fr != 'mal':
                        output.write(key + ' se afla pe frunza initiala ' + fr + '(' + str(frunze[fr][0]) + ', ' +
                                str(frunze[fr][1]) + '). Greutate broscuta: ' + str(broaste[key][0]) + '\n')
                    else:
                        output.write(key + ' se afla pe mal. Greutate broscuta: ' + str(broaste[key][0]) + '\n')
                else:
                    parinte = nod.parinte
                    greutateAnterioara = parinte.info[1][key][0]
                    frunzaAnterioara = parinte.info[1][key][1]
                    greutateCurenta = broaste[key][0]
                    insecteMancate = greutateCurenta - greutateAnterioara + 1
                    if frunzaAnterioara != 'mal':
                        frunzaAnterioaraInfo = parinte.info[2][frunzaAnterioara]
                        if fr != 'mal':
                            output.write(key + ' a mancat ' + str(insecteMancate) + ' insecte. ' +
                                    key + ' a sarit de la ' + frunzaAnterioara + '(' +
                                    str(frunzaAnterioaraInfo[0]) + ', ' + str(frunzaAnterioaraInfo[1]) +
                                    ') la ' + fr + '(' + str(frunze[fr][0]) + ', ' +
                                    str(frunze[fr][1]) + '). Greutate broscuta: ' + str(broaste[key][0]) + '\n')
                        else:
                            output.write(key + ' a mancat ' + str(insecteMancate) + ' insecte. ' +
                                         key + ' a sarit de la ' + frunzaAnterioara + '(' +
                                         str(frunzaAnterioaraInfo[0]) + ', ' + str(frunzaAnterioaraInfo[1]) +
                                         ') la mal. Greutate broscuta: ' + str(broaste[key][0]) + '\n')

            output.write('Stare frunze: ')
            lf = ''
            i = 0
            for fr in frunze:
                i += 1
                if i == len(frunze):
                    lf = fr
                    break
                output.write(fr + '(' + str(frunze[fr][2]) + ', ' + str(frunze[fr][3]) + '), ')
            output.write(lf + '(' + str(frunze[lf][2]) + ', ' + str(frunze[lf][3]) + ')\n\n')

        if afisCost:
            output.write('Cost: ' + str(self.g) + '\n')
        if afisLung:
            output.write('Lungime: ' + str(len(l)) + '\n')






class Graph:
    def __init__(self, input):
        '''
            Atentie sirul 'mal' este rezervat pentru testarea scopului,
            broastele se pot afla pe mal dar nu putem avea frunze cu id-ul 'mal'

        :param input(_io.TextIOWrapper): Fisierul sursa din care extragem datele de intrare
        '''

        continut = input.read().strip().split('\n')

        raza = int(continut[0])
        braux = [x.strip() for x in continut[1].strip().split()]

        nrBroaste = len(braux)//3
        broaste = {}
        for i in range(nrBroaste):
            broaste[braux[i*3]] = (int(braux[i*3+1]), braux[i*3+2])

        fraux = [continut[i].strip().split() for i in range(len(continut)) if i > 1]

        frunze = {}
        for x in fraux:
            frunze[x[0]] = (float(x[1]), float(x[2]), int(x[3]), int(x[4]))

        self.start = (raza, broaste, frunze)
        self.validateFrunze()
        self.validateBroaste()


    def validateFrunze(self):
        '''
            Validarea frunzelor primite. Atentie sirul 'mal' este rezervat pentru testarea scopului,
            broastele se pot afla pe mal dar nu putem avea frunze cu id-ul 'mal'
        '''
        raza = self.start[0]
        frunze = self.start[2]
        for fr in frunze:
            eq = frunze[fr][0]**2 + frunze[fr][1]**2
            if fr == 'mal':
                raise ValueError('Nu pot exista frunze cu id-ul "mal"')
            if eq >= raza ** 2:
                raise ValueError('Exista frunze in afara lacului')
            if frunze[fr][2] < 0:
                raise ValueError('Exista frunze cu numarul de insecte negativ')
            if frunze[fr][3] < 0:
                raise ValueError('Frunza are greutatea maxima acceptata negativa')
            if frunze[fr][2] > frunze[fr][3]:
                raise ValueError('Sunt prea multe insecte pe frunza')

    def validateBroaste(self):
        '''
            Validarea broastele primite. Atentie sirul 'mal' este rezervat pentru testarea scopului,
            broastele se pot afla pe mal dar nu putem avea frunze cu id-ul 'mal'
        '''
        broaste = self.start[1]
        frunze = self.start[2]
        greutateFrunze = {fr : frunze[fr][3] - frunze[fr][2] for fr in frunze}
        for br in broaste:
            if broaste[br][0] <= 0:
                raise ValueError('Exista broaste moarte (greutate <= 0)')
            if broaste[br][1] != 'mal' and broaste[br][1] not in frunze:
                raise ValueError('Exista broaste care stau pe frunze care nu exista')

            frunzaCurenta = broaste[br][1]
            greutateBroasca = broaste[br][0]
            if frunzaCurenta != 'mal':
                greutateFrunze[frunzaCurenta] -= greutateBroasca
                if greutateFrunze[frunzaCurenta] < 0:
                    raise ValueError('Exita prea multe broaste pe o frunza')


    def testeazaScop(self, nodCurent):
        '''

        :param nodCurent (tuple): valoarile nodului curent
        :return:
            bool: True daca nodCurent este nod scop altfel False
        '''
        broaste = nodCurent.info[1]
        for br in broaste:
            if broaste[br][1] != 'mal':
                return False
        return True

    def genereazaSuccesori(self, nodCurent, tipEuristica = 'b'):
        '''

        :param nodCurent (tuple): valoarile nodului curent
        :param tipEuristica (str): euristica pe care vrem sa o folosim
                                       - 'b' pentru banala
                                       - 'a1' pentru admisibila 1
                                       - 'a2' pentru admisibila 2
                                       - 'n' pentru neadmisibila
        :return:
            list: lista succesorilor nodului curent
        '''
        listaSuccesori = []
        # [NodParcurgere()]
        broaste = nodCurent.info[1]
        frunze = nodCurent.info[2]


        salturiPosibile = {x : [] for x in broaste} # {br1 : [(greutateBroasca, frunza)]}
        for br in broaste:

            if broaste[br][1] == 'mal':
                salturiPosibile[br] = [broaste[br]]
                continue

            frunzaCurenta = broaste[br][1]
            salturi = []

            for insecte in range(frunze[frunzaCurenta][2]+1):
                greutateNoua = insecte + broaste[br][0] - 1
                distMax = (greutateNoua + 1) / 3
                distMal = nodCurent.info[0] - (frunze[frunzaCurenta][0]**2 + frunze[frunzaCurenta][1]**2)**(1/2)

                if greutateNoua > 0 and distMal < distMax:
                    salturi.append((greutateNoua, 'mal'))

                for fr in frunze:
                    if fr == frunzaCurenta:
                        continue
                    distFr = ((frunze[fr][0] - frunze[frunzaCurenta][0])**2 +
                                (frunze[fr][1] - frunze[frunzaCurenta][1])**2)**(1/2)

                    if greutateNoua > 0 and greutateNoua <= frunze[fr][3] and distFr <= distMax:
                        salturi.append((greutateNoua, fr))
            if salturi == []:
                return []
            salturiPosibile[br] = salturi

        def costSolutie(newBroaste):
            '''

            :param newBroaste (dict): noile braste generate
            :return:
                float: costul pentru a ajunge la configuratia broastelor date ca parametru
            '''
            cost = 0
            for br in newBroaste:
                frunzaVeche = broaste[br][1]
                frunzaCurenta = newBroaste[br][1]
                if frunzaVeche != 'mal':
                    if frunzaCurenta != 'mal':
                        dist = ((frunze[frunzaVeche][0] - frunze[frunzaCurenta][0])**2 +
                                (frunze[frunzaVeche][1] - frunze[frunzaCurenta][1])**2)**(1/2)
                    else:
                        dist = nodCurent.info[0] - (frunze[frunzaVeche][0] ** 2 + frunze[frunzaVeche][1] ** 2) ** (1 / 2)
                    cost += dist
            return cost

        def validate(newBroaste):
            '''

            :param newBroaste (dict): noile braste generate
            :return:
                bool: True daca configuratia broastelor data ca parametru este valida, altfel False
            '''
            maxGrFrunze = {fr : frunze[fr][3] for fr in frunze}
            insecteFrunze = {fr : frunze[fr][2] for fr in frunze}
            for br in newBroaste:
                greutateNoua = newBroaste[br][0]
                frunzaCurenta = newBroaste[br][1]
                if frunzaCurenta != 'mal':
                    maxGrFrunze[frunzaCurenta] -= greutateNoua
                    if maxGrFrunze[frunzaCurenta] - insecteFrunze[frunzaCurenta] < 0:
                        return False
            return True

        def generateFrunze(newBroaste):
            '''

            :param newBroaste (dict): noile braste generate
            :return:
                bool: False daca nu putem genera o configuratie a frunzelor valida pentru configuratia
                      broastelor data ca parametru
                dict: Configuratia frunzelor pentru configuratia broastelor data ca parametru daca aceasta este valida
            '''
            sol = frunze.copy()

            for br in newBroaste:
                frunzaVeche = broaste[br][1]
                if frunzaVeche == 'mal':
                    continue
                greutateNoua = newBroaste[br][0]
                greutateVeche = broaste[br][0]
                insecteMancate = greutateNoua - greutateVeche + 1
                insecteRamase = sol[frunzaVeche][2] - insecteMancate
                if insecteRamase < 0:
                    return False
                sol[frunzaVeche] = (sol[frunzaVeche][0], sol[frunzaVeche][1], insecteRamase, sol[frunzaVeche][3])


            return sol



        def generateBroaste(k, salturiPosibile, sol = {}):
            '''
            :param k (int): indexul broastei curente pentru care alegem un salt
            :param salturiPosibile (dict): salturile posibile pentru fiecare broasca
            :param sol (dict): salturile alese pentru fiecare broasca
            :return:
            '''

            l = sol
            if k == len(salturiPosibile):
                newFrunze = generateFrunze(l)
                if newFrunze != False and validate(l):
                    listaSuccesori.append((nodCurent.info[0], l.copy(), newFrunze))

                return None
            for (idx, br) in enumerate(salturiPosibile):
                if idx == k:
                    for val in salturiPosibile[br]:
                        l[br] = val
                        generateBroaste(k+1, salturiPosibile, l)

        generateBroaste(0, salturiPosibile)

        listaSuccesori2 = []

        for succ in listaSuccesori:
            costMutare = costSolutie(succ[1])
            if not nodCurent.contineInDrum(succ):
                nodNou = NodParcurgere(succ, nodCurent, cost=nodCurent.g + costMutare, h=self.calculeazaH(succ, nodCurent, tipEuristica))
                listaSuccesori2.append(nodNou)

        return listaSuccesori2


    def calculeazaH(self, nodCurent, parinte, tipEuristica= 'b'):
        '''

        :param nodCurent (tuple): nodul curent caruia ii calculam euristica
        :param parinte (NodParcurgere): parintee nodului curent
        :param tipEuristica (str): euristica pe care vrem sa o folosim
                                       - 'b' pentru banala
                                       - 'a1' pentru admisibila 1
                                       - 'a2' pentru admisibila 2
                                       - 'n' pentru neadmisibila
        :return:
            float: rezultatul euristicii calculate
        '''
        raza = nodCurent[0]
        broaste = nodCurent[1]
        frunze = nodCurent[2]
        if tipEuristica == 'b':
            min = float('inf')
            for br in broaste:
                frunzaCurenta = broaste[br][1]
                if frunzaCurenta != 'mal':
                    x = frunze[frunzaCurenta][0]
                    y = frunze[frunzaCurenta][1]
                    distMal = raza - (x ** 2 + y ** 2) ** (1 / 2)
                    if distMal < min:
                        min = distMal
            if min != float('inf'):
                return min
            return 0

        if tipEuristica == 'a1':
            count = 0
            min = float('inf')
            for br in broaste:
                frunzaCurenta = broaste[br][1]
                if frunzaCurenta != 'mal':
                    count += 1
                    x = frunze[frunzaCurenta][0]
                    y = frunze[frunzaCurenta][1]
                    distMal = raza - (x ** 2 + y ** 2) ** (1 / 2)
                    if distMal < min:
                        min = distMal
            if min != float('inf'):
                return count * min
            return 0


        if tipEuristica == 'a2':
            h = 0
            for br in broaste:
                frunzaCurenta = broaste[br][1]
                if frunzaCurenta != 'mal':
                    x = frunze[frunzaCurenta][0]
                    y = frunze[frunzaCurenta][1]
                    distMal = raza - (x ** 2 + y ** 2) ** (1 / 2)
                    h += distMal
            return h

        if tipEuristica == 'n':
            h = 0
            for br in broaste:
                frunzaCurenta = broaste[br][1]
                istoricBroasca = parinte.istoricBroasca(br)
                istoricBroasca.append(frunzaCurenta)
                repetiti = len(istoricBroasca) - len(set(istoricBroasca))
                if frunzaCurenta != 'mal':
                    x = frunze[frunzaCurenta][0]
                    y = frunze[frunzaCurenta][1]
                    distMal = (x ** 2 + y ** 2) ** (1 / 2) * 100
                    h += distMal

                if repetiti != 0:
                    h *= repetiti + 1
            return h
        return 0

@stopit.threading_timeoutable(default='breathFirst timeout')
def breathFirst(gr, nrSol, output):
    '''

    :param gr (Graph): graful pe care cautam solutii
    :param nrSol (int): numarul de solutii cautate
    :param output (_io.TextIOWrapper): fisierul de output
    :return:
        str: 'breathFirst terminat' daca functia nu a intrat in timeout, altfel 'breathFirst timeout'
    '''
    c = [NodParcurgere(gr.start, None)]
    maxNoduriMemorie = 1
    totalSuccesoriGenerati = 0
    nr = 1
    while len(c) > 0:
        maxNoduriMemorie = max(maxNoduriMemorie, len(c))
        nodCurent = c.pop(0)
        if gr.testeazaScop(nodCurent):
            output.write('Solutie ' + str(nr) + ':\n')
            nodCurent.afisDrum(output, True, True)
            output.write(str(time.time() - t1) + " secunde\n")
            output.write('Numarul maxim de noduri existente in memorie: ' + str(maxNoduriMemorie) + '\n')
            output.write('Numarul total de succesori generati: ' + str(totalSuccesoriGenerati) + '\n')
            output.write('\n-------------------------\n\n')
            nrSol -= 1
            nr += 1
            if nrSol == 0:
                return 'breathFirst terminat'

        lSuccesori = gr.genereazaSuccesori(nodCurent, 'none')
        totalSuccesoriGenerati += len(lSuccesori)

        c.extend(lSuccesori)

    return 'breathFirst terminat'

@stopit.threading_timeoutable(default='depthFirst timeout')
def depthFirst(gr, nrSol, output):
    '''

    :param gr (Graph): graful pe care cautam solutii
    :param nrSol (int): numarul de solutii cautate
    :param output (_io.TextIOWrapper): fisierul de output
    :return:
        str: 'depthFirst terminat' daca functia nu a intrat in timeout, altfel 'depthFirst timeout'
    '''
    df(NodParcurgere(gr.start, None), nrSol, output)
    return 'depthFirst terminat'

def df(nodCurent, nrSol, output, nr = 0, maxNoduriMemorie = 1, totalSuccesoriGenerati = 0, nrNodesInMemory = 1):
    '''

    :param nodCurent (tuple): nodul curent
    :param nrSol (int): numarul de solutii cautate
    :param output (_io.TextIOWrapper): fisierul de output
    :param nr (int): numarul solutiilor gasite
    :param maxNoduriMemorie (int): numarul maxim de noduri in memorie
    :param totalSuccesoriGenerati (int): numarul de succesori generati
    :param nrNodesInMemory (int): numarul de noduri in memorie
    :return:
        tuple: (nrSol, nr, maxNoduriMemorie, totalSuccesoriGenerati)
    '''
    if nrSol <= 0:
        return (nrSol, nr, maxNoduriMemorie, totalSuccesoriGenerati)
    if gr.testeazaScop(nodCurent):
        nr += 1
        output.write('Solutie ' + str(nr) + ':\n')
        nodCurent.afisDrum(output, True, True)
        output.write(str(time.time() - t1) + " secunde\n")
        output.write('Numarul maxim de noduri existente in memorie: ' + str(maxNoduriMemorie) + '\n')
        output.write('Numarul total de succesori generati: ' + str(totalSuccesoriGenerati) + '\n')
        output.write('\n-------------------------\n\n')
        nrSol -= 1
        if nrSol == 0:
            return (nrSol, nr, maxNoduriMemorie, totalSuccesoriGenerati)

    lSuccesori = gr.genereazaSuccesori(nodCurent, 'none')
    totalSuccesoriGenerati += len(lSuccesori)
    nrNodesInMemory += len(lSuccesori)
    maxNoduriMemorie = max(maxNoduriMemorie, nrNodesInMemory)
    for next in lSuccesori:

        if nrSol != 0:
            (nrSol, nr, maxNoduriMemorie, totalSuccesoriGenerati) = df(next, nrSol, output, nr, maxNoduriMemorie,
                                                                       totalSuccesoriGenerati, nrNodesInMemory)
        else:
            break
    return (nrSol, nr, maxNoduriMemorie, totalSuccesoriGenerati)


@stopit.threading_timeoutable(default='depthFirstIterativ timeout')
def depthFirstIterativ(gr, nrSol, output, depthMax):
    '''

    :param gr (Graph): graful pe care cautam solutii
    :param nrSol (int): numarul de solutii cautate
    :param output (_io.TextIOWrapper): fisierul de output
    :param depthMax (int): adancimea maxima
    :return:
        str: 'depthFirstIterativ terminat' daca functia nu a intrat in timeout, altfel 'depthFirstIterativ timeout'
    '''
    nr = 0
    maxNoduriMemorie = 1
    totalSuccesoriGenerati = 0
    for i in range(1, depthMax+1):
        if nrSol != 0:
            (nrSol, nr, maxNoduriMemorie, totalSuccesoriGenerati) = dfi(NodParcurgere(gr.start, None), nrSol, output, i,
                                                                        nr, maxNoduriMemorie, totalSuccesoriGenerati)
        else:
            break
    return 'depthFirstIterativ terminat'

def dfi(nodCurent, nrSol, output, adancime, nr = 0, maxNoduriMemorie = 1, totalSuccesoriGenerati = 0, nrNodesInMemory = 1):
    '''

    :param nodCurent (tuple): nodul curent
    :param nrSol (int): numarul de solutii cautate
    :param output (_io.TextIOWrapper): fisierul de output
    :param adancime (int): adancimea la care cautam solutia
    :param nr (int): numarul solutiilor gasite
    :param maxNoduriMemorie (int): numarul maxim de noduri in memorie
    :param totalSuccesoriGenerati (int): numarul de succesori generati
    :param nrNodesInMemory (int): numarul de noduri in memorie

    :return:
        tuple: (nrSol, nr, maxNoduriMemorie, totalSuccesoriGenerati)
    '''
    if adancime == 1 and gr.testeazaScop(nodCurent):
        nr += 1
        output.write('Solutie ' + str(nr) + ':\n')
        nodCurent.afisDrum(output, True, True)
        output.write(str(time.time() - t1) + " secunde\n")
        output.write('Numarul maxim de noduri existente in memorie: ' + str(maxNoduriMemorie) + '\n')
        output.write('Numarul total de succesori generati: ' + str(totalSuccesoriGenerati) + '\n')
        output.write('\n-------------------------\n\n')
        nrSol -= 1
        if nrSol == 0:
            return (nrSol, nr, maxNoduriMemorie, totalSuccesoriGenerati)

    if adancime > 1:
        lSuccesori = gr.genereazaSuccesori(nodCurent, 'none')
        totalSuccesoriGenerati += len(lSuccesori)
        nrNodesInMemory += len(lSuccesori)
        maxNoduriMemorie = max(maxNoduriMemorie, nrNodesInMemory)
        for next in lSuccesori:
            if nrSol != 0:
                (nrSol, nr, maxNoduriMemorie, totalSuccesoriGenerati) = dfi(next, nrSol, output, adancime - 1, nr, maxNoduriMemorie,
                                                                           totalSuccesoriGenerati, nrNodesInMemory)
            else:
                break
    return (nrSol, nr, maxNoduriMemorie, totalSuccesoriGenerati)



@stopit.threading_timeoutable(default='aStar timeout')
def aStar(gr, nrSol, output, tipEuristica = 'b'):
    '''

    :param gr (Graph): graful pe care cautam solutii
    :param nrSol (int): numarul de solutii cautate
    :param output (_io.TextIOWrapper): fisierul de output
    :param tipEuristica (str): euristica pe care vrem sa o folosim
                                       - 'b' pentru banala
                                       - 'a1' pentru admisibila 1
                                       - 'a2' pentru admisibila 2
                                       - 'n' pentru neadmisibila
    :return:
        str: 'aStar terminat' daca functia nu a intrat in timeout, altfel 'aStar timeout'
    '''

    c = [NodParcurgere(gr.start, None, 0, gr.calculeazaH(gr.start, tipEuristica))]
    maxNoduriMemorie = 1
    totalSuccesoriGenerati = 0
    nr = 1
    while len(c) > 0:
        maxNoduriMemorie = max(maxNoduriMemorie, len(c))
        nodCurent = c.pop(0)
        if gr.testeazaScop(nodCurent):
            output.write('Solutie ' + str(nr) + ':\n')
            nodCurent.afisDrum(output, True, True)
            output.write(str(time.time() - t1) + " secunde\n")
            output.write('Numarul maxim de noduri existente in memorie: ' + str(maxNoduriMemorie) + '\n')
            output.write('Numarul total de succesori generati: ' + str(totalSuccesoriGenerati) + '\n')
            output.write('\n-------------------------\n\n')
            nrSol -= 1
            nr += 1
            if nrSol == 0:
                return 'aStar terminat'

        lSuccesori = gr.genereazaSuccesori(nodCurent, tipEuristica)
        totalSuccesoriGenerati += len(lSuccesori)

        for sol in lSuccesori:
            i = 0
            gasitLoc = False

            for i in range(len(c)):
                if sol.f <= c[i].f:
                    gasitLoc = True
                    break

            if gasitLoc:
                c.insert(i, sol)
            else:
                c.append(sol)


    return 'aStar terminat'

@stopit.threading_timeoutable(default='aStarOptimizat timeout')
def aStarOptimizat(gr, nrSol, output, tipEuristica = 'b'):
    '''

    :param gr (Graph): graful pe care cautam solutii
    :param nrSol (int): numarul de solutii cautate
    :param output (_io.TextIOWrapper): fisierul de output
    :param tipEuristica (str): euristica pe care vrem sa o folosim
                                       - 'b' pentru banala
                                       - 'a1' pentru admisibila 1
                                       - 'a2' pentru admisibila 2
                                       - 'n' pentru neadmisibila
    :return:
        str: 'aStarOptimizat terminat' daca functia nu a intrat in timeout, altfel 'aStarOptimizat timeout'
    '''

    lOpen = [NodParcurgere(gr.start, None, 0, gr.calculeazaH(gr.start, tipEuristica))]
    lClosed = []
    maxNoduriMemorie = 1
    totalSuccesoriGenerati = 0
    nr = 1
    while len(lOpen) > 0:
        maxNoduriMemorie = max(maxNoduriMemorie, len(lOpen))
        nodCurent = lOpen.pop(0)
        lClosed.append(nodCurent)
        if gr.testeazaScop(nodCurent):
            output.write('Solutie ' + str(nr) + ':\n')
            nodCurent.afisDrum(output, True, True)
            output.write(str(time.time() - t1) + " secunde\n")
            output.write('Numarul maxim de noduri existente in memorie: ' + str(maxNoduriMemorie) + '\n')
            output.write('Numarul total de succesori generati: ' + str(totalSuccesoriGenerati) + '\n')
            output.write('\n-------------------------\n\n')
            nrSol -= 1
            nr += 1
            if nrSol == 0:
                return 'aStarOptimizat terminat'

        lSuccesori = gr.genereazaSuccesori(nodCurent, tipEuristica)
        totalSuccesoriGenerati += len(lSuccesori)

        for s in lSuccesori:
            gasitNod = False

            for nod in lOpen:
                if s.info == nod.info:
                    gasitNod = True
                    if s.f >= nod.f:
                        lSuccesori.remove(s)
                    else:
                        lOpen.remove(nod)
                    break
            if not gasitNod:
                for nod in lClosed:
                    if s.info == nod.info:
                        if s.f >= nod.f:
                            lSuccesori.remove(s)
                        else:
                            lClosed.remove(nod)
                        break

        for sol in lSuccesori:
            i = 0
            gasitLoc = False

            for i in range(len(lOpen)):
                if sol.f <= lOpen[i].f:
                    gasitLoc = True
                    break

            if gasitLoc:
                lOpen.insert(i, sol)
            else:
                lOpen.append(sol)
    return 'aStarOptimizat terminat'

@stopit.threading_timeoutable(default='idaStar timeout')
def idaStar(gr, nrSol, output, tipEuristica = 'b'):
    '''
    :param gr (Graph): graful pe care cautam solutii
    :param nrSol (int): numarul de solutii cautate
    :param output (_io.TextIOWrapper): fisierul de output
    :param tipEuristica (str): euristica pe care vrem sa o folosim
                                       - 'b' pentru banala
                                       - 'a1' pentru admisibila 1
                                       - 'a2' pentru admisibila 2
                                       - 'n' pentru neadmisibila
    :return:
        str: 'idaStar terminat' daca functia nu a intrat in timeout, altfel 'idaStar timeout'
    '''
    nodStart = NodParcurgere(gr.start, None, 0, gr.calculeazaH(gr.start, tipEuristica))
    limita = nodStart.f
    nr = 0
    maxNoduriMemorie = 1
    totalSuccesoriGenerati = 0
    noduriGasite = []

    while True:
        nrSol, rez, nr, maxNoduriMemorie, totalSuccesoriGenerati, noduriGasite = \
            construiesteDrum(gr, nodStart, limita, nrSol, output, tipEuristica, nr, maxNoduriMemorie, totalSuccesoriGenerati, noduriGasite)
        if rez == 'gata' or rez == float('inf'):
            break

        limita = rez

    return 'idaStar terminat'

def construiesteDrum(gr, nodCurent, limita, nrSol, output, tipEuristica = 'b',nr = 0, maxNoduriMemorie = 1,
                     totalSuccesoriGenerati = 0, noduriGasite = [], nrNodesInMemory = 1):
    '''
    :param gr (Graph): graful pe care cautam solutii
    :param nodCurent (tuple): nodul curent
    :param limita (float): limita costului unei solutii
    :param nrSol (int): numarul de solutii cautate
    :param output (_io.TextIOWrapper): fisierul de output
    :param tipEuristica (str): euristica pe care vrem sa o folosim
                                       - 'b' pentru banala
                                       - 'a1' pentru admisibila 1
                                       - 'a2' pentru admisibila 2
                                       - 'n' pentru neadmisibila
    :param nr (int): numarul solutiilor gasite
    :param maxNoduriMemorie (int): numarul maxim de noduri in memorie
    :param totalSuccesoriGenerati (int): numarul de succesori generati
    :param noduriGasite (list): lista nodurilor solutie gasite
    :param nrNodesInMemory (int): numarul de noduri in memorie

    :return:
            int, float, int, int, int, list - daca nu am gasit numarul de soultii cautate
            int, str, int, int, int, list - daca am gasit numarul de soultii cautate
    '''
    if nodCurent.f > limita:
        return nrSol, nodCurent.f, nr, maxNoduriMemorie, totalSuccesoriGenerati, noduriGasite
    if gr.testeazaScop(nodCurent) and nodCurent not in noduriGasite:
        noduriGasite.append(nodCurent)
        nr += 1
        output.write('Solutie ' + str(nr) + ':\n')
        nodCurent.afisDrum(output, True, True)
        output.write(str(time.time() - t1) + " secunde\n")
        output.write('Numarul maxim de noduri existente in memorie: ' + str(maxNoduriMemorie) + '\n')
        output.write('Numarul total de succesori generati: ' + str(totalSuccesoriGenerati) + '\n')
        output.write('\n-------------------------\n\n')
        nrSol -= 1
        if nrSol == 0:
            return 0, 'gata', nr, maxNoduriMemorie, totalSuccesoriGenerati, noduriGasite

    lSuccesori = gr.genereazaSuccesori(nodCurent, tipEuristica)
    totalSuccesoriGenerati += len(lSuccesori)
    nrNodesInMemory += len(lSuccesori)
    maxNoduriMemorie = max(maxNoduriMemorie, nrNodesInMemory)

    minim = float('inf')

    for next in lSuccesori:
        nrSol, rez, nr, maxNoduriMemorie, totalSuccesoriGenerati, noduriGasite = \
            construiesteDrum(gr, next, limita, nrSol, output, tipEuristica, nr, maxNoduriMemorie,
                             totalSuccesoriGenerati, noduriGasite, nrNodesInMemory)
        if rez == 'gata':
            return 0, 'gata', nr, maxNoduriMemorie, totalSuccesoriGenerati, noduriGasite
        if rez < minim:
            minim = rez
    return nrSol, minim, nr, maxNoduriMemorie, totalSuccesoriGenerati, noduriGasite




if __name__ == '__main__':
    if len(sys.argv) != 5:
        exit()

    inputFolder = sys.argv[1]
    outputFolder = sys.argv[2]
    NSOL = int(sys.argv[3])
    timeOut = int(sys.argv[4])

    print(f"\nInput folder: {inputFolder}\nOutput folder: {outputFolder}\nNSOL: {NSOL}\nTimeout: {timeOut}\n")
    inputFiles = os.listdir(inputFolder)

    if not os.path.exists(outputFolder):
        os.mkdir(outputFolder)
    for inputFile in inputFiles:

        input = open(inputFolder + '/' + inputFile, 'r')
        gr = Graph(input)
        input.close()

        inputFile = inputFile[:len(inputFile) - len('.txt')]

        print(inputFile + ':')

        path = outputFolder + '/Output_' + inputFile
        if not os.path.exists(path):
            os.mkdir(path)

        # breath first

        outputFile = "breath_first.txt"
        outputName = path + '/' + outputFile

        output = open(outputName, 'w')
        t1 = time.time()
        res = breathFirst(gr, NSOL, output, timeout=timeOut)
        output.write(res)
        output.close()

        print(res)

        # depth first

        outputFile = "depth_first.txt"
        outputName = path + '/' + outputFile

        output = open(outputName, 'w')
        t1 = time.time()
        res = depthFirst(gr, NSOL, output, timeout=timeOut)
        output.write('\n' + res + '\n')
        output.close()

        print(res)

        # depth first iterativ

        outputFile = "depth_first_iterativ.txt"
        outputName = path + '/' + outputFile

        output = open(outputName, 'w')
        t1 = time.time()
        res = depthFirstIterativ(gr, NSOL, output, 20, timeout=timeOut)
        output.write('\n' + res + '\n')
        output.close()

        print(res)

        # A star

        outputFile = "a_star_b.txt"
        outputName = path + '/' + outputFile

        output = open(outputName, 'w')
        t1 = time.time()
        res = aStar(gr, NSOL, output, 'b', timeout=timeOut)
        output.write('\n' + res + '\n')
        output.close()

        print(res + ' b')

        outputFile = "a_star_a1.txt"
        outputName = path + '/' + outputFile

        output = open(outputName, 'w')
        t1 = time.time()
        res = aStar(gr, NSOL, output, 'a1', timeout=timeOut)
        output.write('\n' + res + '\n')
        output.close()

        print(res + ' a1')

        outputFile = "a_star_a2.txt"
        outputName = path + '/' + outputFile

        output = open(outputName, 'w')
        t1 = time.time()
        res = aStar(gr, NSOL, output, 'a2', timeout=timeOut)
        output.write('\n' + res + '\n')
        output.close()

        print(res + ' a2')

        outputFile = "a_star_n.txt"
        outputName = path + '/' + outputFile

        output = open(outputName, 'w')
        t1 = time.time()
        res = aStar(gr, NSOL, output, 'n', timeout=timeOut)
        output.write('\n' + res + '\n')
        output.close()

        print(res + ' n')

        # A star optimizat

        outputFile = "a_star_optimizat_b.txt"
        outputName = path + '/' + outputFile

        output = open(outputName, 'w')
        t1 = time.time()
        res = aStarOptimizat(gr, NSOL, output, 'b', timeout=timeOut)
        output.write('\n' + res + '\n')
        output.close()

        print(res + ' b')

        outputFile = "a_star_optimizat_a1.txt"
        outputName = path + '/' + outputFile

        output = open(outputName, 'w')
        t1 = time.time()
        res = aStarOptimizat(gr, NSOL, output, 'a1', timeout=timeOut)
        output.write('\n' + res + '\n')
        output.close()

        print(res + ' a1')

        outputFile = "a_star_optimizat_a2.txt"
        outputName = path + '/' + outputFile

        output = open(outputName, 'w')
        t1 = time.time()
        res = aStarOptimizat(gr, NSOL, output, 'a2', timeout=timeOut)
        output.write('\n' + res + '\n')
        output.close()

        print(res + ' a2')

        outputFile = "a_star_optimizat_n.txt"
        outputName = path + '/' + outputFile

        output = open(outputName, 'w')
        t1 = time.time()
        res = aStarOptimizat(gr, NSOL, output, 'n', timeout=timeOut)
        output.write('\n' + res + '\n')
        output.close()

        print(res + ' n')

        # IDA star optimizat

        outputFile = "ida_star_b.txt"
        outputName = path + '/' + outputFile

        output = open(outputName, 'w')
        t1 = time.time()
        res = idaStar(gr, NSOL, output, 'b', timeout=timeOut)
        output.write('\n' + res + '\n')
        output.close()

        print(res + ' b')

        outputFile = "ida_star_a1.txt"
        outputName = path + '/' + outputFile

        output = open(outputName, 'w')
        t1 = time.time()
        res = idaStar(gr, NSOL, output, 'a1', timeout=timeOut)
        output.write('\n' + res + '\n')
        output.close()

        print(res + ' a1')

        outputFile = "ida_star_a2.txt"
        outputName = path + '/' + outputFile

        output = open(outputName, 'w')
        t1 = time.time()
        res = idaStar(gr, NSOL, output, 'a2', timeout=timeOut)
        output.write('\n' + res + '\n')
        output.close()

        print(res + ' a2')

        outputFile = "ida_star_n.txt"
        outputName = path + '/' + outputFile

        output = open(outputName, 'w')
        t1 = time.time()
        res = idaStar(gr, NSOL, output, 'n', timeout=timeOut)
        output.write('\n' + res + '\n')
        output.close()

        print(res + ' n')
        print()
