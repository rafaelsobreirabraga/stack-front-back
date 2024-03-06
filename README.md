# Stack - Frontend e Backend

## Descrição

Neste repositório tem exemplo de uma stack que permite a comunicação entre frontend e backend e o acesso de desenvolvedores.

* **Aplicação Frontend** - Aplicação em Python com Flask expondo na porta 8000 um formulário de criação de usuário contendo os campos ID e Name que realiza uma chamada Post com tais dados para a aplicação Backend.

* **Aplicação Backend** - Aplicação em Go (Golang) expondo na porta 8080 o CRUD de Usuários e armazena em um banco Sqlite3 local.