import matplotlib.pyplot as plt
import numpy as np

# Definir la función que queremos graficar
def f(x):
    return (37.93207*np.exp(-6500*x))*np.cos(np.radians(110431.5261*x + 88.381407))
# Crear un rango de valores para x
x = np.linspace(0, 0.002, 3000000)  # Crea 400 puntos entre -10 y 10
y = f(x)  # Aplica la función a cada valor de x

# Crear la gráfica
plt.figure(figsize=(8, 6))  # Tamaño de la figura
plt.plot(x, y, label='$Vl$', color='blue')  # Grafica x contra y
plt.title('Gráfico de $Vl$')  # Título del gráfico
plt.xlabel('$tiempo(s)$')  # Etiqueta del eje x
plt.ylabel('$Vl$')  # Etiqueta del eje y
plt.xscale('linear')
plt.legend()  # Muestra la leyenda
plt.grid(True)  # Muestra una cuadrícula
plt.show()  # Muestra el gráfico
