function renderBarChart(url) {
    return {
        data: [],
        isLoading: true,

        async init() {
            try {
                const response = await fetch(url);
                this.data = await response.json();
                this.isLoading = false;
                
                this.$nextTick(() => {
                    this.renderChart();
                });
            } catch (error) {
                console.error("Failed to load chart data:", error);
            }
        },

        renderChart() {
            const ctx = this.$refs.canvas;
            const labels = this.data.labels;

            const datasets = labels.map((label, index) => {
                const dataPoints = new Array(labels.length).fill(null);
                
                dataPoints[index] = this.data.data[index];

                return {
                    label: label,
                    data: dataPoints,
                    backgroundColor: 'rgba(2, 236, 240, 0.5)',
                    borderWidth: 1,
                    grouped: false,
                    hidden: false,
                };
            });

            const config = {
                type: 'bar',
                data: {
                    labels: labels,
                    datasets: datasets,
                },
                options: {
                    scales: {
                        y: { beginAtZero: true }
                    }
                }
            };

            new Chart(ctx, config);
        },
    }
}