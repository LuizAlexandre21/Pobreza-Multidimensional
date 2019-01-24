##### Pobreza Multidimensional #######
import pandas as pd
import numpy as np
import scipy as sc
import matplotlib.pyplot as plt  
import matplotlib.ticker as mtick
############### Funções ###############
def soma(subdados):
	dim=subdados.shape
	num=dim[1]
	n=0
	lista=[0]		
	soma=[0]
	while n<(num-1):
		n=n+1
		lista.append(n)
	Dados=subdados
	Dados.columns=lista
	Dados[np.isnan(Dados)]=0
	for i in lista:
		n=soma[i]+Dados[i]              
		soma.append(n)
	pov=(1/num)*soma[num]
	return pov

def Stat_Desc(subdados):
	dim=subdados.shape
	num=dim[1]
	n=0
	lista=[0]
	while n<(num-1):
		n=n+1
		lista.append(n)
	Dados=subdados
	Dados.columns=lista
	Mean=[]
	Median=[]
	Std=[]
	fquart=[]
	tquart=[]
	Moda=[]
	for i in lista:
		if i < (num):
			media=Dados[i].mean()
			Mean.append(media)
			desv=Dados[i].std()
			Std.append(desv)
			mediana=Dados[i].median()
			Median.append(mediana)
			fquarti=Dados[i].quantile(q=0.25)
			fquart.append(fquarti)
			tquarti=Dados[i].quantile(q=0.75)
			tquart.append(tquarti)
			mode=Dados[i].mode()
			Moda.append(mode)
		else:
			break
	dados={'Media':Mean,'Desvio':Std,'1º Quartil':fquart,'3º Quartil':tquart,'Mediana':Median,'Moda':Moda}
	tabela=pd.DataFrame(dados)
	return tabela

def Time_dif(subdados):
	dim=subdados.shape
	num=dim[1]
	n=0
	lista=[0]
	while n<(num-1):
		n=n+1
		lista.append(n)
	dados=subdados
	dados.columns=lista
	data={}	
	for i in lista:
		if i<(num-1):
			subdata=dados[i+1]-dados[i]
			data.update({str(i):subdata})
	painel=pd.DataFrame(data)
	print(painel)
	return painel
def to_list(subdados):
	lista=[]
	for i in subdados:
		if i is not None:
			lista.append(i)	
	return lista
########Tratamento dos Dados ########
Local_T="/run/media/alexandre/Alexandre/Pobreza Multidimensional/Script/Trabalho.csv"
Local_C="/run/media/alexandre/Alexandre/Pobreza Multidimensional/Script/Cond_Hab.csv"
Local_R="/run/media/alexandre/Alexandre/Pobreza Multidimensional/Script/Renda.csv"
Local_E="/run/media/alexandre/Alexandre/Pobreza Multidimensional/Script/Educação.csv"
#Local_T="/run/media/administrador/Alexandre/Pobreza Multidimensional/Script/Trabalho.csv"
#Local_C="/run/media/administrador/Alexandre/Pobreza Multidimensional/Script/Cond_Hab.csv"
#Local_R="/run/media/administrador/Alexandre/Pobreza Multidimensional/Script/Renda.csv"
#Local_E="/run/media/administrador/Alexandre/Pobreza Multidimensional/Script/Educação.csv"


######Trabalho
Trabalho=pd.read_csv(Local_T)
Trabalho_F=Trabalho.filter(items=["v9058"])
Trabalho_F[np.isnan(Trabalho_F)]=0
Trabalho_F[Trabalho['v9058']>=10]=1
Trabalho_F[Trabalho['v9058']<=10]=0
Trabalho_F=soma(Trabalho_F)


######Condição da Habitação

####Ajustando os dados  
Cond_Hab=pd.read_csv(Local_C)
Cond_Hab[np.isnan(Cond_Hab)]=0
variables=["v0211","v0212","v0217","v0219","v0221","v0222","v0226","v0227","v0228"]
Cond_Hab_F=Cond_Hab.filter(items=variables)
del(Cond_Hab)

##### Criando Variaveis Binarias

### Agua Canalizada em algum comodo 
Cond_Hab_Dummy=pd.get_dummies(Cond_Hab_F['v0211'])
temp1=Cond_Hab_Dummy[1.0]

### Acesso a rede de agua 
Cond_Hab_Dummy= pd.get_dummies(Cond_Hab_F['v0212'])
temp2=Cond_Hab_Dummy[2.0]
del(Cond_Hab_Dummy)

### Existe Fossa 
Cond_Hab_Dummy=pd.get_dummies(Cond_Hab_F['v0217'])
a=Cond_Hab_Dummy[1.0]
b=Cond_Hab_Dummy[2.0]
c=Cond_Hab_Dummy[3.0]
d=Cond_Hab_Dummy[4.0]
temp3=d+c+a+b

### iluminação Eletrica 
Cond_Hab_Dummy=pd.get_dummies(Cond_Hab_F['v0219'])
temp4=Cond_Hab_Dummy[1.0]

### Tem fogão 
Cond_Hab_Dummy1=pd.get_dummies(Cond_Hab_F['v0221'])
Cond_Hab_Dummy2=pd.get_dummies(Cond_Hab_F['v0222'])
a=Cond_Hab_Dummy1[1.0]
b=Cond_Hab_Dummy2[2.0]
temp5=a+b

### Tem Televisão 
Cond_Hab_Dummy1=pd.get_dummies(Cond_Hab_F['v0226'])
Cond_Hab_Dummy2=pd.get_dummies(Cond_Hab_F['v0227'])
a=Cond_Hab_Dummy1[2.0]
b=Cond_Hab_Dummy2[1.0]
temp6=a+b

### Tem Geladeira 
Cond_Hab_Dummy=pd.get_dummies(Cond_Hab_F['v0228'])
a=Cond_Hab_Dummy[2.0]
b=Cond_Hab_Dummy[4.0]
temp7=a+b

### Gerando a nova base
Cond_Hab_F['v0211']=temp1
Cond_Hab_F['v0212']=temp2
Cond_Hab_F['v0217']=temp3
Cond_Hab_F['v0219']=temp4
Cond_Hab_F['v0221']=temp5
Cond_Hab_F['v0226']=temp6
Cond_Hab_F['v0228']=temp7
del(Cond_Hab_F['v0222'])
del(Cond_Hab_F['v0227'])
Soma_Cond=soma(Cond_Hab_F)


######Educação 
Educ=pd.read_csv(Local_E)
Educ[np.isnan(Educ)]=0
variable=['v0601','v0602','v0611']
Educ_F=Educ.filter(items=variable)

#######Criando Variaveis Binarias

###Sabe ler e escrever 
Educ_Dummy=pd.get_dummies(Educ_F['v0601'])
temp1=Educ_Dummy[1.0]

### Frequenta escola ou creche
Educ_Dummy=pd.get_dummies(Educ_F['v0602'])
temp2=Educ_Dummy[2.0]

### Concluiu o curso que frequentou 
Educ_Dummy=pd.get_dummies(Educ_F['v0611'])
temp3=Educ_Dummy[1.0]

### Gerando os novos dados 
Educ_F['v0601']=temp1
Educ_F['v0602']=temp2
Educ_F['v0611']=temp3
Soma_Educ=soma(Educ_F)


###### Renda
Renda=pd.read_csv("Renda.csv")
Renda_F=Renda.filter(items=["v0101","uf",'id_dom',"v0302","v8005","v0401","v0404","v4727","v4728","v4729","v4721"])
Renda_C=Renda_F.groupby(['id_dom'])['id_dom'].count()
Renda_C=pd.DataFrame(Renda_C)
Renda_C.to_csv("Renda_C.csv")
Renda_C=pd.read_csv("Renda_C.csv")
Renda_P=Renda_F.merge(Renda_C, left_on='id_dom', right_on='id_dom', how='outer')
Renda_P['v4750']=Renda_P['v4721']/Renda_P['id_dom.1']
Renda_P[np.isnan(Renda_P['v4750'])]=0
##Linha de pobreza arbitraria
Renda_P[Renda_P['v4750']<=150]=0
Renda_P[Renda_P['v4750']>=150]=1
print(Renda_P['v4750'])


####Pobmult
Pobmult=Renda.filter(items=['v0101','uf','id_dom','v0302','v8005','v0401','v0404'])
######## Construindo resultados
base={'v0101':Educ['v0101'],'uf':Educ['uf'],'Cond_Hab':Soma_Cond,'Educ':Soma_Educ,'Trabalho':Trabalho_F,'Renda':Renda_P['v4750']}
Pobmult=pd.DataFrame(base)
print(Pobmult)

##### Filtrando por Ano
###Pobreza
Pobmult=Pobmult[Pobmult['uf']==23]
P2002=Pobmult[Pobmult['v0101']==2002]
P2003=Pobmult[Pobmult['v0101']==2003]
P2004=Pobmult[Pobmult['v0101']==2004]
P2005=Pobmult[Pobmult['v0101']==2005]
P2006=Pobmult[Pobmult['v0101']==2006]
P2007=Pobmult[Pobmult['v0101']==2007]
P2008=Pobmult[Pobmult['v0101']==2008]
P2009=Pobmult[Pobmult['v0101']==2009]
P2011=Pobmult[Pobmult['v0101']==2011]
P2012=Pobmult[Pobmult['v0101']==2012]
P2013=Pobmult[Pobmult['v0101']==2013]
P2014=Pobmult[Pobmult['v0101']==2014]
P2015=Pobmult[Pobmult['v0101']==2015]
print(P2002)
###Trabalho
Trabalho=Trabalho[Trabalho['uf']==23]
T=Trabalho.filter(items=["v0101","v9058"])
T2002=T[T['v0101']==2002]
T2003=T[T['v0101']==2003]
T2004=T[T['v0101']==2004]
T2005=T[T['v0101']==2005]
T2006=T[T['v0101']==2006]
T2007=T[T['v0101']==2007]
T2008=T[T['v0101']==2008]
T2009=T[T['v0101']==2009]
T2011=T[T['v0101']==2011]
T2012=T[T['v0101']==2012]
T2013=T[T['v0101']==2013]
T2014=T[T['v0101']==2014]
T2015=T[T['v0101']==2015]
### Renda 
Renda=Renda[Renda['uf']==23]
Renda2002=Renda[Renda['v0101']==2002]
Renda2003=Renda[Renda['v0101']==2003]
Renda2004=Renda[Renda['v0101']==2004]
Renda2005=Renda[Renda['v0101']==2005]
Renda2006=Renda[Renda['v0101']==2006]
Renda2007=Renda[Renda['v0101']==2007]
Renda2008=Renda[Renda['v0101']==2008]
Renda2009=Renda[Renda['v0101']==2009]
Renda2011=Renda[Renda['v0101']==2011]
Renda2012=Renda[Renda['v0101']==2012]
Renda2013=Renda[Renda['v0101']==2013]
Renda2014=Renda[Renda['v0101']==2014]
Renda2015=Renda[Renda['v0101']==2015]


####### Pobreza Multidimensional 
###2002
Pobreza_Mult2002=P2002['Cond_Hab']+P2002['Educ']+P2002['Trabalho']+P2002['Renda']
###2003
Pobreza_Mult2003=P2003['Cond_Hab']+P2003['Educ']+P2003['Trabalho']+P2003['Renda']
###2004
Pobreza_Mult2004=P2004['Cond_Hab']+P2004['Educ']+P2004['Trabalho']+P2004['Renda']
###2005
Pobreza_Mult2005=P2005['Cond_Hab']+P2005['Educ']+P2005['Trabalho']+P2005['Renda']
###2006
Pobreza_Mult2006=P2006['Cond_Hab']+P2006['Educ']+P2006['Trabalho']+P2006['Renda']
###2007
Pobreza_Mult2007=P2007['Cond_Hab']+P2007['Educ']+P2007['Trabalho']+P2007['Renda']
###2008
Pobreza_Mult2008=P2008['Cond_Hab']+P2008['Educ']+P2008['Trabalho']+P2008['Renda']
###2009 
Pobreza_Mult2009=P2009['Cond_Hab']+P2009['Educ']+P2009['Trabalho']+P2009['Renda']
###2011
Pobreza_Mult2011=P2011['Cond_Hab']+P2011['Educ']+P2011['Trabalho']+P2011['Renda']
###2012
Pobreza_Mult2012=P2012['Cond_Hab']+P2012['Educ']+P2012['Trabalho']+P2012['Renda']
###2013 
Pobreza_Mult2013=P2013['Cond_Hab']+P2013['Educ']+P2013['Trabalho']+P2013['Renda']
###2014
Pobreza_Mult2014=P2014['Cond_Hab']+P2014['Educ']+P2014['Trabalho']+P2014['Renda']
###2015 
Pobreza_Mult2015=P2015['Cond_Hab']+P2015['Educ']+P2015['Trabalho']+P2015['Renda']


######Graficos

###Educação
#fig=plt.figure()
#axes=fig.subplots(nrows=2,ncols=2)
#axes[0,0].set_title("2002")
#axes[0,0].hist(P2002['Educ'])
#axes[0,1].set_title("2006")
#axes[0,1].hist(P2006['Educ'])
#axes[1,0].set_title("2011")
#axes[1,0].hist(P2011['Educ'])
#axes[1,1].set_title("2015")
#axes[1,1].hist(P2015['Educ'])
#plt.show()

###Cond_Hab
#fig=plt.figure()
#axes=fig.subplots(nrows=2,ncols=3)
#axes[0,0].set_title("2002")
#axes[0,0].hist(P2002['Cond_Hab'])
#axes[0,1].set_title("2006")
#axes[0,1].hist(P2006['Cond_Hab'])
#axes[1,0].set_title("2011")
#axes[1,0].hist(P2011['Cond_Hab'])
#axes[1,1].set_title("2015")
#axes[1,1].hist(P2015['Cond_Hab'])
#plt.show()

###Trabalho 
#fig=plt.figure()
#axes=fig.subplots(nrows=2,ncols=3)
#axes[0,0].set_title("2002")
#axes[0,0].hist(T2002)
#axes[0,1].set_title("2006")
#axes[0,1].hist(T2006)
#axes[1,0].set_title("2011")
#axes[1,0].hist(T2011)
#axes[1,1].set_title("2015")
#axes[1,1].hist(T2015)
#plt.show()

### Pobreza
#fig=plt.figure()
#axes = fig.subplots(nrows=2, ncols=2)
#axes[0,0].set_title("2002")
#axes[0,0].set_xlabel("Nivel de Pobreza")
#axes[0,0].set_ylabel("Frequencia")
#axes[0,0].hist(Pobreza_Mult2002)
#axes[0,1].hist(Pobreza_Mult2006)
#axes[0,1].set_xlabel("Nivel de Pobreza")
#axes[0,1].set_ylabel("Frequencia")
#axes[0,1].set_title("2006")
#axes[1,0].hist(Pobreza_Mult2011)
#axes[1,0].set_title("2011")
#axes[1,0].set_xlabel("Nivel de Pobreza")
#axes[1,0].set_ylabel("Frequencia")
#axes[1,1].hist(Pobreza_Mult2015)
#axes[1,1].set_title("2015")
#axes[1,1].set_xlabel("Nivel de Pobreza")
#axes[1,1].set_ylabel("Frequencia")
#fig.suptitle('Pobreza Multidimensional', fontsize=16)
#plt.show()

#####Resultados descritivos 
Est2002=Stat_Desc(P2002)
Est2003=Stat_Desc(P2003)
Est2004=Stat_Desc(P2004)
Est2005=Stat_Desc(P2005)
Est2006=Stat_Desc(P2006)
Est2007=Stat_Desc(P2007)
Est2008=Stat_Desc(P2008)
Est2009=Stat_Desc(P2009)
Est2011=Stat_Desc(P2011)
Est2012=Stat_Desc(P2012)
Est2013=Stat_Desc(P2013)
Est2014=Stat_Desc(P2014)
Est2015=Stat_Desc(P2015)
print(Est2005)
##### Variaçao ao longo dos anos
Mean2015=Pobreza_Mult2015.mean()
Mean2014=Pobreza_Mult2014.mean()
Mean2013=Pobreza_Mult2013.mean()
Mean2012=Pobreza_Mult2012.mean()
Mean2011=Pobreza_Mult2011.mean()
Mean2009=Pobreza_Mult2009.mean()
Mean2008=Pobreza_Mult2008.mean()
#Mean2007=Pobreza_Mult2007.mean(),Mean2006=Pobreza_Mult2006.mean(),Mean2005=Pobreza_Mult2005.mean(),Mean2004=Pobreza_Mult2004.mean(),Mean2003=Pobreza_Mult2003,Mean2002=Pobreza_Mult2002.mean()
Mean=[float(Mean2015),float(Mean2014),float(Mean2013),float(Mean2012),float(Mean2011),float(Mean2009)]#,Mean2008,Mean2007,Mean2006,Mean2005,Mean2004,Mean2003]
Mean=pd.DataFrame(Mean)
Mean=Mean.transpose()
Time_dif(Mean)



