/* -------------------------------------------------------------
   Water Purity Tracker - Chart.js Controller (charts.js)
   Visualizes trends, tank comparisons, and safe/unsafe breakdown
   ------------------------------------------------------------- */

document.addEventListener('DOMContentLoaded', () => {
  // Global Chart Styling Defaults for Dark Glass Theme
  if (window.Chart) {
    Chart.defaults.color = '#94a3b8';
    Chart.defaults.font.family = "'Poppins', sans-serif";
    Chart.defaults.plugins.tooltip.backgroundColor = 'rgba(15, 23, 42, 0.9)';
    Chart.defaults.plugins.tooltip.borderColor = 'rgba(56, 189, 248, 0.3)';
    Chart.defaults.plugins.tooltip.borderWidth = 1;
    Chart.defaults.plugins.tooltip.padding = 12;
    Chart.defaults.plugins.tooltip.cornerRadius = 8;
  }

  // 1. Dashboard Daily Trend Line Chart
  const dailyTrendCanvas = document.getElementById('dailyTrendChart');
  if (dailyTrendCanvas) {
    new Chart(dailyTrendCanvas, {
      type: 'line',
      data: {
        labels: ['19 Jul', '20 Jul', '21 Jul', '22 Jul', '23 Jul', '24 Jul', '25 Jul'],
        datasets: [{
          label: 'Average Purity Score',
          data: [94, 88, 84, 76, 95, 78, 83],
          borderColor: '#06b6d4',
          backgroundColor: 'rgba(6, 182, 212, 0.15)',
          fill: true,
          tension: 0.4,
          pointBackgroundColor: '#38bdf8',
          pointRadius: 5,
          pointHoverRadius: 8
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { display: false } },
        scales: {
          y: { min: 0, max: 100, grid: { color: 'rgba(255, 255, 255, 0.05)' } },
          x: { grid: { display: false } }
        }
      }
    });
  }

  // 2. Safe vs Unsafe Distribution Pie Chart
  const safeUnsafeCanvas = document.getElementById('safeUnsafePieChart');
  if (safeUnsafeCanvas) {
    new Chart(safeUnsafeCanvas, {
      type: 'doughnut',
      data: {
        labels: ['Safe Water (Pass)', 'Unsafe Water (Action Needed)'],
        datasets: [{
          data: [18, 7],
          backgroundColor: ['#10b981', '#ef4444'],
          borderColor: 'rgba(15, 23, 42, 0.8)',
          borderWidth: 3,
          hoverOffset: 6
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        cutout: '70%',
        plugins: {
          legend: { position: 'bottom', labels: { boxWidth: 12, padding: 16 } }
        }
      }
    });
  }

  // 3. Parameter Comparison Bar Chart (Block Level)
  const paramCompCanvas = document.getElementById('parameterComparisonChart');
  if (paramCompCanvas) {
    new Chart(paramCompCanvas, {
      type: 'bar',
      data: {
        labels: ['Block A (Boys)', 'Block B (Boys)', 'Block C (Girls)', 'Block D (PG)', 'Mess Block'],
        datasets: [
          {
            label: 'Avg TDS (ppm)',
            data: [340, 480, 210, 630, 250],
            backgroundColor: 'rgba(2, 132, 199, 0.7)',
            borderRadius: 6
          },
          {
            label: 'Avg Turbidity (NTU x100)',
            data: [210, 440, 90, 610, 120],
            backgroundColor: 'rgba(6, 182, 212, 0.7)',
            borderRadius: 6
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { position: 'top' } },
        scales: {
          y: { grid: { color: 'rgba(255, 255, 255, 0.05)' } },
          x: { grid: { display: false } }
        }
      }
    });
  }

  // 4. Analytics Weekly Trend Multi-Axis Chart
  const analyticsWeeklyCanvas = document.getElementById('analyticsWeeklyChart');
  if (analyticsWeeklyCanvas) {
    new Chart(analyticsWeeklyCanvas, {
      type: 'line',
      data: {
        labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
        datasets: [
          {
            label: 'pH Level',
            data: [7.2, 7.5, 6.4, 7.8, 7.1, 7.3, 7.4],
            borderColor: '#38bdf8',
            tension: 0.3,
            yAxisID: 'y'
          },
          {
            label: 'TDS (ppm)',
            data: [340, 360, 580, 420, 290, 310, 330],
            borderColor: '#f59e0b',
            tension: 0.3,
            yAxisID: 'y1'
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          y: {
            type: 'linear', display: true, position: 'left',
            min: 5, max: 10,
            grid: { color: 'rgba(255, 255, 255, 0.05)' }
          },
          y1: {
            type: 'linear', display: true, position: 'right',
            min: 100, max: 800,
            grid: { drawOnChartArea: false }
          }
        }
      }
    });
  }
});
