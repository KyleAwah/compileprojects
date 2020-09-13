var blackout_invoice = gsap.timeline({
    scrollTrigger: {
        trigger: '#invoicemaker_home',
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

blackout_invoice
    .to('#invoicemaker_home', {
        opacity: 0
    })

var blackout_web = gsap.timeline({
    scrollTrigger: {
        trigger: '#websites_home',
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

blackout_web
    .to('#websites_home', {
        opacity: 0
    })



var blackout_bill = gsap.timeline({
    scrollTrigger: {
        trigger: '#billmaker_home',
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

blackout_bill
    .to('#billmaker_home', {
        opacity: 0
    })





var web_intro = gsap.timeline({
    scrollTrigger: {
        trigger: '.website_page_box_1',
        start: "-250px top",
        end: "450px top",
        scrub: true,
        toggleActions: "restart pause reverse reverse"
    },
    defaults: {
        duration: 1,
        opacity: 0
    }
})

web_intro
    .from('#left_top', {
        x: -30
    })
    .from('#right_top', {
        x: 30
    })
    .from('#left_bottom', {
        x: -30
    })
    .from('#right_bottom', {
        x: 30
    })
    .from('.ready_in', {
        y: 30,
        stagger: .5
    })