import numpy as np
import matplotlib.pyplot as plt

# Definir la función que queremos graficar
def f(x):
    return np.arctan(0) * (180 / np.pi) - np.arctan((2 * np.pi * x * 50 * 12e-9) / (1) ) * (180 / np.pi)
# Crear un rango de valores para x
x = np.linspace(0, 1000000000, 6000000)  # Crea 400 puntos entre -10 y 10
y = f(x)  # Aplica la función a cada valor de x

# Crear la gráfica
plt.figure(figsize=(8, 6))  # Tamaño de la figura
plt.plot(x, y, label='ϕ(H(f))$', color='blue')  # Grafica x contra y
plt.title('Gráfico de $ϕ(H(f))$')  # Título del gráfico
plt.xlabel('$f [Hz]$')  # Etiqueta del eje x
plt.ylabel('$ϕ(H(f)) [grados°]$')  # Etiqueta del eje y
plt.xscale('log')
plt.legend()  # Muestra la leyenda
plt.grid(True)  # Muestra una cuadrícula
plt.show()  # Muestra el gráfico