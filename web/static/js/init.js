(function($){
  $(function(){
    
    $('.button-collapse').sideNav();
    $('.parallax').parallax();
    $('select').material_select();
    $(".modal").modal();
    $(".datepicker").pickadate({
      selectMonths: true,
      selectYears: 100,
      max: true,
      format: 'yyyy-mm-dd'
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

    $(".looking-for").on("click",function() {
      $("#looking-for").modal("open");
    });

    $(".interested-in").on("click",function() {
      $("#interested-in").modal("open");
    });

    $(".age-range").on("click",function() {
      $("#age-range").modal("open");
    });

    $(".range-distance").on("click",function() {
      $("#range-distance").modal("open");
    });

    ///////////////////SCROLL FIRE//////////////////////////
    var options = [
    {
      selector: '.end-match-cards', offset: 0, callback: function(el){
      alert("HEY");
      }
    }];
    Materialize.scrollFire(options);



  }); // end of document ready
  })(jQuery); // end of jQuery name space
