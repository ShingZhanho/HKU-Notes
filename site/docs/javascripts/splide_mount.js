document$.subscribe(function() {
    // find all splide elements
    var splides = document.getElementsByClassName('splide');
    for (var i = 0; i < splides.length; i++) {
        var splide = new Splide(splides[i], {
            type: 'slide',
            direction: 'ltr',
            fixHeight: '77vh',
            autoWidth: true,
            autoplay: false,
            trimSpace: false,
            padding: '10%',
            pagination: false,
            breakpoints: {
                680: {
                    destroy: true
                }
            }
        });
        splide.mount();
    }
});