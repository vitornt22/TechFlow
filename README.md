# Projeto Produtos - Angular + Flask + Redis + PostgreSQL

Aplicação fullstack para gerenciamento de produtos.

- **Frontend:** Angular (standalone components)
- **Backend:** Flask
- **Banco de dados:** PostgreSQL
- **Fila:** Redis
- **Worker:** Processa operações de criação, atualização e remoção de produtos

---

## Como rodar o código

- **Apenas execute esse comando** -

  ```bash
  docker compose up --build
  ```

## Acesse a aplicação

Após carregar o comando acima, você pode acessar a aplicação no link abaixo.

- **Frontend:** [http://localhost:4200](http://localhost:4200)

## Utilize as credenciais abaixo para realizar login

- **Email** admin@test.com
- **Senha** 123456

> **Todos os produtos criados, atualizados ou deletados serão processados pelo worker via fila Redis.**

> **Os campos para adição são os mesmo para edição do produto. Ao clicar em editar, as informações do produto serão exibidas nas entradas do formulário da parte superior e o botão atualizar salva as novas informações sobre o determinado produto.**

---

## Comandos úteis

- **Ver logs do backend:**

```bash
docker-compose logs -f flask_backend
```

- **Ver logs do worker:**

```bash
docker-compose logs -f redis_worker
```

- **Para executar os testes no container use**

```bash
	docker exec -it flask_backend /bin/bash
	export PYTHONPATH=$(pwd)
	pytest -v
```

## Atenção

- **Se houver algum problema com portas em utilização na execução do docker compose usar os comando abaixos para matar os processos em execução da sua máquina**

```bash
sudo lsof -i :NUMERO DA PORTA
sudo kill -9 <PID>
```

## variaveis de ambiente .env

```bash
DATABASE_URL=postgresql://postgres:123456@db:5432/testdb
REDIS_URL=redis://redis:6379
JWT_SECRET_KEY=supersecretkey
```
