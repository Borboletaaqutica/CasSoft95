import tkinter as tk
from tkinter import messagebox
import json
import os
import sys
import random
import time
import turtle
from datetime import datetime

# VARIÁVEIS GLOBAIS
macetadas = 0
macetadas_por_clique = 1
auto_macetadores = 0
poder_auto_macetador = 1
preco_upgrade = 20
preco_auto = 50
preco_turbo_auto = 100

conquistas = {
    "primeiro_click": False,
    "dez_macetadas": False,
    "cinquenta_macetadas": False,
    "primeiro_auto": False
}

SAVE_FILE = "save.json"
modo_escuro_ativo = False

# SPLASH SCREEN
def splash_screen():
    splash = tk.Tk()
    splash.title("Iniciando Sistema")
    splash.geometry("400x300")  # Tamanho fixo da splash screen
    splash.configure(bg="#000000")
    splash.overrideredirect(1)  # Remove os botões de controle da janela
    splash.eval('tk::PlaceWindow . center')  # Centraliza a janela na tela

    titulo = tk.Label(
        splash,
        text="Iniciando Sistema",
        bg="#000000",
        fg="#FFFFFF",
        font=("MS Sans Serif", 20, "bold")
    )
    titulo.pack(pady=50)

    subtitulo = tk.Label(
        splash,
        text="Feito por um adolescente solitário",
        bg="#000000",
        fg="#AAAAAA",
        font=("MS Sans Serif", 12, "italic")
    )
    subtitulo.pack()

    # Fecha a splash screen após 3 segundos
    splash.after(3000, splash.destroy)
    splash.mainloop()

# SALVAMENTO E CARREGAMENTO
def salvar_jogo():
    dados = {
        "macetadas": macetadas,
        "macetadas_por_clique": macetadas_por_clique,
        "auto_macetadores": auto_macetadores,
        "poder_auto_macetador": poder_auto_macetador,
        "preco_upgrade": preco_upgrade,
        "preco_auto": preco_auto,
        "preco_turbo_auto": preco_turbo_auto,
        "conquistas": conquistas
    }
    with open(SAVE_FILE, "w") as f:
        json.dump(dados, f)

def carregar_jogo():
    global macetadas, macetadas_por_clique, auto_macetadores, poder_auto_macetador
    global preco_upgrade, preco_auto, preco_turbo_auto, conquistas

    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            dados = json.load(f)
            macetadas = dados.get("macetadas", 0)
            macetadas_por_clique = dados.get("macetadas_por_clique", 1)
            auto_macetadores = dados.get("auto_macetadores", 0)
            poder_auto_macetador = dados.get("poder_auto_macetador", 1)
            preco_upgrade = dados.get("preco_upgrade", 20)
            preco_auto = dados.get("preco_auto", 50)
            preco_turbo_auto = dados.get("preco_turbo_auto", 100)
            conquistas.update(dados.get("conquistas", {}))

# Função de notificação
def mostrar_notificacao(texto):
    notificacao_label.config(text=texto)
    notificacao_label.place(relx=0.5, rely=0.95, anchor="s")
    janela.after(3000, lambda: notificacao_label.place_forget())

# Atualização de UI
def atualizar_labels():
    contador_label.config(text=f"Macetadas computadas: {macetadas}")
    upgrade_label.config(text=f"Upgrade de Clique ({preco_upgrade} macetadas)")
    auto_label.config(text=f"AutoMacetador ({preco_auto} macetadas)")
    turbo_label.config(text=f"Turbo AutoMacetador ({preco_turbo_auto} macetadas)")
    auto_status.config(text=f"{auto_macetadores} ativos | Força: {poder_auto_macetador}/s")

# Conquistas
def checar_conquistas():
    if macetadas >= 1 and not conquistas["primeiro_click"]:
        conquistas["primeiro_click"] = True
        mostrar_notificacao("🏆 Primeira macetada realizada!")
    if macetadas >= 10 and not conquistas["dez_macetadas"]:
        conquistas["dez_macetadas"] = True
        mostrar_notificacao("🏆 10 macetadas atingidas!")
    if macetadas >= 50 and not conquistas["cinquenta_macetadas"]:
        conquistas["cinquenta_macetadas"] = True
        mostrar_notificacao("🏆 50 macetadas! Tá on fire!")
    if auto_macetadores >= 1 and not conquistas["primeiro_auto"]:
        conquistas["primeiro_auto"] = True
        mostrar_notificacao("🏆 Comprou seu primeiro AutoMacetador!")

# Funções principais
def funcao():
    global macetadas
    macetadas += macetadas_por_clique
    greeting.config(text="🛠️ Macetou!")
    atualizar_labels()
    checar_conquistas()

def comprar_upgrade():
    global macetadas, macetadas_por_clique, preco_upgrade
    if macetadas >= preco_upgrade:
        macetadas -= preco_upgrade
        macetadas_por_clique += 1
        preco_upgrade = int(preco_upgrade * 1.5)
        atualizar_labels()

def comprar_auto_macetador():
    global macetadas, auto_macetadores, preco_auto
    if macetadas >= preco_auto:
        macetadas -= preco_auto
        auto_macetadores += 1
        preco_auto = int(preco_auto * 1.5)
        atualizar_labels()
        checar_conquistas()

def comprar_turbo_auto():
    global macetadas, poder_auto_macetador, preco_turbo_auto
    if macetadas >= preco_turbo_auto:
        macetadas -= preco_turbo_auto
        poder_auto_macetador += 1
        preco_turbo_auto = int(preco_turbo_auto * 1.7)
        atualizar_labels()

def gerar_macetadas_auto():
    global macetadas
    macetadas += auto_macetadores * poder_auto_macetador
    atualizar_labels()
    checar_conquistas()
    janela.after(1000, gerar_macetadas_auto)

def loop_salvar_auto():
    salvar_jogo()
    janela.after(5000, loop_salvar_auto)

# Função para atualizar o relógio no menu principal
def atualizar_relogio():
    hora_atual = datetime.now().strftime("%H:%M:%S")
    relogio_label.config(text=f"🕒 {hora_atual}")
    tela_boas_vindas.after(1000, atualizar_relogio)

# Função para ativar o modo escuro
def ativar_modo_escuro():
    # Modo escuro para o menu principal
    tela_boas_vindas.configure(bg="#1E1E1E")
    titulo_boas_vindas.configure(bg="#1E1E1E", fg="#FFFFFF")
    descricao.configure(bg="#1E1E1E", fg="#FFFFFF")
    botao_jogar.configure(bg="#333333", fg="#FFFFFF")
    botao_cobrinha.configure(bg="#333333", fg="#FFFFFF")
    botao_modo_escuro.configure(bg="#333333", fg="#FFFFFF")
    mais_coisas_label.configure(bg="#1E1E1E", fg="#FFFFFF")
    relogio_label.configure(bg="#1E1E1E", fg="#FFFFFF")

    # Modo escuro para o Macetador
    global modo_escuro_ativo
    modo_escuro_ativo = True

# Função para iniciar o jogo principal
def iniciar_jogo():
    tela_boas_vindas.destroy()  # Fecha a tela de boas-vindas
    iniciar_macetador()  # Inicia o jogo principal

# Função para iniciar o jogo da cobrinha
def iniciar_cobrinha():
    tela_boas_vindas.destroy()  # Fecha a tela de boas-vindas

    # Configuração da tela
    janela_cobrinha = turtle.Screen()
    janela_cobrinha.title("CassSoft 95™ - Jogo da Cobrinha")
    janela_cobrinha.bgcolor("black")  # Fundo fixo preto, independente do modo escuro
    janela_cobrinha.setup(width=800, height=600)  # Tamanho fixo da janela
    janela_cobrinha.tracer(0)

    # Cabeça da cobrinha
    cabeca = turtle.Turtle()
    cabeca.speed(0)
    cabeca.shape("square")
    cabeca.color("green")
    cabeca.penup()
    cabeca.goto(0, 0)
    cabeca.direction = "stop"

    # Comida
    comida = turtle.Turtle()
    comida.speed(0)
    comida.shape("circle")
    comida.color("red")
    comida.penup()
    comida.goto(0, 100)

    # Segmentos do corpo
    segmentos = []

    # Mensagem no canto superior
    mensagem = turtle.Turtle()
    mensagem.hideturtle()
    mensagem.penup()
    mensagem.color("white")
    mensagem.goto(0, 260)
    mensagem.write("Aperte M pra voltar ao menu", align="center", font=("Arial", 14, "bold"))

    # Movimento da cobrinha
    def mover():
        if cabeca.direction == "up":
            y = cabeca.ycor()
            cabeca.sety(y + 20)
        if cabeca.direction == "down":
            y = cabeca.ycor()
            cabeca.sety(y - 20)
        if cabeca.direction == "left":
            x = cabeca.xcor()
            cabeca.setx(x - 20)
        if cabeca.direction == "right":
            x = cabeca.xcor()
            cabeca.setx(x + 20)

        # Teletransporte ao atingir as bordas
        if cabeca.xcor() > 390:  # Saiu pela borda direita
            cabeca.setx(-390)
        if cabeca.xcor() < -390:  # Saiu pela borda esquerda
            cabeca.setx(390)
        if cabeca.ycor() > 290:  # Saiu pela borda superior
            cabeca.sety(-290)
        if cabeca.ycor() < -290:  # Saiu pela borda inferior
            cabeca.sety(290)

    # Controle da cobrinha
    def ir_para_cima():
        if cabeca.direction != "down":
            cabeca.direction = "up"

    def ir_para_baixo():
        if cabeca.direction != "up":
            cabeca.direction = "down"

    def ir_para_esquerda():
        if cabeca.direction != "right":
            cabeca.direction = "left"

    def ir_para_direita():
        if cabeca.direction != "left":
            cabeca.direction = "right"

    # Voltar ao menu principal
    def voltar_ao_menu():
        janela_cobrinha.bye()
        iniciar_tela_boas_vindas()

    # Teclas de controle
    janela_cobrinha.listen()
    janela_cobrinha.onkeypress(ir_para_cima, "Up")
    janela_cobrinha.onkeypress(ir_para_baixo, "Down")
    janela_cobrinha.onkeypress(ir_para_esquerda, "Left")
    janela_cobrinha.onkeypress(ir_para_direita, "Right")
    janela_cobrinha.onkeypress(voltar_ao_menu, "m")

    # Loop principal do jogo
    while True:
        janela_cobrinha.update()

        # Verificar colisão com a comida
        if cabeca.distance(comida) < 20:
            # Mover a comida para uma nova posição
            x = random.randint(-390, 390)
            y = random.randint(-290, 290)
            comida.goto(x, y)

            # Adicionar um novo segmento ao corpo
            novo_segmento = turtle.Turtle()
            novo_segmento.speed(0)
            novo_segmento.shape("square")
            novo_segmento.color("green")
            novo_segmento.penup()
            segmentos.append(novo_segmento)

        # Mover os segmentos do corpo
        for index in range(len(segmentos) - 1, 0, -1):
            x = segmentos[index - 1].xcor()
            y = segmentos[index - 1].ycor()
            segmentos[index].goto(x, y)

        # Mover o primeiro segmento para onde está a cabeça
        if len(segmentos) > 0:
            x = cabeca.xcor()
            y = cabeca.ycor()
            segmentos[0].goto(x, y)

        mover()

        # Verificar colisão com o próprio corpo
        for segmento in segmentos:
            if segmento.distance(cabeca) < 20:
                cabeca.goto(0, 0)
                cabeca.direction = "stop"

                # Esconder os segmentos do corpo
                for segmento in segmentos:
                    segmento.goto(1000, 1000)
                segmentos.clear()

        time.sleep(0.1)

# Função para a tela principal do jogo
def iniciar_macetador():
    global janela, notificacao_label, contador_label, upgrade_label, auto_label, turbo_label, auto_status, greeting

    # App principal
    janela = tk.Tk()
    janela.title("CassSoft 95™ - Macetador")
    janela.geometry("1024x768")  # Tamanho fixo da janela
    janela.configure(bg="#1E1E1E" if modo_escuro_ativo else "#C0C0C0")

    # Mensagem no canto superior
    mensagem_voltar = tk.Label(
        janela,
        text="M pra voltar ao menu",
        bg="#1E1E1E" if modo_escuro_ativo else "#C0C0C0",
        fg="white" if modo_escuro_ativo else "black",
        font=("MS Sans Serif", 12, "italic")
    )
    mensagem_voltar.pack(anchor="ne", padx=10, pady=10)

    # Função para voltar ao menu principal
    def voltar_ao_menu():
        janela.destroy()
        iniciar_tela_boas_vindas()

    # Atalho para voltar ao menu
    janela.bind("m", lambda event: voltar_ao_menu())

    # INTERFACE
    frame_top = tk.Frame(janela, bg="#000080")
    titulo = tk.Label(frame_top, text="CassSoft 95™ - MACETADOR", bg="#000080", fg="white", pady=10, font=("MS Sans Serif", 18, "bold"))
    titulo.pack(padx=20, pady=20)
    frame_top.pack(fill="x")

    greeting = tk.Label(janela, text="👋 Oi macetador", bg="#1E1E1E" if modo_escuro_ativo else "#C0C0C0", fg="white" if modo_escuro_ativo else "black", relief="sunken", bd=2, padx=20, pady=10, font=("MS Sans Serif", 14))
    greeting.pack(pady=20)

    botao = tk.Button(janela, text="💥 Macetar", command=funcao, width=25, height=3, bg="#333333" if modo_escuro_ativo else "#F0F0F0", fg="white" if modo_escuro_ativo else "black", relief="raised", bd=4, font=("MS Sans Serif", 14))
    botao.pack(pady=20)

    contador_label = tk.Label(janela, text="Macetadas computadas: 0", bg="#1E1E1E" if modo_escuro_ativo else "#C0C0C0", fg="white" if modo_escuro_ativo else "black", relief="sunken", bd=2, padx=20, pady=10, font=("MS Sans Serif", 14))
    contador_label.pack(pady=20)

    upgrade_button = tk.Button(janela, text="⬆️ Upgrade de Clique", command=comprar_upgrade, bg="#333333" if modo_escuro_ativo else "#D0D0D0", relief="raised", bd=3, font=("MS Sans Serif", 14))
    upgrade_button.pack(pady=10)
    upgrade_label = tk.Label(janela, text="", bg="#1E1E1E" if modo_escuro_ativo else "#C0C0C0", font=("MS Sans Serif", 14))
    upgrade_label.pack()

    auto_button = tk.Button(janela, text="🤖 Comprar AutoMacetador", command=comprar_auto_macetador, bg="#333333" if modo_escuro_ativo else "#D0D0D0", relief="raised", bd=3, font=("MS Sans Serif", 14))
    auto_button.pack(pady=10)
    auto_label = tk.Label(janela, text="", bg="#1E1E1E" if modo_escuro_ativo else "#C0C0C0", font=("MS Sans Serif", 14))
    auto_label.pack()
    auto_status = tk.Label(janela, text="", bg="#1E1E1E" if modo_escuro_ativo else "#C0C0C0", font=("MS Sans Serif", 14))
    auto_status.pack()

    turbo_button = tk.Button(janela, text="⚡ Turbo AutoMacetador", command=comprar_turbo_auto, bg="#333333" if modo_escuro_ativo else "#D0D0D0", relief="raised", bd=3, font=("MS Sans Serif", 14))
    turbo_button.pack(pady=10)
    turbo_label = tk.Label(janela, text="", bg="#1E1E1E" if modo_escuro_ativo else "#C0C0C0", font=("MS Sans Serif", 14))
    turbo_label.pack()

    notificacao_label = tk.Label(janela, text="", bg="#FFFF99", fg="black", font=("MS Sans Serif", 12), relief="solid", bd=1, padx=10, pady=5)

    # CARREGAR JOGO, INICIAR LOOPS
    carregar_jogo()
    atualizar_labels()
    janela.after(1000, gerar_macetadas_auto)
    janela.after(5000, loop_salvar_auto)

    janela.mainloop()

# Função para iniciar a tela de boas-vindas
def iniciar_tela_boas_vindas():
    global tela_boas_vindas, titulo_boas_vindas, descricao, botao_jogar, botao_cobrinha, botao_modo_escuro, mais_coisas_label, relogio_label
    tela_boas_vindas = tk.Tk()
    tela_boas_vindas.title("CassSoft 95™ - Bem-vindo")
    tela_boas_vindas.geometry("1024x768")  # Tamanho fixo da janela
    tela_boas_vindas.configure(bg="#C0C0C0")

    titulo_boas_vindas = tk.Label(
        tela_boas_vindas,
        text="Bem-vindo ao CassSoft 95™ - Macetador!",
        bg="#C0C0C0",
        fg="black",
        font=("MS Sans Serif", 20, "bold"),
        pady=40
    )
    titulo_boas_vindas.pack()

    descricao = tk.Label(
        tela_boas_vindas,
        text="Escolha uma das opções abaixo para começar.",
        bg="#C0C0C0",
        fg="black",
        font=("MS Sans Serif", 16),
        pady=20
    )
    descricao.pack()

    botao_jogar = tk.Button(
        tela_boas_vindas,
        text="🎮 Jogar Macetador",
        command=iniciar_jogo,
        bg="#008000",
        fg="white",
        font=("MS Sans Serif", 16, "bold"),
        relief="raised",
        bd=4,
        padx=40,
        pady=20
    )
    botao_jogar.pack(pady=20)

    botao_cobrinha = tk.Button(
        tela_boas_vindas,
        text="🐍 Outros Jogos (Cobrinha)",
        command=iniciar_cobrinha,
        bg="#000080",
        fg="white",
        font=("MS Sans Serif", 16, "bold"),
        relief="raised",
        bd=4,
        padx=40,
        pady=20
    )
    botao_cobrinha.pack(pady=20)

    botao_modo_escuro = tk.Button(
        tela_boas_vindas,
        text="🌙 Modo Escuro",
        command=ativar_modo_escuro,
        bg="#333333",
        fg="white",
        font=("MS Sans Serif", 16, "bold"),
        relief="raised",
        bd=4,
        padx=40,
        pady=20
    )
    botao_modo_escuro.pack(pady=20)

    mais_coisas_label = tk.Label(
        tela_boas_vindas,
        text="Mais coisas em breve!",
        bg="#C0C0C0",
        fg="black",
        font=("MS Sans Serif", 12, "italic")
    )
    mais_coisas_label.pack(pady=10)

    relogio_label = tk.Label(
        tela_boas_vindas,
        text="",
        bg="#C0C0C0",
        fg="black",
        font=("MS Sans Serif", 14, "bold")
    )
    relogio_label.pack(pady=10)

    atualizar_relogio()  # Inicia o relógio
    tela_boas_vindas.mainloop()

# Inicia o aplicativo com a splash screen e a tela de boas-vindas
splash_screen()
iniciar_tela_boas_vindas()
