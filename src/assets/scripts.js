window.onscroll = function() {scrollFunction()};

function scrollFunction() {
    if (document.documentElement.scrollTop > 1500) {
        document.getElementById("scroll-up-button").style.display = "block";
    } else {
        document.getElementById("scroll-up-button").style.display = "none";
    }
}