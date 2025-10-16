document$.subscribe(function() {
    // find all splide elements
    var splides = document.getElementsByClassName('splide');
    for (var i = 0; i < splides.length; i++) {
        var splide = new Splide(splides[i], {
            type: 'slide',
            autoplay: false,
            arrows: true,
            pagination: false,
            direction: 'ltr',

            width: '100%',
            autoHeight: true,
            fixedWidth: 'max-content',
            trimspace: 'move',
            focus: 'center',

            drag: 'free',
            freeDrag: true,
            snap: false,
            
            lazyLoad: 'nearby',

            mediaQuery: 'max',
            breakpoints: {
                768: { // Mobile (max-width: 768px)
                    arrows: false,
                    direction: 'ttb',
                    height: '100%',
                    fixedWidth: '100%',
                    focus: undefined,
                    trimspace: true,
                    wheel: true,
                    releaseWheel: true,
                },
            },
        });
        splide.mount();
    }
});