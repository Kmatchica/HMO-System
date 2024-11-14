//Format amount: This function is used for formatting a number. Sample: input = 1234, output = 1,234.00
function init_format(id){
    let amt = $(id).val().replace(',','').replace('.00','');
    return Number(amt).toLocaleString('en-US', {minimumFractionDigits: 2});
}
//End: Format amount
// Function to reload dropdown options globally by dropdown id
function reloadDropdowns(dropdownid) {
    $.ajax({
        type: 'GET',
        url: location.href, // You may want to change this if the content is dynamic
        success: function(data) {
            var dropdownoptions = $(data).find('#' + dropdownid + ' option');
            var selectedoptions = $('#' + dropdownid).val();

            $('#' + dropdownid).empty(); // Clear existing options

            dropdownoptions.each(function() {
                var option = $(this).clone();
                if ($(this).val() == selectedoptions) {
                    option.attr('selected', 'selected');
                }
                $('#' + dropdownid).append(option); // Add the options back
            });
        },
    });
}

// Initialize reloading of dropdowns globally on the page
function initializeDropdownReloading() {
    // Add the class .reload-dropdown to all the dropdowns you want to reload
    $('.reload-dropdown').each(function() {
        const dropdownid = $(this).attr('id'); // Get the ID of each dropdown
        setInterval(function() {
            reloadDropdowns(dropdownid);
        }, 5000); // Set interval to reload every 5 seconds (adjust as necessary)
    });
}

// Call the function to initialize dropdown reloading when the page loads
$(document).ready(function() {
    initializeDropdownReloading();
});