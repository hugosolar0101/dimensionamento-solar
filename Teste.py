import sqlite3
import tkinter as tk
from tkinter import ttk
import requests
import os
import sys
from tkinter import messagebox

def caminho_arquivo(nome):
    if getattr(sys, 'frozen', False):
        return os.path.join(os.path.dirname(sys.executable), nome)
    return nome

# conexão
conn = sqlite3.connect(caminho_arquivo("DIM2026.db"))
cursor = conn.cursor()

URL_BANCO = "https://raw.githubusercontent.com/hugosolar0101/dimensionamento-solar/main/DIM2026.db"
URL_VERSAO = "https://raw.githubusercontent.com/hugosolar0101/dimensionamento-solar/main/versao.txt"

# =========================
# 🔥 CARREGAR DADOS NA MEMÓRIA (AQUI!)
# =========================

inversores = {}
modulos = {}
dimensionamento = {}

# carregar inversores
cursor.execute("SELECT id, marca, modelo FROM inversores")
for id_, marca, modelo in cursor.fetchall():
    inversores[(marca, modelo)] = id_

# carregar módulos
cursor.execute("SELECT id, marca, modelo FROM modulos")
for id_, marca, modelo in cursor.fetchall():
    modulos[(marca, modelo)] = id_

# carregar dimensionamento
cursor.execute("SELECT inversor_id, modulo_id, qtd_max FROM dimensionamento")
for inv_id, mod_id, qtd in cursor.fetchall():
    dimensionamento[(inv_id, mod_id)] = qtd


# =========================
# FUNÇÕES
# =========================

def carregar_marcas_inversor():
    marcas = set()
    for (marca, modelo) in inversores.keys():
        marcas.add(marca)
    return sorted(marcas)

def carregar_marcas_modulo():
    marcas = set()
    for (marca, modelo) in modulos.keys():
        marcas.add(marca)
    return sorted(marcas)


def carregar_modelos_inversor(event=None):
    marca = combo_marca_inv.get()

    modelos = [modelo for (m, modelo) in inversores.keys() if m == marca]

    combo_modelo_inv['values'] = modelos
    combo_modelo_inv.set("")
    combo_modelo_inv.config(state="readonly")

    label_resultado.config(text="Selecione os dados")


def carregar_modelos_modulo(event=None):
    marca = combo_marca_mod.get()

    modelos = [modelo for (m, modelo) in modulos.keys() if m == marca]

    combo_modelo_mod['values'] = modelos
    combo_modelo_mod.set("")
    combo_modelo_mod.config(state="readonly")

    label_resultado.config(text="Selecione os dados")


def calcular(event=None):
    marca_inv = combo_marca_inv.get()
    modelo_inv = combo_modelo_inv.get()

    marca_mod = combo_marca_mod.get()
    modelo_mod = combo_modelo_mod.get()

    if not modelo_inv or not modelo_mod:
        label_resultado.config(text="Selecione os dados")
        return

    inv_id = inversores.get((marca_inv, modelo_inv))
    mod_id = modulos.get((marca_mod, modelo_mod))

    resultado = dimensionamento.get((inv_id, mod_id))

    if resultado:
        label_resultado.config(
            text=str(resultado),
            bg="#d4edda",
            fg="#155724"
        )
    else:
        label_resultado.config(
            text="N/A",
            bg="#ffcccc",
            fg="#c0392b"
        )

def limpar():
    combo_marca_inv.set("")
    combo_modelo_inv.set("")
    combo_modelo_inv.config(state="disabled")

    combo_marca_mod.set("")
    combo_modelo_mod.set("")
    combo_modelo_mod.config(state="disabled")

    label_resultado.config(
        text="Selecione os dados",
        bg="#ffffff",
        fg="#7f8c8d"
    )
    
def on_enter(e):
    botao_limpar.config(bg="#c0392b")  # vermelho mais escuro

def on_leave(e):
    botao_limpar.config(bg="#e74c3c")  # vermelho padrão

def obter_versao_local():
    if os.path.exists("versao.txt"):
        with open("versao.txt", "r") as f:
            return f.read().strip()
    return "0.0"

def obter_versao_online():
    try:
        r = requests.get(URL_VERSAO)
        return r.text.strip()
    except:
        return None

def atualizar_banco():
    global conn

    try:
        versao_local = obter_versao_local()
        versao_online = obter_versao_online()

        if not versao_online:
            messagebox.showerror("Erro", "Sem conexão com a internet")
            return

        if versao_online == versao_local:
            messagebox.showinfo("Atualização", "Banco já está atualizado")
            return

        resposta = messagebox.askyesno("Atualização", "Nova versão disponível. Deseja atualizar?")
        if not resposta:
            return

        # 🔥 FECHAR BANCO ANTES DE ATUALIZAR
        conn.close()

        # baixar banco novo
        r = requests.get(URL_BANCO)

        with open("DIM2026.db", "wb") as f:
            f.write(r.content)

        # atualizar versão local
        with open("versao.txt", "w") as f:
            f.write(versao_online)

        messagebox.showinfo("Sucesso", "Banco atualizado! Reinicie o programa.")
        sys.exit()

    except Exception as e:
        messagebox.showerror("Erro", str(e))


# =========================
# INTERFACE PROFISSIONAL
# =========================

janela = tk.Tk()
janela.title("Dimensionamento Fotovoltaico")
janela.geometry("600x500")
janela.configure(bg="#e9ecef")

janela.iconbitmap(caminho_arquivo("icone.ico"))

fonte_label = ("Segoe UI", 10)
fonte_titulo = ("Segoe UI", 14, "bold")
fonte_resultado = ("Segoe UI", 11, "bold")

# =========================
# CARD CENTRAL
# =========================

card = tk.Frame(janela, bg="white", bd=1, relief="solid")
card.place(relx=0.5, rely=0.5, anchor="center", width=450, height=480)

# =========================
# TÍTULO
# =========================

tk.Label(
    card,
    text="Dimensionamento Fotovoltaico",
    font=fonte_titulo,
    bg="white",
    fg="#2c3e50"
).pack(pady=(15, 20))

# =========================
# CONTEÚDO
# =========================

conteudo = tk.Frame(card, bg="white")
conteudo.pack()

# Marca inversor
tk.Label(conteudo, text="Marca do Inversor", font=fonte_label, bg="white").grid(row=0, column=0, sticky="w")
combo_marca_inv = ttk.Combobox(conteudo, state="readonly", width=30)
combo_marca_inv['values'] = carregar_marcas_inversor()
combo_marca_inv.grid(row=1, column=0, pady=5)

# Modelo inversor
tk.Label(conteudo, text="Modelo do Inversor", font=fonte_label, bg="white").grid(row=2, column=0, sticky="w", pady=(10,0))
combo_modelo_inv = ttk.Combobox(conteudo, state="disabled", width=30)
combo_modelo_inv.grid(row=3, column=0, pady=5)

# Marca módulo
tk.Label(conteudo, text="Marca da Placa", font=fonte_label, bg="white").grid(row=4, column=0, sticky="w", pady=(10,0))
combo_marca_mod = ttk.Combobox(conteudo, state="readonly", width=30)
combo_marca_mod['values'] = carregar_marcas_modulo()
combo_marca_mod.grid(row=5, column=0, pady=5)

# Modelo módulo
tk.Label(conteudo, text="Modelo da Placa", font=fonte_label, bg="white").grid(row=6, column=0, sticky="w", pady=(10,0))
combo_modelo_mod = ttk.Combobox(conteudo, state="disabled", width=30)
combo_modelo_mod.grid(row=7, column=0, pady=5)

# =========================
# RESULTADO
# =========================

frame_resultado = tk.Frame(card, bg="white")
frame_resultado.pack(pady=25)

tk.Label(frame_resultado, text="Resultado:", font=fonte_label, bg="white").pack()

label_resultado = tk.Label(
    frame_resultado,
    text="Selecione os dados",
    width=20,
    font=fonte_resultado,
    bg="#ffffff",
    fg="#7f8c8d",
    relief="solid",
    bd=1,
    pady=5
)
label_resultado.pack(pady=5)

# =========================
# BOTÃO LIMPAR
# =========================

botao_limpar = tk.Button(
    card,
    text="Limpar",
    command=limpar,
    bg="#e74c3c",
    fg="white",
    font=("Segoe UI", 10, "bold"),
    relief="flat",
    padx=10,
    pady=5
)
botao_limpar.pack(pady=10)

botao_limpar.bind("<Enter>", on_enter)
botao_limpar.bind("<Leave>", on_leave)
botao_limpar.config(cursor="hand2")

# =========================
# BOTÃO ATUALIZAR
# =========================

botao_atualizar = tk.Button(
    card,
    text="Atualizar Banco",
    command=atualizar_banco,
    bg="#3498db",
    fg="white",
    font=("Segoe UI", 10, "bold"),
    relief="flat",
    padx=10,
    pady=5
)
botao_atualizar.pack(pady=5)

# =========================
# EVENTOS
# =========================

combo_marca_inv.bind("<<ComboboxSelected>>", carregar_modelos_inversor)
combo_marca_mod.bind("<<ComboboxSelected>>", carregar_modelos_modulo)

combo_modelo_inv.bind("<<ComboboxSelected>>", calcular)
combo_modelo_mod.bind("<<ComboboxSelected>>", calcular)


# iniciar
janela.mainloop()

conn.close()