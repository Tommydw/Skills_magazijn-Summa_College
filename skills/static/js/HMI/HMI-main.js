// start WebSocket
var socket = io.connect('/hmi');

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
var startingDone = false;
/* temp */
var blokje;
var oldTimeColor = document.querySelector('#time').style.color;
/* get document data */
var oldSendButtonCLR = document.querySelector('#sendButton').style.getPropertyValue('--clr');
var oldSendButtonFGC = document.querySelector('#sendButton').style.getPropertyValue('--fgc');
var oldSendButtonText = document.querySelector('#sendButtonText').text;
/* animatie */
var blokieLocatie = ['translateX(-506px)', 'translateX(-758px)', 'translateX(-1006px)', 'translateX(0px)'];

// functie secondes naar tijd String
function sec2time(timeInSeconds) {
    if (timeInSeconds < 60)
        return new Date(timeInSeconds * 1000).toISOString().substring(17,23);
    // else return new Date(timeInSeconds * 1000).toISOString().substring(11,23);
    else return new Date(timeInSeconds * 1000).toISOString().substring(11,19);
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

// laad één foto in de cache
function preloadImage(name){
    const img = new Image();
    //const img = document.createElement('img');
    img.src = "../static/photos/" + name;
    return img
}

// zet een list van foto's in de cache
function preloadImages(images){
    for (var i = 0; i < images.length; i++){
        images[i] = preloadImage(images[i])
    }
    return images
}


// zoom, voor blijvoorbeeld telefoons
function zoomScreen(){
    var formWidth = document.getElementsByClassName('form')[0].offsetWidth;
    if (formWidth - 15 > screen.width){
        document.getElementsByClassName('form')[0].style.zoom = screen.width/(formWidth+15);
    }
    else
    {
        document.getElementsByClassName('form')[0].style.zoom = 1;
    }

    var statusWindowWidth = document.getElementsByClassName('statusBox')[0].offsetWidth;
    if (1000 > statusWindowWidth){
        document.getElementsByClassName('statusWindow')[0].style.zoom = statusWindowWidth / 1440;
    }
    else
    {
        document.getElementsByClassName('statusWindow')[0].style.zoom = 1000 / 1440;
    }
}

function clientTimeMS(){
    return (new Date().getTime() - (new Date().getTimezoneOffset() * 60 * 1000))
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
        if (Jdata.type == 'full') startingDone = true;
        if (startingDone){
            // console.log(Jdata);
            newtime = parseFloat(Jdata.time);   // nieuwe tijd opslaan
            updateTijd = waitTime + Jdata.users.indexOf(socket.id);
            oldClientTime = (clientTimeMS() / 1000) - (newtime - oldtime);     // client tijd min het verschil tussen de server updates
            updateDisplay();
            if (Jdata.state.error) buttonEnable = false; 
            else buttonEnable = !Jdata.state.order.orderActive; // maak de verzend button actief als er geen order is, en niet actief als er een order al geplaatst is
            // verberg loading
            $('#loading').hide();  
            // aantal active users weergeven.
            document.getElementById('users').innerHTML = Jdata.users.length;
            // print JSON data
            // document.getElementById('data').innerHTML = JSON.stringify(Jdata, null, 2); // print JSON in html
            // $('#content').show();
        
            // // stuur een connect request als de user niet meer op de lijst staat
            // if (Jdata.users.indexOf(socket.id) == -1){
            //     socket.emit('socket_connect');
            // }
        }
        else console.warn('Waiting for a full Jdata');
    }
});

// start loop van 100ms
setInterval(()=> {
    // Update de tijd
    clientTime = clientTimeMS() / 1000;
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

    try{
        if ( Jdata.state.error)
        {
                document.querySelector('#sendButton').style.setProperty('--clr', '#b00');
                document.querySelector('#sendButton').style.setProperty('--fgc', '#800');
                document.querySelector('#sendButtonText').text = 'Error mode!';
        }
        else
        {
            if (buttonEnable)
            {
                document.querySelector('#sendButton').style.setProperty('--clr', oldSendButtonCLR);
                document.querySelector('#sendButton').style.setProperty('--fgc', oldSendButtonFGC);
                document.querySelector('#sendButtonText').text = oldSendButtonText;
                document.getElementById('statusSystem').src = statusMagazijn[0].src;
            }
            else 
            {
                document.querySelector('#sendButton').style.setProperty('--clr', '#000');
                document.querySelector('#sendButton').style.setProperty('--fgc', '#111');
                document.querySelector('#sendButtonText').text = 'Verwerken...';
            }
        }
    }
    catch
    {
        buttonEnable = false;
        document.querySelector('#sendButton').style.setProperty('--clr', oldSendButtonCLR);
        document.querySelector('#sendButton').style.setProperty('--fgc', oldSendButtonFGC);
        document.querySelector('#sendButtonText').text = oldSendButtonText;
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
    zoomScreen();
    socket.on('connect', function() {
        // stuur socket_connect naar backend
        socket.emit('socket_connect');        
    }); 
    // laad de afbeeldingen in de cache
    blokje = preloadImages(['blokje/rood.png', 
                            'blokje/zwart.png', 
                            'blokje/zilver.png', 
                            'blokje/deksel.png', 
                            'blokje/muntje.png',
                            'blokje/niets.png']);
    statusMagazijn = preloadImages(['status/leeg.png',
                                    'status/mag1.png',
                                    'status/mag2.png',
                                    'status/mag3.png']);
    updateBlokje();       
    document.getElementById('statusSystem').src = statusMagazijn[0].src;
    document.getElementById('blokie').src = blokje[5].src;
});

// als de screen-size word aangepast, word er opnieuw de verhouding berekend
window.addEventListener("orientationchange", function(event) {
    zoomScreen();
});
