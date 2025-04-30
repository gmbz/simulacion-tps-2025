import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sys import argv as arguments, exit
from os import path as filepath

# argumentos: -c <num_tiradas> -n <num_corridas> -s <estrategia> -a <tipo_capital>.
# Se debe cumplir:
#   -c y -n deben ser enteros mayores a cero
#   -s es la estrategia utilizada, puede ser m (Martingala), d (D’Alambert), f (Fibonacci), o (Martingala invertida)
#   -a es el tipo de capital, puede ser: f (fijo) o i (infinito)

if len(arguments) != 9 or arguments[1] != "-c" or arguments[3] != "-n" or arguments[5] != "-s" or arguments[7] != "-a":
    print("La cantidad de argumentos o su orden es incorrecta.\n")
    print("Uso: python/python3 {} -c <cantidad_de_tiradas>[int 1-1000] -n <cantidad_de_corridas>[int 1-100] -e "
          "<numero_elegido>[int 0-36] -s <estrategia>[m, d, f, p] -a <tipo_capital>[f, i]\n".format(filepath.basename(__file__)))
    print("Las estraegias pueden ser: m (Martingala), d (D'Alambert), f (Fibonacci), o (Martingala invertida)")
    print("El tipo de capital puede ser: f (fijo) o i (infinito)")
    print("Ejemplo: python/python3 {} -c 1000 -n 10 -s m -a f".format(filepath.basename(__file__)))
    exit(1)

cantidad_tiradas = int(arguments[2])
cantidad_corridas = int(arguments[4])
estrategia = arguments[6]
tipo_capital = arguments[8]

apuesta_inicial = 5
capital_inicial = 10000
resultados_rojo = [1, 3, 5, 7, 9, 12, 14, 16,18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
frec_relativa_esperada = 18/37 # apostando al rojo, 18 numeros rojos de 37

serie_fibonacci = [1, 1]
indice_fibonacci = 0

estrategias = {
    'f': {
        'title': f'ESTRATEGIA FIBONACCI',
    },
    'm': {
        'title': f'ESTRATEGIA MARTINGALA',
    },
    'd': {
        'title': f'ESTRATEGIA DALEMBERT',
    },
    'o': {
        'title': f'ESTRATEGIA MARGINGALA INVERTIDA',
    },
}

def estrategia_dalembert(ultima_apuesta, is_win, capital):
    unidad = apuesta_inicial
    if is_win:
        capital += ultima_apuesta
        # Evitar apuestas menores que la unidad inicial
        proxima_apuesta = max(ultima_apuesta - unidad, unidad)
    else:
        capital -= ultima_apuesta
        proxima_apuesta = ultima_apuesta + unidad

    return proxima_apuesta, capital

def estrategia_fibonacci(ultima_apuesta, is_win, capital):
    global indice_fibonacci
    if is_win:
        capital += ultima_apuesta
        if indice_fibonacci > 1:
            indice_fibonacci -= 2
        else:
            indice_fibonacci = 0
    else:
        capital -= ultima_apuesta
        indice_fibonacci += 1
        if indice_fibonacci >= len(serie_fibonacci):
            nuevo_valor = serie_fibonacci[-1] + serie_fibonacci[-2]
            serie_fibonacci.append(nuevo_valor)
    
    proxima_apuesta = serie_fibonacci[indice_fibonacci]
    
        

    return proxima_apuesta, capital

def estrategia_martingala_invertida(ultima_apuesta, is_win, capital):
    unidad = apuesta_inicial
    if is_win:
        capital += ultima_apuesta
        proxima_apuesta = ultima_apuesta + unidad #si gana se aumenta la apuesta
    else:
        capital -= ultima_apuesta
        proxima_apuesta = apuesta_inicial #si pierde se vuelve a la apuesta inicial

    proxima_apuesta = min(proxima_apuesta, capital) #no se apuesta más de lo disponible
    
    return proxima_apuesta, capital


def ejecutar_corrida():
    df = pd.DataFrame()
    df['tiradas'] = np.random.randint(0, 37, cantidad_tiradas)

    wins = []
    frecuencia_relativa = []
    apuestas = []
    flujo_caja = []

    apuestas.append(apuesta_inicial)
    flujo_caja.append(capital_inicial)

    capital = capital_inicial
    for index, tirada in enumerate(df['tiradas']):

        is_win = tirada in resultados_rojo
        wins.append(is_win)

        frecuencia_relativa.append(wins.count(True) / (index + 1))

        if estrategia == 'f':
            proxima_apuesta, capital = estrategia_fibonacci(apuestas[-1], is_win, capital)
        elif estrategia == 'd':
            proxima_apuesta, capital = estrategia_dalembert(apuestas[-1], is_win, capital)
        elif estrategia == 'o':
            proxima_apuesta, capital = estrategia_martingala_invertida(apuestas[-1], is_win, capital)

        if proxima_apuesta > capital and tipo_capital == 'f':  # banca rota
            break

        if len(apuestas) == cantidad_tiradas:
            break

        apuestas.append(proxima_apuesta)
        flujo_caja.append(capital)

    df = pd.DataFrame({
        'flujo_caja': flujo_caja,
        'apuestas': apuestas,
        'wins': wins,
        'frec_rel': frecuencia_relativa
    })
    
    df.index = df.index + 1
    
    return df

def grafico_flujo_caja(corridas):
    print('Graficando flujo de caja...')
    plt.figure()
        
    for corrida in corridas:
        sns.lineplot(x=corrida.index, y=corrida['flujo_caja'], alpha=1, linewidth=1, label=None)

    esperado_label = 'Capital inicial'
    plt.axhline(capital_inicial, color='red', linestyle='--', label=f'{esperado_label}') 
    
    title = f'{estrategias[estrategia]['title']} - {cantidad_corridas} CORRIDAS'
    xlabel = 'n (número de tiradas)'
    ylabel = 'c (capital)'
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

def graficar_histograma(corridas):
    print('Graficando histograma...')
    fig, ax = plt.subplots()

    ax.set_xlabel('n (número de tiradas)')
    ax.set_ylabel('fr (frecuencia relativa)')

    for corrida in corridas:
        ax.bar(corrida.index, corrida['frec_rel'], alpha=0.5)

    ax.axhline(frec_relativa_esperada, color='r', linestyle='--', label='fre (frecuencia relativa esperada)')
    ax.legend()

    ax.set_title(f"HISTOGRAMA {estrategias[estrategia]['title']} - {cantidad_corridas} CORRIDAS")
    plt.show()


### MAIN ###
corridas = []
for corrida in range(cantidad_corridas):
    corridas.append(ejecutar_corrida())

grafico_flujo_caja(corridas)
graficar_histograma(corridas)

df_promedio_list = []
df_promedio = pd.concat(corridas).groupby(level=0).mean()
df_promedio_list.append(df_promedio)
grafico_flujo_caja(df_promedio_list)
graficar_histograma(df_promedio_list)