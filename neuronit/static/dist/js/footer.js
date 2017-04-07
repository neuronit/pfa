/**
 * Created by Xavier on 17/02/2017.
 */

// Window load event used just in case window height is dependant upon images
$(window).bind("load", function () {

    var footerHeight = 0,
        footerTop = 0,
        $footer = $("#footer");

    positionFooter();

    function positionFooter() {

        footerHeight = $footer.height();
        footerTop = ($(window).scrollTop() + $(window).height() - footerHeight) + "px";

        $footer.css({
            position: "absolute"
        })
        $footer.css({
            top: footerTop
        })

    }

    $(window)
        .scroll(positionFooter)
        .resize(positionFooter)

});
