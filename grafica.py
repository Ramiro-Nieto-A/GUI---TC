import matplotlib.pyplot as plt
import numpy as np

# Definir la función que queremos graficar
def f(x):
    return (1 * 1e-3 * (0.18) * (-6500) * np.exp(-6500 * x * 1e-6) * np.cos(110240.0651 * x * 1e-6 + 5.04e-3) - 1 * 1e-3 * (0.18) * 110240.0651 * np.exp(-6500 * x * 1e-6) * np.sin(110240.0651 * x * 1e-6 + 5.04e-3))

# Crear un rango de valores para x
x = np.linspace(0, 1000, 3000000)  # Crea 400 puntos entre -10 y 10
y = f(x)  # Aplica la función a cada valor de x

# Crear la gráfica
plt.figure(figsize=(8, 6))  # Tamaño de la figura
plt.plot(x, y, label='$Vl$', color='blue')  # Grafica x contra y
plt.title('Gráfico de $Vl$')  # Título del gráfico
plt.xlabel('$tiempo(µs)$')  # Etiqueta del eje x
plt.ylabel('$V$')  # Etiqueta del eje y
plt.xscale('linear')
plt.legend()  # Muestra la leyenda
plt.grid(True)  # Muestra una cuadrícula
plt.show()  # Muestra el gráfico
