$(document).ready(function() {
    var url = window.location.href;
    var activeCategoryID = url.substring(url.lastIndexOf('#') + 1);

    if (activeCategoryID) {
        $('.navbar-nav li').removeClass('active');
        $('.navbar-nav li').find('a[href="#' + activeCategoryID + '"]').parent().addClass('active');
    }
});
