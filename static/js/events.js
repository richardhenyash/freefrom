/**
* @fileOverview JavaScript Event Handler Library.
* @author <a href="https://github.com/richardhenyash">Richard Ash</a>
* @version 1.1.1
*/
/*jshint esversion: 6 */

// Initialisation Event Handlers //

// DataTables event handlers
$(document).ready(function() {
    $("#productsTable").DataTable();
} );
$(document).ready(function() {
    $("#reviewsTable").DataTable();
} );

// On load event handler for product view form to update rating stars
$("#product-view-form").ready(function() {
    let rating = $('input[name="rating"]');
    let ratingval
    if (rating) {
        let ratingval = parseInt(rating.val())
        if (ratingval == 1) {
            $("#star-1").removeClass("far fa-star").addClass("fas fa-star");
            $("#star-2").removeClass("far fa-star").addClass("far fa-star");
            $("#star-3").removeClass("far fa-star").addClass("far fa-star");
            $("#star-4").removeClass("far fa-star").addClass("far fa-star");
            $("#star-5").removeClass("far fa-star").addClass("far fa-star");
        } else if (ratingval == 2) {
            $("#star-1").removeClass("far fa-star").addClass("fas fa-star");
            $("#star-2").removeClass("far fa-star").addClass("fas fa-star");
            $("#star-3").removeClass("far fa-star").addClass("far fa-star");
            $("#star-4").removeClass("far fa-star").addClass("far fa-star");
            $("#star-5").removeClass("far fa-star").addClass("far fa-star");
        } else if (ratingval == 3) {
            $("#star-1").removeClass("far fa-star").addClass("fas fa-star");
            $("#star-2").removeClass("far fa-star").addClass("fas fa-star");
            $("#star-3").removeClass("far fa-star").addClass("fas fa-star");
            $("#star-4").removeClass("far fa-star").addClass("far fa-star");
            $("#star-5").removeClass("far fa-star").addClass("far fa-star");
        } else if (ratingval == 4) {
            $("#star-1").removeClass("far fa-star").addClass("fas fa-star");
            $("#star-2").removeClass("far fa-star").addClass("fas fa-star");
            $("#star-3").removeClass("far fa-star").addClass("fas fa-star");
            $("#star-4").removeClass("far fa-star").addClass("fas fa-star");
            $("#star-5").removeClass("far fa-star").addClass("far fa-star");
        } else if (ratingval == 5) {
            $("#star-1").removeClass("far fa-star").addClass("fas fa-star");
            $("#star-2").removeClass("far fa-star").addClass("fas fa-star");
            $("#star-3").removeClass("far fa-star").addClass("fas fa-star");
            $("#star-4").removeClass("far fa-star").addClass("fas fa-star");
            $("#star-5").removeClass("far fa-star").addClass("fas fa-star");
        }
    }
});

// On click event added to rating stars //
$("#star-5").click(function() {
    $("#star-1").removeClass("far fa-star").addClass("fas fa-star");
    $("#star-2").removeClass("far fa-star").addClass("fas fa-star");
    $("#star-3").removeClass("far fa-star").addClass("fas fa-star");
    $("#star-4").removeClass("far fa-star").addClass("fas fa-star");
    $("#star-5").removeClass("far fa-star").addClass("fas fa-star");
    $('input[name="rating"]').val(5);
});

$("#star-4").click(function() {
    $("#star-1").removeClass("far fa-star").addClass("fas fa-star");
    $("#star-2").removeClass("far fa-star").addClass("fas fa-star");
    $("#star-3").removeClass("far fa-star").addClass("fas fa-star");
    $("#star-4").removeClass("far fa-star").addClass("fas fa-star");
    $("#star-5").removeClass("fas fa-star").addClass("far fa-star");
    $('input[name="rating"]').val(4);
});

$("#star-3").click(function() {
    $("#star-1").removeClass("far fa-star").addClass("fas fa-star");
    $("#star-2").removeClass("far fa-star").addClass("fas fa-star");
    $("#star-3").removeClass("far fa-star").addClass("fas fa-star");
    $("#star-4").removeClass("fas fa-star").addClass("far fa-star");
    $("#star-5").removeClass("fas fa-star").addClass("far fa-star");
    $('input[name="rating"]').val(3);
});

$("#star-2").click(function() {
    $("#star-1").removeClass("far fa-star").addClass("fas fa-star");
    $("#star-2").removeClass("far fa-star").addClass("fas fa-star");
    $("#star-3").removeClass("fas fa-star").addClass("far fa-star");
    $("#star-4").removeClass("fas fa-star").addClass("far fa-star");
    $("#star-5").removeClass("fas fa-star").addClass("far fa-star");
    $('input[name="rating"]').val(2);
});

$("#star-1").click(function() {
    $("#star-1").removeClass("far fa-star").addClass("fas fa-star");
    $("#star-2").removeClass("fas fa-star").addClass("far fa-star");
    $("#star-3").removeClass("fas fa-star").addClass("far fa-star");
    $("#star-4").removeClass("fas fa-star").addClass("far fa-star");
    $("#star-5").removeClass("fas fa-star").addClass("far fa-star");
    $('input[name="rating"]').val(1);
});
