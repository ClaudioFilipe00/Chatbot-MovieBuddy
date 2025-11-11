from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import requests, os, random, webbrowser, threading, uvicorn, sys
from dotenv import load_dotenv
from pathlib import Path
from nlp_engine import extrair_genero_idioma

base_path_raw = getattr(sys, '_MEIPASS', '.')
base_path = Path(base_path_raw).resolve()
env_path = base_path / '.env'
load_dotenv(env_path)

TMDB_API_KEY = os.getenv("TMDB_API_KEY")

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

conversa = {"genero": None, "idioma": None, "paginas": {}, "finalizado": False}

MAPA_IDIOMAS = {
    "en": "inglês", "pt": "português", "fr": "francês", "es": "espanhol",
    "it": "italiano", "de": "alemão", "tr": "turco", "ja": "japonês",
    "ko": "coreano", "ru": "russo"
}

MAPA_GENEROS_PT = {
    "ação": 28, "aventura": 12, "animação": 16, "comédia": 35, "crime": 80,
    "documentário": 99, "drama": 18, "família": 10751, "fantasia": 14,
    "história": 36, "terror": 27, "música": 10402, "mistério": 9648,
    "romance": 10749, "ficção científica": 878, "filme de tv": 10770,
    "suspense": 53, "guerra": 10752, "faroeste": 37
}

RESPOSTAS_INICIAIS = [
    "Opa! Qual o gênero de filme para hoje? Me diz aí!",
    "E aí! Qual a boa? Qual tipo de filme você tá a fim de assistir?",
    "Fala! Pra começar, qual gênero de filme te agrada mais?"
]
RESPOSTAS_MAIS_SUGESTOES = [
    "Beleza! Vou buscar mais opções para você...",
    "Tranquilo! Rodando a máquina de sugestões...",
    "Sem problemas! Segue mais uma dose de filmes para você!"
]
MENSAGEM_BEM_VINDO = "**E aí!** Sou o MovieBuddy, seu guia de filmes. O que está buscando?"

static_path = base_path / 'static'
app.mount("/static", StaticFiles(directory=static_path), name="static")

@app.get("/", response_class=HTMLResponse)
async def serve_index():
    try:
        with open(static_path / "index.html", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "<h1>Erro: index.html não encontrado na pasta 'static'.</h1>"

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    texto = data["mensagem"].lower().strip()
    estava_finalizado = conversa["finalizado"]
    genero, idioma = extrair_genero_idioma(texto)
    genero_id = MAPA_GENEROS_PT.get(genero) if genero else None

    if any(p in texto for p in ["obrigado", "valeu", "até mais", "já escolhi", "finalizar", "tchau"]):
        conversa["finalizado"] = True
        conversa["genero"] = None
        conversa["idioma"] = None
        return {"resposta": "Fechou! Divirta-se com o filme! Estarei aqui se precisar de mais dicas."}

    if estava_finalizado and not genero_id and not idioma:
        conversa["finalizado"] = False
        return {"resposta": "Bem-vindo de volta! Qual filme vamos buscar hoje?"}

    if genero_id and idioma:
        conversa["genero"], conversa["idioma"] = genero_id, idioma
        conversa["paginas"][genero_id] = 1
        conversa["finalizado"] = False
        return buscar_filmes(genero_id, idioma, genero, primeira=True)

    if genero_id and not idioma:
        conversa["genero"] = genero_id
        conversa["paginas"][genero_id] = 1
        conversa["finalizado"] = False
        return {"resposta": f"Massa! Quer ver os filmes de **{genero}**? Só me diz qual idioma prefere!"}

    if idioma and conversa["genero"]:
        conversa["idioma"] = idioma
        nome_genero = next((k for k, v in MAPA_GENEROS_PT.items() if v == conversa["genero"]), "gênero escolhido")
        return buscar_filmes(conversa["genero"], idioma, nome_genero, primeira=True)

    if any(x in texto for x in ["mais", "outras", "novas", "não gostei", "me mostre", "próximo"]):
        g = conversa["genero"]
        if g:
            conversa["paginas"][g] = conversa["paginas"].get(g, 1) + 1
            nome_genero = next((k for k, v in MAPA_GENEROS_PT.items() if v == g), "gênero escolhido")
            prefixo = random.choice(RESPOSTAS_MAIS_SUGESTOES)
            return buscar_filmes(g, conversa["idioma"], nome_genero, primeira=False, prefixo_resposta=prefixo)
        else:
            return {"resposta": "Calma lá! Antes preciso que você escolha um gênero, beleza?"}

    if texto == 'iniciar':
        return {"resposta": MENSAGEM_BEM_VINDO}

    if not conversa["genero"]:
        return {"resposta": random.choice(RESPOSTAS_INICIAIS)}

    nome_genero = next((k for k, v in MAPA_GENEROS_PT.items() if v == conversa["genero"]), "gênero escolhido")
    nome_idioma = MAPA_IDIOMAS.get(conversa["idioma"], "idioma padrão")
    return {"resposta": f"Ainda quer ver mais sugestões de **{nome_genero}** em **{nome_idioma}**? É só pedir!"}

def buscar_filmes(genero_id, idioma, nome_genero, primeira=False, prefixo_resposta=None):
    pagina = conversa["paginas"].get(genero_id, 1)
    filmes_filtrados = []
    max_paginas_api = 10
    pagina_inicial = pagina
    while len(filmes_filtrados) < 10:
        params = {"api_key": TMDB_API_KEY, "with_genres": genero_id, "language": "pt-BR", "page": pagina, "sort_by": "vote_average.desc" if primeira else "popularity.desc", "vote_count.gte": 10}
        try:
            r = requests.get("https://api.themoviedb.org/3/discover/movie", params=params)
            r.raise_for_status()
        except requests.RequestException as e:
            print(f"Erro ao buscar filmes: {e}")
            break
        filmes_api = r.json().get("results", [])
        if not filmes_api:
            break
        for f in filmes_api:
            if not (f.get("poster_path") and f.get("overview") and f.get("title")):
                continue
            if idioma and f.get("original_language") != idioma:
                continue
            filmes_filtrados.append(f)
            if len(filmes_filtrados) >= 10:
                break
        pagina += 1
        if pagina > (pagina_inicial + max_paginas_api):
            break
    conversa["paginas"][genero_id] = pagina
    if not filmes_filtrados:
        nome_idioma = MAPA_IDIOMAS.get(idioma, "idioma solicitado")
        return {"resposta": f"Vish... Não achei mais nenhum filme de **{nome_genero}** em **{nome_idioma}**. Que tal tentar outro gênero?"}
    nome_idioma = MAPA_IDIOMAS.get(idioma, "idioma padrão")
    if primeira:
        prefixo_final = f"Top! Encontrei os melhores filmes de **{nome_genero}** em **{nome_idioma}**:"
    elif prefixo_resposta:
        prefixo_final = f"{prefixo_resposta} Sugestões de **{nome_genero}** em **{nome_idioma}**:"
    else:
        prefixo_final = f"Aqui estão mais sugestões de **{nome_genero}** em **{nome_idioma}**:"
    lista = []
    for f in filmes_filtrados[:10]:
        lista.append({"titulo": f["title"], "sinopse": f["overview"], "nota": f["vote_average"], "poster": f"https://image.tmdb.org/t/p/w500{f['poster_path']}"})
    return {"resposta": prefixo_final, "filmes": lista}

def abrir_navegador():
    webbrowser.open("http://127.0.0.1:8000/")

if __name__ == "__main__":
    threading.Timer(2.5, abrir_navegador).start()
    uvicorn.run(app, host="127.0.0.1", port=8000)
