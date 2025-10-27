document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('[name="grade"]').forEach( box => {
        const score = parseInt(box.dataset.score);
        if (score <= 50) {
            hue = (score / 50) * 60;
        } else {
            hue = 60 + ((score - 50) / 50) * 30;  
        }
        if(box.className=="grade"){
            box.style.backgroundColor = `hsl(${hue}, 100%, 40%)`;
        }
        else{
            box.style.color=`hsl(${hue}, 100%, 40%)`;
        }
    })
});