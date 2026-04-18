async function loadDashboard() {
    try {
        const response = await fetch('data/summary.json');
        const data = await response.json();

        // 1. Update KPIs
        document.getElementById('kpi-sales').innerText = new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(data.kpis.total_sales);
        document.getElementById('kpi-profit').innerText = new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(data.kpis.total_profit);
        document.getElementById('kpi-orders').innerText = data.kpis.total_orders.toLocaleString();
        document.getElementById('kpi-avg-ticket').innerText = new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(data.kpis.avg_ticket);

        // 2. Seasonality Chart (Line)
        const seasonalityCtx = document.getElementById('seasonalityChart').getContext('2d');
        new Chart(seasonalityCtx, {
            type: 'line',
            data: {
                labels: data.seasonality.map(i => i.MonthYear),
                datasets: [{
                    label: 'Vendas Mensais',
                    data: data.seasonality.map(i => i.Sales),
                    borderColor: '#00f2fe',
                    backgroundColor: 'rgba(0, 242, 254, 0.1)',
                    fill: true,
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { display: false } },
                scales: {
                    y: { grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#94a3b8' } },
                    x: { grid: { display: false }, ticks: { color: '#94a3b8' } }
                }
            }
        });

        // 3. Products Chart (Bar)
        const productsCtx = document.getElementById('productsChart').getContext('2d');
        new Chart(productsCtx, {
            type: 'bar',
            data: {
                labels: data.top_products.map(i => i['Product Name'].substring(0, 20) + '...'),
                datasets: [{
                    label: 'Vendas',
                    data: data.top_products.map(i => i.Sales),
                    backgroundColor: '#4facfe',
                    borderRadius: 8
                }]
            },
            options: {
                indexAxis: 'y',
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { display: false } },
                scales: {
                    x: { grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#94a3b8' } },
                    y: { grid: { display: false }, ticks: { color: '#94a3b8' } }
                }
            }
        });

        // 4. Region Chart (Doughnut)
        const regionCtx = document.getElementById('regionChart').getContext('2d');
        new Chart(regionCtx, {
            type: 'doughnut',
            data: {
                labels: data.region_sales.map(i => i.Region),
                datasets: [{
                    data: data.region_sales.map(i => i.Sales),
                    backgroundColor: ['#00f2fe', '#4facfe', '#f093fb', '#a18cd1'],
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { position: 'bottom', labels: { color: '#94a3b8' } } }
            }
        });

        // 5. Category Chart (Polar Area)
        const categoryCtx = document.getElementById('categoryChart').getContext('2d');
        new Chart(categoryCtx, {
            type: 'polarArea',
            data: {
                labels: data.category_sales.map(i => i.Category),
                datasets: [{
                    data: data.category_sales.map(i => i.Sales),
                    backgroundColor: ['rgba(0, 242, 254, 0.5)', 'rgba(79, 172, 254, 0.5)', 'rgba(240, 147, 251, 0.5)'],
                    borderColor: '#fff',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { position: 'bottom', labels: { color: '#94a3b8' } } },
                scales: { r: { grid: { color: 'rgba(255,255,255,0.1)' }, ticks: { display: false } } }
            }
        });

        // 6. Customers Chart (Bar)
        const customersCtx = document.getElementById('customersChart').getContext('2d');
        new Chart(customersCtx, {
            type: 'bar',
            data: {
                labels: data.top_customers.map(i => i['Customer Name']),
                datasets: [{
                    label: 'Volume de Compras',
                    data: data.top_customers.map(i => i.Sales),
                    backgroundColor: '#accent'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { display: false } },
                scales: {
                    y: { grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#94a3b8' } },
                    x: { grid: { display: false }, ticks: { color: '#94a3b8' } }
                }
            }
        });

        // 7. Generate Insights
        generateInsights(data);

    } catch (error) {
        console.error('Erro ao carregar o dashboard:', error);
    }
}

function generateInsights(data) {
    const container = document.getElementById('insights-container');
    const insights = [];

    // Logistic Insight
    const topRegion = data.region_sales[0].Region;
    const botRegion = data.region_sales[data.region_sales.length -1].Region;
    insights.push({
        title: "Expansão Regional",
        text: `A região <b>${topRegion}</b> domina as vendas. No entanto, a região <b>${botRegion}</b> apresenta potencial subexplorado; recomendamos uma campanha de marketing direcionada para esta área.`
    });

    // Inventory Insight
    const topProd = data.top_products[0]['Product Name'];
    insights.push({
        title: "Gestão de Estoque",
        text: `O produto <b>${topProd}</b> é o carro-chefe. Sugerimos aumentar o estoque preventivo em 20% no último trimestre devido à sazonalidade observada no gráfico de vendas.`
    });

    // Profitability Insight
    const worstSub = data.subcat_profit[0];
    if (worstSub.Profit < 0) {
        insights.push({
            title: "Otimização de Portfólio",
            text: `A subcategoria <b>${worstSub['Sub-Category']}</b> está gerando prejuízo operacional (<b>${new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(worstSub.Profit)}</b>). Reavaliar fornecedores ou descontinuar itens de baixa performance.`
        });
    }

    // Customer Insight
    const topCust = data.top_customers[0]['Customer Name'];
    insights.push({
        title: "Fidelização",
        text: `<b>${topCust}</b> é o seu maior cliente por faturamento. Implementar um programa VIP ou benefícios exclusivos para garantir a retenção dos top 10 clientes listados.`
    });

    container.innerHTML = insights.map(i => `
        <div class="insight-card">
            <h4>${i.title}</h4>
            <p>${i.text}</p>
        </div>
    `).join('');
}

window.onload = loadDashboard;
