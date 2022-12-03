$(document).ready(function() {
    //-------------
    //- DOUGHNUT CHART EXPENSES AND INCOMES
    //-------------

    var expensesCanvas = $('#doughnutChartExpenses')
    var expensesDataset = expensesCanvas.attr("data-datasets")
    var expensesData = {}
    if (expensesDataset) {
         expensesData = JSON.parse(expensesDataset)
    }

    var incomesCanvas = $('#doughnutChartIncomes')
    var incomesDataset = incomesCanvas.attr("data-datasets")
    var incomesData = {}
    if (incomesDataset) {
         incomesData = JSON.parse(incomesDataset)
    }

    var donutOptions = {
      maintainAspectRatio : false,
      responsive : true,
      aspectRatio: 1,
      plugins: {
        colorschemes: {
          scheme: 'brewer.Paired12'
        }
      },
      legend: {
        position: 'left',
        padding: 2,
        labels: {
          pointStyle: 'circle',
          usePointStyle: true,
        }
      }
    }

    var expensesConfig = {
      type: 'doughnut',
      data: expensesData,
      options: donutOptions,
    };
    var incomesConfig = {
      type: 'doughnut',
      data: incomesData,
      options: donutOptions,
    };


    var chart1 = new Chart(expensesCanvas, expensesConfig)
    var chart2 = new Chart(incomesCanvas, incomesConfig)
});
