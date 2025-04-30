import random
import argparse
import sys
import matplotlib.pyplot as plt
from collections import Counter

def jugar_martingala(banco, apuesta_inicial, capital_infinito=False, max_rondas=10000):
    apuesta = apuesta_inicial
    rondas = 0
    historia_banco = []
    resultados = []
    aciertos_acumulados = []
    salidas_ruleta = []

    aciertos = 0
    errores = 0

    while capital_infinito or banco > 0:
        if rondas >= max_rondas:
            print(f"Se alcanzó el máximo de {max_rondas} rondas.")
            break

        rondas += 1
        resultado = random.randint(0, 36)
        salidas_ruleta.append(resultado)
        es_rojo = resultado != 0 and resultado % 2 == 0  # simplificación: pares = rojo

        if not capital_infinito and banco < apuesta:
            print("No alcanza el banco para seguir apostando.")
            break

        if not capital_infinito:
            banco -= apuesta

        if es_rojo:
            if not capital_infinito:
                banco += apuesta * 2
            apuesta = apuesta_inicial
            aciertos += 1
            resultados.append("Acierto")
        else:
            apuesta *= 2
            errores += 1
            resultados.append("Error")

        historia_banco.append(banco if not capital_infinito else apuesta)
        aciertos_acumulados.append(aciertos / rondas)

    print(f"\nJuego terminado. Banco final: {banco if not capital_infinito else '∞'}")
    print(f"Aciertos: {aciertos}, Errores: {errores}")

    graficar_resultados(historia_banco, resultados, aciertos_acumulados, salidas_ruleta)

def graficar_resultados(banco_hist, resultados, aciertos_acumulados, salidas_ruleta):
    rondas = range(1, len(banco_hist) + 1)

    plt.figure(figsize=(15, 4))

    # Gráfico 1: Flujo de caja
    plt.subplot(1, 3, 1)
    plt.plot(rondas, banco_hist, label="Flujo de Caja", color='blue')
    plt.xlabel("Ronda")
    plt.ylabel("Capital")
    plt.title("Flujo de Caja")
    plt.grid(True)

    # Gráfico 2: Frecuencia relativa de números
    conteo = Counter(salidas_ruleta)
    total = len(salidas_ruleta)
    numeros = list(range(37))
    frecuencias = [conteo.get(n, 0) / total for n in numeros]

    plt.subplot(1, 3, 2)
    plt.bar(numeros, frecuencias, color='orange')
    plt.xlabel("Número")
    plt.ylabel("Frecuencia relativa")
    plt.title("Frecuencia relativa de números (0–36)")
    plt.xticks(numeros, rotation=90)

    # Gráfico 3: Tasa de éxito acumulada
    plt.subplot(1, 3, 3)
    plt.plot(rondas, aciertos_acumulados, color='green')
    plt.xlabel("Ronda")
    plt.ylabel("Tasa acumulada de acierto")
    plt.ylim(0, 1)
    plt.title("Efectividad acumulada")
    plt.grid(True)

    plt.tight_layout()
    plt.show()

def main():
    parser = argparse.ArgumentParser(description="Simulador de ruleta con estrategia Martingala")
    parser.add_argument("-s", "--strategy", choices=["martingala"], required=True,
                        help="Estrategia a usar: martingala (por ahora es la única disponible)")
    parser.add_argument("-a", "--capital", choices=["finito", "infinito"], required=True,
                        help="Tipo de capital: finito o infinito")

    args = parser.parse_args()

    if args.strategy == "martingala":
        capital_infinito = args.capital == "infinito"
        banco_inicial = 10000 if not capital_infinito else None
        jugar_martingala(banco=banco_inicial, apuesta_inicial=10, capital_infinito=capital_infinito)
    else:
        print("Estrategia no reconocida.")
        sys.exit(1)

if __name__ == "__main__":
    main()
