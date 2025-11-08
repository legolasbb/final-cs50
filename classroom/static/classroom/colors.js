document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('[name="grade"]').forEach( box => {
        const score = parseInt(box.dataset.score);
        if(box.className=="grade"){
            box.style.backgroundColor = `hsl(${score}, 100%, 40%)`;
        }
        else{
            box.style.color=`hsl(${score}, 100%, 40%)`;
        }
    })
});