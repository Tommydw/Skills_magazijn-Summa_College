document.getElementsByClassName('err-content')[0]
.addEventListener('click', function (event) {
    reload();
});
function reload(){
    document.getElementById("ricky").play();
    document.getElementById("rick").style.display = 'block';
    document.getElementsByClassName("err-page")[0].style.display = 'none';
}

function zoom(){
    if (screen.width - 37.5 < document.getElementsByClassName("main-message")[0].offsetWidth)
        document.querySelector(".main-message").style.width = String(screen.width - 2 * 37.5)+"px";
}
window.onload = function(){
    zoom();
    document.getElementsByClassName("bg")[0].style.display = 'flex';
}
window.addEventListener("orientationchange", function(event) {
    zoom();
});
