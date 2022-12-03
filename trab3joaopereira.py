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
                    numVariaveisExtras+=1
                    info += [numVariaveisExtras]
                    dictInfo = dict(zip(chavesFonteTensaoContCorrente, info))
                    listaFontesTensaoContCorrente.append(dictInfo)
    return listaResistores, listaFontesCorrenteIndep, listaFontesTensaoIndep, listaFontesCorrenteContTensao, listaFontesCorrenteContCorrente, listaFontesTensaoContTensao, listaFontesTensaoContCorrente, numVariaveisExtras

def montaMatrizes(listaResistores, listaFontesCorrenteIndep, listaFontesTensaoIndep, listaFontesCorrenteContTensao, listaFontesCorrenteContCorrente, listaFontesTensaoContTensao, listaFontesTensaoContCorrente, numVariaveisExtras):
    #MANTER PARA TER CONTROLE DO NÚMERO DAS VARIÁVEIS EXTRAS
    numNos = tamanhoMatrizGn(listaResistores, listaFontesCorrenteIndep, listaFontesCorrenteContTensao) 
    #print(numNos, numVariaveisExtras)
    matrizGn = np.zeros((numNos + numVariaveisExtras + 1, numNos + numVariaveisExtras + 1))
    listaI = np.zeros(numNos + numVariaveisExtras + 1)
    #FEITO
    for resistor in listaResistores:
        #print(resistor)
        matrizGn[int(resistor["No1"])][int(resistor["No1"])] += 1/float(resistor["Valor"])
        matrizGn[int(resistor["No1"])][int(resistor["No2"])] -= 1/float(resistor["Valor"])
        matrizGn[int(resistor["No2"])][int(resistor["No1"])] -= 1/float(resistor["Valor"])
        matrizGn[int(resistor["No2"])][int(resistor["No2"])] += 1/float(resistor["Valor"])
    #FEITO
    for fonteCorrContTens in listaFontesCorrenteContTensao:
        #print(fonteCorrContTens)
        matrizGn[int(fonteCorrContTens["No1"])][int(fonteCorrContTens["Controle1"])] += float(fonteCorrContTens["Valor"])
        matrizGn[int(fonteCorrContTens["No1"])][int(fonteCorrContTens["Controle2"])] -= float(fonteCorrContTens["Valor"])
        matrizGn[int(fonteCorrContTens["No2"])][int(fonteCorrContTens["Controle1"])] -= float(fonteCorrContTens["Valor"])
        matrizGn[int(fonteCorrContTens["No2"])][int(fonteCorrContTens["Controle2"])] += float(fonteCorrContTens["Valor"])
    #FEITO
    for fonteCorrContCorr in listaFontesCorrenteContCorrente:
        #print(fonteCorrContCorr)
        matrizGn[int(fonteCorrContCorr["No1"])][numNos + fonteCorrContCorr["Variavel"]] += float(fonteCorrContCorr["Valor"])
        matrizGn[int(fonteCorrContCorr["No2"])][numNos + fonteCorrContCorr["Variavel"]] -= float(fonteCorrContCorr["Valor"])
        matrizGn[int(fonteCorrContCorr["Controle1"])][numNos + fonteCorrContCorr["Variavel"]] += 1
        matrizGn[int(fonteCorrContCorr["Controle2"])][numNos + fonteCorrContCorr["Variavel"]] -= 1
        matrizGn[numNos + fonteCorrContCorr["Variavel"]][int(fonteCorrContCorr["Controle1"])] -= 1
        matrizGn[numNos + fonteCorrContCorr["Variavel"]][int(fonteCorrContCorr["Controle2"])] += 1
    #FEITO
    for fonteTensContTens in listaFontesTensaoContTensao:
        #print(fonteTensContTens)
        matrizGn[int(fonteTensContTens["No1"])][numNos + fonteTensContTens["Variavel"]] += 1
        matrizGn[int(fonteTensContTens["No2"])][numNos + fonteTensContTens["Variavel"]] -= 1
        matrizGn[numNos + fonteTensContTens["Variavel"]][int(fonteTensContTens["No1"])] -= 1
        matrizGn[numNos + fonteTensContTens["Variavel"]][int(fonteTensContTens["No2"])] += 1
        matrizGn[numNos + fonteTensContTens["Variavel"]][int(fonteTensContTens["Controle1"])] += float(fonteTensContTens["Valor"])
        matrizGn[numNos + fonteTensContTens["Variavel"]][int(fonteTensContTens["Controle2"])] -= float(fonteTensContTens["Valor"])
    #FEITO
    for fonteTensContCorr in listaFontesTensaoContCorrente:
        #print(fonteTensContCorr)
        matrizGn[int(fonteTensContCorr["No1"])][numNos + fonteTensContCorr["Variavel2"]] += 1
        matrizGn[int(fonteTensContCorr["No2"])][numNos + fonteTensContCorr["Variavel2"]] -= 1
        matrizGn[int(fonteTensContCorr["Controle1"])][numNos + fonteTensContCorr["Variavel1"]] += 1
        matrizGn[int(fonteTensContCorr["Controle2"])][numNos + fonteTensContCorr["Variavel1"]] -= 1
        matrizGn[numNos + fonteTensContCorr["Variavel1"]][int(fonteTensContCorr["Controle1"])] -= 1
        matrizGn[numNos + fonteTensContCorr["Variavel1"]][int(fonteTensContCorr["Controle2"])] += 1
        matrizGn[numNos + fonteTensContCorr["Variavel2"]][int(fonteTensContCorr["No1"])] -= 1
        matrizGn[numNos + fonteTensContCorr["Variavel2"]][int(fonteTensContCorr["No2"])] += 1
        matrizGn[numNos + fonteTensContCorr["Variavel2"]][numNos + fonteTensContCorr["Variavel1"]] += float(fonteTensContCorr["Valor"])
    #FEITO
    for fonteCorrIndep in listaFontesCorrenteIndep:
        #print(fonteCorrIndep)
        listaI[int(fonteCorrIndep["No1"])] -= float(fonteCorrIndep["Valor"])
        listaI[int(fonteCorrIndep["No2"])] += float(fonteCorrIndep["Valor"])
    #FONTE DE TENSÃO INDEP OK!    
    for fonteTensIndep in listaFontesTensaoIndep:
        #print(fonteTensIndep)
        listaI[numNos + fonteTensIndep["Variavel"]] -= float(fonteTensIndep["Valor"])
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

#print(f"Netlist 0: {main('netlist0.txt')}")
#Netlist1: OK
print(f"Netlist 1: {main('netlist1.txt')}")
#Netlist2: OK 
print(f"Netlist 2: {main('netlist2.txt')}")
#Netlist3: OK 
print(f"Netlist 3: {main('netlist3.txt')}")
#Netlist4: OK
print(f"Netlist 4: {main('netlist4.txt')}")
