import html
import re
import unicodedata

import requests
import streamlit as st

API_URL = "https://hp-api.onrender.com/api/characters"
LIMITE = 24
SUGESTOES = ["Potter", "Weasley", "Malfoy", "Black", "Granger"]

# nome em português, cor principal, cor de destaque
CASAS = {
    "Gryffindor": ("Grifinória", "#c8402f", "#e8b84a"),
    "Slytherin": ("Sonserina", "#2f8f5b", "#c9d1d9"),
    "Ravenclaw": ("Corvinal", "#3d6fd6", "#c79a5c"),
    "Hufflepuff": ("Lufa-Lufa", "#e0b020", "#8d6e1c"),
}
SEM_CASA = ("Sem casa", "#7b86a0", "#a9b3c9")

GENERO = {"male": "Masculino", "female": "Feminino"}
ESPECIE = {
    "human": "Humano", "werewolf": "Lobisomem", "half-giant": "Meio-gigante",
    "giant": "Gigante", "cat": "Gato", "ghost": "Fantasma", "goblin": "Goblin",
    "house-elf": "Elfo doméstico", "centaur": "Centauro", "poltergeist": "Poltergeist",
    "owl": "Coruja", "dragon": "Dragão", "acromantula": "Acromântula",
    "vampire": "Vampiro", "three-headed dog": "Cão de três cabeças",
}
ANCESTRALIDADE = {
    "pure-blood": "Sangue-puro", "half-blood": "Mestiço", "muggleborn": "Nascido trouxa",
    "muggle": "Trouxa", "squib": "Squib", "quarter-veela": "Quarto veela",
    "half-veela": "Meio veela",
}
CORES = {
    "brown": "Castanho", "black": "Preto", "blonde": "Loiro", "blond": "Loiro",
    "grey": "Cinza", "gray": "Cinza", "green": "Verde", "blue": "Azul",
    "red": "Vermelho", "white": "Branco", "silver": "Prateado", "hazel": "Avelã",
    "auburn": "Ruivo escuro", "ginger": "Ruivo", "bald": "Careca", "sandy": "Areia",
    "yellow": "Amarelo", "pale": "Pálido", "golden": "Dourado", "orange": "Laranja",
    "dark": "Escuro", "dark brown": "Castanho-escuro", "brownish": "Acastanhado",
}

st.set_page_config(page_title="Mundo Bruxo", page_icon="⚡", layout="centered")

CASTELO = (
    "url(\"data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' "
    "viewBox='0 0 1200 220' preserveAspectRatio='xMidYMax slice'><g fill='%23101a30'>"
    "<rect x='0' y='175' width='1200' height='45'/>"
    "<rect x='60' y='130' width='60' height='90'/><polygon points='54,130 90,80 126,130'/>"
    "<rect x='250' y='110' width='44' height='110'/><polygon points='244,110 272,50 300,110'/>"
    "<rect x='330' y='145' width='90' height='75'/>"
    "<rect x='470' y='70' width='50' height='150'/><polygon points='462,70 495,0 528,70'/>"
    "<rect x='540' y='120' width='36' height='100'/><polygon points='534,120 558,70 582,120'/>"
    "<rect x='620' y='140' width='110' height='80'/>"
    "<rect x='780' y='95' width='46' height='125'/><polygon points='772,95 803,35 834,95'/>"
    "<rect x='880' y='135' width='70' height='85'/><polygon points='874,135 915,95 956,135'/>"
    "<rect x='1020' y='105' width='40' height='115'/><polygon points='1014,105 1040,55 1066,105'/>"
    "<rect x='1100' y='150' width='80' height='70'/>"
    "</g></svg>\")"
)

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@500;700&family=Inter:wght@400;500&display=swap');

.stApp { background: #0a0f1c; color: #e6ebf5; color-scheme: dark; font-family: 'Inter', sans-serif; }
[data-testid="stHeader"], footer, #MainMenu { visibility: hidden; }
.block-container { max-width: 980px; padding-top: 3.5rem; position: relative; z-index: 1; }

/* céu estrelado */
.stApp::before {
  content: ""; position: fixed; inset: 0; z-index: 0; pointer-events: none; opacity: .55;
  background-image:
    radial-gradient(1px 1px at 20px 30px, #fff, transparent),
    radial-gradient(1.5px 1.5px at 120px 80px, #cfe0ff, transparent),
    radial-gradient(1px 1px at 220px 160px, #fff, transparent),
    radial-gradient(1px 1px at 70px 190px, #f1e6c8, transparent),
    radial-gradient(1.5px 1.5px at 170px 240px, #fff, transparent);
  background-size: 260px 280px;
  animation: brilho 7s ease-in-out infinite alternate;
}
@keyframes brilho { from { opacity: .35; } to { opacity: .7; } }
@media (prefers-reduced-motion: reduce) { .stApp::before { animation: none; } }

/* lua e castelo */
.stApp::after {
  content: ""; position: fixed; inset: 0; z-index: 0; pointer-events: none;
  background:
    radial-gradient(circle at 88% 110px, #f1e6c8 0 26px, rgba(241,230,200,.16) 27px, transparent 150px) no-repeat 0 0 / 100% 100%,
    __CASTELO__ no-repeat bottom center / 100% 200px;
}

.raio { text-align: center; font-size: 1.8rem; color: #e8b84a; filter: drop-shadow(0 0 10px rgba(232,184,74,.6)); }
.titulo {
  font-family: 'Cinzel', serif; font-size: 2.8rem; font-weight: 700; text-align: center; margin: 4px 0 0;
  letter-spacing: .03em; background: linear-gradient(180deg, #fbf1d3, #d6b25e);
  -webkit-background-clip: text; background-clip: text; color: transparent;
}
.subtitulo { text-align: center; color: #9aa7c2; margin: 8px 0 22px; }
.orn { display: flex; align-items: center; gap: 14px; color: #d6b25e; margin: 6px auto 22px; max-width: 420px; }
.orn span { flex: 1; height: 1px; background: linear-gradient(90deg, transparent, #d6b25e, transparent); }

div[data-baseweb="input"] {
  background: #121b2e; border: 1px solid #2a3b5c; border-radius: 12px; overflow: hidden;
}
div[data-baseweb="input"]:focus-within { border-color: #d6b25e; box-shadow: 0 0 0 1px #d6b25e, 0 0 24px rgba(214,178,94,.18); }
div[data-baseweb="input"] input { background: transparent; color: #e6ebf5; font-size: 1.05rem; padding: 14px 16px; }
div.stButton > button {
  background: rgba(18,27,46,.7); color: #cfd8ea; border: 1px solid #2a3b5c; border-radius: 999px;
  padding: 2px 14px; font-size: .85rem; width: 100%;
}
div.stButton > button:hover { border-color: #d6b25e; color: #f1e6c8; }

.cab { text-align: center; margin: 34px 0 18px; }
.cab h2 { font-family: 'Cinzel', serif; font-size: 1.9rem; color: #f1e6c8; margin: 0; }
.cab p { color: #9aa7c2; margin: 4px 0 0; }

.grade { display: grid; grid-template-columns: repeat(auto-fit, minmax(380px, 1fr)); gap: 18px; }
.grade.unico { grid-template-columns: minmax(0, 560px); justify-content: center; }
.card {
  display: flex; gap: 18px; padding: 20px; border-radius: 14px;
  background: linear-gradient(165deg, rgba(21,32,58,.96), rgba(15,22,38,.96));
  border: 1px solid #243350; border-top: 3px solid var(--c);
  box-shadow: 0 18px 40px rgba(0,0,0,.35);
}
.foto {
  position: relative; width: 104px; height: 136px; flex: 0 0 104px; border-radius: 10px; overflow: hidden;
  display: flex; align-items: center; justify-content: center;
  font-family: 'Cinzel', serif; font-size: 2.4rem; color: #fff;
  background: linear-gradient(145deg, var(--c), #0f1626); border: 2px solid var(--a);
}
.foto img { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }
.info { flex: 1; min-width: 0; }
.nome { font-family: 'Cinzel', serif; font-size: 1.2rem; color: #f1e6c8; line-height: 1.2; margin-bottom: 8px; }
.selos { display: flex; flex-wrap: wrap; gap: 6px; margin-bottom: 10px; }
.selo { font-size: .72rem; padding: 3px 10px; border-radius: 999px; border: 1px solid #34466a; color: #cfd8ea; }
.selo.casa { border-color: var(--c); background: color-mix(in srgb, var(--c) 22%, transparent); color: #f6efdc; }
.d { display: flex; justify-content: space-between; gap: 12px; padding: 6px 0; border-top: 1px solid #1d2a44; font-size: .86rem; }
.d span:first-child { color: #8a97b1; flex: 0 0 auto; }
.d span:last-child { text-align: right; color: #e6ebf5; }

.vazio { text-align: center; color: #9aa7c2; margin-top: 34px; line-height: 1.7; }
.rodape { text-align: center; color: #5f6c88; font-size: .78rem; margin: 70px 0 160px; }
@media (max-width: 520px) { .grade { grid-template-columns: 1fr; } .card { flex-direction: column; align-items: center; } }
</style>
""".replace("__CASTELO__", CASTELO)

st.markdown(CSS, unsafe_allow_html=True)


# ---------------------------------------------------------------------------
def normalizar(texto):
    sem_acento = unicodedata.normalize("NFKD", texto)
    return "".join(c for c in sem_acento if not unicodedata.combining(c)).lower().strip()


def traduzir(tabela, valor):
    if not valor:
        return ""
    return tabela.get(valor.lower(), valor[:1].upper() + valor[1:])


def formatar_nascimento(p):
    data = p.get("dateOfBirth")
    if data:
        return data.replace("-", "/") if re.fullmatch(r"\d{2}-\d{2}-\d{4}", data) else data
    return str(p["yearOfBirth"]) if p.get("yearOfBirth") else ""


def campo(rotulo, valor):
    if not valor:
        return ""
    return f'<div class="d"><span>{rotulo}</span><span>{html.escape(str(valor))}</span></div>'


def cartao(p):
    casa, cor, acento = CASAS.get(p.get("house"), SEM_CASA)
    nome = html.escape(p["name"])

    foto = f'<span>{html.escape(p["name"][:1])}</span>'
    if p.get("image"):
        foto += f'<img src="{html.escape(p["image"])}" alt="" loading="lazy" referrerpolicy="no-referrer">'

    selos = f'<span class="selo casa">{casa}</span>'
    selos += f'<span class="selo">{"Vivo(a)" if p.get("alive") else "Falecido(a)"}</span>'
    if p.get("hogwartsStudent"):
        selos += '<span class="selo">Estudante de Hogwarts</span>'
    if p.get("hogwartsStaff"):
        selos += '<span class="selo">Equipe de Hogwarts</span>'
    if p.get("wizard") is False:
        selos += '<span class="selo">Não bruxo</span>'

    varinha = p.get("wand") or {}
    partes = [varinha.get("wood"), varinha.get("core")]
    if varinha.get("length"):
        partes.append(f'{varinha["length"]} pol.')
    atores = ", ".join(filter(None, [p.get("actor"), *(p.get("alternate_actors") or [])]))

    dados = "".join([
        campo("Também conhecido(a) como", ", ".join(p.get("alternate_names") or [])),
        campo("Espécie", traduzir(ESPECIE, p.get("species"))),
        campo("Gênero", traduzir(GENERO, p.get("gender"))),
        campo("Nascimento", formatar_nascimento(p)),
        campo("Ancestralidade", traduzir(ANCESTRALIDADE, p.get("ancestry"))),
        campo("Olhos", traduzir(CORES, p.get("eyeColour"))),
        campo("Cabelo", "Ruivo" if (p.get("hairColour") or "").lower() == "red"
              else traduzir(CORES, p.get("hairColour"))),
        campo("Patrono", p.get("patronus") and p["patronus"][:1].upper() + p["patronus"][1:]),
        campo("Varinha", " · ".join(x for x in partes if x)),
        campo("Ator", atores),
    ])

    return (
        f'<div class="card" style="--c:{cor};--a:{acento}">'
        f'<div class="foto">{foto}</div>'
        f'<div class="info"><div class="nome">{nome}</div>'
        f'<div class="selos">{selos}</div>{dados}</div></div>'
    )


def cabecalho(titulo, subtitulo):
    st.markdown(
        f'<div class="cab"><h2>{html.escape(titulo)}</h2><p>{html.escape(subtitulo)}</p></div>',
        unsafe_allow_html=True,
    )


@st.cache_data(ttl=3600, show_spinner="Convocando os personagens...")
def carregar_personagens():
    resposta = requests.get(API_URL, timeout=45)
    resposta.raise_for_status()
    return resposta.json()


def usar_sugestao(termo):
    st.session_state["q"] = termo


# ---------------------------------------------------------------------------
st.markdown(
    '<div class="raio">⚡</div>'
    '<h1 class="titulo">Explore o mundo bruxo</h1>'
    '<p class="subtitulo">Busque um personagem pelo nome ou um sobrenome para ver a família inteira.</p>'
    '<div class="orn"><span></span>✦<span></span></div>',
    unsafe_allow_html=True,
)

st.session_state.setdefault("q", "")
st.text_input(
    "Buscar", key="q", label_visibility="collapsed",
    placeholder="Ex.: Hermione, Weasley, Dumbledore...  (Enter para buscar)",
)
colunas = st.columns(len(SUGESTOES))
for coluna, termo in zip(colunas, SUGESTOES):
    coluna.button(termo, key=f"sug-{termo}", on_click=usar_sugestao, args=(termo,))

try:
    personagens = carregar_personagens()
except requests.RequestException:
    st.error("Não foi possível consultar a API agora. Tente novamente em instantes.")
    st.stop()

consulta = normalizar(st.session_state["q"])

if not consulta:
    st.markdown(
        '<p class="vazio">Digite um nome para começar.<br>'
        'Experimente <b>Weasley</b> ou <b>Potter</b> e veja toda a família reunida.</p>',
        unsafe_allow_html=True,
    )
else:
    familia = [p for p in personagens if normalizar(p["name"]).split()[-1:] == [consulta]]

    if len(familia) >= 2:
        sobrenome = familia[0]["name"].split()[-1]
        cabecalho(f"Família {sobrenome}", f"{len(familia)} membros encontrados")
        resultados = familia
    else:
        resultados = [
            p for p in personagens
            if consulta in normalizar(p["name"])
            or any(consulta in normalizar(a) for a in (p.get("alternate_names") or []))
        ]
        if resultados:
            total = len(resultados)
            cabecalho("Resultado" if total == 1 else "Resultados",
                      f"{total} personagem encontrado" if total == 1
                      else f"{total} personagens encontrados")

    if not resultados:
        st.markdown(
            '<p class="vazio">Nenhum personagem encontrado.<br>Confira a grafia ou tente só o sobrenome.</p>',
            unsafe_allow_html=True,
        )
    else:
        exibidos = resultados[:LIMITE]
        classe = "grade unico" if len(exibidos) == 1 else "grade"
        st.markdown(
            f'<div class="{classe}">{"".join(cartao(p) for p in exibidos)}</div>',
            unsafe_allow_html=True,
        )
        if len(resultados) > LIMITE:
            st.caption(f"Mostrando {LIMITE} de {len(resultados)}. Refine a busca para ver os demais.")

st.markdown('<p class="rodape">Dados: HP-API · hp-api.onrender.com</p>', unsafe_allow_html=True)