var options = [
{
  selector: '.end-match-cards', offset: 0, callback: function(el){
    getNewNodes()
    Materialize.scrollFire(options);
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
        if (result.success){
          var matchesUsernames = result.matchesUsernames;
          var matchesPictures = result.matchesPictures;
          var matchesLocations = result.matchesLocations;
          var matchesAges = result.matchesAges;
          var matchesDistances = result.matchesDistances;
          var matchesLikes = result.matchesLikes;
          matchesUsernamesLength = matchesUsernames.length;
          htmlMatchCards = "";
          alert("HERE");
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

            console.log(htmlMatchCards);
          }
          // $( ".match-cards").append(htmlMatchCards);
          $( ".end-match-cards").before(htmlMatchCards);
          $('.materialboxed').materialbox();
          $(".start-from").val(parseInt($(".start-from").val())+ 1);

        } else {
          console.log('Error in AJAX');
        }
      }
    }
  );
}

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
        }
        else
        {
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
      $( ".btn.looking-for" ).text($($node).text());
      is_change = true;
    }
  } else if (modal.hasClass("interested-in-modal")) {
    $node = $(modal).find("ul.select-dropdown li.active");
    if($node.size() > 0){
      $(".btn.interested-in").text($($node).text());
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
  ageMin = ageMin < 18 ? 18 : ageMin;
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
