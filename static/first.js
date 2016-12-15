
$( document ).ready(function() {
    $(":button.next").on("click", function() {
      var next_visible = $('.next.is_visible').next();
      $('.next.is_visible').hide().removeClass('is_visible');
      var result = next_visible.show().addClass('is_visible');
    });
});

