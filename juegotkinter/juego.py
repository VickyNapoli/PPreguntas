import sqlite3
import tkinter as tk
from tkinter import messagebox

class JuegoPreguntas:
    def __init__(self, root):
        self.root = root
        self.root.title("Juego de Preguntas y Respuestas")

        self.conn = sqlite3.connect("preguntas.db")
        self.c = self.conn.cursor()

        self.c.execute(
            """
            CREATE TABLE IF NOT EXISTS preguntas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pregunta TEXT,
                respuesta_correcta TEXT,
                respuesta_incorrecta1 TEXT,
                respuesta_incorrecta2 TEXT,
                respuesta_incorrecta3 TEXT
            )
            """
        )

        self.c.execute("SELECT COUNT(*) FROM preguntas")
        if self.c.fetchone()[0] == 0:
            self.insertar_preguntas_por_defecto()

        self.mostrar_pregunta()

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

    def insertar_preguntas_por_defecto(self):
        preguntas_por_defecto = [
            ("¿Cuál es la capital de Francia?", "París", "Londres", "Berlín", "Madrid"),
            ("¿En qué año se independizó Estados Unidos?", "1776", "1789", "1804", "1820"),
            ("¿Cuál es el río más largo del mundo?", "Amazonas", "Nilo", "Misisipi", "Yangtsé")
        ]

        for pregunta in preguntas_por_defecto:
            self.c.execute(
                """
                INSERT INTO preguntas (pregunta, respuesta_correcta, respuesta_incorrecta1, respuesta_incorrecta2, respuesta_incorrecta3)
                VALUES (?, ?, ?, ?, ?)
                """,
                pregunta
            )

        self.conn.commit()

    def mostrar_pregunta(self):
        self.c.execute("SELECT * FROM preguntas ORDER BY RANDOM() LIMIT 1")
        pregunta = self.c.fetchone()

        if pregunta:
            ventana_juego = tk.Toplevel(self.root)
            juego = Juego(self.conn, ventana_juego, pregunta, self.mostrar_pregunta)
        else:
            messagebox.showerror("Error", "No hay preguntas en la base de datos. Agrega preguntas para jugar.")

class Juego:
    def __init__(self, conn, root, pregunta, mostrar_pregunta):
        self.conn = conn
        self.root = root
        self.pregunta = pregunta
        self.mostrar_pregunta = mostrar_pregunta

        self.root.title("Juego: Pregunta y Respuestas")

        self.label_pregunta = tk.Label(root, text=pregunta[1])
        self.label_pregunta.pack(pady=10)

        respuestas = [pregunta[i] for i in range(2, 6)]
        respuestas_correctas = [pregunta[2]]

        self.boton_respuestas = []
        for i, respuesta in enumerate(respuestas):
            boton_respuesta = tk.Button(root, text=respuesta, command=lambda r=respuesta: self.verificar_respuesta(r))
            boton_respuesta.pack(pady=5)
            self.boton_respuestas.append(boton_respuesta)

    def verificar_respuesta(self, respuesta_usuario):
        respuesta_correcta = self.pregunta[2]
        if respuesta_usuario == respuesta_correcta:
            messagebox.showinfo("Correcto", "¡Respuesta correcta!")
        else:
            messagebox.showerror("Incorrecto", f"Respuesta incorrecta. La respuesta correcta es: {respuesta_correcta}")

        self.root.destroy()

        self.mostrar_pregunta()

if __name__ == "__main__":
    root = tk.Tk()
    juego_preguntas = JuegoPreguntas(root)
    root.mainloop()
