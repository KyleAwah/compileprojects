var blackout_home = gsap.timeline({
    scrollTrigger: {
        trigger: '#main',
        start: "100px top",
        end: "700px top",
        scrub: true,
        toggleActions: "restart pause reverse reverse"
    },
    defaults: {
        duration: 1,
        opacity: 0
    }
})

blackout_home
    .to('#main', {
        opacity: 0
    })

var blackout_website = gsap.timeline({
    scrollTrigger: {
        trigger: '.content_box_1',
        start: "-250px top",
        end: "top top",
        scrub: true,
        toggleActions: "restart pause reverse reverse"
    },
    defaults: {
        duration: 1,
        opacity: 0
    }
})

blackout_website
    .from('.content_box_1', {
        opacity: 0
    })
    .from('.web_text', {
        y: 40,
        stagger: 0.4,
    })

var homepage_tl = gsap.timeline({
    scrollTrigger: {
        trigger: '#main'
    },
    defaults: {
        duration: 1,
        opacity: 0
    }
})

homepage_tl
    .from('.word_intro', {
        delay: 0.4,
        x: -50,
        stagger: 0.8,
    })

    .from('.main_home_in', {
        y: -50,
        stagger: 0.4,
    })

    .from('.menu_in', {
        x: 50,
        stagger: 0.4
    })

    .from('label', {
        x: 50
    })
    
    .from('#nav_logo', {
        x: -50
    }, "-=2.0")

    .from('#scroll_down', {
        delay: 0.4,
        y: -50,
        ease: 'elastic(1, 0.3)'
    })






var bill_tl = gsap.timeline({
    scrollTrigger: {
        trigger: '.content_box_3',
        start: "-500px top",
        end: "top top",
        scrub: true,
        toggleActions: "restart pause reverse reverse"
    },
    defaults: {
        duration: 1,
        opacity: 0
    }
})

bill_tl
    .from('.bill_words', {
        y: 50,
        stagger: 0.8,
    })
    .from('#comp_filled', {
        y: -50,
    })