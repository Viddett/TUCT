const BtnPalette = document.querySelector('.btn-palette')
const BtnNextProg = document.querySelector('.btn-next-prog')
const BtnStartStop = document.querySelector('.btn-start-stop')

BtnPalette.addEventListener('click', () => { 
    alert("Clicked palette button")
});

BtnNextProg.addEventListener('click', () => { 
    alert("Clicked next program button")
});

BtnStartStop.addEventListener('click', () => { 
    alert("Clicked start stop button")
});