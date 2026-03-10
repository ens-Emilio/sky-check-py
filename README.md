# 🌤️ Sky Check Py

Um aplicativo desktop elegante para previsão do tempo em tempo real, construído com Python e tkinter.

## 🚀 Funcionalidades
- Busca por nome de cidade (suporta nomes compostos).
- Exibição de temperatura atual em graus Celsius (°C).
- Sensação térmica, umidade relativa e velocidade do vento (km/h).
- Ícones climáticos dinâmicos carregados diretamente da API.
- Interface responsiva com suporte a atalhos de teclado (Enter).
- Tratamento de erros para cidades não encontradas e problemas de conexão.

## 🛠️ Tecnologias
- **Python 3.10+**: Linguagem base.
- **tkinter**: Interface gráfica nativa (sem necessidade de bibliotecas externas complexas).
- **requests**: Para comunicação assíncrona com a API OpenWeatherMap.
- **python-dotenv**: Para gestão segura de credenciais.

## 📦 Instalação e Execução

### 1. Preparar o ambiente
Clone o repositório ou baixe os arquivos para sua máquina. Recomenda-se o uso de um ambiente virtual:

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows
```

### 2. Instalar dependências
```bash
pip install -r requirements.txt
```

### 3. Configurar Chave de API
O aplicativo utiliza a API gratuita do [OpenWeatherMap](https://openweathermap.org/api).

1. Obtenha sua chave no site oficial.
2. Abra o arquivo `.env` na raiz do projeto.
3. Insira sua chave no campo `OPENWEATHER_API_KEY`:
   ```env
   OPENWEATHER_API_KEY=seu_codigo_aqui
   ```
   *Nota: Se a chave for nova, pode levar de 30min a 2h para ser ativada pelo serviço.*

### 4. Rodar o Aplicativo
```bash
python main.py
```

## ⚖️ Licença
Este projeto está licenciado sob a **Licença MIT** - consulte o arquivo [LICENSE](LICENSE) para mais detalhes.

---
**Autor:** [ens-Emilio](https://github.com/ens-Emilio)
