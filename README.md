# Sistema de Gestão de Inventário Sustentável

Projeto de Extensão Universitária em Engenharia de Software para auxiliar pequenos comércios locais a gerenciar estoques de forma eficiente e sustentável.

## Funcionalidades
- Controle de entrada/saída de produtos
- Alertas de validade próxima
- Relatórios de estoque
- Interface gráfica amigável

## Tecnologias
- Python 3.8+
- SQLite
- Tkinter (GUI)
- pandas (relatórios)

## Como Executar:

## 1: Clone o repositório
    git clone https://github.com/seu-usuario/projeto-extensao-ii.git

## 2: Configure o ambiente virtual
    python -m venv venv
    source venv/bin/activate  # Linux/Mac
    venv\Scripts\activate     # Windows

## 3: Instale as dependências
    pip install -r requirements.txt

## 4: Inicie o aplicativo
    python src/main.py

### **Passo 4: Estrutura de Branches**
Sugestão de fluxo:
- **`main`**: Branch estável (aprove para versões funcionais).
- **`develop`**: Branch de desenvolvimento (integre features aqui).
- **`feature/nome-da-feature`**: Branches temporárias para novas funcionalidades.

Crie a branch `develop`:
```bash
git checkout -b develop