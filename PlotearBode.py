import control as ctl
import matplotlib.pyplot as plt
import numpy as np


#Aca definen su funcion transferencia, las listas numerador y denominador tienen los coeficientes de los polinomios
# Se escriben de la forma [a_n  a_(n-1) a_(n-2) ... a_0] donde se pasa a:  a_n * s^n + a_(n-1)* s^(n-1) + ... a_0
w_0 = 10e3
Xi = 0.2
numerador = [1]
denominador = [(1/w_0**2), 2*Xi/w_0, 1]
system = ctl.TransferFunction(numerador, denominador)

# Con esto modifico los limites del grafico
omega_min = 0.1*w_0  #radianes/seg
omega_max = 100*w_0  
numero_puntos = 1000  # Numero de puntos que hace mi simulacion (mientras más, más resolución)

omega = np.logspace(np.log10(omega_min), np.log10(omega_max), numero_puntos)

# Esta funcion me devuelve el módulo
magnitud, Fase, omega = ctl.bode(system, omega, dB=True, Hz=False, deg=True, Plot=False)

# Ploteo la magnitud
plt.figure()
plt.subplot(2, 1, 1)
plt.semilogx(omega, 20 * np.log10(magnitud))  # Convierto a dB
plt.title('Bode')
plt.ylabel('Magnitud (dB)')
plt.xlim([omega_min, omega_max])
plt.ylim([-80, 10])  #Ajusten la escala minima y maxima segun requieran

# Ploteo la Fase
plt.subplot(2, 1, 2)
plt.semilogx(omega, Fase * (180 / np.pi))  #Convierto a grados
plt.xlabel('Frecuencia (rad/s)')
plt.ylabel('Fase (grados)')
plt.xlim([omega_min, omega_max])
plt.ylim([-180, 0])  #Ajusten la escala minima y maxima segun requieran

plt.tight_layout()
plt.show()
