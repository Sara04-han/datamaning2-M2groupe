import pandas as pd
import numpy as np

def GR1(df_marks,target,cont,disc,H):
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
        return disc[GRfinal.index(max(GRfinal))], 'nan'
    else:
        return cont[len(GRfinal)-GRfinal.index(max(GRfinal))], MxCont[len(GRfinal)-GRfinal.index(max(GRfinal))]

def GR(df,disc,cont,target,H,):
    # Fonction du calcul du gain Ratio
    #### Calcul DisContinue
    Nomcol=df.columns
    sort = df.sort_values(by=Nomcol[target])
    nbrcont = len(disc)
    GRfinal = list()
    value = []

    for j in range(nbrcont):
        rat = sort.groupby([Nomcol[disc[j]], Nomcol[target]]).size().unstack(fill_value=0)
        h = int(rat.shape[0])
        rat = pd.DataFrame(rat)
        value.append(rat.index.name)
        Entrop = list()
        listN = list()
        value1 = list()
        for i in range(h):
            Nno = rat.iat[i, 0]
            Nyes = rat.iat[i, 1]
            N = Nyes + Nno
            pno = Nno / N
            pyes = Nyes / N
            if pno == 0 or pyes == 0:
                en = 0
            else:
                en = -pno * np.log2(pno) - pyes * np.log2(pyes)
                value1.append(rat.index[i])
            Entrop.append(en)
            listN.append(N)
        value.append(value1)
        Gai = H
        Splitinf = 0
        Taille_Tab = int(len(df))
        for i in range(h):
            Gai = Gai - (listN[i] / Taille_Tab) * Entrop[i]
            Splitinf = Splitinf - (listN[i] / Taille_Tab) * np.log2(listN[i] / Taille_Tab)
        if (Splitinf == 0):
            GRfinal.append(0)
        else:
            GRfinal.append(Gai / Splitinf)
    col_max=disc[GRfinal.index(max(GRfinal))]
    for i in range(len(value)):
        if Nomcol[col_max] == value[i]:
            index=value[i+1]
    if sum(GRfinal)== 0 or len(index)==0:
        print('FINI')
    else:
        if (GRfinal.index(max(GRfinal)) + 1 <= len(disc)):
            col_max = disc[GRfinal.index(max(GRfinal))]
            print(Nomcol[col_max], index)
            DivTab(df,col_max,index,0)
        else:
            index=[0,0]
            col_max = cont[len(GRfinal)-GRfinal.index(max(GRfinal))]
            print(Nomcol[col_max], index,col_max,MxCont[len(GRfinal)-GRfinal.index(max(GRfinal))])
            print(df['thalach'])
            DivTab(df,col_max,index,MxCont[len(GRfinal)-GRfinal.index(max(GRfinal))])
def DivTab(data,Value,index,Max):
    #Fonction de division des tableau
    disc=[1,2,5,6,8,10,11,12]
    cont=[0,3,4,7,9]
    Nomcol=data.columns
    Result=list()
    target = 13
    H=entropieH(data,target)
    if(Max==0):
        for i in range(len(index)):
            df = pd.DataFrame(columns=Nomcol)
            test = data[Nomcol[Value]] == index[i]
            h = 0
            for i in range(len(data)):
                if test[i] == True:
                    df.loc[h] = data.loc[i]
                    h = h + 1
            Result.append(df)
    else:
        df=pd.DataFrame(columns=Nomcol)
        df1=pd.DataFrame(columns=Nomcol)
        h = 0
        h1 = 0
        for i in range(len(data)):
            if data.iat[i,Value] < Max :
                df.loc[h] = data.loc[i]
                h = h+1
            else:
                df1.loc[h1] = data.loc[i]
                h1 = h1+1
        Result.append(df)
        Result.append(df1)
    #print(Result)
    GR(Result[0],disc,cont,target,h)
def entropieH(df_marks,target):
    #Fonction Calcul de l'entropie
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
    #print(H)
    return H

def main():
    data = pd.read_csv('dataset.csv')
    data = pd.DataFrame(data)
    target=13
    cont=[0,3,4,7,9]
    disc=[1,2,5,6,8,10,11,12]
    H=entropieH(data,target)
    GRRESULT,maxGRRESULT=GR1(data,target,cont,disc,H)
    index=[1,0,2,3]
    child=DivTab(data,GRRESULT,index,0)
main()