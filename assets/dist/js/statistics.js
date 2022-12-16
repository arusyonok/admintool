$(document).ready(function() {
    //-------------
    //- DOUGHNUT CHART EXPENSES AND INCOMES
    //-------------

    var donutOptions = {
      maintainAspectRatio : true,
      responsive : true,
      aspectRatio: 1,
      plugins: {
        colorschemes: {
          scheme: 'brewer.Paired12'
        }
      },
      legend: {
        position: 'top',
        padding: 2,
        labels: {
          pointStyle: 'circle',
          usePointStyle: true,
        }
      }
    }

    var expensesCanvas = $('#expenses-by-category-chart')
    var expensesDataset = expensesCanvas.attr("data-datasets")
    var expensesData = {}
    if (expensesDataset) {
         expensesData = JSON.parse(expensesDataset)
    }

    var expensesByDateCanvas = $('#expenses-by-date-chart')
    var expensesByDateDataset = expensesByDateCanvas.attr("data-datasets")
    var expensesByDateData = {}
    if (expensesByDateDataset) {
        expensesByDateData = JSON.parse(expensesByDateDataset)
    }

    var incomesByDateCanvas = $('#incomes-by-date-chart')
    var incomesByDateDataset = incomesByDateCanvas.attr("data-datasets")
    var incomesByDateData = {}
    if (incomesByDateDataset) {
         incomesByDateData = JSON.parse(incomesByDateDataset)
    }

    var incomesCanvas = $('#incomes-by-category-chart')
    var incomesDataset = incomesCanvas.attr("data-datasets")
    var incomesData = {}
    if (incomesDataset) {
         incomesData = JSON.parse(incomesDataset)
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

    var expensesByDateConfig = {
      type: 'doughnut',
      data: expensesByDateData,
      options: donutOptions,
    };

    var incomesByDateConfig = {
      type: 'doughnut',
      data: incomesByDateData,
      options: donutOptions,
    };

    var chart1 = new Chart(expensesCanvas, expensesConfig)
    var chart2 = new Chart(incomesCanvas, incomesConfig)
    var chart3 = new Chart(expensesByDateCanvas, expensesByDateConfig)
    var chart4 = new Chart(incomesByDateCanvas, incomesByDateConfig)
});
