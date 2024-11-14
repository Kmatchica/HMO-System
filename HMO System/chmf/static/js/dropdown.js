
//Refresh Dropdown: Function to refresh the dropdown list
function reloadDropdowns(var_url, dropdownid) {
    $.ajax({
      url: var_url,  // URL defined in urls.py
      method: 'GET',
      success: function(response) {
        let dropdown = $('#' + dropdownid);
        let selectedValue = dropdown.val(); // Store the current selected value
        dropdown.empty(); // Clear existing options

        // Loop through the response and append options to the dropdown
        $.each(response, function(index, value) {
          dropdown.append($('<option>', {
            value: value.productcode, // Value from server
            text: value.productname // Text to display
          }));
        });

         // Restore the previously selected value if it still exists
         if (selectedValue) {
          dropdown.val(selectedValue); 
        }

      },
      error: function(xhr, status, error) {
        console.error('Error: ' + error);
      }
    });
}
//End: Refresh Dropdown

//Function to initialize and refresh dropdown list
function setupDropdownAutoReload(var_url, dropdownid, interval) {
  reloadDropdowns(var_url, dropdownid); // Initial call on page load

  setInterval(function() {
    reloadDropdowns(var_url, dropdownid); // Refresh every X seconds
  }, interval);
}
//End: Function to initialize and refresh dropdown list