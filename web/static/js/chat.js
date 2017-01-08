(function($){
  $(function(){

    // First route to show
    var GLOBALSTATE = {
        route: '.list-text'
    };
    // Set first Route
    setRoute(GLOBALSTATE.route);
    var url_for_question = $(".chat-main").data("question");


    $('#head .mdi-chevron-down').on('click', function() {
        if ($('#hangout').hasClass('collapsed')) {
            $(this).removeClass('mdi-chevron-up').addClass('mdi-chevron-down');
            $('#hangout').removeClass('collapsed');
        } else {
            $(this).removeClass('mdi-chevron-down').addClass('mdi-chevron-up');
            $('#hangout').addClass('collapsed');
        }
    });

    $('.list-text > ul > li').on('click', function() {
        $('ul.chat > li').eq(1).html('<img src="' + $(this).find('img').prop('src') + '"><div class="message"><p>' + $(this).find('.txt').text() + '</p></div>');

        // timeout just for eyecandy...
        setTimeout(function() {
            $('.shown').removeClass('shown');

            $('.list-chat').addClass('shown');
            setRoute('.list-chat');
            $('.chat-input').focus();
        }, 300);
    });

    $('.mdi-arrow-left').on('click', function() {
        $('.shown').removeClass('shown');
        setRoute('.list-text');
    });

    //dirtiest, ugliest, hackiest ripple effect solution ever... but they work xD
    /*$('.floater').on('click', function(event) {
        var $ripple = $('<div class="ripple tiny bright"></div>');
        var x = event.offsetX;
        var y = event.offsetY;
        var $me = $(this);

        $ripple.css({
            top: y,
            left: x
        });
        $(this).append($ripple);

        setTimeout(function() {
            $me.find('.ripple').remove();
        }, 530)

    });*/

    // Have to Delegate ripple due to dom manipulation (add)
    $('ul.mat-ripple').on('click', 'li', function(event) {
        if ($(this).parent().hasClass('tiny')) {
            var $ripple = $('<div class="ripple tiny"></div>');
        } else {
            var $ripple = $('<div class="ripple"></div>');
        }
        var x = event.offsetX;
        var y = event.offsetY;

        var $me = $(this);

        $ripple.css({
            top: y,
            left: x
        });

        $(this).append($ripple);
        setTimeout(function() {
            $me.find('.ripple').remove();
        }, 530)
    });


    // Set Routes - set floater
    function setRoute(route) {
        GLOBALSTATE.route = route;
        $(route).addClass('shown');

        if (route === '.list-chat') {
            $('.mdi-menu').hide();
            $('.mdi-arrow-left').show();
            $('#content').addClass('chat');
        } else {
            $('#content').removeClass('chat');
            $('.mdi-menu').show();
            $('.mdi-arrow-left').hide();
        }
    }


    $('.mdi-send').on('click', function() {
        var $chatmessage = '<p>' + $('.chat-input').val() + '</p>';
        $('ul.chat > li > .current').append($chatmessage);
        $('.chat-input').val('');
    });

    $('.chat-input').on('keyup', function(event) {
        event.preventDefault();
        if (event.which === 13) {
            $('.mdi-send').trigger('click');
        }
    });



    $('#head').on('click', '.mdi-fullscreen', function() {
        $(this).removeClass('mdi-fullscreen').addClass('mdi-fullscreen-exit');
        $('#hangout').css({
            width: '900px'
        });
    });

    $('#head').on('click', '.mdi-fullscreen-exit', function() {
        $(this).removeClass('mdi-fullscreen-exit').addClass('mdi-fullscreen');
        $('#hangout').css({
            width: '400px'
        });
    });

    // Filter
    $('.search-filter').on('keyup', function() {
        var filter = $(this).val();
        $(GLOBALSTATE.route + ' .list > li').filter(function() {
            var regex = new RegExp(filter, 'ig');

            if (regex.test($(this).text())) {
                $(this).show();
            } else {
                $(this).hide();
            }
        });
    });
    $('.mdi-radiobox-marked').on('click', function(){
      $('.chat-input').val('');
      $.ajax
      (
        {
          // method: 'POST',
          url: url_for_question,
          success: function(result)
          {
            if (result.success)
            {
              $('.chat-input').val(result.question);
            }
            else
            {
              console.log('Error on request');
            }
          }
        }
      );

      // get20q
    });
}); // end of document ready
})(jQuery); // end of jQuery name space
