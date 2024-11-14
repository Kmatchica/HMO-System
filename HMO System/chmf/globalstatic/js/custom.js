//Format amount: This function is used for formatting a number. Sample: input = 1234, output = 1,234.00
function init_format(id){
    let amt = $(id).val().replace(',','').replace('.00','');
    return Number(amt).toLocaleString('en-US', {minimumFractionDigits: 2});
}
//End: Format amount
function reloadDropdowns(dropdownid) {
    $.ajax({
        type: 'GET',
        url: location.href,
        success: function(data) {
            var dropdownoptions = $(data).find('#' + dropdownid + ' option');
            var selectedoptions = $('#' + dropdownid).val();

            $('#' + dropdownid).empty(); // Clear existing options

            dropdownoptions.each(function() {
                var option = $(this).clone();
                if ($(this).val() == selectedoptions) {
                    option.attr('selected', 'selected');
                }
                $('#' + dropdownid).append(option); 
            });
        },
    });
}


function initializeDropdownReloading() {
 
    $('.reload-dropdown').each(function() {
        const dropdownid = $(this).attr('id');
        setInterval(function() {
            reloadDropdowns(dropdownid);
        }, 5000); 
    });
}


$(document).ready(function() {
    initializeDropdownReloading();
});