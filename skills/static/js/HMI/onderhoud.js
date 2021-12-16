// start WebSocket
var socket = io.connect('/');

// Om de hoeveel sec moet de client om een update vragen
var waitTime = 0.5;

// init default values
/* Jdata | JSON */
var startupJson = JSON.parse('{"time":0}');
var Jdata = startupJson;
var Type = 'full';
var dataCount = 0;
/* time */
let oldtime;
let oldClientTime = 0;
let newtime = 0;
let clientTime;
/* status */
var connected = false;
var requested = false;
var buttonEnable = false;
/* temp */
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

// krijg connected van server, client is verbonden met de server
socket.on('connected', () => {
    console.log('Websocket connected');
    socket.emit('get_data', Jdata, 'full');
    requested = true;
    connected = true;
});

// krijg data van server, JSON data naat Jdata
socket.on('data', function(data){
    requested = false;
    dataCount++;
    oldtime = parseFloat(Jdata.time);   // oude tijd opslaan

    if (connected){
        // nieuwe data omzetten
        Jdata = mergeObject(Jdata, JSON.parse(data));
        // console.log(Jdata);
        newtime = parseFloat(Jdata.time);   // nieuwe tijd opslaan
        updateTijd = waitTime + Jdata.users.indexOf(socket.id);
        const d = new Date();   // client tijd aanmaken
        oldClientTime = (d.getTime() / 1000) - (newtime - oldtime);     // client tijd min het verschil tussen de server updates
        updateDisplay(Jdata);
        buttonEnable = !Jdata.state.order.orderActive; // maak de verzend button actief als er geen order is, en niet actief als er een order al geplaatst is
        // verberg loading
        $('#loading').hide();  
        // aantal active users weergeven.
        document.getElementById('users').innerHTML = Jdata.users.length;
        // print JSON data
        document.getElementById('data').innerHTML = JSON.stringify(Jdata, null, 2); // print JSON in html
        // $('#content').show();
    }
});


// start loop van 100ms
setInterval(()=> {
    // Update de tijd
    const d = new Date();
    clientTime = d.getTime() / 1000;
    // display huidige client tijd min de laatste update van de server
    document.getElementById('time').innerHTML = sec2time(clientTime-oldClientTime); 
    // controller of er om nieuwe data gevraagd kan worden
    if (connected && !requested){
        if (clientTime-oldClientTime > updateTijd ){
            requested = true;   // vraag maar één keer om een data request
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
    // als de laatste update meer dan 10 sec geleden is, word de text rood gemaakt
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
    // als de user niet in de lijst staat, stuur een connect request
    try
    {
        if (Jdata.users.indexOf(socket.id) == -1 && connected){
            socket.emit('socket_connect');
        }
    }
    catch 
    {
        console.warn("No user in Jdata");
        socket.emit('socket_connect');
    }
    
    // stuur een user beacon 
    if (connected) {
        socket.emit('update_user');
        // console.log('update');
    }
}, 10000);


// Klaar met laden
$(document).ready(function() {
    socket.on('connect', function() {
        // stuur socket_connect naar backend
        socket.emit('socket_connect');        
    }); 
});

function updateDisplay(Jdata){
    
}