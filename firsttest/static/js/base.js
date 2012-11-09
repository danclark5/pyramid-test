$(document).ready(function() {
    $(".alert-message").fadeIn(1000, function() {
    });
    $(".close").click(function() {
        $(this).parent(".alert-message").fadeOut(800, function(){});
    });

});

$(function centerPopup(){
    /* Taken from http://tuljo.com/web-development/center-popup-jquery */
	$('.centerPopup, .fence').each(function(){
		$(this).css('left',($(window).width()-$(this).outerWidth())/ 2 + 'px');
		$(this).css('top',($(window).height()-$(this).outerHeight())/ 2 + 'px');
	});
});
