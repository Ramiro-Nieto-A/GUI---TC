import pandas as pd
import matplotlib.pyplot as plt

# Cargar los datos del CSV
data = pd.read_csv('bode2.csv')

# Graficar Gain en función de Frequency
plt.figure(figsize=(12, 6))
plt.subplot(2, 1, 1)  # (nrows, ncols, index)
plt.plot(data['Frequency (Hz)'], data['Gain (dB)'], label='Gain', color='b')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Gain (dB)')
plt.title('Gain vs Frequency')
plt.grid(True)
plt.legend()

# Graficar Phase en función de Frequency
plt.subplot(2, 1, 2)
plt.plot(data['Frequency (Hz)'], data['Phase (°)'], label='Phase', color='r')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Phase (°)')
plt.title('Phase vs Frequency')
plt.grid(True)
plt.legend()

# Ajustar el diseño para evitar superposiciones
plt.tight_layout()
plt.show()
