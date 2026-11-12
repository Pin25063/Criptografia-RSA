"""
Proyecto 3 - Criptografia RSA
Curso: Matematica discreta, seccion 20
Autores: Jose Pinto y Valeria Hernandez
Modalidad: Colaborativa
Modulo: rsa_gui.py
Descripcion: Modulo de Interfaz Grafica de Usuario (GUI) construida con Tkinter.
Presenta las pestañas para encriptar y desencriptar, validando las entradas
y conectandose con las funciones del modulo rsa_math.
"""

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

import rsa_math


def crear_interfaz():
    """
    Construye la ventana principal y los elementos graficos de la aplicacion.
    Utiliza widgets basicos de tkinter y ttk.
    """
    ventana = tk.Tk()
    ventana.title("Proyecto 3 - Criptografia RSA | Matematica Discreta")
    ventana.geometry("820x720")
    ventana.minsize(750, 620)

    # Encabezado principal
    frame_encabezado = tk.Frame(ventana, bg="#1E3A8A", pady=10)
    frame_encabezado.pack(fill=tk.X)

    lbl_titulo = tk.Label(
        frame_encabezado,
        text="Criptografia RSA - Matematica Discreta 1",
        font=("Helvetica", 15, "bold"),
        fg="white",
        bg="#1E3A8A"
    )
    lbl_titulo.pack()

    lbl_subtitulo = tk.Label(
        frame_encabezado,
        text="Jose Pinto y Valeria Hernandez | Seccion 20",
        font=("Helvetica", 10),
        fg="#E0E7FF",
        bg="#1E3A8A"
    )
    lbl_subtitulo.pack()

    # Panel de pestañas
    cuaderno = ttk.Notebook(ventana)
    cuaderno.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    pestana_enc = ttk.Frame(cuaderno)
    pestana_des = ttk.Frame(cuaderno)

    cuaderno.add(pestana_enc, text="  🔒 Encriptar Mensaje  ")
    cuaderno.add(pestana_des, text="  🔓 Desencriptar Mensaje  ")

    # ==========================================================================
    # PESTAÑA 1: ENCRIPTAR
    # ==========================================================================
    frame_inputs_enc = ttk.LabelFrame(pestana_enc, text=" Entradas de Encriptacion ", padding=10)
    frame_inputs_enc.pack(fill=tk.X, padx=10, pady=5)
    frame_inputs_enc.columnconfigure(1, weight=1)

    # Mensaje original
    lbl_m = ttk.Label(frame_inputs_enc, text="Mensaje original (M):")
    lbl_m.grid(row=0, column=0, sticky=tk.W, pady=3)
    entry_m = ttk.Entry(frame_inputs_enc, width=50)
    entry_m.grid(row=0, column=1, columnspan=5, sticky=tk.EW, pady=3, padx=5)

    # Parametros RSA
    lbl_p_enc = ttk.Label(frame_inputs_enc, text="Primo p:")
    lbl_p_enc.grid(row=1, column=0, sticky=tk.W, pady=3)
    entry_p_enc = ttk.Entry(frame_inputs_enc, width=10)
    entry_p_enc.grid(row=1, column=1, sticky=tk.W, pady=3, padx=5)

    lbl_q_enc = ttk.Label(frame_inputs_enc, text="Primo q:")
    lbl_q_enc.grid(row=1, column=2, sticky=tk.W, pady=3)
    entry_q_enc = ttk.Entry(frame_inputs_enc, width=10)
    entry_q_enc.grid(row=1, column=3, sticky=tk.W, pady=3, padx=5)

    lbl_e_enc = ttk.Label(frame_inputs_enc, text="Exponente e:")
    lbl_e_enc.grid(row=1, column=4, sticky=tk.W, pady=3)
    entry_e_enc = ttk.Entry(frame_inputs_enc, width=10)
    entry_e_enc.grid(row=1, column=5, sticky=tk.W, pady=3, padx=5)

    # Botones de accion en Encriptar
    frame_botones_enc = ttk.Frame(frame_inputs_enc)
    frame_botones_enc.grid(row=2, column=0, columnspan=6, pady=8, sticky=tk.EW)

    def cargar_ejemplo_enc():
        entry_m.delete(0, tk.END)
        entry_m.insert(0, "RSA")
        entry_p_enc.delete(0, tk.END)
        entry_p_enc.insert(0, "367")
        entry_q_enc.delete(0, tk.END)
        entry_q_enc.insert(0, "373")
        entry_e_enc.delete(0, tk.END)
        entry_e_enc.insert(0, "17")

    def limpiar_enc():
        entry_m.delete(0, tk.END)
        entry_p_enc.delete(0, tk.END)
        entry_q_enc.delete(0, tk.END)
        entry_e_enc.delete(0, tk.END)
        entry_res_c.config(state="normal")
        entry_res_c.delete(0, tk.END)
        entry_res_c.config(state="readonly")
        lbl_res_l_val.config(text="-")
        lbl_res_pub_val.config(text="-")
        txt_resumen_enc.delete("1.0", tk.END)

    btn_accion_enc = tk.Button(
        frame_botones_enc,
        text="🔐 Encriptar",
        bg="#2563EB",
        fg="white",
        font=("Helvetica", 10, "bold"),
        padx=12,
        pady=3
    )
    btn_accion_enc.pack(side=tk.LEFT, padx=5)

    btn_ejemplo_enc = ttk.Button(frame_botones_enc, text="💡 Cargar Ejemplo de Referencia", command=cargar_ejemplo_enc)
    btn_ejemplo_enc.pack(side=tk.LEFT, padx=5)

    btn_limpiar_enc = ttk.Button(frame_botones_enc, text="🧹 Limpiar", command=limpiar_enc)
    btn_limpiar_enc.pack(side=tk.LEFT, padx=5)

    # Resultados principales de Encriptar
    frame_salida_enc = ttk.LabelFrame(pestana_enc, text=" Resultados de Salida ", padding=8)
    frame_salida_enc.pack(fill=tk.X, padx=10, pady=3)
    frame_salida_enc.columnconfigure(1, weight=1)

    lbl_res_c = ttk.Label(frame_salida_enc, text="Cifrado (C):", font=("Helvetica", 9, "bold"))
    lbl_res_c.grid(row=0, column=0, sticky=tk.W)
    entry_res_c = ttk.Entry(frame_salida_enc, width=50, font=("Consolas", 10))
    entry_res_c.grid(row=0, column=1, sticky=tk.EW, padx=5)
    entry_res_c.config(state="readonly")

    lbl_res_l = ttk.Label(frame_salida_enc, text="Longitud (L):", font=("Helvetica", 9, "bold"))
    lbl_res_l.grid(row=0, column=2, sticky=tk.W, padx=5)
    lbl_res_l_val = ttk.Label(frame_salida_enc, text="-", font=("Consolas", 10))
    lbl_res_l_val.grid(row=0, column=3, sticky=tk.W)

    lbl_res_pub = ttk.Label(frame_salida_enc, text="Llave Publica (e, n):", font=("Helvetica", 9, "bold"))
    lbl_res_pub.grid(row=0, column=4, sticky=tk.W, padx=5)
    lbl_res_pub_val = ttk.Label(frame_salida_enc, text="-", font=("Consolas", 10))
    lbl_res_pub_val.grid(row=0, column=5, sticky=tk.W)

    def copiar_a_desencriptar():
        cifrado = entry_res_c.get()
        longitud = lbl_res_l_val.cget("text")
        p = entry_p_enc.get()
        q = entry_q_enc.get()
        e = entry_e_enc.get()

        if not cifrado:
            messagebox.showwarning("Aviso", "Primero debe encriptar un mensaje para copiar los datos.")
            return

        entry_c_des.delete(0, tk.END)
        entry_c_des.insert(0, cifrado)

        entry_l_des.delete(0, tk.END)
        entry_l_des.insert(0, longitud)

        entry_p_des.delete(0, tk.END)
        entry_p_des.insert(0, p)

        entry_q_des.delete(0, tk.END)
        entry_q_des.insert(0, q)

        entry_e_des.delete(0, tk.END)
        entry_e_des.insert(0, e)

        cuaderno.select(pestana_des)

    btn_copiar_des = ttk.Button(frame_salida_enc, text="➡️ Enviar a Desencriptar", command=copiar_a_desencriptar)
    btn_copiar_des.grid(row=1, column=0, columnspan=6, sticky=tk.E, pady=4)

    # Area de texto para detalle y resumen
    frame_detalle_enc = ttk.LabelFrame(pestana_enc, text=" Resumen Detallado del Proceso ", padding=8)
    frame_detalle_enc.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

    scroll_enc = ttk.Scrollbar(frame_detalle_enc)
    scroll_enc.pack(side=tk.RIGHT, fill=tk.Y)

    txt_resumen_enc = tk.Text(frame_detalle_enc, yscrollcommand=scroll_enc.set, font=("Consolas", 9), wrap=tk.WORD)
    txt_resumen_enc.pack(fill=tk.BOTH, expand=True)
    scroll_enc.config(command=txt_resumen_enc.yview)

    # Evento al presionar "Encriptar"
    def al_encriptar():
        mensaje = entry_m.get()
        p_str = entry_p_enc.get()
        q_str = entry_q_enc.get()
        e_str = entry_e_enc.get()

        # Validamos mensaje
        valido_m, error_m = rsa_math.validar_mensaje_original(mensaje)
        if not valido_m:
            messagebox.showerror("Error en Mensaje", error_m)
            return

        # Validamos parametros
        valido_params, error_params, p, q, e, n, phi = rsa_math.validar_parametros_rsa(p_str, q_str, e_str)
        if not valido_params:
            messagebox.showerror("Error en Parametros RSA", error_params)
            return

        # Ejecutamos el algoritmo
        cifrado, L, resumen = rsa_math.ejecutar_encriptacion(mensaje, p, q, e, n, phi)

        # Mostramos en pantalla
        entry_res_c.config(state="normal")
        entry_res_c.delete(0, tk.END)
        entry_res_c.insert(0, cifrado)
        entry_res_c.config(state="readonly")

        lbl_res_l_val.config(text=str(L))
        lbl_res_pub_val.config(text=f"({e}, {n})")

        txt_resumen_enc.delete("1.0", tk.END)
        txt_resumen_enc.insert(tk.END, resumen)
        txt_resumen_enc.see("1.0")

    btn_accion_enc.config(command=al_encriptar)

    # ==========================================================================
    # PESTAÑA 2: DESENCRIPTAR
    # ==========================================================================
    frame_inputs_des = ttk.LabelFrame(pestana_des, text=" Entradas de Desencriptacion ", padding=10)
    frame_inputs_des.pack(fill=tk.X, padx=10, pady=5)
    frame_inputs_des.columnconfigure(1, weight=1)

    # Cifrado C
    lbl_c_des = ttk.Label(frame_inputs_des, text="Cifrado (C):")
    lbl_c_des.grid(row=0, column=0, sticky=tk.W, pady=3)
    entry_c_des = ttk.Entry(frame_inputs_des, width=50)
    entry_c_des.grid(row=0, column=1, columnspan=5, sticky=tk.EW, pady=3, padx=5)

    # Longitud L y parametros
    lbl_l_des = ttk.Label(frame_inputs_des, text="Longitud (L):")
    lbl_l_des.grid(row=1, column=0, sticky=tk.W, pady=3)
    entry_l_des = ttk.Entry(frame_inputs_des, width=8)
    entry_l_des.grid(row=1, column=1, sticky=tk.W, pady=3, padx=5)

    lbl_p_des = ttk.Label(frame_inputs_des, text="Primo p:")
    lbl_p_des.grid(row=1, column=2, sticky=tk.W, pady=3)
    entry_p_des = ttk.Entry(frame_inputs_des, width=8)
    entry_p_des.grid(row=1, column=3, sticky=tk.W, pady=3, padx=5)

    lbl_q_des = ttk.Label(frame_inputs_des, text="Primo q:")
    lbl_q_des.grid(row=1, column=4, sticky=tk.W, pady=3)
    entry_q_des = ttk.Entry(frame_inputs_des, width=8)
    entry_q_des.grid(row=1, column=5, sticky=tk.W, pady=3, padx=5)

    lbl_e_des = ttk.Label(frame_inputs_des, text="Exponente e:")
    lbl_e_des.grid(row=2, column=0, sticky=tk.W, pady=3)
    entry_e_des = ttk.Entry(frame_inputs_des, width=8)
    entry_e_des.grid(row=2, column=1, sticky=tk.W, pady=3, padx=5)

    # Botones de accion en Desencriptar
    frame_botones_des = ttk.Frame(frame_inputs_des)
    frame_botones_des.grid(row=3, column=0, columnspan=6, pady=8, sticky=tk.EW)

    def cargar_ejemplo_des():
        entry_c_des.delete(0, tk.END)
        entry_c_des.insert(0, "026054 123875")
        entry_l_des.delete(0, tk.END)
        entry_l_des.insert(0, "3")
        entry_p_des.delete(0, tk.END)
        entry_p_des.insert(0, "367")
        entry_q_des.delete(0, tk.END)
        entry_q_des.insert(0, "373")
        entry_e_des.delete(0, tk.END)
        entry_e_des.insert(0, "17")

    def limpiar_des():
        entry_c_des.delete(0, tk.END)
        entry_l_des.delete(0, tk.END)
        entry_p_des.delete(0, tk.END)
        entry_q_des.delete(0, tk.END)
        entry_e_des.delete(0, tk.END)
        entry_res_d.config(state="normal")
        entry_res_d.delete(0, tk.END)
        entry_res_d.config(state="readonly")
        entry_res_m.config(state="normal")
        entry_res_m.delete(0, tk.END)
        entry_res_m.config(state="readonly")
        txt_resumen_des.delete("1.0", tk.END)

    btn_accion_des = tk.Button(
        frame_botones_des,
        text="🔓 Desencriptar",
        bg="#059669",
        fg="white",
        font=("Helvetica", 10, "bold"),
        padx=12,
        pady=3
    )
    btn_accion_des.pack(side=tk.LEFT, padx=5)

    btn_ejemplo_des = ttk.Button(frame_botones_des, text="💡 Cargar Ejemplo de Referencia", command=cargar_ejemplo_des)
    btn_ejemplo_des.pack(side=tk.LEFT, padx=5)

    btn_limpiar_des = ttk.Button(frame_botones_des, text="🧹 Limpiar", command=limpiar_des)
    btn_limpiar_des.pack(side=tk.LEFT, padx=5)

    # Resultados de Desencriptar
    frame_salida_des = ttk.LabelFrame(pestana_des, text=" Resultados de Salida ", padding=8)
    frame_salida_des.pack(fill=tk.X, padx=10, pady=3)
    frame_salida_des.columnconfigure(3, weight=1)

    lbl_res_d = ttk.Label(frame_salida_des, text="Exponente Privado (d):", font=("Helvetica", 9, "bold"))
    lbl_res_d.grid(row=0, column=0, sticky=tk.W)
    entry_res_d = ttk.Entry(frame_salida_des, width=15, font=("Consolas", 10))
    entry_res_d.grid(row=0, column=1, sticky=tk.W, padx=5)
    entry_res_d.config(state="readonly")

    lbl_res_m = ttk.Label(frame_salida_des, text="Mensaje Recuperado (M):", font=("Helvetica", 9, "bold"))
    lbl_res_m.grid(row=0, column=2, sticky=tk.W, padx=10)
    entry_res_m = ttk.Entry(frame_salida_des, width=40, font=("Consolas", 10, "bold"))
    entry_res_m.grid(row=0, column=3, sticky=tk.EW, padx=5)
    entry_res_m.config(state="readonly")

    # Area de texto para detalle y resumen
    frame_detalle_des = ttk.LabelFrame(pestana_des, text=" Resumen Detallado del Proceso ", padding=8)
    frame_detalle_des.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

    scroll_des = ttk.Scrollbar(frame_detalle_des)
    scroll_des.pack(side=tk.RIGHT, fill=tk.Y)

    txt_resumen_des = tk.Text(frame_detalle_des, yscrollcommand=scroll_des.set, font=("Consolas", 9), wrap=tk.WORD)
    txt_resumen_des.pack(fill=tk.BOTH, expand=True)
    scroll_des.config(command=txt_resumen_des.yview)

    # Evento al presionar "Desencriptar"
    def al_desencriptar():
        cifrado_str = entry_c_des.get()
        longitud_str = entry_l_des.get()
        p_str = entry_p_des.get()
        q_str = entry_q_des.get()
        e_str = entry_e_des.get()

        # Validamos parametros RSA
        valido_params, error_params, p, q, e, n, phi = rsa_math.validar_parametros_rsa(p_str, q_str, e_str)
        if not valido_params:
            messagebox.showerror("Error en Parametros RSA", error_params)
            return

        # Validamos cifrado C y longitud L
        valido_c, error_c, bloques_c_int, L = rsa_math.validar_cifrado_y_longitud(cifrado_str, longitud_str, n)
        if not valido_c:
            messagebox.showerror("Error en Cifrado o Longitud", error_c)
            return

        # Ejecutamos desencriptacion
        mensaje_rec, d, resumen, error_des = rsa_math.ejecutar_desencriptacion(bloques_c_int, L, p, q, e, n, phi)
        if error_des is not None:
            messagebox.showerror("Error de Desencriptacion", error_des)
            return

        # Mostramos resultados
        entry_res_d.config(state="normal")
        entry_res_d.delete(0, tk.END)
        entry_res_d.insert(0, str(d))
        entry_res_d.config(state="readonly")

        entry_res_m.config(state="normal")
        entry_res_m.delete(0, tk.END)
        entry_res_m.insert(0, mensaje_rec)
        entry_res_m.config(state="readonly")

        txt_resumen_des.delete("1.0", tk.END)
        txt_resumen_des.insert(tk.END, resumen)
        txt_resumen_des.see("1.0")

    btn_accion_des.config(command=al_desencriptar)

    # Iniciar ventana con valores de ejemplo
    cargar_ejemplo_enc()

    return ventana


def iniciar_interfaz():
    """
    Inicializa y ejecuta el bucle principal de la aplicacion grafica.
    """
    app = crear_interfaz()
    app.mainloop()
