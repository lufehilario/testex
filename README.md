

1. **Clone o repositório:**

   ```bash
   git clone https://github.com/Zenmuron-94/Post-It.git
   ```

2. **Navegue até o diretório do projeto:**

   ```bash
   cd twitter_clone
   ```

3. **Configure as variáveis de ambiente:**

   Crie um arquivo `.env` com as configurações necessárias (baseado em `env.dev` se existir).

4. **Inicie os serviços com Docker Compose:**

   ```bash
   docker-compose up -d --build
   ```

   Isso irá construir as imagens Docker e iniciar os containers para o web server e o banco de dados.

5. **Execute migrações e colete arquivos estáticos:**

   ```bash
   docker-compose exec web python manage.py migrate
   docker-compose exec web python manage.py collectstatic --no-input
   ```

6. **Acesse a aplicação:**

   Abra o navegador e vá para `http://127.0.0.1:8000/` para ver a aplicação em execução.

