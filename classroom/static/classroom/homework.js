document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('homework').style.display='block'
    document.getElementById('add').style.display='none'
   

    const add_button = document.getElementById('add_button')
    const homework_button = document.getElementById('homework_button')

    add_button.addEventListener('click', ()=> {
        console.log('add')
        document.getElementById('homework').style.display='none'
        document.getElementById('add').style.display='block'
    })
    homework_button.addEventListener('click', () => {
        console.log('homeworks')
        document.getElementById('homework').style.display='block'
        document.getElementById('add').style.display='none'
    })
});
