// start WebSocket
var socket = io.connect('/');

// Om de hoeveel sec moet de client om een update vragen
var waitTime = 0.5;

var startupJson = JSON.parse('{"time":0}');
var Jdata = startupJson;
var Type = 'full';
var dataCount = 0;

let oldtime;
let oldClientTime = 0;
let newtime = 0;
let clientTime;

var connected = false;
var requested = false;
var buttonEnable = true;
var blokje;

var oldTimeColor = document.querySelector('#time').style.color;

// functie secondes naar tijd String
function sec2time(timeInSeconds) {
    var pad = function(num, size) { return ('000' + num).slice(size * -1); },
    time = parseFloat(timeInSeconds).toFixed(3),
    hours = Math.floor(time / 60 / 60),
    minutes = Math.floor(time / 60) % 60,
    seconds = Math.floor(time - minutes * 60),
    milliseconds = time.slice(-3);
    if (hours > 0){
        return pad(hours, 2) + ':' + pad(minutes, 2) + ':' + pad(seconds, 2) + '.' + pad(milliseconds, 3);
    }else if (minutes > 0){
        return pad(minutes, 2) + ':' + pad(seconds, 2) + '.' + pad(milliseconds, 3);
    }else{
        return pad(seconds, 2) + '.' + pad(milliseconds, 3) + ' Sec.';
    }
}

// Combineer de nieuwe data met de oude data
function mergeObject(oldObject, newObject){
    if (Jdata == startupJson || newObject.type == 'full'){
        oldObject = newObject;
        dataCount = 0;
    }
    else{
        Object.keys(newObject).forEach(function(x_itmes){
            if (typeof(newObject[x_itmes]) == 'object'){
                Object.keys(newObject[x_itmes]).forEach(function(i_items){
                    oldObject[x_itmes][i_items] = newObject[x_itmes][i_items];});
            }else{
                oldObject[x_itmes] = newObject[x_itmes];
            }
        });
    }
    return oldObject;
}


function preloadImage(name){
    const img = new Image();
    //const img = document.createElement('img');
    img.src = 'static/photos/' + name;
    return img
}

function preloadImages(images){
    for (var i = 0; i < images.length; i++){
        images[i] = preloadImage(images[i])
    }
    return images
}


// zoom voor blijvoorbeeld telefoons
function zoomScreen(){
    var formWidth = document.getElementsByClassName('form')[0].offsetWidth;
    if (formWidth - 15 > screen.width){
        document.getElementsByClassName('form')[0].style.zoom = screen.width/(formWidth+15);
    }
    else
    {
        document.getElementsByClassName('form')[0].style.zoom = 1;
    }
}

// krijg connected van server
socket.on('connected', () => {
    console.log('Websocket connected');
    socket.emit('get_data', Jdata, 'full');
    requested = true;
    connected = true;
});

// krijg data van server
socket.on('data', function(data){
    requested = false;
    dataCount++;
    oldtime = parseFloat(Jdata.time);   // oude tijd opslaan
    // nieuwe data omzetten
    Jdata = mergeObject(Jdata, JSON.parse(data));
    newtime = parseFloat(Jdata.time);   // nieuwe tijd opslaan
    updateTijd = waitTime + Jdata.users.indexOf(socket.id);
    //console.log(data);
    const d = new Date();   // client tijd aanmaken
    oldClientTime = (d.getTime() / 1000) - (newtime - oldtime);     // client tijd min het verschil tussen de server updates
    // document.getElementById('data').innerHTML = JSON.stringify(Jdata, null, 2); // print JSON in html
    updateDisplay(Jdata);
    $('#content').show();
    $('#loading').hide();  
    document.getElementById('users').innerHTML = Jdata.users.length;

    // if (Jdata.users.indexOf(socket.id) == -1){
    //     socket.emit('socket_connect');
    // }
});

// start loop van 100ms
setInterval(()=> {
    // Update de tijd
    const d = new Date();
    clientTime = d.getTime() / 1000;
    // huidige client tijd min de laatste update van de server
    document.getElementById('time').innerHTML = sec2time(clientTime-oldClientTime); 
    // controller of er om nieuwe data gevraagd kan worden
    if (connected && !requested){
        if (clientTime-oldClientTime > updateTijd ){
            requested = true;
            // Vraag om de 10 keer een volledige data update
            if (dataCount > 10) {
                Type = 'full';
                dataCount = 0;
            }
            else
                Type = 'small'
            socket.emit('get_data', Jdata, Type);
        }
    }
    if (clientTime-oldClientTime > 10) {
        document.querySelector('#time').style.color = 'red';
        document.querySelector('#timeText').style.color = 'red';
    }
    else
    {
        document.querySelector('#time').style.color = oldTimeColor;
        document.querySelector('#timeText').style.color = oldTimeColor;
    }
},100);

// stuur om de 10 sec een bericht naar der server om te bevestigen dat de client online is
setInterval(() => {
    if (connected) {
        socket.emit('update_user');
        // console.log('update');
    }

    if (Jdata.users.indexOf(socket.id) == -1 && connected){
        socket.emit('socket_connect');
    }
}, 10000);


// Klaar met laden
$(document).ready(function() {
    zoomScreen();
    socket.on('connect', function() {
        // stuur socket_connect naar backend
        socket.emit('socket_connect');        
    }); 
    blokje = preloadImages(['blokje/rood.png', 
                            'blokje/zwart.png', 
                            'blokje/zilver.png', 
                            'blokje/deksel.png', 
                            'blokje/muntje.png',
                            'blokje/niets.png']);
    updateBlokje();       
});

window.addEventListener("orientationchange", function(event) {
    zoomScreen();
});
