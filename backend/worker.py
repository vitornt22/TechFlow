import time
import json
from app import create_app, redis_client, db
from app.models import Product

app = create_app()


def process_queue():
    with app.app_context():
        while True:
            message = redis_client.lpop("products_queue")
            if message:
                try:
                    msg = json.loads(message)
                    op = msg["operation"]

                    if op == "create":
                        data = msg["data"]
                        p = Product(
                            nome=data["nome"],
                            marca=data["marca"],
                            valor=data["valor"]
                        )
                        db.session.add(p)
                        db.session.commit()
                        print(f"[CREATE] Produto criado: {p.id}")

                    elif op == "update":
                        p = Product.query.get(msg["id"])
                        if p:
                            data = msg["data"]
                            p.nome = data.get("nome", p.nome)
                            p.marca = data.get("marca", p.marca)
                            p.valor = data.get("valor", p.valor)
                            db.session.commit()
                            print(f"[UPDATE] Produto atualizado: {p.id}")
                        else:
                            print(
                                f"[UPDATE] Produto com id {msg['id']} não encontrado")

                    elif op == "delete":
                        p = Product.query.get(msg["id"])
                        if p:
                            db.session.delete(p)
                            db.session.commit()
                            print(f"[DELETE] Produto deletado: {p.id}")
                        else:
                            print(
                                f"[DELETE] Produto com id {msg['id']} não encontrado")

                    else:
                        print(f"[ERROR] Operação desconhecida: {op}")

                except Exception as e:
                    print(f"[ERROR] Falha ao processar mensagem: {message}")
                    print(f"[ERROR] Detalhes: {e}")

            else:
                time.sleep(1)


if __name__ == "__main__":
    process_queue()
