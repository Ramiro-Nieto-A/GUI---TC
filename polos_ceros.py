import matplotlib.pyplot as plt

# Datos de los puntos
x = [0]  # Coordenadas x
y = [0]  # Coordenadas y
w = [-25000,-25000]
z = [256986,-256986]

# Crear el gráfico de dispersión
plt.figure(figsize=(8, 6))  # Tamaño de la figura
plt.scatter(x, y, color='blue', marker='o', label='Puntos')  # Representar los puntos
plt.scatter(w, z, color='red', marker='x', label='Puntos')  # Representar los puntos

# Personalizar el gráfico
plt.title('Gráfico de dispersión de puntos')
plt.xlabel('Eje x')
plt.ylabel('Eje y')
plt.axhline(0, color='black',linewidth=0.5)  # Añadir línea horizontal en y=0
plt.axvline(0, color='black',linewidth=0.5)  # Añadir línea vertical en x=0
plt.legend()
plt.grid(True)
plt.show()  # Mostrar el gráfico
