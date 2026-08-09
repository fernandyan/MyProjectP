from datetime import datetime

from flask import Flask, render_template

app = Flask(__name__)


@app.context_processor
def inject_year():
    return {"current_year": datetime.now().year}

perfil = {
    "nome": "Seu Nome",
    "titulo": "Desenvolvedor Python",
    "tagline": "Construo aplicações web modernas e eficientes com Python e Flask.",
    "bio": "Olá! Sou um desenvolvedor apaixonado por tecnologia, focado em criar "
           "soluções limpas, escaláveis e com boa experiência para o usuário. "
           "Tenho experiência com backend, APIs e ferramentas de automação.",
    "localizacao": "Brasil",
    "email": "seuemail@exemplo.com",
}

habilidades = [
    "Python",
    "Flask",
    "HTML",
    "CSS",
    "JavaScript",
    "SQL",
    "Git",
    "Docker",
]

projetos = [
    {
        "titulo": "Gerenciador de Tarefas",
        "descricao": "Aplicação web para organizar tarefas com autenticação, "
                     "prioridades e categorias, construída com Flask e SQLite.",
        "tecnologias": ["Flask", "SQLite", "Bootstrap"],
        "link": "#",
        "github": "#",
    },
    {
        "titulo": "API de Previsão do Tempo",
        "descricao": "API REST que consome dados meteorológicos e retorna "
                     "previsões em JSON, com cache de respostas.",
        "tecnologias": ["Python", "Flask", "REST"],
        "link": "#",
        "github": "#",
    },
    {
        "titulo": "Dashboard de Vendas",
        "descricao": "Dashboard interativo com gráficos para análise de vendas, "
                     "filtros dinâmicos e exportação de relatórios.",
        "tecnologias": ["Flask", "Chart.js", "Pandas"],
        "link": "#",
        "github": "#",
    },
]

experiencias = [
    {
        "cargo": "Desenvolvedor Backend",
        "empresa": "Empresa XYZ",
        "periodo": "2023 - Presente",
        "descricao": "Desenvolvimento de APIs e manutenção de sistemas internos.",
    },
    {
        "cargo": "Estagiário de Desenvolvimento",
        "empresa": "Empresa ABC",
        "periodo": "2022 - 2023",
        "descricao": "Apoio no desenvolvimento de aplicações web e correção de bugs.",
    },
]

educacao = [
    {
        "curso": "Bacharelado em Ciência da Computação",
        "instituicao": "Universidade Exemplo",
        "periodo": "2018 - 2022",
    },
    {
        "curso": "Bootcamp de Desenvolvimento Web",
        "instituicao": "Escola Exemplo",
        "periodo": "2022",
    },
]

contato = {
    "email": "seuemail@exemplo.com",
    "github": "https://github.com/seu-usuario",
    "linkedin": "https://linkedin.com/in/seu-usuario",
}


@app.route("/")
def index():
    return render_template(
        "index.html",
        perfil=perfil,
        habilidades=habilidades,
        projetos=projetos,
        experiencias=experiencias,
        educacao=educacao,
        contato=contato,
    )


if __name__ == "__main__":
    app.run(debug=True)
