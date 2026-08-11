import stripe
from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    url_for,
)

from models import Produto, db

loja_bp = Blueprint("loja", __name__)


@loja_bp.route("/loja")
def loja():
    produtos = Produto.query.filter_by(disponivel=True).order_by(Produto.id).all()
    return render_template(
        "loja/index.html",
        produtos=produtos,
        publishable_key=current_app.config["STRIPE_PUBLISHABLE_KEY"],
    )


@loja_bp.route("/loja/checkout/<int:produto_id>", methods=["POST"])
def checkout(produto_id):
    produto = db.session.get(Produto, produto_id)
    if not produto or not produto.disponivel:
        flash("Produto não encontrado.", "danger")
        return redirect(url_for("loja.loja"))

    base_url = current_app.config["BASE_URL"]
    try:
        sessao = stripe.checkout.Session.create(
            mode="payment",
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "unit_amount": produto.preco_centavos,
                        "product_data": {"name": produto.nome},
                    },
                    "quantity": 1,
                }
            ],
            success_url=f"{base_url}{url_for('loja.sucesso')}",
            cancel_url=f"{base_url}{url_for('loja.cancelado')}",
        )
    except stripe.error.StripeError:
        flash("Não foi possível iniciar o pagamento. Tente novamente.", "danger")
        return redirect(url_for("loja.loja"))

    return redirect(sessao.url, code=303)


@loja_bp.route("/loja/sucesso")
def sucesso():
    return render_template("loja/sucesso.html")


@loja_bp.route("/loja/cancelado")
def cancelado():
    return render_template("loja/cancelado.html")