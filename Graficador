import tkinter as tk
from tkinterdnd2 import DND_FILES, TkinterDnD
import pandas as pd
import matplotlib.pyplot as plt
import os

# Variables globales
archivo_actual = None

def suavizar_serie(serie, ventana=7):
    return serie.rolling(window=ventana, center=True).mean().fillna(method='bfill').fillna(method='ffill')

def procesar_archivo(ruta_archivo, col_rem, col_caudal, invertir_rem, invertir_caudal, ventana_suavizado):
    try:
        df = pd.read_excel(ruta_archivo)

        if col_rem not in df.columns or col_caudal not in df.columns:
            print(f"⚠️ Las columnas '{col_rem}' o '{col_caudal}' no están en el archivo.")
            return

        remanencia = df[col_rem]
        caudalimetro = df[col_caudal]
        if invertir_rem:
            remanencia = remanencia[::-1].reset_index(drop=True)
        else:
            remanencia = remanencia.reset_index(drop=True)
        if invertir_caudal:
            caudalimetro = caudalimetro[::-1].reset_index(drop=True)
        else:
            caudalimetro = caudalimetro.reset_index(drop=True)

        min_len = min(len(remanencia), len(caudalimetro))
        remanencia = remanencia[:min_len]
        caudalimetro = caudalimetro[:min_len]

        remanencia = remanencia - remanencia.iloc[0]
        caudalimetro = caudalimetro - caudalimetro.iloc[0]

        remanencia_suavizada = suavizar_serie(remanencia, ventana=ventana_suavizado)
        diferencia = caudalimetro - remanencia_suavizada

        plt.figure(figsize=(12, 6))
        plt.plot(remanencia_suavizada, label='Remanencia (suavizada)', color='red')
        plt.plot(caudalimetro, label='Caudalímetro', color='blue')
        plt.plot(diferencia, label='Diferencia', linestyle='--', color='green')
        plt.title(f'{col_rem} vs {col_caudal} y su Diferencia')
        plt.xlabel('Índice')
        plt.ylabel('Valor desde cero')
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    except Exception as e:
        print(f"Error al procesar el archivo: {e}")

def on_drop(event):
    global archivo_actual
    ruta = event.data.strip('{}')
    if os.path.isfile(ruta) and ruta.endswith(('.xlsx', '.xls')):
        archivo_actual = ruta
        label_archivo.config(text=f"📄 Archivo cargado:\n{os.path.basename(ruta)}")
        boton_borrar.config(state="normal")
        boton_graficar.config(state="normal")
    else:
        label_archivo.config(text="❌ Archivo inválido.")

def borrar_archivo():
    global archivo_actual
    archivo_actual = None
    label_archivo.config(text="📂 Ningún archivo cargado")
    boton_borrar.config(state="disabled")
    boton_graficar.config(state="disabled")

def actualizar_grafico(event=None):
    """Actualiza el gráfico en tiempo real al mover el control deslizante."""
    if archivo_actual:
        col_rem = entry_remanencia.get().strip()
        col_caudal = entry_caudal.get().strip()
        invertir_rem = var_invertir_rem.get()
        invertir_caudal = var_invertir_caudal.get()
        ventana_suavizado = slider_suavizado.get()  # Obtener el valor del control deslizante
        procesar_archivo(archivo_actual, col_rem, col_caudal, invertir_rem, invertir_caudal, ventana_suavizado)

def graficar():
    """Función llamada al presionar el botón 'Graficar'."""
    actualizar_grafico()

# Crear ventana
root = TkinterDnD.Tk()
root.title("Diferencia entre columnas")
root.geometry("600x400")
root.configure(bg="#f0f0f0")

frame = tk.Frame(root, bg="#f0f0f0")
frame.pack(padx=20, pady=10)

tk.Label(frame, text="Nombre columna 1:", bg="#f0f0f0").grid(row=0, column=0, sticky="e")
entry_remanencia = tk.Entry(frame, width=30)
entry_remanencia.insert(0, "Remanencia Total")
entry_remanencia.grid(row=0, column=1, padx=10, pady=5)

tk.Label(frame, text="Nombre columna 2:", bg="#f0f0f0").grid(row=1, column=0, sticky="e")
entry_caudal = tk.Entry(frame, width=30)
entry_caudal.insert(0, "Caudalímetro Total")
entry_caudal.grid(row=1, column=1, padx=10, pady=5)

# Checkboxes
var_invertir_rem = tk.BooleanVar(value=True)
check_rem = tk.Checkbutton(frame, text="Invertir columna 1", variable=var_invertir_rem, bg="#f0f0f0")
check_rem.grid(row=2, column=0, columnspan=2, sticky="w")

var_invertir_caudal = tk.BooleanVar(value=False)
check_caudal = tk.Checkbutton(frame, text="Invertir columna 2", variable=var_invertir_caudal, bg="#f0f0f0")
check_caudal.grid(row=3, column=0, columnspan=2, sticky="w")

# Crear control deslizante para el factor de suavizado
tk.Label(frame, text="Factor de suavizado:", bg="#f0f0f0").grid(row=4, column=0, sticky="e")
slider_suavizado = tk.Scale(frame, from_=1, to=50, orient="horizontal", bg="#f0f0f0", command=actualizar_grafico)
slider_suavizado.set(7)  # Valor inicial
slider_suavizado.grid(row=4, column=1, padx=10, pady=5)

# Zona drag & drop
label_drop = tk.Label(root, text="📥 Arrastrá un archivo Excel aquí", bg="#d0e0ff", font=("Arial", 14), relief="ridge")
label_drop.pack(expand=False, fill=tk.X, padx=20, pady=10)
label_drop.drop_target_register(DND_FILES)
label_drop.dnd_bind('<<Drop>>', on_drop)

# Estado del archivo
label_archivo = tk.Label(root, text="📂 Ningún archivo cargado", bg="#f0f0f0", font=("Arial", 12))
label_archivo.pack(pady=5)

# Botones
boton_frame = tk.Frame(root, bg="#f0f0f0")
boton_frame.pack(pady=10)

boton_borrar = tk.Button(boton_frame, text="❌ Quitar archivo", command=borrar_archivo, state="disabled")
boton_borrar.grid(row=0, column=0, padx=10)

boton_graficar = tk.Button(boton_frame, text="📊 Graficar", command=graficar, state="disabled")
boton_graficar.grid(row=0, column=1, padx=10)

root.mainloop()
