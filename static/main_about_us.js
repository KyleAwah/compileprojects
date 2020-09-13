var blackout_bill = gsap.timeline({
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

blackout_bill
    .to('#websites_home', {
        opacity: 0
    })


var web_intro = gsap.timeline({
    scrollTrigger: {
        trigger: '.website_page_box_1',
        markers: true,
        start: "-250px top",
        end: "350px top",
        scrub: true,
        toggleActions: "restart pause reverse reverse"
    },
    defaults: {
        duration: 2,
        opacity: 0
    }
})

web_intro
    .from('.title_1', {
        y: 30,
        duration: 3
    })
   .from('.dev_img_holder', {
        x: 30
    })
    .from('.dev_para', {
        x: -30
    })










var web_intro_2 = gsap.timeline({
    scrollTrigger: {
        trigger: '.title_2',
        markers: true,
        start: "-250px top",
        end: "350px top",
        scrub: true,
        toggleActions: "restart pause reverse reverse"
    },
    defaults: {
        duration: 1,
        opacity: 0
    }
})

web_intro_2
    .from('.title_2', {
        y: 30
    })
    .from('#left_top', {
        x: -30
    })
    .from('#right_top', {
        x: 30
    })











var web_intro_3 = gsap.timeline({
    scrollTrigger: {
        trigger: '.title_3',
        markers: true,
        start: "-250px top",
        end: "350px top",
        scrub: true,
        toggleActions: "restart pause reverse reverse"
    },
    defaults: {
        duration: 1,
        opacity: 0
    }
})

web_intro_3
    .from('.title_3', {
        y: 30
    })
    .from('.flex_holder', {
        y: 30,
        stagger: 0.6
    })
    .from('.ready_title', {
        y: 30,
    })
   .from('#hold_call_to_action', {
        y: -30,
    })