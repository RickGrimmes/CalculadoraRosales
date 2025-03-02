import sympy as sp
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import font as tkFont
import pandas as pd
import matplotlib.pyplot as plt

class RungeKutta:
    def __init__(self, root):
        self.root = root
        self.root.title("Método de Runge-Kutta - Cuarto Orden")
        self.root.geometry("900x600")
        self.root.configure(bg="#ffcccc")

        self.custom_font = tkFont.Font(family="Chakra Petch", size=11)

        self.contenedor_principal = tk.Frame(self.root, bg="#ffffff", padx=20, pady=20)
        self.contenedor_principal.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Parte superior para entradas y botón
        self.frame_entradas = tk.Frame(self.contenedor_principal, bg="#ffffff")
        self.frame_entradas.pack(fill=tk.X, padx=10, pady=10)

        # Parte inferior dividida en dos
        self.frame_inferior = tk.Frame(self.contenedor_principal, bg="#ffffff")
        self.frame_inferior.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.frame_procedimiento = tk.Frame(self.frame_inferior, bg="#ffffff")
        self.frame_procedimiento.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.frame_resultados = tk.Frame(self.frame_inferior, bg="#ffffff")
        self.frame_resultados.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Entradas
        tk.Label(self.frame_entradas, text="Ecuación:", bg="#ffffff", font=self.custom_font).grid(row=0, column=0, sticky="w")
        self.entrada_ecuacion = tk.Entry(self.frame_entradas, width=30, font=self.custom_font)
        self.entrada_ecuacion.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.frame_entradas, text="x inicial:", bg="#ffffff", font=self.custom_font).grid(row=1, column=0, sticky="w")
        self.entrada_x0 = tk.Entry(self.frame_entradas, font=self.custom_font)
        self.entrada_x0.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.frame_entradas, text="y inicial:", bg="#ffffff", font=self.custom_font).grid(row=2, column=0, sticky="w")
        self.entrada_y0 = tk.Entry(self.frame_entradas, font=self.custom_font)
        self.entrada_y0.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(self.frame_entradas, text="Paso (h):", bg="#ffffff", font=self.custom_font).grid(row=3, column=0, sticky="w")
        self.entrada_h = tk.Entry(self.frame_entradas, font=self.custom_font)
        self.entrada_h.grid(row=3, column=1, padx=5, pady=5)

        tk.Label(self.frame_entradas, text="x final:", bg="#ffffff", font=self.custom_font).grid(row=4, column=0, sticky="w")
        self.entrada_xf = tk.Entry(self.frame_entradas, font=self.custom_font)
        self.entrada_xf.grid(row=4, column=1, padx=5, pady=5)

        tk.Button(self.frame_entradas, text="Calcular", command=self.calcular, bg="#007bff", fg="white", font=self.custom_font, padx=10, pady=5).grid(row=5, columnspan=2, pady=10)

        # Área procedimiento
        tk.Label(self.frame_procedimiento, text="Procedimiento:", bg="#ffffff", font=self.custom_font).pack(anchor="w", padx=10)
        self.area_proceso = tk.Text(self.frame_procedimiento, height=20, width=60, font=self.custom_font)
        self.area_proceso.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Tabla de resultados
        tk.Label(self.frame_resultados, text="Resultados:", bg="#ffffff", font=self.custom_font).pack(anchor="w", padx=10)
        columnas = ("Iteración", "x", "y", "k1", "k2", "k3", "k4", "y_siguiente")
        self.tabla_resultados = ttk.Treeview(self.frame_resultados, columns=columnas, show="headings")
        for col in columnas:
            self.tabla_resultados.heading(col, text=col)
            self.tabla_resultados.column(col, anchor="center", width=100)
        self.tabla_resultados.pack(fill=tk.BOTH, expand=True, pady=5, padx=10)

    def metodo_runge_kutta(self, funcion, x0, y0, h, xf):
        x, y = sp.symbols('x y')
        f = sp.lambdify((x, y), funcion, 'numpy')
        
        resultados = []
        pasos = []
        
        num_iteraciones = int((xf - x0) / h)
        
        for i in range(num_iteraciones + 1):
            k1 = f(x0, y0)
            k2 = f(x0 + h / 2, y0 + (h / 2) * k1)
            k3 = f(x0 + h / 2, y0 + (h / 2) * k2)
            k4 = f(x0 + h, y0 + h * k3)
            
            y_next = y0 + (h / 6) * (k1 + 2 * k2 + 2 * k3 + k4)
            
            x0 = round(x0, 4)
            y0 = round(y0, 4)
            k1 = round(k1, 4)
            k2 = round(k2, 4)
            k3 = round(k3, 4)
            k4 = round(k4, 4)
            y_next = round(y_next, 4)
            
            pasos.append(f"Iteración {i + 1}:")
            pasos.append(f"  x{i} = {x0}, y{i} = {y0}")
            pasos.append(f"  k1 = {k1}, k2 = {k2}, k3 = {k3}, k4 = {k4}")
            pasos.append(f"  y{i + 1} = {y_next}\n")
            
            resultados.append([i + 1, x0, y0, k1, k2, k3, k4, y_next])
            
            x0 += h
            y0 = y_next
        
        return resultados, pasos

    def calcular(self):
        try:
            ecuacion = sp.sympify(self.entrada_ecuacion.get())
            x0 = float(self.entrada_x0.get())
            y0 = float(self.entrada_y0.get())
            h = float(self.entrada_h.get())
            xf = float(self.entrada_xf.get())
            
            resultados, pasos = self.metodo_runge_kutta(ecuacion, x0, y0, h, xf)
            
            for fila in self.tabla_resultados.get_children():
                self.tabla_resultados.delete(fila)
            
            for resultado in resultados:
                self.tabla_resultados.insert("", "end", values=resultado)
            
            self.area_proceso.delete("1.0", tk.END)
            self.area_proceso.insert(tk.END, "\n".join(pasos))
            
            self.mostrar_tabla(resultados)
            self.graficar(resultados)
        except Exception as e:
            messagebox.showerror("Error", f"Ha ocurrido un problema: {e}")

    def mostrar_tabla(self, resultados):
        df = pd.DataFrame(resultados, columns=['Iteración', 'x', 'y', 'k1', 'k2', 'k3', 'k4', 'y_siguiente'])

    def graficar(self, resultados):
        df = pd.DataFrame(resultados, columns=['Iteración', 'x', 'y', 'k1', 'k2', 'k3', 'k4', 'y_siguiente'])
        plt.plot(df['x'], df['y_siguiente'], marker='o')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.title('Método de Runge-Kutta - Cuarto Orden')
        plt.grid(True)
        plt.show()

if __name__ == "__main__":
    print("Usa el archivo main.py, por algo lo creé -_-")