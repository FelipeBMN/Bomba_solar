import math
import os


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
clear_screen()

# DADOS DA INSTALAÇÃO -----------------------------------------------------------

# fator_solar = 4.6

temperatura_min = 12

temperatura_max = 80

# DADOS DA BOMBA ----------------------------------------------------------------

# Fator de potência
# fp = 0.7

# Fator de serviço
# fs = 1.1

# Rendimento
# rend = 72.5/100

# Tensão da bomba
V_bomba_220 = 220
V_bomba_380 = 380

# Corrente da bomba
I_bomba_220 = 5.85
I_bomba_380 = 3.35

# DADOS DAS PLACAS ----------------------------------------------------------------

# Desempenho do sistema fotovoltaico
Desempenho_sistema_fotovoltaico = 0.8

# Potência de pico da placa
Wp = 330

# Tensão de circuito aberto (stc) placa
V_oc_stc = 44.72

# Tensão de funcionamento maxima potencia (stc) placa
V_mpp_stc = 37.26

# Coeficiente de temperatura Voc
Co_V_oc = -0.3

# Coeficiente de temperatura Pmax
Co_V_mpp = -0.4

# Corrente da placa de maxima potencia 
I_mpp_stc = 8.86

# Corrente de curto circuito
I_cc_stc = 9.57

# DADOS DAS INVERSOR ----------------------------------------------------------------

# Tensão maxima 220
V_cfw_220_min = 200

# Tensão minima 220
V_cfw_220_max = 410

# Tensão maxima 380
V_cfw_380_min = 360

# Tensão minima 380
V_cfw_380_max = 810

# Calculo ---------------------------------------------------------------------------

# Calculando Potência minima de módulos
P_mpp_220 = math.sqrt(3) * V_bomba_220 * I_bomba_220 / \
    Desempenho_sistema_fotovoltaico
P_mpp_380 = math.sqrt(3) * V_bomba_380 * I_bomba_380 / \
    Desempenho_sistema_fotovoltaico

print(f'Potencia Wp necessária 220v: {math.ceil(P_mpp_220)}')
print(f'Potencia Wp necessária 380v: {math.ceil(P_mpp_380)}')
print()

# Numero Minimo de placas
Np_min_220_necessário = math.ceil(P_mpp_220/Wp)
Np_min_380_necessário = math.ceil(P_mpp_380/Wp)

print(f'Numero minimo de placas para 220v: {Np_min_220_necessário}')
print(f'Numero minimo de placas para 380v: {Np_min_380_necessário}')
print()

# Calculando Voc da placa corrigido
V_oc = V_oc_stc * (1 + (temperatura_min - 25) * Co_V_oc/100)

# Calculando Vmpp da placa corrigido
V_mpp = V_mpp_stc * (1 + (temperatura_max - 25) * Co_V_mpp/100)

print(f'Tensão de circuito abeto placa: {V_oc}v')
print(f'Tensão de maxima potência placa: {V_mpp}v')
print()

# Para 220v
Np_220_max = math.floor(V_cfw_220_max/V_oc)
Np_220_min = math.ceil(V_cfw_220_min/V_mpp)
print(
    f'Para 220v podemos utilizar entre {Np_220_min} a {Np_220_max} módulos em serie')

# Para 380v
Np_380_max = math.floor(V_cfw_380_max/V_oc)
Np_380_min = math.ceil(V_cfw_380_min/V_mpp)
print(
    f'Para 380v podemos utilizar entre {Np_380_min} a {Np_380_max} módulos em serie')
print()

# Montando sistema
# Para 220v
paralelo_220 = 1
serie_220 = 1
while (True):
    if Np_min_220_necessário <= Np_220_min*paralelo_220:
        serie_220 = Np_220_min
        break
    if Np_min_220_necessário <= Np_220_max*paralelo_220:
        for i in range(Np_220_min, Np_220_max+1):
            if i*paralelo_220 < Np_min_220_necessário:
                serie_220 = i
                break
    paralelo_220 = paralelo_220 + 1
print(f'Sera necessário {paralelo_220} sequencia(s) de {serie_220} módulos em serie para 220v')

# Para 380v 
paralelo_380 = 1
serie_380 = 1
while(True):
    if Np_min_380_necessário <= Np_380_min*paralelo_380 :
       serie_380 = Np_380_min
       break
    if Np_min_380_necessário <= Np_380_max*paralelo_380:
       for i in range(Np_380_min,Np_380_max+1):
            if i*paralelo_380 < Np_min_380_necessário:
                serie_380 = i
                break
    paralelo_380 = paralelo_380 + 1
print(f'Sera necessário {paralelo_380} sequencia(s) de {serie_380} módulos em serie para 380v')
print()

print('---------------------------- 220V --------------------------------')
print(f'Sera necessário {paralelo_220} sequencia(s) de {serie_220} módulos em serie para 220v')
print(f'Potência mais proxima possível para 220v: {serie_220*paralelo_220*Wp}')
print(f'Tensão Voc: {round(serie_220*V_oc,2)}')
print(f'Tensão Vmpp: {round(serie_220*V_mpp,2)}')
print(f'Corrente Impp: {round(paralelo_220*I_mpp_stc,2)}')
print(f'Corrente Icc: {round(paralelo_220*I_cc_stc,2)}')

print('---------------------------- 380V --------------------------------')
print(f'Sera necessário {paralelo_380} sequencia(s) de {serie_380} módulos em serie para 380v')
print(f'Potência mais proxima possível para 380v: {round(serie_380*paralelo_380*Wp,2)}')
print(f'Tensão Voc: {round(serie_380*V_oc,2)}')
print(f'Tensão Vmpp: {round(serie_380*V_mpp,2)}')
print(f'Corrente Impp: {round(paralelo_380*I_mpp_stc,2)}')
print(f'Corrente Icc: {round(paralelo_380*I_cc_stc,2)}')