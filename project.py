import pandas as pd
import numpy as np
def TB(df_marks,target,cont,disc,H,Pd):
    Nomcol=df_marks.columns
    sort = df_marks.sort_values(by=Nomcol[Pd])
    df=sort.drop_duplicates(subset=[Nomcol[Pd]])
    value=marks_list = df[Nomcol[Pd]].tolist()
    sort = df_marks.sort_values(by=Nomcol[1])
    df=sort.drop_duplicates(subset=[Nomcol[1]])
    value1=marks_list = df[Nomcol[1]].tolist()
    N=list()
    for i in range(len(value)):
        for j in range(len(value1)):
            N.append(0)
    for j in range(len(value)):
        for i in range(303):
            if (sort.iat[i,Pd]==value[j]):
                for y in range(len(value1)):
                    if (sort.iat[i,1]==value1[y]):
                        N[j*2+y]=N[j*2+y]+1
                        if (sort.iat[i,target]==0):
                            pno=pno+1
                        if (sort.iat[i,target]==1):
                            pyes=pyes+1



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
        GRfinal.append(max(GR))
        MxCont[j]=mincol+GR.index(max(GR))*pas
    if (GRfinal.index(max(GRfinal))+1<=len(disc)):
        return disc[GRfinal.index(max(GRfinal))], 'nan'
    else:
        return cont[len(GRfinal)-GRfinal.index(max(GRfinal))], MxCont[len(GRfinal)-GRfinal.index(max(GRfinal))]

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
    Pd,Mx=GR(df_marks, target, cont, disc,H)
    print(Pd,Mx)
    TB(df_marks, target, cont, disc, H, Pd)
main()