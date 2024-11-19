document.addEventListener('DOMContentLoaded', function() {
    
    const choice = document.getElementById('choice')
    const display = document.getElementById('class')
    display.style.display='none'

    
    choice.addEventListener('change', () => {
        console.log(choice.value);
        if(choice.value == "ST"){
            display.style.display='none'
        }
        else{
            display.style.display='block'
        }
    } )
});
