const btn = document.querySelector('.btn')

var colorArray = ['#FF0000', '#00FF00', '#0000FF']
var colorCounter = 0

btn.addEventListener('click', () => { 
    colorCounter++
    if (colorCounter >= colorArray.length) {
        colorCounter = 0
    }
    //btn.style.backgroundColor = colorArray[colorCounter]
    //btn.style.boxShadow = '0 0 20px' + colorArray[colorCounter]
});