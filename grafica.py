import numpy as np
import matplotlib.pyplot as plt

# Definir la función que queremos graficar
def f(x):
    return 20 * np.log10(1 / np.sqrt(1 + ((2 * np.pi * x)**2) * (50**2) * ((15e-9)**2)))
# Crear un rango de valores para x
x = np.linspace(0, 100000000, 3000000)  # Crea 400 puntos entre -10 y 10
y = f(x)  # Aplica la función a cada valor de x

# Crear la gráfica
plt.figure(figsize=(8, 6))  # Tamaño de la figura
plt.plot(x, y, label='$|H(f)|(db)$', color='blue')  # Grafica x contra y
plt.title('Gráfico de $|H(f)|(db)$')  # Título del gráfico
plt.xlabel('$f$')  # Etiqueta del eje x
plt.ylabel('$|H|(db)$')  # Etiqueta del eje y
plt.xscale('log')
plt.legend()  # Muestra la leyenda
plt.grid(True)  # Muestra una cuadrícula
plt.show()  # Muestra el gráfico
