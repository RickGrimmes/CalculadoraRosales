import sympy as sp
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import font as tkFont
import pandas as pd
import matplotlib.pyplot as plt

class NewtonRaphson:
    def __init__(self, root):
        self.root = root
        self.root.title("Método de Newton-Raphson")
        self.root.geometry("900x600")
        self.root.configure(bg="#ffffcc")

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

        tk.Label(self.frame_entradas, text="x0 (Valor inicial):", bg="#ffffff", font=self.custom_font).grid(row=1, column=0, sticky="w")
        self.entrada_x0 = tk.Entry(self.frame_entradas, font=self.custom_font)
        self.entrada_x0.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.frame_entradas, text="Tolerancia:", bg="#ffffff", font=self.custom_font).grid(row=2, column=0, sticky="w")
        self.entrada_tol = tk.Entry(self.frame_entradas, font=self.custom_font)
        self.entrada_tol.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(self.frame_entradas, text="Nivel Precisión (decimales):", bg="#ffffff", font=self.custom_font).grid(row=3, column=0, sticky="w")
        self.entrada_precision = tk.Entry(self.frame_entradas, font=self.custom_font)
        self.entrada_precision.grid(row=3, column=1, padx=5, pady=5)

        tk.Button(self.frame_entradas, text="Calcular", command=self.ejecutar_calculo, bg="#007bff", fg="white", font=self.custom_font, padx=10, pady=5).grid(row=4, columnspan=2, pady=10)

        # Área procedimiento
        tk.Label(self.frame_procedimiento, text="Procedimiento:", bg="#ffffff", font=self.custom_font).pack(anchor="w", padx=10)
        self.area_proceso = tk.Text(self.frame_procedimiento, height=20, width=60, font=self.custom_font)
        self.area_proceso.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Tabla de resultados
        tk.Label(self.frame_resultados, text="Resultados:", bg="#ffffff", font=self.custom_font).pack(anchor="w", padx=10)
        columnas = ("Iteración", "x", "f(x)", "f'(x)", "x_nuevo")
        self.tabla_resultados = ttk.Treeview(self.frame_resultados, columns=columnas, show="headings")
        for col in columnas:
            self.tabla_resultados.heading(col, text=col)
            self.tabla_resultados.column(col, anchor="center", width=100)
        self.tabla_resultados.pack(fill=tk.BOTH, expand=True, pady=5, padx=10)

    def metodo_newton_raphson(self, f_expr, x_inicial, tolerancia, precision, max_iter=100):
        x = sp.symbols('x')
        funcion = sp.sympify(f_expr)
        derivada = sp.diff(funcion, x)

        funcion_lambda = sp.lambdify(x, funcion, 'numpy')
        derivada_lambda = sp.lambdify(x, derivada, 'numpy')

        resultados = []
        pasos = []

        for i in range(max_iter):
            f_x_inicial = funcion_lambda(x_inicial)
            df_x_inicial = derivada_lambda(x_inicial)

            if df_x_inicial == 0:
                messagebox.showerror("Error", "La derivada es cero, no se puede continuar.")
                return None, None

            x_siguiente = x_inicial - (f_x_inicial / df_x_inicial)
            
            x_inicial = round(x_inicial, precision)
            f_x_inicial = round(f_x_inicial, precision)
            df_x_inicial = round(df_x_inicial, precision)
            x_siguiente = round(x_siguiente, precision)
            
            pasos.append(f"Paso {i+1}:")
            pasos.append(f"  x{i} = {x_inicial}")
            pasos.append(f"  f(x{i}) = {f_x_inicial}")
            pasos.append(f"  f'(x{i}) = {df_x_inicial}")
            pasos.append(f"  x{i+1} = {x_inicial} - ({f_x_inicial} / {df_x_inicial}) = {x_siguiente}\n")
            
            resultados.append([i+1, x_inicial, f_x_inicial, df_x_inicial, x_siguiente])
            
            if abs(x_siguiente - x_inicial) < tolerancia:
                break
            x_inicial = x_siguiente
        else:
            messagebox.showwarning("Advertencia", "El método no converge en el número máximo de iteraciones.")

        return resultados, pasos

    def ejecutar_calculo(self):
        try:
            expresion = sp.sympify(self.entrada_ecuacion.get())
            x_inicial = float(self.entrada_x0.get())
            tolerancia = float(self.entrada_tol.get())
            precision = int(self.entrada_precision.get())
            
            if precision < 0:
                messagebox.showerror("Error", "La precisión debe ser un número entero positivo.")
                return
            
            datos, pasos = self.metodo_newton_raphson(expresion, x_inicial, tolerancia, precision)
            
            if datos is None:
                return
            
            for fila in self.tabla_resultados.get_children():
                self.tabla_resultados.delete(fila)
            
            for registro in datos:
                self.tabla_resultados.insert("", "end", values=registro)
            
            self.area_proceso.delete("1.0", tk.END)
            self.area_proceso.insert(tk.END, "\n".join(pasos))
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}")

    def mostrar_tabla(self, resultados):
        df = pd.DataFrame(resultados, columns=['Iteración', 'x', 'f(x)', 'f\'(x)', 'x_nuevo'])

    def graficar(self, resultados):
        df = pd.DataFrame(resultados, columns=['Iteración', 'x', 'f(x)', 'f\'(x)', 'x_nuevo'])
        plt.plot(df['x'], df['x_nuevo'], marker='o')
        plt.xlabel('x')
        plt.ylabel('x_nuevo')
        plt.title('Método de Newton-Raphson')
        plt.grid(True)
        plt.show()

if __name__ == "__main__":
    print("Usa el archivo main.py, por algo lo creé -_-")