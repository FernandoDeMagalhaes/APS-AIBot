import tkinter as tk
from tkinter import messagebox, scrolledtext, Tk, Frame
import numpy as np
import requests
import pandas as pd
from bs4 import BeautifulSoup
from IPython.display import display
import matplotlib.pyplot as plt
import feedparser
from pandastable import Table, TableModel
from datetime import datetime, timedelta
from modelo_de_treinamento import treinar_modelo_sentimento, treinar_modelo_topic, obter_dataframe_completo

print("Iniciando IA e Sincronizando com G1... Aguarde.")
modelo_ia_sent, vetorizador_sent, acuracia_sent_valor, tempo_sent_valor, encoder_sent = treinar_modelo_sentimento()
modelo_ia_topic, vetorizador_topic, acuracia_topic_valor, tempo_topic_valor, encoder_topic = treinar_modelo_topic()


def gerar_comparativo_5_dias():
    url_rss = "https://g1.globo.com/rss/g1/meio-ambiente/"
    feed = feedparser.parse(url_rss)

    hoje = datetime.now()
    limite = hoje - timedelta(days=5)

    contagem_temas = {"Queimadas": 0, "Enchentes": 0, "Poluição": 0, "Clima": 0, "Fauna": 0, "Garimpo": 0,
                      "Desmatamento": 0, "Preservação": 0, "Outros": 0}
    total_encontrado = 0

    print(f"DEBUG: Analisando feed do G1... {len(feed.entries)} entradas encontradas.")

    for entry in feed.entries:
        data_noticia = datetime(*(entry.published_parsed[:6]))

        if data_noticia >= limite:
            texto_noticia = (entry.title + " " + entry.summary).lower()
            res = analisar_tema(texto_noticia)
            achou_tema = False

            if (res == 'queimada'):
                contagem_temas["Queimadas"] += 1
                achou_tema = True

            if (res == 'enchente'):
                contagem_temas["Enchentes"] += 1
                achou_tema = True

            if (res == 'poluicao'):
                contagem_temas["Poluição"] += 1
                achou_tema = True

            if (res == 'clima'):
                contagem_temas["Clima"] += 1
                achou_tema = True

            if (res == 'fauna'):
                contagem_temas["Fauna"] += 1
                achou_tema = True

            if (res == 'garimpo'):
                contagem_temas["Garimpo"] += 1
                achou_tema = True

            if (res == 'desmatamento'):
                contagem_temas["Desmatamento"] += 1
                achou_tema = True

            if (res == 'preservacao'):
                contagem_temas["Preservação"] += 1
                achou_tema = True

            if (res == 'outros'):
                contagem_temas["Outros"] += 1
                achou_tema = True

            if achou_tema:
                total_encontrado += 1

    print(f"DEBUG: Total de notícias classificadas: {total_encontrado}")

    if total_encontrado == 0:
        messagebox.showinfo("Comparativo",
                            "O G1 não publicou notícias com as palavras-chave cadastradas nos últimos 5 dias.")
        return

    assuntos = list(contagem_temas.keys())
    valores = list(contagem_temas.values())
    plt.figure(figsize=(15, 6))
    plt.bar(assuntos, valores, color=['#e67e22', '#3498db', '#95a5a6', '#2ecc71', '#e67e22', '#3498db', '#95a5a6'])
    plt.title(f"Comparativo de Assuntos (Últimos 5 dias)\nTotal: {total_encontrado} notícias")
    plt.ylabel("Quantidade")
    plt.show()


def gerar_comparativo_5_dias_sentimento():
    url_rss = "https://g1.globo.com/rss/g1/meio-ambiente/"
    feed = feedparser.parse(url_rss)

    hoje = datetime.now()
    limite = hoje - timedelta(days=5)

    categoria = ["Dia 1", "Dia 2", "Dia 3", "Dia 4", "Dia 5"]
    positivas = {"d1": 0, "d2": 0, "d3": 0, "d4": 0, "d5": 0}
    negativas = {"d1": 0, "d2": 0, "d3": 0, "d4": 0, "d5": 0}
    neutras = {"d1": 0, "d2": 0, "d3": 0, "d4": 0, "d5": 0}

    total_encontrado = 0

    print(f"DEBUG: Analisando feed do G1... {len(feed.entries)} entradas encontradas.")

    for entry in feed.entries:
        data_noticia = datetime(*(entry.published_parsed[:6]))

        if data_noticia >= limite:
            texto_noticia = (entry.title + " " + entry.summary).lower()
            res = analisar_sentimento(texto_noticia)


            if (data_noticia.date() == hoje.date()):


                if (res == 'positivo'):
                    positivas["d1"] += 1
                    total_encontrado += 1

                if (res == 'neutro'):
                    neutras["d1"] += 1
                    total_encontrado += 1

                if (res == 'negativo'):
                    negativas["d1"] += 1
                    total_encontrado += 1



            if (data_noticia.date() == (hoje.date() - timedelta(days=1))):


                if (res == 'positivo'):
                    positivas["d2"] += 1
                    total_encontrado += 1

                if (res == 'neutro'):
                    neutras["d2"] += 1
                    total_encontrado += 1

                if (res == 'negativo'):
                    negativas["d2"] += 1
                    total_encontrado += 1


            if (data_noticia.date() == (hoje.date() - timedelta(days=2))):


                if (res == 'positivo'):
                    positivas["d3"] += 1
                    total_encontrado += 1

                if (res == 'neutro'):
                    neutras["d3"] += 1
                    total_encontrado += 1

                if (res == 'negativo'):
                    negativas["d3"] += 1
                    total_encontrado += 1


            if (data_noticia.date() == (hoje.date() - timedelta(days=3))):


                if (res == 'positivo'):
                    positivas["d4"] += 1
                    total_encontrado += 1

                if (res == 'neutro'):
                    neutras["d4"] += 1
                    total_encontrado += 1

                if (res == 'negativo'):
                    negativas["d4"] += 1
                    total_encontrado += 1


            if (data_noticia.date() == (hoje.date() - timedelta(days=4))):


                if (res == 'positivo'):
                    positivas["d5"] += 1
                    total_encontrado += 1

                if (res == 'neutro'):
                    neutras["d5"] += 1
                    total_encontrado += 1

                if (res == 'negativo'):
                    negativas["d5"] += 1
                    total_encontrado += 1

    print(f"DEBUG: Total de notícias classificadas: {total_encontrado}")


    if total_encontrado == 0:
        messagebox.showinfo("Comparativo",
                            "O G1 não publicou notícias com as palavras-chave cadastradas nos últimos 5 dias.")
        return

    valores_pos = list(positivas.values())
    valores_neu = list(neutras.values())
    valores_neg = list(negativas.values())

    barWidth = 0.25

    plt.figure(figsize=(10, 6))

    r1 = np.arange(len(valores_neu))
    r2 = [x - barWidth for x in r1]
    r3 = [x + barWidth for x in r1]

    plt.bar(r1, valores_neu, color=['#0000ff'], width=barWidth, label="Positivas")
    plt.bar(r2, valores_pos, color=['#00ff00'], width=barWidth, label="Neutras")
    plt.bar(r3, valores_neg, color=['#ff0000'], width=barWidth, label="Negativas")

    plt.title(f"Comparativo sentimento por dia \n{total_encontrado} encontradas")
    plt.ylabel("Quantidade")
    plt.show()

def gerar_informe():
    url_rss = "https://g1.globo.com/rss/g1/meio-ambiente/"
    feed = feedparser.parse(url_rss)

    hoje = datetime.now()
    limite = hoje - timedelta(days=5)

    dados = []

    for entry in feed.entries:
        data_noticia = datetime(*(entry.published_parsed[:6]))

        if data_noticia >= limite:
            texto_noticia = (entry.title + " " + entry.summary).lower()
            res_sent = analisar_sentimento(texto_noticia)
            res_tema = analisar_tema(texto_noticia)

            dado = []
            dado.insert(0, texto_noticia)
            dado.insert(1, res_sent)
            dado.insert(2, res_tema)

            dados.append(dado)

    df = pd.DataFrame(dados, columns=['texto', 'sentimento', 'tema'])

    root = Tk()

    frame = Frame(root)

    frame.pack(padx=20, pady=10)

    table = Table(frame, dataframe=df, editable=False)

    table.show()

    root.mainloop()



# Análise e Scraping
def extrair_noticia_real(url):
    try:
        header = {'User-Agent': 'Mozilla/5.0'}
        resposta = requests.get(url, headers=header, timeout=10)
        if resposta.status_code == 200:
            soup = BeautifulSoup(resposta.text, 'html.parser')
            for s in soup(["script", "style"]): s.decompose()
            texto_limpo = '\n'.join(chunk for chunk in (l.strip() for l in soup.get_text().splitlines()) if chunk)
            log = (f"Protocolo: {url.split(':')[0].upper()} | Status: {resposta.status_code} OK\n"
                   f"Pacotes: {len(resposta.content)} bytes recebidos via rede.")
            return texto_limpo[:2500], log
        return None, f"Erro {resposta.status_code}"
    except Exception as e:
        return None, str(e)


def analisar_sentimento(texto):
    vetor = vetorizador_sent.transform([texto]).toarray()
    pred = modelo_ia_sent.predict(vetor)
    res = encoder_sent.inverse_transform([np.argmax(pred)])[0]

    return res


def analisar_tema(texto):
    vetor = vetorizador_topic.transform([texto]).toarray()
    pred = modelo_ia_topic.predict(vetor)
    res = encoder_topic.inverse_transform([np.argmax(pred)])[0]

    return res


def run_ia():
    url = ent_link.get().strip()
    texto = txt_input.get("1.0", tk.END).strip()
    if url:
        conteudo, log = extrair_noticia_real(url)
        if conteudo:
            texto_final, log_rede = conteudo, log
            txt_input.delete("1.0", tk.END);
            txt_input.insert(tk.END, texto_final)
            txt_logs.delete("1.0", tk.END);
            txt_logs.insert(tk.END, log_rede)
        else:
            messagebox.showerror("Erro", log);
            return
    elif texto:
        texto_final = texto
        txt_logs.delete("1.0", tk.END);
        txt_logs.insert(tk.END, "Entrada Manual - Sem tráfego externo.")
    else:
        messagebox.showwarning("Aviso", "Insira link ou texto.");
        return

    res_sent = analisar_sentimento(texto_final)
    res_topic = analisar_tema(texto_final)
    res = f"{res_sent} {res_topic}"

    cores_res = {"positivo": "#27ae60", "negativo": "#c0392b", "neutro": "#2980b9"}
    lbl_resultado.config(text=f"VEREDITO IA: {res.upper()}", fg=cores_res.get(res_sent, "black"))


# Gráfico
def visualizar_estatisticas_json():
    palavra = ent_filtro.get().strip().lower()
    df = obter_dataframe_completo()
    df_f = df[df['content'].str.contains(palavra, case=False, na=False)] if palavra else df

    if df_f.empty: messagebox.showinfo("Busca", "Nada encontrado."); return

    cont = df_f['sentiment'].value_counts()
    labels = cont.index.tolist()
    valores = cont.values.tolist()

    # Cores do gráfico
    mapa_cores = {'positivo': '#2ecc71', 'negativo': '#e74c3c', 'neutro': '#3498db'}
    cores_ordenadas = [mapa_cores.get(l, '#95a5a6') for l in labels]

    plt.figure(figsize=(7, 5))
    plt.pie(valores, labels=[f"{l.upper()} ({v})" for l, v in zip(labels, valores)],
            autopct='%1.1f%%', colors=cores_ordenadas, shadow=True, startangle=140)
    plt.title(f"Estatística: {palavra.upper() if palavra else 'Geral'}")
    plt.show()


# Interface
janela = tk.Tk()
janela.title("APS - Monitoramento Ambiental Inteligente")
janela.geometry("900x850")
janela.configure(bg="#f4f7f6")

tk.Label(janela, text="SISTEMA DE ANÁLISE AMBIENTAL (IA + REDES)", font=("Helvetica", 16, "bold"), bg="#f4f7f6").pack(
    pady=10)

frame_btns = tk.Frame(janela, bg="#f4f7f6")
frame_btns.pack(pady=10)

tk.Button(frame_btns, text="GRÁFICO POR ASSUNTO", command=visualizar_estatisticas_json, bg="#f39c12", fg="white").grid(
    row=0, column=0, padx=5)
tk.Entry(frame_btns, textvariable=(ent_filtro := tk.StringVar(value="")), width=12).grid(row=0, column=1,
                                                                                         padx=5)
tk.Button(frame_btns, text="TEMAS ULTIMOS 5 DIAS (G1 REAL)", command=gerar_comparativo_5_dias, bg="#8e44ad", fg="white",
          font=("Arial", 9, "bold")).grid(row=1, column=0, padx=20)

tk.Button(frame_btns, text="SENTIMENTOS ULTIMOS 5 DIAS (G1 REAL)", command=gerar_comparativo_5_dias_sentimento,
          bg="#8e44ad", fg="white",
          font=("Arial", 9, "bold")).grid(row=1, column=1, padx=20)

tk.Button(frame_btns, text="NOTICIAS DOS ULTIMOS 5 DIAS (G1 REAL)", command=gerar_informe,
          bg="#8e44ad", fg="white",
          font=("Arial", 9, "bold")).grid(row=1, column=2, padx=20)

tk.Label(janela, text="Link da Notícia (Monitoramento Real):", bg="#f4f7f6", font=("Arial", 10, "bold")).pack()
ent_link = tk.Entry(janela, width=100);
ent_link.pack(pady=5)
txt_input = scrolledtext.ScrolledText(janela, width=95, height=12);
txt_input.pack(pady=10)

tk.Button(janela, text="EXECUTAR ANÁLISE", command=run_ia, bg="#2980b9", fg="white",
          font=("Arial", 11, "bold"), height=2, width=30).pack(pady=10)

txt_logs = tk.Text(janela, width=95, height=4, bg="#ecf0f1");
txt_logs.pack()
lbl_resultado = tk.Label(janela, text="AGUARDANDO...", font=("Helvetica", 22, "bold"), bg="#f4f7f6");
lbl_resultado.pack(pady=20)

janela.mainloop()