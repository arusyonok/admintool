$(document).ready(function() {
    $("#category_select").change(function() {
        var parent_id = $(this).val();
        $("#id_sub_category").children().not(':first').hide()
        $("#id_sub_category").children("[parent_id="+ parent_id +"]").show()
        $("#id_sub_category").val($("#id_sub_category option:selected").val());
    }).change();

    $("#delete-confirmation-modal").on("shown.bs.modal", function(event) {
        var relatedItem = $(event.relatedTarget);
        var url = relatedItem.attr("href");
        var form = $(this).children().find("form");
        form.attr("action", url)
    });


    //-------------
    //- BALANCE HORIZONTAL BAR CHART -
    //-------------

    var barChartCanvas = $('#barChart')
    var barChartDataset = JSON.parse(barChartCanvas.attr("data-datasets"))
    var barChartOptions = {
        legend: {
            display: false,
        },
        responsive: true,
        maintainAspectRatio: false,
        datasetFill: false,
    }
    var barChartConfig = {
      type: 'horizontalBar',
      data: barChartDataset,
      options: barChartOptions
    };

    var chart = new Chart(barChartCanvas, barChartConfig)
});
