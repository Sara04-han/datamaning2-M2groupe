import pandas as pd
import numpy as np
def TB(df_marks,target,cont,disc,H,Pd,Max):
    Nomcol=df_marks.columns
    sort = df_marks.sort_values(by=Nomcol[Pd])
    df=sort.drop_duplicates(subset=[Nomcol[Pd]])
    value=marks_list = df[Nomcol[Pd]].tolist()
    sort = df_marks.sort_values(by=Nomcol[9])
    df=sort.drop_duplicates(subset=[Nomcol[9]])
    value1=marks_list = df[Nomcol[9]].tolist()
    N=list()
    pno=list()
    pyes=list()
    Entropy=list()
    for i in range(len(value)):
        for j in range(len(value1)):
            N.append(0)
            pno.append(0)
            pyes.append(0)
    for j in range(len(value)):
        for i in range(303):
            pnot = 0
            pyest = 0
            if (sort.iat[i,Pd]==value[j]):
                for y in range(len(value1)):
                    if (sort.iat[i,9]==value1[y]):
                        N[j*len(value1)+y]=N[j*len(value1)+y]+1
                        if (sort.iat[i,target]==1):
                            pyes[j*len(value1)+y]=pyes[j*len(value1)+y]+1
                        if (sort.iat[i, target]==0):
                            pno[j*len(value1)+y]=pno[j*len(value1)+y]+1
    Gaintest=list()
    N0=list()
    for i in range(int(len(N)/len(value1))):
        C0=0
        for j in range(len(value1)):
            C0=C0+N[j+i*len(value1)]
        N0.append(C0)
    for i in range(len(N)):
        if (pyes[i] == 0 or pno[i] == 0):
            Entropy.append(0)
        else:
            Entropy.append(-pno[i]/N[i]*np.log2(pno[i]/N[i])-pyes[i]/N[i]*np.log2(pyes[i]/N[i]))

    GR=list()
    for i in range(1,len(value)+1):
        Test=N[(i-1)*len(value1):(i)*len(value1)]
        Gain=H
        Split=0
        for j in range(len(value1)):
            Gain=Gain-Test[j]/N0[i-1]*Entropy[j+(i-1)*(len(value1))]
            if(N0[i-1]-Test[j]==0):
                Split=Split-Test[j]/N0[i-1]*np.log2(Test[j]/N0[i-1])
            elif (Test[j]==0):
                Split=Split-(N0[i-1]-Test[j])/N0[i-1]*np.log2((N0[i-1]-Test[j])/N0[i-1])
            else :
                Split=Split-Test[j]/N0[i-1]*np.log2(Test[j]/N0[i-1])-(N0[i-1]-Test[j])/N0[i-1]*np.log2((N0[i-1]-Test[j])/N0[i-1])
        if (Split==0):
            GR.append(0)
        else:
            GR.append(Gain/Split)
    ##

def GR(df_marks,target,cont,disc,H):
    ##disccontinue
    Nomcol=df_marks.columns
    sort = df_marks.sort_values(by=Nomcol[target])
    nbrcont=len(disc)
    Nomcol=df_marks.columns
    GRfinal = list()
    for j in range(nbrcont):
        rat = sort.groupby(Nomcol[disc[j]])[Nomcol[target]].value_counts()
        h = rat.shape[0]
        rat = pd.DataFrame(rat)
        Entrop = list()
        listN=list()
        for i in range(int(h/2)):
            Nno = rat.iat[i*2, 0]
            Nyes = rat.iat[(i*2)+1, 0]
            N = Nyes + Nno
            pno = Nno / N
            pyes = Nyes / N
            en = -pno * np.log2(pno) - pyes * np.log2(pyes)
            Entrop.append(en)
            listN.append(N)
        Gai=H
        Splitinf=0
        for i in range(int(h/2)):
            Gai=Gai - (listN[i]/303) * Entrop[i]
            Splitinf=Splitinf-(listN[i]/303)*np.log2(listN[i]/303)
        GRfinal.append(Gai/Splitinf)
    ##continue
    nbrcont=len(cont)
    MxCont = np.zeros(5)
    for j in range(nbrcont):
        sort = df_marks.sort_values(by=Nomcol[cont[j]])
        Entropysupp = list()
        Entropyinf = list()
        Gain = list()
        Splitinfo = list()
        GR = list()
        maxcol = sort[Nomcol[cont[j]]].max()
        mincol = sort[Nomcol[cont[j]]].min()
        pas = (maxcol - mincol) / 8
        for y in range(8):
            Nsupp = 0
            pyessupp = 0
            pnosupp = 0
            Ninf = 0
            pyesinf = 0
            pnoinf = 0
            for i in range(303):
                if sort.iat[i, cont[j]] > (mincol+y*pas):
                    Nsupp = Nsupp + 1
                    if (int(sort.iat[i, target]) == 1):
                        pyessupp = pyessupp + 1
                    if (int(sort.iat[i, target]) == 0):
                        pnosupp = pnosupp + 1
                if sort.iat[i, cont[j]] <= (mincol+y*pas):
                    Ninf = Ninf + 1
                    if (int(sort.iat[i,target]) == 1):
                        pyesinf = pyesinf + 1
                    if (int(sort.iat[i, target]) == 0):
                        pnoinf = pnoinf + 1
            if (pyessupp == 0 or pnosupp == 0):
                Entropysupp.append(0)
            else:
                pnosupp1 = pnosupp / Nsupp
                pyessupp1 = pyessupp / Nsupp
                ensupp = -pnosupp1 * np.log2(pnosupp1) - pyessupp1 * np.log2(pyessupp1)
                Entropysupp.append(ensupp)
            if (pyesinf == 0 or pnoinf == 0):
                Entropyinf.append(0)
            else:
                pnoinf1 = pnoinf / Ninf
                pyesinf1 = pyesinf / Ninf
                eninf = -pnoinf1 * np.log2(pnoinf1) - pyesinf1 * np.log2(pyesinf1)
                Entropyinf.append(eninf)
            Gain.append(H - (Ninf / 303 * Entropyinf[y] + Nsupp / 303 * Entropysupp[y]))
            if (Nsupp == 0 or Ninf == 0):
                Splitinfo.append(0)
            else:
                Splitinfo.append(-(Ninf/303)*np.log2(Ninf/303)-(Nsupp/303)*np.log2(Nsupp/303))
            GR.append(Gain[y]/Splitinfo[y])
        GRfinal.append(max(GR[1:]))
        MxCont[j]=mincol+GR.index(max(GR[1:]))*pas
    if (GRfinal.index(max(GRfinal))+1<=len(disc)):
        return disc[GRfinal.index(max(GRfinal))], 'nan', MxCont
    else:
        return cont[len(GRfinal)-GRfinal.index(max(GRfinal))], MxCont[len(GRfinal)-GRfinal.index(max(GRfinal))], MxCont

def entropieH(df_marks,target):
    Nomcol=df_marks.columns
    sort = df_marks.sort_values(by=Nomcol[target])
    rat = sort.groupby(Nomcol[target]).size().div(len(sort))
    rat = pd.DataFrame(rat)
    lograt = np.log2(rat)
    taille = rat.shape
    ligne = taille[0]
    H = 0
    for i in range(ligne):
        H = H + (rat.iat[i, 0] * lograt.iat[i, 0]) * (-1)
    return H
def typecolone():
    print('Quelle est le numéro de la  colone target')
    target=input()
    target=int(target)
    print('Quelle est le numéro de la colone avec des valeurs discontinues')
    disc=input().split()
    disc = list(map(int, disc))
    print('Quelle est le numéro de la colone avec des valeurs continues')
    cont=input().split()
    cont = list(map(int, cont))
    return target,cont, disc
def main():
    data = pd.read_csv('dataset.csv')
    df_marks = pd.DataFrame(data)
    #target, cont, disc=typecolone()
    target=13
    cont=[0,3,4,7,9]
    disc=[1,2,5,6,10,11,12]
    H=entropieH(df_marks,target)
    Pd,Mx,Max=GR(df_marks, target, cont, disc,H)
    TB(df_marks, target, cont, disc, H, Pd,Max)
main()