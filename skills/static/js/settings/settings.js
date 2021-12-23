// start WebSocket
var socket = io.connect('/settings');

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
var startingDone = false;
var warningGiven = false;


function clientTimeMS(){
    return (new Date().getTime() - (new Date().getTimezoneOffset() * 60 * 1000))
}

// onderhoudsmodus de-/activeren
const devModeOnderhoud = document.getElementById('devswitchtoggle')
devModeOnderhoud.addEventListener('change', (event) => {
    if (event.currentTarget.checked) {
        document.getElementById('devswitchtoggle').checked = Jdata.state.devMode; // zet de switch weer uit
        socket.emit('devMode', true);
    } else {
        document.getElementById('devswitchtoggle').checked = Jdata.state.devMode; // zet de switch weer aan
        socket.emit('devMode', false);
    }
});


const MasterSlaveChoice = document.getElementById('MasterSlaveToggle')
MasterSlaveChoice.addEventListener('change', (event) => {
    if (event.currentTarget.checked) {
        document.getElementById('MasterSlaveToggle').checked = Jdata.state.master; // zet de switch weer uit
        socket.emit('MasterSlave', true);
    } else {
        document.getElementById('MasterSlaveToggle').checked = Jdata.state.master; // zet de switch weer aan
        socket.emit('MasterSlave', false);
    }
});

const hotspotChoice = document.getElementById('WifiToggle')
hotspotChoice.addEventListener('change', (event) => {
    if (event.currentTarget.checked){var state = "aan";}
    else{var state = "uit";}
    if (confirm("Weet je zeker dat je de hotspot " + state + " wilt zetten, want de server zal even offline gaan."))
    {
        if (event.currentTarget.checked) {
            document.getElementById('WifiToggle').checked = Jdata.state.hotspotMode; // zet de switch weer uit
            socket.emit('hotspot', true);
        } else {
            document.getElementById('WifiToggle').checked = Jdata.state.hotspotMode; // zet de switch weer aan
            socket.emit('hotspot', false);
        } 
    }
});

function powerOff(){
    if (confirm("Weet je zeker dat je de server wilt uitzetten?"))
        socket.emit('shutdownActivate');
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
        if (Jdata.type == 'full') startingDone = true;
        if (startingDone){
            // console.log(Jdata.state.master);
            newtime = parseFloat(Jdata.time);   // nieuwe tijd opslaan
            updateTijd = waitTime + Jdata.users.indexOf(socket.id);
            oldClientTime = (clientTimeMS() / 1000) - (newtime - oldtime);     // client tijd min het verschil tussen de server updates
            // verberg loading
            $('#loading').hide();  
            // print JSON data
            document.getElementById('devswitchtoggle').checked = Jdata.state.devMode;
            document.getElementById('MasterSlaveToggle').checked = Jdata.state.master;
            document.getElementById('WifiToggle').checked = Jdata.state.hotspotMode;
            // $('#content').show();        
            
            if (!warningGiven && Jdata.state.devMode){
                window.alert('Letop! In developer mode worden de outputs overschreden. En de inputs worden ook uitgelezen in een error state, het is dus mogelijk dat er een proces in werking treed!');
                warningGiven = true;
            }
            if (Jdata.state.devMode){
                document.querySelector('#onderhoudtoggle').style.display='flex';
            }
            else{
                document.querySelector('#onderhoudtoggle').style.display='none';
            }

        }
        else console.warn('Waiting for a full Jdata');
    }
});

// start loop van 100ms
setInterval(()=> {
    // Update de tijd
    clientTime = clientTimeMS() / 1000;
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
