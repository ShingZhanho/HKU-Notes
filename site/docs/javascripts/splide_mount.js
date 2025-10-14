document$.subscribe(function() {
    // find all splide elements
    var splides = document.getElementsByClassName('splide');
    for (var i = 0; i < splides.length; i++) {
        var splide = new Splide(splides[i], {
            type: 'slide',
            autoplay: false,
            trimSpace: false,
            padding: '10%',
        });
        splide.mount();
    }
});