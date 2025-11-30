# 🛡️ Guardião Digital

## Sistema Inteligente de Análise de URLs para Proteção do Usuário

Um projeto em Python usando SOLID, POO, FastAPI e análise inteligente conectada a APIs oficiais.

## 🌐 Visão Geral

O **Guardião Digital** é um sistema que analisa URLs suspeitas usando múltiplas fontes de verificação, incluindo:

- Google Safe Browsing  
- VirusTotal  
- Classificador próprio baseado em regras  
- Módulo de reputação  
- Histórico de análises  

O objetivo é fornecer ao usuário uma resposta rápida, clara e confiável sobre o nível de risco de um link.

Esse projeto usa **boas práticas de desenvolvimento**, como:

- Programação orientada a objetos  
- Padrões SOLID  
- Arquitetura Limpa  
- Testes automatizados (pytest)  
- Integração com APIs reais  
- Estrutura modular e extensível  

## 🚀 Tecnologias Utilizadas

- Python 3.11+
- FastAPI (backend HTTP)
- Pydantic v2
- Requests
- Pytest
- Uvicorn
- Google Safe Browsing API
- VirusTotal API

## ⚙️ Instalação

### 1️⃣ Clonar o repositório

```bash
git clone https://github.com/seu-usuario/guardiao-digital.git
cd guardiao-digital
```

### 2️⃣ Criar ambiente virtual

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 3️⃣ Instalar dependências

```bash
pip install -r requirements.txt
```

## 🔐 Configurar variáveis de ambiente

Crie um arquivo `.env`:

```bash
GOOGLE_SAFE_BROWSING_KEY=sua_key
VIRUSTOTAL_KEY=sua_key
ENV=development
APP_NAME=Guardião Digital
```

## ▶️ Executar o servidor

```bash
uvicorn src.main:app --reload
```

Acesse:  
`http://localhost:8000/docs`  

Swagger automático 🚀

## 🧪 Rodar Testes

```bash
pytest -q
```

## Rodar UI

```bash
py -m ui.app
```

## 🧠 Como funciona a análise?

O Guardião Digital usa três camadas principais:

### 🔍 1. Detectores externos  

APIs oficiais como:

- Google Safe Browsing  
- VirusTotal  

Elas retornam reputação global da URL.

### 🧪 2. Classificação heurística  

Detecta:

- URLs muito longas  
- Termos suspeitos  
- Domínios recém-criados  
- Padrões comuns de phishing  

### 🧩 3. Agregador  

Combina todos os resultados e define o risco:

| Resultado                              | Risco     |
|----------------------------------------|-----------|
| Algum detector aponta `malicious`      | 🔴 ALTO   |
| Apenas regras acusam suspeita          | 🟡 MÉDIO  |
| Nada detectado                         | 🟢 BAIXO  |

## 📜 Licença

MIT — livre para estudar, usar e modificar.
