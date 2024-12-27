const createPriceChart = () => {
    const ctx = document.getElementById('priceChart').getContext('2d');
    return new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['1g', '2g', '3g', '4g', '5g', '6g', '7g'],
            datasets: [{
                label: 'Token Değeri',
                data: [0, 0.2, 0.5, 0.8, 0.6, 1.2, 1.0],
                borderColor: '#3fb950',
                tension: 0.4,
                fill: true,
                backgroundColor: 'rgba(63, 185, 80, 0.1)'
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { display: false },
                tooltip: {
                    backgroundColor: '#21262d',
                    borderColor: '#30363d',
                    borderWidth: 1
                }
            },
            scales: {
                y: {
                    grid: { color: '#30363d' },
                    ticks: { color: '#8b949e' }
                },
                x: {
                    grid: { color: '#30363d' },
                    ticks: { color: '#8b949e' }
                }
            }
        }
    });
};

document.addEventListener('DOMContentLoaded', createPriceChart);