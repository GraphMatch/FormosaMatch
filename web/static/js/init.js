(function($){
  $(function(){
    sideNavOptions = {
      menuWidth: 300, // Default is 240
      edge: 'right', // Choose the horizontal origin
      closeOnClick: true, // Closes side-nav on <a> clicks, useful for Angular/Meteor
      draggable: true // Choose whether you can drag to open on touch screens
    };
    $('.button-collapse').sideNav();
    $('.parallax').parallax();
    $('select').material_select();
    $(".datepicker").pickadate({
      selectMonths: true,
      selectYears: 100,
      max: true,
      formatSubmit: 'yyyy-mm-dd'
    });
    $('#signin-modal').modal({
      complete: function(){
        $("#signin-modal input").val("");
        $("#signin-modal input").removeClass("invalid");
      }
    });
    $("#sign-up").on("click", function(){
      $(".sign-up-1").hide("slide", { direction: "left" },400, function(){
        $(".sign-up-2").show("slide", { direction: "right"},400);
      });
    });
    $("#sign-up-2").on("click", function() {
      $(".sign-up-2").hide("slide", { direction: "left"},400, function(){
        $(".sign-up-3").show("slide", {direction: "right"},400);
      });
    });
    $("#back-sign-up-2").on("click", function() {
      $(".sign-up-3").hide("slide", { direction: "right"},400, function(){
        $(".sign-up-2").show("slide", {direction: "left"},400);
      });
    });
    $("#back-sign-up-1").on("click", function() {
      $(".sign-up-2").hide("slide", { direction: "right"},400, function(){
        $(".sign-up-1").show("slide", {direction: "left"},400);
      });
    });
    ///ALERT BUTTON
    $(".card-alert").on("click",".alert-button",function(){
      $(this).parent().fadeOut();
    });


  }); // end of document ready
  })(jQuery); // end of jQuery name space
