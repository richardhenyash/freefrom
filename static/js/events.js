/**
* @fileOverview JavaScript Event Handler Module.
* @author <a href="https://github.com/richardhenyash">Richard Ash</a>
* @version 1.1.1
*/
/*jshint esversion: 6 */

// Initialisation Event Handlers //

// DataTables event handlers

// Products Table
$(document).ready(function() {
    $("#productsTable").DataTable({
        // Fix width of rating column
        "columnDefs": [
            { "width": "6rem", "targets": 3 }
        ]
    });
});
// Reviews Table
$(document).ready(function() {
    $("#reviewsTable").DataTable({
        "columnDefs": [
            // Fix width of user name column
            { "width": "25%", "targets": 0 }
            // Fix width of rating column
            { "width": "6rem", "targets": 1 },
        ]
    });
});

// On load event handler for product view form to update rating stars
$("#product-view-form").ready(function() {
    let rating = $('input[name="rating"]');
    if (rating) {
        let ratingval = parseInt(rating.val());
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

// On Click Event Handlers //

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
