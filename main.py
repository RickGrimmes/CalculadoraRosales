import tkinter as tk
from euler_mejorado import EulerMejorado
from runge_kutta import RungeKutta
from newton_raphson import NewtonRaphson

class MenuPrincipal:
    def __init__(self, root):
        self.root = root
        self.root.title("Métodos Numéricos")
        self.root.geometry("400x300")
        self.root.configure(bg="#f0f0f0")

        tk.Button(self.root, text="Euler Mejorado", command=self.abrir_euler_mejorado, bg="#007bff", fg="white", font=("Arial", 12, "bold"), padx=10, pady=10).pack(pady=10)
        tk.Button(self.root, text="Runge-Kutta", command=self.abrir_runge_kutta, bg="#ff6666", fg="white", font=("Arial", 12, "bold"), padx=10, pady=10).pack(pady=10)
        tk.Button(self.root, text="Newton-Raphson", command=self.abrir_newton_raphson, bg="#ffcc00", fg="white", font=("Arial", 12, "bold"), padx=10, pady=10).pack(pady=10)
        tk.Button(self.root, text="Cerrar todo", command=self.root.quit, bg="#000000", fg="white", font=("Arial", 12, "bold"), padx=10, pady=10).pack(pady=10)

    def abrir_euler_mejorado(self):
        nueva_ventana = tk.Toplevel(self.root)
        EulerMejorado(nueva_ventana)

    def abrir_runge_kutta(self):
        nueva_ventana = tk.Toplevel(self.root)
        RungeKutta(nueva_ventana)

    def abrir_newton_raphson(self):
        nueva_ventana = tk.Toplevel(self.root)
        NewtonRaphson(nueva_ventana)

if __name__ == "__main__":
    root = tk.Tk()
    app = MenuPrincipal(root)
    root.mainloop()