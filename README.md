# Projeto 1 - Análise de Vendas (Superstore) 📊

Fala pessoal! Esse aqui é o meu primeiro projeto de análise de dados. A ideia foi pegar um dataset clássico de vendas (o "Sample Superstore") e transformar aquela bagunça de linhas e colunas em algo que faça sentido para o negócio.

## 🛠️ O que eu usei:
- **Python (Pandas)**: Pra limpar os dados, ajustar as datas e calcular os lucros no `analyze.py`.
- **HTML/CSS (Vanilla)**: Pra montar o visual do dashboard (com um estilo mais "dark mode" e moderno).
- **Chart.js**: Usei essa lib pra criar os gráficos interativos.
- **JavaScript**: Pra puxar os dados processados pelo Python e mostrar tudo na tela.

## 📈 O que o projeto mostra:
- O faturamento total e o lucro líquido.
- Quais produtos estão vendendo mais (e quais estão dando prejuízo).
- O comportamento das vendas ao longo dos meses (sazonalidade).
- Onde estão os nossos melhores clientes.

## 💡 Insights que eu tirei:
No final do dashboard, deixei uma parte de "Business Insights" que gera recomendações automáticas, tipo onde vale a pena investir mais em marketing ou onde o estoque precisa subir.

## 🚀 Como rodar na sua máquina:
1. Primeiro, roda o script pra processar os dados:
   ```bash
   python analyze.py
   ```
2. Depois, sobe um servidorzinho pra ver o dashboard:
   ```bash
   python -m http.server 8000
   ```
3. Abre no navegador: `http://localhost:8000`

Valeu por dar uma olhada! Qualquer sugestão é bem-vinda. 🚀
