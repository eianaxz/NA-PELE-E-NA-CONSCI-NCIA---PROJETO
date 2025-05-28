# NA-PELE-E-NA-CONSCI-NCIA---PROJETO
🧩 Introdução
Na Pele e na Consciência é um simulador interativo que apresenta dilemas éticos e propõe ao usuário tomar decisões que influenciam diretamente o desenrolar da narrativa. O projeto foi desenvolvido em Python com uma interface gráfica feita em Tkinter, oferecendo uma experiência envolvente, intuitiva e educativa.

Esse sistema foi pensado para promover empatia, reflexão crítica e responsabilidade social, sendo ideal para treinamentos, projetos educacionais ou simplesmente para quem deseja mergulhar em decisões morais complexas de forma interativa.
____________________________________________________________________________________________________________________________________________________________________

🛠 Funcionalidades
CRUD completo (Cadastro, Leitura, Atualização e Exclusão de usuários)

Autenticação 2FA (Autenticação em duas etapas via e-mail)

Sistema de dilemas éticos com múltiplas escolhas, consequências e finais distintos

Perfil personalizado, com atributos, visual customizado e barra de progresso

Interface gráfica interativa, dividida em frames, com validações visuais e mensagens de erro amigáveis

Banco de dados local com SQLite, garantindo persistência dos dados de forma simples e eficiente
____________________________________________________________________________________________________________________________________________________________________

🎯 Objetivo
O objetivo principal do projeto é estimular o pensamento ético e a empatia por meio de uma ferramenta acessível, segura e dinâmica. A partir de histórias ramificadas, o usuário é convidado a refletir sobre suas decisões, lidar com consequências e moldar seu próprio caminho narrativo.

____________________________________________________________________________________________________________________________________________________________________

| Biblioteca        | Finalidade                                                                   |
| ----------------- | ---------------------------------------------------------------------------- |
| `tkinter` / `ttk` | Interface gráfica e componentes modernos                                     |
| `sqlite3`         | Banco de dados local para usuários e escolhas                                |
| `dotenv`          | Gerenciamento de variáveis de ambiente                                       |
| `os`              | Manipulação de arquivos e diretórios do sistema                              |
| `re`              | Validação de campos com expressões regulares                                 |
| `datetime`        | Controle de datas e horários                                                 |
| `random`          | Geração de variações e decisões aleatórias                                   |
| `smtplib`         | Envio de e-mails com o código de verificação 2FA                             |
Obs.: Todas as bibliotecas são nativas do Python, exceto python-dotenv, que precisa ser instalada manualmente.
Para visualizar e gerenciar o banco de dados SQLite, instale o DB Browser SQLite.
____________________________________________________________________________________________________________________________________________________________________

💻 Como Instalar
Certifique-se de ter o Python 3.10+ instalado
Baixe em: https://www.python.org/downloads/

Abra o terminal na pasta do projeto
Você pode clonar o repositório com:

git clone 

Instale a única biblioteca externa necessária:
pip install python-dotenv

Para iniciar o projeto, execute o arquivo principal no terminal com:
python sistema_cadastro.py
____________________________________________________________________________________________________________________________________________________________________

🔁 Fluxogramas
Para melhor visualização da lógica e fluxo de telas, decisões e consequências, consulte os fluxogramas do projeto no link abaixo:

➡️ https://drive.google.com/drive/folders/1fr21EiuWRLU93n4kjorVfFN_Y4kewuJR?usp=sharing
