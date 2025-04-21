import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sys import argv as arguments, exit
from os import path as filepath

# argumentos: -c <num_tiradas> -n <num_corridas> -e <numero_elegido>. -c y -n deben ser enteros mayores a cero y -e debe estar entre 0 y 36
if len(arguments) != 7 or arguments[1] != "-c" or arguments[3] != "-n" or arguments[5] != "-e":
    print("La cantidad de argumentos o su orden es incorrecta.\n")
    print("Uso: python/python3 {} -c <cantidad_de_tiradas>[int 1-1000] -n <cantidad_de_corridas>[int 1-100] -e "
          "<numero_elegido>[int 0-36]\n".format(filepath.basename(__file__)))
    print("Ejemplo: python/python3 {} -c 1000 -n 10 -e 8".format(filepath.basename(__file__)))
    exit(1)

cantidad_tiradas = int(arguments[2])
cantidad_corridas = int(arguments[4])
numero_elegido = int(arguments[6])

tiradas = np.random.randint(0, 37, cantidad_tiradas)
desviacion_estandar_esperada = np.arange(0, 37, 1).std()
varianza_esperada = np.arange(0, 37, 1).var()
esperanza_matematica_esperada = np.arange(0, 37, 1).mean()

col_to_keys = {
    'desv_est': {
        'title': f'DESVÍO ESTANDAR DEL NUMERO {numero_elegido}',
        'ylabel': 'vd (valor del desvio)',
        'xlabel': 'n (numero tiradas)',
        'esperado_label': 'vde (valor del desvio esperado)'
    },
    'var': {
        'title': f'VARIANZA DEL NUMERO {numero_elegido}',
        'ylabel': 'vv (valor de la varianza)',
        'xlabel': 'n (numero tiradas)',
        'esperado_label': 'vve (valor de la varianza esperada)'
    },
    'frec_rel': {
        'title': f'FRECUENCIA RELATIVA DEL NUMERO {numero_elegido}',
        'ylabel': 'fr (frecuencia relativa)',
        'xlabel': 'n (numero tiradas)',
        'esperado_label': 'frn (frecuencia relativa esperada)'
    },
    'frec_rel_%': {
        'title': f'FRECUENCIA RELATIVA (%) DEL NUMERO {numero_elegido}',
        'ylabel': 'fr (frecuencia relativa)',
        'xlabel': 'n (numero tiradas)',
        'esperado_label': 'frn (frecuencia relativa esperada)'
    },
    'esp_mat': {
        'title': f'ESPERANZA MATEMATICA DEL NUMERO {numero_elegido}',
        'ylabel': 'vp (valor promedio de las tiradas)',
        'xlabel': 'n (numero tiradas)',
        'esperado_label': 'vpe (valor promedio esperado)'
    }
}

lineas_horizontales = {
    'desv_est': desviacion_estandar_esperada,
    'var': varianza_esperada,
    'esp_mat': esperanza_matematica_esperada,
    'frec_rel': 1/37,
    'frec_rel_%': (1/37)*100
}


def ejecutar_corrida():
    df = pd.DataFrame()
    df['tiradas'] = np.random.randint(0, 37, cantidad_tiradas)

    frec_abs_acumulada = []
    frec_rel_acumulada = []
    esp_mat_acumulada = []
    desv_est_acumulada = []
    var_acumulada = []

    cantidad_ocurrencias = 0
    for index, tirada in enumerate(df['tiradas']):
        if tirada == numero_elegido:
            cantidad_ocurrencias += 1
        frec_abs_acumulada.append(cantidad_ocurrencias)
        frec_rel_acumulada.append(cantidad_ocurrencias/(index+1))
        esp_mat_acumulada.append(np.mean(df['tiradas'][:index+1]))
        desv_est_acumulada.append(np.std(df['tiradas'][:index+1]))
        var_acumulada.append(np.var(df['tiradas'][:index+1]))

    df['frec_abs'] = frec_abs_acumulada
    df['frec_rel'] = frec_rel_acumulada
    df['frec_rel_%'] = np.array(frec_rel_acumulada) * 100
    df['esp_mat'] = esp_mat_acumulada
    df['desv_est'] = desv_est_acumulada
    df['var'] = var_acumulada

    df.index = df.index + 1

    return df


def graficar(corridas, es_promedio):
    for col in ['desv_est', 'var', 'esp_mat', 'frec_rel', 'frec_rel_%']:
        plt.figure()

        for corrida in corridas:
            sns.lineplot(x=corrida.index,
                         y=corrida[col], alpha=0.6, linewidth=2, label=None)

        if col in lineas_horizontales:
            valor_esperado = lineas_horizontales[col]
            esperado_label = col_to_keys[col]['esperado_label']
            plt.axhline(valor_esperado, color='red', linestyle='--',
                        label=f'{esperado_label} = {valor_esperado:.4f}')

        title = f'{col_to_keys[col]['title']}{' PROMEDIO' if es_promedio else ''} - {cantidad_corridas} corridas'
        xlabel = col_to_keys[col]['xlabel']
        ylabel = col_to_keys[col]['ylabel']

        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.show()


def graficar_histograma(corridas, es_promedio):
    fig, ax = plt.subplots()

    ax.set_xlabel('n')
    ax.set_ylabel('fr (frecuencia relativa)')

    for corrida in corridas:
        ax.bar(corrida['tiradas'], corrida['frec_rel_%'], alpha=0.5)

    ax.axhline((1/37)*100, color='r', linestyle='--',
               label='fre (frecuencia relativa esperada)')

    ax.legend()

    if es_promedio:
        ax.set_title(f"HISTOGRAMA PROMEDIO {cantidad_corridas} CORRIDAS")
    else:
        ax.set_title(f"HISTOGRAMA {cantidad_corridas} CORRIDAS")

    plt.show()


def calcular_histograma(corridas):
    histogramas = []
    for corrida in corridas:
        df_prom = corrida.groupby('tiradas', as_index=False)[
            ['frec_rel', 'frec_abs']].mean()
        df_prom['frec_rel_%'] = df_prom['frec_rel']*100
        histogramas.append(df_prom)
    return histogramas


### MAIN ###
corridas = []
for corrida in range(cantidad_corridas):
    corridas.append(ejecutar_corrida())
df_promedio_list = []
df_promedio = pd.concat(corridas).groupby(level=0).mean()
df_promedio_list.append(df_promedio)
graficar(corridas, False)
graficar(df_promedio_list, True)
histogramas = calcular_histograma(corridas)
histograma_promedio_list = []
histograma_promedio = pd.concat(histogramas).groupby(level=0).mean()
histograma_promedio_list.append(histograma_promedio)
graficar_histograma(histogramas, False)
graficar_histograma(histograma_promedio_list, True)
