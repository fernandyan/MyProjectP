from app import app
from models import Educacao, Experiencia, Post, Produto, Projeto, User, db

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"
ADMIN_EMAIL = "admin@example.com"


def seed():
    with app.app_context():
        db.create_all()

        admin = User.query.filter_by(username=ADMIN_USERNAME).first()
        if not admin:
            admin = User(
                username=ADMIN_USERNAME,
                email=ADMIN_EMAIL,
                is_admin=True,
            )
            admin.set_password(ADMIN_PASSWORD)
            db.session.add(admin)
            print(f"Usuário admin criado: {ADMIN_USERNAME} / {ADMIN_PASSWORD}")
        else:
            print("Usuário admin já existe.")

        if Projeto.query.count() == 0:
            db.session.add_all(
                [
                    Projeto(
                        titulo="Gerenciador de Tarefas",
                        descricao="Aplicação web para organizar tarefas com "
                                  "autenticação, prioridades e categorias, "
                                  "construída com Flask e SQLite.",
                        tecnologias="Flask, SQLite, Bootstrap",
                        link="#",
                        github="#",
                    ),
                    Projeto(
                        titulo="API de Previsão do Tempo",
                        descricao="API REST que consome dados meteorológicos e "
                                  "retorna previsões em JSON, com cache de "
                                  "respostas.",
                        tecnologias="Python, Flask, REST",
                        link="#",
                        github="#",
                    ),
                    Projeto(
                        titulo="Dashboard de Vendas",
                        descricao="Dashboard interativo com gráficos para "
                                  "análise de vendas, filtros dinâmicos e "
                                  "exportação de relatórios.",
                        tecnologias="Flask, Chart.js, Pandas",
                        link="#",
                        github="#",
                    ),
                ]
            )
            print("Projetos de exemplo criados.")

        if Experiencia.query.count() == 0:
            db.session.add_all(
                [
                    Experiencia(
                        cargo="Desenvolvedor Backend",
                        empresa="Empresa XYZ",
                        periodo="2023 - Presente",
                        descricao="Desenvolvimento de APIs e manutenção de "
                                  "sistemas internos.",
                    ),
                    Experiencia(
                        cargo="Estagiário de Desenvolvimento",
                        empresa="Empresa ABC",
                        periodo="2022 - 2023",
                        descricao="Apoio no desenvolvimento de aplicações web "
                                  "e correção de bugs.",
                    ),
                ]
            )
            print("Experiências de exemplo criadas.")

        if Educacao.query.count() == 0:
            db.session.add_all(
                [
                    Educacao(
                        curso="Bacharelado em Ciência da Computação",
                        instituicao="Universidade Exemplo",
                        periodo="2018 - 2022",
                    ),
                    Educacao(
                        curso="Bootcamp de Desenvolvimento Web",
                        instituicao="Escola Exemplo",
                        periodo="2022",
                    ),
                ]
            )
            print("Educação de exemplo criada.")

        if Post.query.count() == 0:
            db.session.add_all(
                [
                    Post(
                        titulo="Bem-vindo ao meu blog",
                        conteudo="Este é o meu primeiro post. Aqui vou compartilhar "
                                 "aprendizados, tutoriais e novidades sobre "
                                 "desenvolvimento de software.",
                        author=admin,
                    ),
                    Post(
                        titulo="Por que uso Flask para projetos web",
                        conteudo="Flask é leve, flexível e fácil de aprender. Neste "
                                 "post exploro os motivos pelos quais escolhi esse "
                                 "framework para os meus projetos.",
                        author=admin,
                    ),
                ]
            )
            print("Postagens de exemplo criadas.")

        if Produto.query.count() == 0:
            db.session.add_all(
                [
                    Produto(
                        nome="E-book: Introdução ao Flask",
                        descricao="Guia completo para criar aplicações web com Flask.",
                        preco_centavos=2990,
                        disponivel=True,
                    ),
                    Produto(
                        nome="Curso: API REST com Python",
                        descricao="Curso prático de construção de APIs REST escaláveis.",
                        preco_centavos=4990,
                        disponivel=True,
                    ),
                    Produto(
                        nome="Consulta de carreira",
                        descricao="Sessão individual de mentoria sobre desenvolvimento web.",
                        preco_centavos=9900,
                        disponivel=True,
                    ),
                ]
            )
            print("Produtos de exemplo criados.")

        db.session.commit()
        print("Seed concluído.")


if __name__ == "__main__":
    seed()
