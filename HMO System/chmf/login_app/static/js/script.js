$(document).ready(function() {
    $('[data-toggle="collapse"]').on('click', function() {
      $('#sidebar-collapse').toggleClass('collapse');
      $('body').toggleClass('sidebar-collapsed');
    });
  });