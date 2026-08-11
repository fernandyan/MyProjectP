import stripe

from models import Produto, db

from .conftest import csrf_para, login


def _criar_produto(nome="E-book Flask", preco_centavos=2990, disponivel=True):
    produto = Produto(
        nome=nome,
        descricao="Descrição do produto.",
        preco_centavos=preco_centavos,
        disponivel=disponivel,
    )
    db.session.add(produto)
    db.session.commit()
    return produto


def test_loja_lista_apenas_produtos_disponiveis(client):
    _criar_produto(nome="Produto Ativo")
    _criar_produto(nome="Produto Oculto", disponivel=False)
    response = client.get("/loja")
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "Produto Ativo" in html
    assert "Produto Oculto" not in html
    assert "US$ 29.90" in html


def test_loja_vazia_sem_produtos(client):
    response = client.get("/loja")
    assert response.status_code == 200
    assert "Nenhum produto disponível" in response.get_data(as_text=True)


def test_checkout_redireciona_para_stripe(client, monkeypatch):
    produto = _criar_produto(preco_centavos=4990)
    chamadas = {}

    def fake_create(**kwargs):
        chamadas.update(kwargs)
        return type("Session", (), {"url": "https://checkout.stripe.com/pay/test_123"})()

    monkeypatch.setattr(stripe.checkout.Session, "create", fake_create)

    response = client.post(f"/loja/checkout/{produto.id}")
    assert response.status_code == 303
    assert response.headers["Location"] == "https://checkout.stripe.com/pay/test_123"

    linha = chamadas["line_items"][0]
    assert linha["quantity"] == 1
    assert linha["price_data"]["currency"] == "usd"
    assert linha["price_data"]["unit_amount"] == 4990
    assert chamadas["mode"] == "payment"
    assert chamadas["success_url"].startswith("http://127.0.0.1:5000/loja/sucesso")
    assert chamadas["cancel_url"].startswith("http://127.0.0.1:5000/loja/cancelado")


def test_checkout_produto_inexistente(client, monkeypatch):
    def fake_create(**kwargs):
        raise AssertionError("Não deve chamar a API do Stripe")

    monkeypatch.setattr(stripe.checkout.Session, "create", fake_create)

    response = client.post("/loja/checkout/999", follow_redirects=True)
    assert response.status_code == 200
    assert "Produto não encontrado" in response.get_data(as_text=True)


def test_admin_cria_produto(client):
    login(client, "admin", "admin123")
    csrf = csrf_para(client, "/admin/produtos/novo")
    response = client.post(
        "/admin/produtos/novo",
        data={
            "nome": "Curso de Flask",
            "descricao": "Curso completo.",
            "preco_centavos": "7990",
            "disponivel": "y",
            "csrf_token": csrf,
        },
        follow_redirects=True,
    )
    assert response.status_code == 200
    produto = Produto.query.filter_by(nome="Curso de Flask").first()
    assert produto is not None
    assert produto.preco_centavos == 7990
    assert produto.disponivel is True