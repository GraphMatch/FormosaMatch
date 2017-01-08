var options = [
{
  // selector: '.end-match-cards', offset: 0, callback: function(el){
  selector: '#endMatchCard', offset: 0, callback: function(el){
    getNewNodes()
  }
}];
Materialize.scrollFire(options);

function getNewNodes() {
  var age = $( ".btn.age-range" ).text().split("-");
  var ageMin = parseInt(age[0]);
  var ageMax = parseInt(age[1]);
  var startFrom = (parseInt($(".start-from").val())* 20)+ 1;
  ageMin = ageMin < 18 ? 18 : ageMin;
  ageMax = ageMax > 99 ? 99 : ageMax;
  var lookingFor = $( ".btn.looking-for" ).text();
  var interestedIn = $( ".btn.interested-in" ).text();
  var rangeDistance = parseInt($( ".btn.range-distance" ).text());
  rangeDistance = rangeDistance < 1 ? 1 : rangeDistance;
  var url_for_filter = $("main").data("filter");
  jsonData = JSON.stringify({'startFrom': startFrom,'lookingFor':lookingFor, 'interestedIn':interestedIn, 'ageMax':ageMax, 'ageMin':ageMin, 'rangeDistance':rangeDistance});
  $.ajax
  (
    {
      method: 'POST',
      url: url_for_filter,
      contentType: "application/json",
      data: jsonData,
      success: function(result)
      {
        if (result.success)
        {
          if (result.matchesUsernames.length > 0)
          {
          var matchesUsernames = result.matchesUsernames;
          var matchesPictures = result.matchesPictures;
          var matchesLocations = result.matchesLocations;
          var matchesAges = result.matchesAges;
          var matchesDistances = result.matchesDistances;
          var matchesLikes = result.matchesLikes;
          matchesUsernamesLength = matchesUsernames.length;
          htmlMatchCards = "";
          for (var i = 0; i < matchesUsernamesLength; i++){
            username = matchesUsernames[i];
            htmlUser = "<div class=\"col m4\"><div class=\"card\"><div class=\"card-image\">";
            if ((typeof(matchesPictures[username]) !== 'undefined') && (matchesPictures[username] != "")){
              htmlUser = htmlUser + "<img class=\"materialboxed\" data-caption=\""+username+"\" src=\""+matchesPictures[username]+"\">";
            } else {
              htmlUser = htmlUser + "<img src=\"../static/picture/no-pic.png\">";
            }
            htmlUser = htmlUser + "<span class=\"card-title\" style=\"width:100%; background: rgba(0, 0, 0, 0.5);\">"+username+"</span></div>";
            htmlUser = htmlUser + "<div class=\"center card-content\"><h5>"+ matchesAges[i]+" . "+matchesLocations[i] + "</h5>";
            htmlUser = htmlUser + "<h5>"+matchesDistances[i]+" km away from your location</h5></div>";
            htmlUser = htmlUser + "<div class=\"card-action center\">";
            if (matchesLikes[i] > 0){
              htmlUser = htmlUser + "<a class=\"waves-effect waves-teal btn deep-purple lighten-2\">Liked<i class=\"material-icons left\">done</i></a>";
            } else {
              htmlUser = htmlUser + "<a class=\"waves-effect btn-flat no-like waves-purple\">Like</a>";
            }
            htmlUser = htmlUser + "</div></div></div>";
            htmlMatchCards = htmlMatchCards + htmlUser;
          }
          // $( ".match-cards").append(htmlMatchCards);
          optionsScript = "<script>var options = [{selector: '#endMatchCard', offset: 0, callback: function(el){getNewNodes()}}];</script>"
          htmlMatchCards = htmlMatchCards + optionsScript
          $( ".end-match-cards").before(htmlMatchCards);
          Materialize.scrollFire(options);
          $('.materialboxed').materialbox();
          $(".start-from").val(parseInt($(".start-from").val())+ 1);
        }
        } else {
          console.log('Error in AJAX');
        }
      }
    }
  );
}

$(".advanced-filter").on("click",function () {
  $('#modalAdvancedFilter').modal("open");
});

$(".match-cards").on("click",".no-like", function(){
  thisParent = $(this).parent();
  var $card_node = $(this).closest(".card");
  var pic = $($card_node).find(".card-image img").attr('src');
  var distanceClicked = $($card_node).find(".card-distance").text();
  var usernameClicked = $(this).closest(".card").find('.card-title').text();
  var url_for_like = $("main").data("like");
  console.log("clicked");
  console.log(usernameClicked);
  console.log($(this).closest(".card"));
  $.ajax
  (
    {
      url: url_for_like+usernameClicked,
      success: function(result)
      {
        if (result.success)
        {
          thisParent.html("<a class=\"waves-effect waves-teal btn deep-purple lighten-2\">Liked<i class=\"material-icons left\">done</i></a>")
          console.log(result.message);
          if(result.matched)
          {
            var $modal_node = $("#modalMatch");
            $($modal_node).find(".matched-username").text(usernameClicked);
            $($modal_node).find(".matched-distance").text(distanceClicked);
            $($modal_node).find("img").attr("src",pic);
            $('#modalMatch').modal('open');
          }
        }else{
          console.log(result.error);
        }
      }
    }
  );
});



$(".modal-filter").on("click",".modal-close", function(){
  $( ".match-cards").html("");
  $(".preloader-wrapper").css('display','block');
  // --------------------------------------
  var is_change = false;
  var age = $( ".btn.age-range" ).text().split("-");
  var ageMin = parseInt(age[0]);
  var ageMax = parseInt(age[1]);
  var modal = $(this).closest(".modal");
  if(modal.hasClass("looking-for-modal")){
    $node = $(modal).find("ul.select-dropdown li.active");
    if($node.size() > 0 ){
      $( ".btn.looking-for" ).text($($node).text().toLowerCase());
      is_change = true;
    }
  } else if (modal.hasClass("interested-in-modal")) {
    $node = $(modal).find("ul.select-dropdown li.active");
    if($node.size() > 0){
      $(".btn.interested-in").text($($node).text().toLowerCase());
      is_change = true;
    }
  } else if (modal.hasClass("age-range-modal")) {
    $node = $(modal).find(".input-field input");
    if($node.first().val() != ""){
      ageMin = $node.first().val();
      $node.first().val("");
      is_change = true;
    }
    if($node.last().val() != ""){
      ageMax = $node.last().val();
      $node.last().val("");
      is_change = true;
    }
  } else if (modal.hasClass("range-distance-modal")) {
    $node = $(modal).find(".input-field input");
    if($node.val() != ""){
      var temp = $node.val() < 1 ? 1 : $node.val();
      $(".btn.range-distance").text(temp);
      is_change = true;
      $node.val("");
    }
  }


  ageMax = ageMax < ageMin ? ageMin + 1 : ageMax;
  ageMin = ageMin > ageMax ? ageMin - 1 : ageMin;
  ageMin = ageMin < 18 ? 18 : ageMin;
  ageMax = ageMax < 18 ? 19 : ageMax;
  ageMin = ageMin > 99 ? 98 : ageMin;
  ageMax = ageMax > 99 ? 99 : ageMax;
  age = ageMin + " - " + ageMax;
  $(".btn.age-range").text(age);
  var lookingFor = $( ".btn.looking-for" ).text();
  var interestedIn = $( ".btn.interested-in" ).text();
  var rangeDistance = parseInt($( ".btn.range-distance" ).text());
  rangeDistance = rangeDistance < 1 ? 1 : rangeDistance;
  jsonData = JSON.stringify({'lookingFor':lookingFor, 'interestedIn':interestedIn, 'ageMax':ageMax, 'ageMin':ageMin, 'rangeDistance':rangeDistance});
  if(is_change){
    var url_for_filter = $("main").data("filter");
    $.ajax
    (
      {
        method: 'POST',
        url: url_for_filter,
        contentType: "application/json",
        data: jsonData,
        success: function(result)
        {
          console.log(result);
          if (result.success)
          {
            var matchesUsernames = result.matchesUsernames;
            var matchesPictures = result.matchesPictures;
            var matchesLocations = result.matchesLocations;
            var matchesAges = result.matchesAges;
            var matchesDistances = result.matchesDistances;
            var matchesLikes = result.matchesLikes;

            matchesUsernamesLength = matchesUsernames.length;
            htmlMatchCards = "";

            for (var i = 0; i < matchesUsernamesLength; i++)
            {
              username = matchesUsernames[i];
              // Create cards for each user

              htmlUser = "<div class=\"col m4\"><div class=\"card\"><div class=\"card-image\">";
              if ((typeof(matchesPictures[username]) !== 'undefined') && (matchesPictures[username] != ""))
              {
                htmlUser = htmlUser + "<img class=\"materialboxed\" data-caption=\""+username+"\" src=\""+matchesPictures[username]+"\">";
              }
              else
              {
                htmlUser = htmlUser + "<img src=\"../static/picture/no-pic.png\">";
              }

              htmlUser = htmlUser + "<span class=\"card-title\" style=\"width:100%; background: rgba(0, 0, 0, 0.5);\">"+username+"</span></div>";
              htmlUser = htmlUser + "<div class=\"center card-content\"><h5>"+ matchesAges[i]+" . "+matchesLocations[i] + "</h5>";
              htmlUser = htmlUser + "<h5>"+matchesDistances[i]+" km away from your location</h5></div>";
              htmlUser = htmlUser + "<div class=\"card-action center\">";
              if (matchesLikes[i] > 0)
              {
                htmlUser = htmlUser + "<a class=\"waves-effect waves-teal btn deep-purple lighten-2\">Liked<i class=\"material-icons left\">done</i></a>";
              }
              else
              {
                htmlUser = htmlUser + "<a class=\"waves-effect btn-flat no-like waves-purple\">Like</a>";
              }
              htmlUser = htmlUser + "</div></div></div>";
              htmlMatchCards = htmlMatchCards + htmlUser;
            }
            $( ".match-cards").html(htmlMatchCards);
            $('.materialboxed').materialbox();
            $(".preloader-wrapper").css('display','none');
          }
          else
          {
            console.log('Error in AJAX');
          }

        }
      }
    );
  }

});

$(".chips-container").on("click",".delete-tag",function() {
  if($(".chips-container .chip").length == 1){
    $(".filter-nav").css("height","64px");
  }
});

$(".advanced-search").on("click",function(){
  var has_advanced_filter = false;
  var append_values = "";
  var height_min = $("#modalAdvancedFilter .row select.filter-for-height-min").val();
  if (height_min) {
    if($(".chips-container div.min-height-tag").length < 1){
      append_values = append_values + "<div data-value='"+height_min+"' class='chip min-height-tag'>Min Height<i class='delete-tag close material-icons'>close</i></div>";
      has_advanced_filter = true;
    } else {
      $(".chips-container div.min-height-tag").data("value",height_min);
    }
  }
  var height_max = $("#modalAdvancedFilter .row select.filter-for-height-max").val();
  if (height_max) {
    if($(".chips-container div.max-height-tag").length < 1){
      append_values = append_values + "<div data-value='"+height_max+"' class='chip max-height-tag'>Max Height<i class='delete-tag close material-icons'>close</i></div>";
      has_advanced_filter = true;
    } else {
      $(".chips-container div.max-height-tag").data("value",height_max);
    }
  }
  var body_type = $("#modalAdvancedFilter .row select.filter-for-body-type").val();
  if (body_type) {
    if($(".chips-container div.body-type-tag").length < 1){
      append_values = append_values + "<div data-value='"+body_type+"' class='chip body-type-tag'>Body Type<i class='delete-tag close material-icons'>close</i></div>";
      has_advanced_filter = true;
    } else {
      $(".chips-container div.body-type-tag").data("value",body_type);
    }
  }
  var smoking = $("#modalAdvancedFilter .row select.filter-for-smoking").val();
  if (smoking) {
    if($(".chips-container div.smoking-tag").length < 1){
      append_values = append_values + "<div data-value='"+smoking+"' class='chip smoking-tag'>Smoking<i class='delete-tag close material-icons'>close</i></div>";
      has_advanced_filter = true;
    } else {
      $(".chips-container div.smoking-tag").data("value",smoking);
    }
  }
  var drinking = $("#modalAdvancedFilter .row select.filter-for-drinking").val();
  if (drinking) {
    if($(".chips-container div.drinking-tag").length < 1){
      append_values = append_values + "<div data-value='"+drinking+"' class='chip drinking-tag'>Drinking<i class='delete-tag close material-icons'>close</i></div>";
      has_advanced_filter = true;
    } else {
      $(".chips-container div.drinking-tag").data("value", drinking);
    }
  }
  var education = $("#modalAdvancedFilter .row select.filter-for-education").val();
  if (education) {
    if($(".chips-container div.education-tag").length < 1){
      append_values = append_values + "<div data-value='"+education+"' class='chip education-tag'>Education Level<i class='delete-tag close material-icons'>close</i></div>";
      has_advanced_filter = true;
    } else {
      $(".chips-container div.education-tag").data("value",education);
    }
  }
  if (has_advanced_filter) {
    $(".filter-nav").css("height","128px");
    $(".chips-container").append($(append_values));
  }


});
