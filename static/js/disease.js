$("#disease_box_ctn").hide();

function showDiseases() {
    if ($("#disease_box_ctn").is(":visible")) {
        $("#disease_box_ctn").hide();
    } else {
        $("#disease_box_ctn").show();
    }
}