        // Move all JavaScript code here
        $(document).ready(function() {
            // Search functionality
            $("#search_query").on("keyup", function() {
                var value = $(this).val().toLowerCase();
                $("#table-body tr").filter(function() {
                    $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1);
                });
            });
    
            $("#search_approval").on("keyup", function() {
                var value = $(this).val().toLowerCase();
                $("#table-body-approval tr").filter(function() {
                    $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1);
                });
            });
    
            $("#search_update").on("keyup", function() {
                var value = $(this).val().toLowerCase();
                $("#table-body-update tr").filter(function() {
                    $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1);
                });
            });
    
            $("#search_terminate").on("keyup", function() {
                var value = $(this).val().toLowerCase();
                $("#table-body-terminate tr").filter(function() {
                    $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1);
                });
            });
        });
    
    
    
    /////////////////////////////////////// auto reload and search ///////////////////////////////////////
    
        $(document).ready(function() {
    function reloadAccessShow() {
        $('#accessshow').load(location.href + ' #accessshow');
    }
    
    function reloadAccessApproval() {
        $('#accessapproval').load(location.href + ' #accessapproval');
    }
    
    function reloadAccessUpdate() {
        $('#accessupdate').load(location.href + ' #accessupdate');
    }
    
    function reloadAccessTerminate() {
        $('#accessterminate').load(location.href + ' #accessterminate');
    }
    
    function checkTextBoxes() {
        var searchQueryValue = $('#search_query').val();
        var searchApprovalValue = $('#search_approval').val();
        var searchUpdateValue = $('#search_update').val();
        var searchTerminateValue = $('#search_terminate').val();
        
        if (searchQueryValue === '') {
            reloadAccessShow();
        }
        
        if (searchApprovalValue === '') {
            reloadAccessApproval();
        }
        
        if (searchUpdateValue === '') {
            reloadAccessUpdate();
        }
    
        if (searchTerminateValue === '') {
            reloadAccessTerminate();
        }
    }
    
    setInterval(checkTextBoxes, 5000);
    checkTextBoxes();
    });
    /////////////////////////////////////////////////////////////////////////////////////  
    function openTab(evt, accessname) {
        var i, x, tablinks;
        x = document.getElementsByClassName("tab");
        for (i = 0; i < x.length; i++) {
            x[i].style.display = "none";
        }
        tablinks = document.getElementsByClassName("tablink");
        for (i = 0; i < tablinks.length; i++) {
            tablinks[i].className = tablinks[i].className.replace(" w3-red", "");
        }
        document.getElementById(accessname).style.display = "block";
        evt.currentTarget.className += " w3-red";
    }