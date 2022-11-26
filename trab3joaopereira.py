import numpy as np

def tamanhoMatrizGn(*args):
    tamanho = 0
    for lista in args:
        for el in lista:
            if int(el["No1"]) > tamanho:
                tamanho = int(el["No1"])
            if int(el["No2"]) > tamanho:
                tamanho = int(el["No2"])
    return tamanho

def lerNetList(netlist):
    chavesResistores = ["Nome", "No1", "No2", "Valor"]
    chavesFonteCorrenteIndep = ["Nome", "No1", "No2", "Tipo", "Valor"]
    chavesFonteTensaoIndep = ["Nome", "No1", "No2", "Tipo", "Valor", "Variavel"]
    chavesFonteCorrenteContTensao = ["Nome", "No1", "No2", "Controle1", "Controle2", "Valor"]
    chavesFonteCorrenteContCorrente = ["Nome", "No1", "No2", "Controle1", "Controle2", "Valor", "Variavel"]
    chavesFonteTensaoContTensao = ["Nome", "No1", "No2", "Controle1", "Controle2", "Valor", "Variavel"]
    chavesFonteTensaoContCorrente = ["Nome", "No1", "No2", "Controle1", "Controle2", "Valor", "Variavel1", "Variavel2"]
    
    with open(netlist, "r", encoding="utf-8") as arqNet:
        listaI = []
        listaResistores = []
        listaFontesCorrenteIndep = []
        listaFontesTensaoIndep = []
        listaFontesCorrenteContTensao = []
        listaFontesCorrenteContCorrente = []
        listaFontesTensaoContTensao = []
        listaFontesTensaoContCorrente = []
        numVariaveisExtras = 0
        for line in arqNet:
            if line != '\n' and line[0] != "*":
                #print(f"{line} é a linha atual")
                info = line.split()
                #print(info)
                if line[0] == "R":
                    dictInfo = dict(zip(chavesResistores, info))
                    listaResistores.append(dictInfo)
                elif line[0] == "I":
                    dictInfo = dict(zip(chavesFonteCorrenteIndep, info))
                    listaFontesCorrenteIndep.append(dictInfo)
                elif line[0] == "V":
                    numVariaveisExtras+=1
                    info += [numVariaveisExtras]
                    dictInfo = dict(zip(chavesFonteTensaoIndep, info))
                    listaFontesTensaoIndep.append(dictInfo)
                elif line[0] == "G":
                    dictInfo = dict(zip(chavesFonteCorrenteContTensao, info))
                    listaFontesCorrenteContTensao.append(dictInfo)
                elif line[0] == "F":
                    numVariaveisExtras+=1
                    info += [numVariaveisExtras]
                    dictInfo = dict(zip(chavesFonteCorrenteContCorrente, info))
                    listaFontesCorrenteContCorrente.append(dictInfo)
                elif line[0] == "E":
                    numVariaveisExtras+=1
                    info += [numVariaveisExtras]
                    dictInfo = dict(zip(chavesFonteTensaoContTensao, info))
                    listaFontesTensaoContTensao.append(dictInfo)
                elif line[0] == "H":
                    numVariaveisExtras+=1
                    info += [numVariaveisExtras]
                    dictInfo = dict(zip(chavesFonteTensaoContCorrente, info))
                    listaFontesTensaoContCorrente.append(dictInfo)
    return listaResistores, listaFontesCorrenteIndep, listaFontesTensaoIndep, listaFontesCorrenteContTensao, listaFontesCorrenteContCorrente, listaFontesTensaoContTensao, listaFontesTensaoContCorrente, numVariaveisExtras

def montaMatrizes(listaResistores, listaFontesCorrenteIndep, listaFontesTensaoIndep, listaFontesCorrenteContTensao, listaFontesCorrenteContCorrente, listaFontesTensaoContTensao, listaFontesTensaoContCorrente, numVariaveisExtras):
    #MANTER PARA TER CONTROLE DO NÚMERO DAS VARIÁVEIS EXTRAS
    numNos = tamanhoMatrizGn(listaResistores, listaFontesCorrenteIndep, listaFontesCorrenteContTensao) 
    matrizGn = np.zeros((numNos + numVariaveisExtras + 1, numNos + numVariaveisExtras + 1))
    listaI = np.zeros(numNos + numVariaveisExtras + 1)
    for resistor in listaResistores:
        #print(resistor)
        matrizGn[int(resistor["No1"])][int(resistor["No1"])] += 1/int(resistor["Valor"])
        matrizGn[int(resistor["No1"])][int(resistor["No2"])] -= 1/int(resistor["Valor"])
        matrizGn[int(resistor["No2"])][int(resistor["No1"])] -= 1/int(resistor["Valor"])
        matrizGn[int(resistor["No2"])][int(resistor["No2"])] += 1/int(resistor["Valor"])

    #FAZENDO AGORA
    for fonteCorrContTens in listaFontesCorrenteContTensao:
        #print(fonteCorrContTens)
        matrizGn[int(fonteCorrContTens["No1"])][int(fonteCorrContTens["Controle1"])] += int(fonteCorrContTens["Valor"])
        matrizGn[int(fonteCorrContTens["No1"])][int(fonteCorrContTens["Controle2"])] -= int(fonteCorrContTens["Valor"])
        matrizGn[int(fonteCorrContTens["No2"])][int(fonteCorrContTens["Controle1"])] -= int(fonteCorrContTens["Valor"])
        matrizGn[int(fonteCorrContTens["No2"])][int(fonteCorrContTens["Controle2"])] += int(fonteCorrContTens["Valor"])
    for fonteCorrContCorr in listaFontesCorrenteContCorrente:
        #print(fonteCorrContCorr)
        matrizGn[int(fonteCorrContCorr["No1"])][int(fonteCorrContCorr["Controle1"])] += int(fonteCorrContCorr["Valor"])
        matrizGn[int(fonteCorrContCorr["No1"])][int(fonteCorrContCorr["Controle2"])] -= int(fonteCorrContCorr["Valor"])
        matrizGn[int(fonteCorrContCorr["No2"])][int(fonteCorrContCorr["Controle1"])] -= int(fonteCorrContCorr["Valor"])
        matrizGn[int(fonteCorrContCorr["No2"])][int(fonteCorrContCorr["Controle2"])] += int(fonteCorrContCorr["Valor"])
    for fonteTensContTens in listaFontesTensaoContTensao:
        print(fonteTensContTens)
        matrizGn[int(fonteTensContTens["No1"])][int(fonteTensContTens["Controle1"])] += int(fonteTensContTens["Valor"])
        matrizGn[int(fonteTensContTens["No1"])][int(fonteTensContTens["Controle2"])] -= int(fonteTensContTens["Valor"])
        matrizGn[int(fonteTensContTens["No2"])][int(fonteTensContTens["Controle1"])] -= int(fonteTensContTens["Valor"])
        matrizGn[int(fonteTensContTens["No2"])][int(fonteTensContTens["Controle2"])] += int(fonteTensContTens["Valor"])
    for fonteTensContCorr in listaFontesTensaoContCorrente:
        #print(fonteTensContCorr)
        matrizGn[int(fonteTensContCorr["No1"])][int(fonteTensContCorr["Controle1"])] += int(fonteTensContCorr["Valor"])
        matrizGn[int(fonteTensContCorr["No1"])][int(fonteTensContCorr["Controle2"])] -= int(fonteTensContCorr["Valor"])
        matrizGn[int(fonteTensContCorr["No2"])][int(fonteTensContCorr["Controle1"])] -= int(fonteTensContCorr["Valor"])
        matrizGn[int(fonteTensContCorr["No2"])][int(fonteTensContCorr["Controle2"])] += int(fonteTensContCorr["Valor"])
    for fonteCorrIndep in listaFontesCorrenteIndep:
        #print(fonteCorrIndep)
        listaI[int(fonteCorrIndep["No1"])] -= int(fonteCorrIndep["Valor"])
        listaI[int(fonteCorrIndep["No2"])] += int(fonteCorrIndep["Valor"])
    #FONTE DE TENSÃO INDEP OK!    
    for fonteTensIndep in listaFontesTensaoIndep:
        #print(fonteTensIndep)
        listaI[numNos + fonteTensIndep["Variavel"]] -= int(fonteTensIndep["Valor"])
        matrizGn[int(fonteTensIndep["No1"])][numNos + fonteTensIndep["Variavel"]] += 1
        matrizGn[int(fonteTensIndep["No2"])][numNos + fonteTensIndep["Variavel"]] -= 1
        matrizGn[numNos + fonteTensIndep["Variavel"]][int(fonteTensIndep["No1"])] -= 1
        matrizGn[numNos + fonteTensIndep["Variavel"]][int(fonteTensIndep["No2"])] += 1
        
    return matrizGn[1:,1:], listaI[1:]

def main(arqNetList):
    listaResistores, listaFontesCorrenteIndep, listaFontesTensaoIndep, listaFontesCorrenteContTensao, listaFontesCorrenteContCorrente, listaFontesTensaoContTensao, listaFontesTensaoContCorrente, numVariaveisExtras = lerNetList(arqNetList)
    matrizGn, listaI = montaMatrizes(listaResistores, listaFontesCorrenteIndep, listaFontesTensaoIndep, listaFontesCorrenteContTensao, listaFontesCorrenteContCorrente, listaFontesTensaoContTensao, listaFontesTensaoContCorrente, numVariaveisExtras)
    print(matrizGn)
    print(listaI)    
    matrizE = np.linalg.solve(matrizGn, listaI)
    return matrizE

print(f"Netlist 0: {main('netlist0.txt')}")
#print(f"Netlist 1: {main('netlist1.txt')}")
#print(f"Netlist 2: {main('netlist2.txt')}")
#print(f"Netlist 3: {main('netlist3.txt')}")
