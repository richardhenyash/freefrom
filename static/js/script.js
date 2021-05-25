//  Event Handlers //

// On click event added to rating stars //
$("#star-5").click(function() {
    $("#star-1").removeClass("far fa-star").addClass("fas fa-star");
    $("#star-2").removeClass("far fa-star").addClass("fas fa-star");
    $("#star-3").removeClass("far fa-star").addClass("fas fa-star");
    $("#star-4").removeClass("far fa-star").addClass("fas fa-star");
    $("#star-5").removeClass("far fa-star").addClass("fas fa-star");
});

$("#star-4").click(function() {
    $("#star-1").removeClass("far fa-star").addClass("fas fa-star");
    $("#star-2").removeClass("far fa-star").addClass("fas fa-star");
    $("#star-3").removeClass("far fa-star").addClass("fas fa-star");
    $("#star-4").removeClass("far fa-star").addClass("fas fa-star");
    $("#star-5").removeClass("fas fa-star").addClass("far fa-star");
});

$("#star-3").click(function() {
    $("#star-1").removeClass("far fa-star").addClass("fas fa-star");
    $("#star-2").removeClass("far fa-star").addClass("fas fa-star");
    $("#star-3").removeClass("far fa-star").addClass("fas fa-star");
    $("#star-4").removeClass("fas fa-star").addClass("far fa-star");
    $("#star-5").removeClass("fas fa-star").addClass("far fa-star");
});

$("#star-2").click(function() {
    $("#star-1").removeClass("far fa-star").addClass("fas fa-star");
    $("#star-2").removeClass("far fa-star").addClass("fas fa-star");
    $("#star-3").removeClass("fas fa-star").addClass("far fa-star");
    $("#star-4").removeClass("fas fa-star").addClass("far fa-star");
    $("#star-5").removeClass("fas fa-star").addClass("far fa-star");
});

$("#star-1").click(function() {
    $("#star-1").removeClass("far fa-star").addClass("fas fa-star");
    $("#star-2").removeClass("fas fa-star").addClass("far fa-star");
    $("#star-3").removeClass("fas fa-star").addClass("far fa-star");
    $("#star-4").removeClass("fas fa-star").addClass("far fa-star");
    $("#star-5").removeClass("fas fa-star").addClass("far fa-star");
});
