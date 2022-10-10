$(document).ready(function() {
    $("#category_select").change(function() {
        var parent_id = $(this).val();
        $("#id_sub_category").children().not(':first').hide()
        $("#id_sub_category").children("[parent_id="+ parent_id +"]").show()
        $("#id_sub_category").val($("#id_sub_category option:first").val());
    });
});