import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Constante gravitacional estándar
G = 9.81
PALETA_COLORES = ["#1f77b4", "#d62728", "#2ca02c", "#9467bd", "#ff7f0e"]


class SimuladorTrayectoriasApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador Bidimensional de Trayectorias Parabólicas - UJGH")
        self.root.geometry("980x680")
        self.root.minsize(880, 620)

        self.contador_curvas = 0
        self.configurar_estilos()
        self.construir_interfaz()
        self.inicializar_grafica()

    def configurar_estilos(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure("Titulo.TLabel", font=("Arial", 13, "bold"), foreground="#1a365d")
        style.configure("Subtitulo.TLabel", font=("Arial", 10, "bold"), foreground="#2d3748")
        style.configure("Resultado.TLabel", font=("Consolas", 10), foreground="#1a202c")
        style.configure("Accion.TButton", font=("Arial", 10, "bold"))

    def construir_interfaz(self):
        # Encabezado
        frame_header = ttk.Frame(self.root, padding=(15, 10, 15, 5))
        frame_header.pack(fill="x")
        ttk.Label(
            frame_header,
            text="SIMULADOR BIDIMENSIONAL DE TRAYECTORIAS PARABÓLICAS (R²)",
            style="Titulo.TLabel",
        ).pack(anchor="w")
        ttk.Label(
            frame_header,
            text="Facultad de Ingeniería - Escuela de Ingeniería en Sistemas | UJGH (VI TECNOFINGNOVA 2026)",
            font=("Arial", 9),
            foreground="#4a5568",
        ).pack(anchor="w")

        # Contenedor principal dividido en panel izquierdo (controles) y derecho (gráfica)
        frame_main = ttk.Frame(self.root, padding=10)
        frame_main.pack(fill="both", expand=True)

        # Panel Izquierdo
        panel_izq = ttk.Frame(frame_main, width=300)
        panel_izq.pack(side="left", fill="y", padx=(5, 10))
        panel_izq.pack_propagate(False)

        # Sección: Parámetros de Entrada
        lf_inputs = ttk.LabelFrame(panel_izq, text=" Parámetros de Entrada ", padding=10)
        lf_inputs.pack(fill="x", pady=(0, 10))

        ttk.Label(lf_inputs, text="Velocidad Inicial v₀ (m/s):").pack(anchor="w")
        self.entry_vel = ttk.Entry(lf_inputs)
        self.entry_vel.insert(0, "30")
        self.entry_vel.pack(fill="x", pady=(2, 8))

        ttk.Label(lf_inputs, text="Ángulo de Tiro θ (grados, 1° - 89°):").pack(anchor="w")
        self.entry_ang = ttk.Entry(lf_inputs)
        self.entry_ang.insert(0, "45")
        self.entry_ang.pack(fill="x", pady=(2, 8))

        self.var_comparar = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            lf_inputs,
            text="Mantener trayectorias anteriores",
            variable=self.var_comparar,
        ).pack(anchor="w", pady=(2, 10))

        ttk.Button(
            lf_inputs,
            text="Simular Trayectoria",
            style="Accion.TButton",
            command=self.calcular_y_graficar,
        ).pack(fill="x", pady=3)

        ttk.Button(
            lf_inputs,
            text="Limpiar Gráfica",
            command=self.limpiar_grafica,
        ).pack(fill="x", pady=3)

        ttk.Button(
            lf_inputs,
            text="Exportar Gráfica (PNG)",
            command=self.exportar_grafica,
        ).pack(fill="x", pady=3)

        # Sección: Métricas Calculadas
        lf_resultados = ttk.LabelFrame(panel_izq, text=" Métricas Vectoriales y Cinemáticas ", padding=10)
        lf_resultados.pack(fill="both", expand=True)

        self.lbl_resultados = ttk.Label(
            lf_resultados,
            text="Ingrese los parámetros y presione\n'Simular Trayectoria'.",
            style="Resultado.TLabel",
            justify="left",
        )
        self.lbl_resultados.pack(anchor="nw", fill="x")

        # Panel Derecho: Gráfica Matplotlib
        panel_der = ttk.LabelFrame(frame_main, text=" Visualización en Plano Cartesiano ", padding=5)
        panel_der.pack(side="right", fill="both", expand=True)

        self.fig, self.ax = plt.subplots(figsize=(6.5, 5), dpi=100)
        self.fig.patch.set_facecolor("#ffffff")
        self.canvas = FigureCanvasTkAgg(self.fig, master=panel_der)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def inicializar_grafica(self):
        self.ax.clear()
        self.ax.axhline(0, color="#2d3748", linewidth=1.2)
        self.ax.axvline(0, color="#2d3748", linewidth=1.2)
        self.ax.set_title("Trayectoria Parabólica en R² (Modelo Ideal, g = 9.81 m/s²)", fontsize=11, fontweight="bold")
        self.ax.set_xlabel("Distancia horizontal x (m)", fontsize=10)
        self.ax.set_ylabel("Altura y (m)", fontsize=10)
        self.ax.grid(True, linestyle="--", alpha=0.6)
        self.fig.tight_layout()
        self.canvas.draw()

    def limpiar_grafica(self):
        self.contador_curvas = 0
        self.inicializar_grafica()
        self.lbl_resultados.config(text="Gráfica reiniciada.\nListo para nueva simulación.")

    def calcular_y_graficar(self):
        try:
            v0 = float(self.entry_vel.get().strip())
            theta_grados = float(self.entry_ang.get().strip())
        except ValueError:
            messagebox.showerror("Error de entrada", "Ingrese valores numéricos válidos para velocidad y ángulo.")
            return

        # Validación de dominio físico
        if v0 <= 0:
            messagebox.showwarning("Valor fuera de rango", "La velocidad inicial (v₀) debe ser mayor que 0 m/s.")
            return
        if not (0 < theta_grados < 90):
            messagebox.showwarning("Valor fuera de rango", "El ángulo de tiro (θ) debe estar entre 0° y 90° (exclusivo).")
            return

        # Álgebra Vectorial: Descomposición en R²
        theta_rad = np.radians(theta_grados)
        v0x = v0 * np.cos(theta_rad)
        v0y = v0 * np.sin(theta_rad)

        # Cinemática: Fórmulas analíticas
        t_hmax = v0y / G
        t_vuelo = (2 * v0y) / G
        h_max = (v0y ** 2) / (2 * G)
        x_hmax = v0x * t_hmax
        alcance = (v0 ** 2 * np.sin(2 * theta_rad)) / G

        # Muestreo discreto de la trayectoria
        t = np.linspace(0, t_vuelo, num=300)
        x = v0x * t
        y = v0y * t - 0.5 * G * (t ** 2)

        # Actualizar panel de métricas
        resumen = (
            f"Entrada:\n"
            f"  v₀ = {v0:.2f} m/s | θ = {theta_grados:.2f}°\n"
            f"{'-' * 30}\n"
            f"Componentes Vectoriales:\n"
            f"  v₀x = {v0x:.2f} m/s\n"
            f"  v₀y = {v0y:.2f} m/s\n"
            f"{'-' * 30}\n"
            f"Métricas de Vuelo:\n"
            f"  t(h_max)  = {t_hmax:.2f} s\n"
            f"  t_vuelo   = {t_vuelo:.2f} s\n"
            f"  h_max     = {h_max:.2f} m\n"
            f"  x_max     = {alcance:.2f} m\n"
            f"{'-' * 30}\n"
            f"Coordenadas Clave:\n"
            f"  Vértice: ({x_hmax:.2f}, {h_max:.2f}) m\n"
            f"  Impacto: ({alcance:.2f}, 0.00) m"
        )
        self.lbl_resultados.config(text=resumen)

        # Renderizado
        if not self.var_comparar.get():
            self.contador_curvas = 0
            self.ax.clear()
            self.ax.axhline(0, color="#2d3748", linewidth=1.2)
            self.ax.axvline(0, color="#2d3748", linewidth=1.2)

        color = PALETA_COLORES[self.contador_curvas % len(PALETA_COLORES)]
        etiqueta = f"v₀={v0:.1f} m/s, θ={theta_grados:.1f}°"

        self.ax.plot(x, y, color=color, linewidth=2.2, label=etiqueta)

        # Marcadores de vértice (h_max) e impacto (x_max)
        self.ax.scatter([x_hmax], [h_max], color=color, zorder=5, s=40)
        self.ax.annotate(
            f"h_max: {h_max:.1f}m",
            xy=(x_hmax, h_max),
            xytext=(0, 8),
            textcoords="offset points",
            ha="center",
            fontsize=8,
            color=color,
            fontweight="bold",
        )
        self.ax.scatter([alcance], [0], color=color, marker="x", zorder=5, s=50)

        # Vector velocidad inicial (solo en modo individual para evitar saturación visual)
        if not self.var_comparar.get():
            escala_vector = max(alcance, h_max) * 0.25 / v0
            self.ax.quiver(
                0, 0, v0x * escala_vector, v0y * escala_vector,
                angles="xy", scale_units="xy", scale=1,
                color="#e53e3e", width=0.006, label=r"Vector $\vec{v}_0$ (escala visual)"
            )

        self.contador_curvas += 1
        self.ax.set_title("Trayectoria Parabólica en R² (Modelo Ideal, g = 9.81 m/s²)", fontsize=11, fontweight="bold")
        self.ax.set_xlabel("Distancia horizontal x (m)", fontsize=10)
        self.ax.set_ylabel("Altura y (m)", fontsize=10)
        self.ax.set_xlim(left=-max(alcance * 0.05, 1))
        self.ax.set_ylim(bottom=-max(h_max * 0.05, 1))
        self.ax.grid(True, linestyle="--", alpha=0.6)
        self.ax.legend(loc="upper right", fontsize=8.5, framealpha=0.9)
        self.fig.tight_layout()
        self.canvas.draw()

    def exportar_grafica(self):
        ruta = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("Imagen PNG", "*.png"), ("Imagen PDF", "*.pdf")],
            title="Guardar gráfica del simulador",
        )
        if ruta:
            self.fig.savefig(ruta, dpi=300, bbox_inches="tight")
            messagebox.showinfo("Exportación exitosa", f"Gráfica guardada en:\n{ruta}")


if __name__ == "__main__":
    root = tk.Tk()
    app = SimuladorTrayectoriasApp(root)
    root.mainloop()