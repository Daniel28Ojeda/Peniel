// MENU COLAPSÁVEL
const sidebar = document.getElementById('sidebar');
const main = document.querySelector('.main');
const toggle = document.getElementById('toggleMenu');

if (toggle) {
    toggle.onclick = () => {
        sidebar.classList.toggle('collapsed');
        main.classList.toggle('expanded');
    };
}

// GRÁFICO LINHA
const linha = document.getElementById('graficoLinha');
if (linha) {
    new Chart(linha, {
        type: 'line',
        data: {
            labels: ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun'],
            datasets: [{
                data: [12, 19, 8, 15, 22, 30],
                tension: 0.4,
                fill: true
            }]
        },
        options: {
            plugins: { legend: { display: false } },
            scales: {
                x: { grid: { display: false } },
                y: { beginAtZero: true }
            }
        }
    });
}

// GRÁFICO PIZZA
const pizza = document.getElementById('graficoPizza');
if (pizza) {
    new Chart(pizza, {
        type: 'doughnut',
        data: {
            labels: ['Aprovadas', 'Pendentes', 'Rejeitadas'],
            datasets: [{
                data: [94, 21, 13]
            }]
        },
        options: {
            plugins: { legend: { position: 'bottom' } }
        }
    });
}
