$(document).ready(function() {
    $(".category_select").change(function() {
        var category_id = $(this).val();
        var parent_form_div = $(this).parent().closest("form")
        var sub_categories_select = parent_form_div.find(".sub_category")

        sub_categories_select.children().not(":first").hide()
        sub_categories_select.children("[parent_id="+ category_id +"]").show()
        sub_categories_select.val(sub_categories_select.find(':first').val())
    });

    $("#delete-confirmation-modal").on("shown.bs.modal", function(event) {
        var relatedItem = $(event.relatedTarget);
        var url = relatedItem.attr("href");
        var form = $(this).children().find("form");
        form.attr("action", url)
    });
});
