from app import app
from models import Educacao, Experiencia, Projeto, User, db

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"


def seed():
    with app.app_context():
        db.create_all()

        if not User.query.filter_by(username=ADMIN_USERNAME).first():
            admin = User(username=ADMIN_USERNAME)
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

        db.session.commit()
        print("Seed concluído.")


if __name__ == "__main__":
    seed()
