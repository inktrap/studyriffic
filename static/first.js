
$( document ).ready(function() {
    $(":button.next").on("click", function() {
      var current = $('.next.is_visible');
      var next = current.next();
      current.removeClass('is_visible').hide().addClass('is_hidden');
      next.show().removeClass('is_hidden').addClass('is_visible');
    });
});

