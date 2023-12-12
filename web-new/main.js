const btnPalette = document.querySelector('.btn-palette')
const btnNextProg = document.querySelector('.btn-next-prog')
const btnStartStop = document.querySelector('.btn-start-stop')

btnPalette.addEventListener('click', () => { 
    alert("Clicked palette button")
});

btnNextProg.addEventListener('click', () => { 
    alert("Clicked next program button")
});

btnStartStop.addEventListener('click', () => { 
    alert("Clicked start stop button")
});