import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as patches

# Datos de ejemplo
# x_cero = [0]
# y_cero = [0]
x_polo = [-258198.8897]
y_polo = [0]


# Crear el gráfico de dispersión
# plt.scatter(x_cero, y_cero, s=100, c='blue', marker='o', label='Ceros')  # Puntos rojos, tamaño 100, marcador circular
plt.scatter(x_polo, y_polo, s=100, c='red', marker='x', label='Polos')  # Puntos rojos, tamaño 100, marcador circular


# Configurar los ejes para que se centren en 0
plt.axhline(0, color='black', linewidth=0.5)
plt.axvline(0, color='black', linewidth=0.5)

# Añadir una circunferencia
circle = patches.Circle((0, 0), radius=20058198.8897, edgecolor='green', facecolor='none', linestyle='dotted')
plt.gca().add_patch(circle)

# Establecer límites en los ejes para centrar el gráfico en el origen
plt.xlim(-300000, 300000)
plt.ylim(-300000, 300000)

# Añadir etiquetas a los ejes
plt.xlabel('σ')
plt.ylabel('jω')
plt.legend()

# Título del gráfico
plt.title('Gráfico de Polos y Ceros')
# Mostrar los ejes en notación científica
plt.ticklabel_format(style='sci', axis='both', scilimits=(0,0))

# Mostrar el gráfico
plt.grid(True)  # Añadir cuadrícula para mejor visualización
plt.gca().set_aspect('equal', adjustable='box')  # Asegurar que la circunferencia no se deforme
plt.show()
