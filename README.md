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
- **requiriments.txt** tem a lista de bibliotecas usadas no código.
- **app.py** cria as páginas no **Render** usando **Flask**.
- **funcoes.py** contém as funções que geram os títulos rápidos para a soja e para o milho.
- **graficos_usda.py** organiza a coleta de dados do formulário de Consulta e gera uma série de gráficos.
- **telegram_funcoes.py** guarda o código do robô "ZéBot" usado para cadastrar usuários em uma tabela e para disparar mensagens.
- **templates** é uma pasta com os modelos de HTML usados no trabalho.
