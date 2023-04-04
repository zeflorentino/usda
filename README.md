# **Bot do USDA**

Robô criado para automatizar a leitura dos relatórios do **Departamento de Agricultura dos Estados Unidos (USDA)** que trazem [**projeções atualizadas**](https://www.usda.gov/oce/commodity/wasde) para a produção de grãos e oleaginosas no mundo.

Os códigos presentes neste repositório criam:

- **Site no** [**Render**](https://usda-zeflorentino.onrender.com/) para que as funcionalidades fiquem disponíveis online;
- Títulos rápidos a partir dos dados mais importantes de cada commodity;
- Página para consulta de relatórios anteriores;
- Página que recebe informações da **API do Telegram** e mantém o robô respondendo em tempo real;
- Cadastramento de usuários em uma **tabela do Google Sheets**;
- Consulta de usuários cadastrados para disparo mensagem coletiva quando solicitado pelo administrador.

## **Conteúdos**

- **app.py** cria as páginas no **Render** usando **Flask**.
- **funcoes.py** contém as funções que geram os títulos rápidos para a soja e para o milho e a consulta na base de dados antiga.
- **requiriments.txt** tem a lista de bibliotecas usadas no código.
- **telegram_funcoes.py** guarda o código do robô "ZéBot" usado para cadastrar usuários em uma tabela e para disparar mensagens.
- **templates** é uma pasta com os modelos de HTML usados na página de consulta de relatórios.
