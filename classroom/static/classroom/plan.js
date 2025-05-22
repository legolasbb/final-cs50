document.addEventListener('DOMContentLoaded', function() {

    document.getElementById('plan_view').style.display ='block'
    document.getElementById('add_view').style.display = 'none'
    
    const add_button = document.getElementById("add_button")
    const plan_button = document.getElementById("plan_button")
    //change beetween plan view and add new lesson view
    //think about fetching when wanting to get plan
    add_button.addEventListener('click', ()=> {
        console.log('add')
        document.getElementById('plan_view').style.display ='none'
        document.getElementById('add_view').style.display = 'block'
    })
    plan_button.addEventListener('click', ()=> {
        console.log('plan')
        document.getElementById('add_view').style.display = 'none'
        document.getElementById('plan_view').style.display ='block'
    })
});
