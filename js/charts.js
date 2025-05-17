// Chart.js configuration
Chart.defaults.font.family = "'Inter', 'Helvetica', 'Arial', sans-serif";
Chart.defaults.color = '#64748b';

// Common colors
const chartColors = {
    primary: '#3b82f6',
    info: '#0ea5e9',
    success: '#22c55e',
    warning: '#f59e0b',
    error: '#ef4444',
    primaryLight: '#60a5fa',
};

// Reports page charts
if (document.getElementById('incomeExpenseChart')) {
    const incomeExpenseChart = new Chart(
        document.getElementById('incomeExpenseChart'),
        {
            type: 'line',
            data: {
                labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
                datasets: [
                    {
                        label: 'Income',
                        data: [12500, 13200, 14100, 11300, 15000, 16800, 15900, 14100, 17800, 15900, 16800, 18700],
                        borderColor: chartColors.primary,
                        backgroundColor: 'rgba(59, 130, 246, 0.1)',
                        tension: 0.4,
                        fill: true
                    },
                    {
                        label: 'Expenses',
                        data: [6500, 5600, 7500, 4700, 6500, 7500, 5600, 6500, 8400, 7500, 6500, 9300],
                        borderColor: chartColors.error,
                        backgroundColor: 'rgba(239, 68, 68, 0.1)',
                        tension: 0.4,
                        fill: true
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: {
                        grid: {
                            display: false
                        }
                    },
                    y: {
                        beginAtZero: true,
                        ticks: {
                            callback: value => 'RM ' + value.toLocaleString()
                        }
                    }
                },
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                },
                interaction: {
                    intersect: false,
                    mode: 'index'
                }
            }
        }
    );
}

if (document.getElementById('incomePieChart')) {
    const incomePieChart = new Chart(
        document.getElementById('incomePieChart'),
        {
            type: 'doughnut',
            data: {
                labels: ['Development', 'Design', 'Consulting'],
                datasets: [{
                    data: [75870, 30348, 20232],
                    backgroundColor: [
                        '#4E79A7',
                        '#F28E2B',
                        '#E15759'
                    ],
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                const value = context.parsed;
                                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                const percentage = Math.round((value / total) * 100);
                                return `RM ${value.toLocaleString()} (${percentage}%)`;
                            }
                        }
                    }
                }
            }
        }
    );
}

if (document.getElementById('expensePieChart')) {
    const expensePieChart = new Chart(
        document.getElementById('expensePieChart'),
        {
            type: 'doughnut',
            data: {
                labels: ['Software', 'Equipment', 'Office', 'Other'],
                datasets: [{
                    data: [12714, 10595, 10595, 8476],
                    backgroundColor: [
                        '#76B7B2',
                        '#59A14F',
                        '#EDC948',
                        '#B07AA1'
                    ],
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                const value = context.parsed;
                                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                const percentage = Math.round((value / total) * 100);
                                return `RM ${value.toLocaleString()} (${percentage}%)`;
                            }
                        }
                    }
                }
            }
        }
    );
}

// Tax Center page charts
if (document.getElementById('taxIncomePieChart')) {
    const taxIncomePieChart = new Chart(
        document.getElementById('taxIncomePieChart'),
        {
            type: 'doughnut',
            data: {
                labels: ['Development', 'Design', 'Consulting'],
                datasets: [{
                    data: [85400, 22680, 17600],
                    backgroundColor: [
                        chartColors.primary,
                        chartColors.info,
                        chartColors.success
                    ],
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    }
                }
            }
        }
    );
}

if (document.getElementById('taxDeductionPieChart')) {
    const taxDeductionPieChart = new Chart(
        document.getElementById('taxDeductionPieChart'),
        {
            type: 'doughnut',
            data: {
                labels: ['Equipment', 'Home Office', 'Software', 'Training'],
                datasets: [{
                    data: [8250, 6100, 5400, 4600],
                    backgroundColor: [
                        chartColors.primaryLight,
                        chartColors.success,
                        chartColors.warning,
                        chartColors.info
                    ],
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    }
                }
            }
        }
    );
} 