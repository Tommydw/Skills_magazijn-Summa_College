// start WebSocket
var socket = io.connect('/hmi/onderhoud');

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
var warningGiven = false;
/* temp */
var oldTimeColor = document.querySelector('#time').style.color;

// als de screen-size word aangepast, word er opnieuw de verhouding berekend
window.addEventListener("orientationchange", function(event) {
    zoomScreen();
});

// wanneer op JSON switch geklikt word
const jsonInfo = document.getElementById('showJsonInfo')
jsonInfo.addEventListener('change', (event) => {
    if (event.currentTarget.checked) {
        // display json data
        document.querySelector('#data').style.position = 'relative';
        document.querySelector('#data').style.visibility = 'visible';
        document.querySelector('#data').style.height = 'fit-content';
        document.querySelector(".onderhoud").style.width = 'auto';
    } else {
        // hide json data
        document.querySelector('#data').style.position = 'absolute';
        document.querySelector('#data').style.visibility = 'hidden';
        document.querySelector('#data').style.height = '0';
        document.querySelector(".onderhoud").style.width = '-webkit-fill-available';
    }
});

// onderhoudsmodus de-/activeren
const devModeOnderhoud = document.getElementById('devModeOnderhoud')
devModeOnderhoud.addEventListener('change', (event) => {
    if (event.currentTarget.checked) {
        document.getElementById('devModeOnderhoud').checked = Jdata.state.devMode; // zet de switch weer uit
        socket.emit('devMode', true);
    } else {
        document.getElementById('devModeOnderhoud').checked = Jdata.state.devMode; // zet de switch weer aan
        socket.emit('devMode', false);
    }
});

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

// secondes naar tijd string
function secondsToTimeString(seconds) {
    return new Date(seconds * 1000).toISOString().substr(11, 8);
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

// pritty print
function syntaxHighlight(json) {
    if (typeof json != 'string') {
         json = JSON.stringify(json, undefined, 2);
    }
    json = json.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    return json.replace(/("(\\u[a-zA-Z0-9]{4}|\\[^u]|[^\\"])*"(\s*:)?|\b(true|false|null)\b|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?)/g, function (match) {
        var cls = 'number';
        if (/^"/.test(match)) {
            if (/:$/.test(match)) {
                cls = 'key';
            } else {
                cls = 'string';
            }
        } else if (/true/.test(match)) {
            cls = 'boolean-true'; 
        } else if (/false/.test(match)) {
                cls = 'boolean-false';
        } else if (/null/.test(match)) {
            cls = 'null';
        }
        return '<span class="' + cls + '">' + match + '</span>';
    });
}

// stuur een toggle request voor een output naar de server
function sendSate(name){
    if (Jdata.state.devMode){
        socket.emit('toggleSate', name);
    }
    else
    {
        console.warn('Enable devmode firts!');
        alert('Zet eerst developer modes aan om de outputs te kunnen schakelen')
    }

}

// zoom, voor blijvoorbeeld telefoons
function zoomScreen(){
//     var formWidth = document.getElementsByClassName('switch')[0].offsetWidth;
    if (screen.width - 15 < 380){
        document.getElementsByClassName('switch')[0].style.zoom = (screen.width - 15) / 380;
    }
    else
    {
        document.getElementsByClassName('switch')[0].style.zoom = 1;
    }
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
            const d = new Date();   // client tijd aanmaken
            oldClientTime = (d.getTime() / 1000) - (newtime - oldtime);     // client tijd min het verschil tussen de server updates
            updateDisplay();
            buttonEnable = !Jdata.state.order.orderActive; // maak de verzend button actief als er geen order is, en niet actief als er een order al geplaatst is
            // verberg loading
            $('#loading').hide();  
            // aantal active users weergeven.
            document.getElementById('users').innerHTML = Jdata.users.length;
            // print JSON data
            document.getElementById('data').innerHTML = syntaxHighlight(JSON.stringify(Jdata, null, 2)); // print JSON in html
            document.getElementById('devModeOnderhoud').checked = Jdata.state.devMode;
            // $('#content').show();        
            
            if (!warningGiven && Jdata.state.devMode){
                window.alert('Letop! In developer mode worden de outputs overschreden. En de inputs worden ook uitgelezen in een error state, het is dus mogelijk dat er een proces in werking treed!');
                warningGiven = true;
            }
        }
        else console.warn('Waiting for a full Jdata');
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
    $('.tooltipped').tooltip();
    zoomScreen();
    socket.on('connect', function() {
        // stuur socket_connect naar backend
        socket.emit('socket_connect');        
    }); 
});

// display de status
function updateDisplay(){
    // info
    document.querySelector('#state_timeState').textContent = secondsToTimeString(Jdata.time);
    if (Jdata.state.master) document.querySelector('#state_master').className = 'stateInfo led-blue-on';
    else document.querySelector('#state_master').className = 'stateInfo led-blue-off';

    if (Jdata.state.gpio) document.querySelector('#state_gpio').className = 'stateInfo led-blue-on';
    else document.querySelector('#state_gpio').className = 'stateInfo led-red-on';

    if (!Jdata.state.gpio) document.querySelector('#name_gpio').style.color = 'rgb(255 50 50)';
    else document.querySelector('#name_gpio').style.color = '#fff';
    
    if (Jdata.state.mcp1) document.querySelector('#state_mcp1').className = 'stateInfo led-blue-on';
    else document.querySelector('#state_mcp1').className = 'stateInfo led-red-on';

    if (!Jdata.state.mcp1) document.querySelector('#name_mcp1').style.color = 'rgb(255 50 50)';
    else document.querySelector('#name_mcp1').style.color = '#fff';
    
    if (Jdata.state.mcp2) document.querySelector('#state_mcp2').className = 'stateInfo led-blue-on';
    else document.querySelector('#state_mcp2').className = 'stateInfo led-red-on';

    if (!Jdata.state.mcp2) document.querySelector('#name_mcp2').style.color = 'rgb(255 50 50)';
    else document.querySelector('#name_mcp2').style.color = '#fff';
    
    if (Jdata.state.error) document.querySelector('#state_error').className = 'stateInfo led-red-on';
    else document.querySelector('#state_error').className = 'stateInfo led-green-off';

    if (Jdata.state.error) document.querySelector('#name_error').style.color = 'rgb(255 50 50)';
    else document.querySelector('#name_error').style.color = '#fff';
    
    if (Jdata.state.errorActive) document.querySelector('#state_errorActive').className = 'stateInfo led-blue-on';
    else document.querySelector('#state_errorActive').className = 'stateInfo led-blue-off';

    if (Jdata.state.errorActive) document.querySelector('#name_errorActive').style.color = 'rgb(255 50 50)';
    else document.querySelector('#name_errorActive').style.color = '#fff';
    
    if (Jdata.state.devMode) document.querySelector('#state_devMode').className = 'stateInfo led-blue-on';
    else document.querySelector('#state_devMode').className = 'stateInfo led-blue-off';

    document.querySelector('#state_cpu').textContent = String(Jdata.state.cpu[0]);
    

    // inputs
    if (Jdata.io.mcp1Noodstop) document.querySelector('#state_mcp1Noodstop').className = 'stateIO led-green-on';
    else document.querySelector('#state_mcp1Noodstop').className = 'stateIO led-green-off';

    if (Jdata.io.mag1) document.querySelector('#state_mag1').className = 'stateIO led-green-on';
    else document.querySelector('#state_mag1').className = 'stateIO led-green-off';

    if (Jdata.io.mag2) document.querySelector('#state_mag2').className = 'stateIO led-green-on';
    else document.querySelector('#state_mag2').className = 'stateIO led-green-off';

    if (Jdata.io.mag3) document.querySelector('#state_mag3').className = 'stateIO led-green-on';
    else document.querySelector('#state_mag3').className = 'stateIO led-green-off';

    if (Jdata.io.eind) document.querySelector('#state_eind').className = 'stateIO led-green-on';
    else document.querySelector('#state_eind').className = 'stateIO led-green-off';

    if (Jdata.io.MCP1_pi) document.querySelector('#state_MCP1_pi').className = 'stateIO led-green-on';
    else document.querySelector('#state_MCP1_pi').className = 'stateIO led-green-off';

    // inputs
    if (Jdata.io.mcp2Noodstop) document.querySelector('#state_mcp2Noodstop').className = 'stateIO led-green-on';
    else document.querySelector('#state_mcp2Noodstop').className = 'stateIO led-green-off';

    if (Jdata.io.PLCactief) document.querySelector('#state_PLCactief').className = 'stateIO led-green-on';
    else document.querySelector('#state_PLCactief').className = 'stateIO led-green-off';

    if (Jdata.io.PLCbusy) document.querySelector('#state_PLCbusy').className = 'stateIO led-green-on';
    else document.querySelector('#state_PLCbusy').className = 'stateIO led-green-off';

    if (Jdata.io.PLCerror) document.querySelector('#state_PLCerror').className = 'stateIO led-green-on';
    else document.querySelector('#state_PLCerror').className = 'stateIO led-green-off';

    if (Jdata.io.MCP2_pi) document.querySelector('#state_MCP2_pi').className = 'stateIO led-green-on';
    else document.querySelector('#state_MCP2_pi').className = 'stateIO led-green-off';



    // outputs
    if (Jdata.io.loopRun) document.querySelector('#state_loopRun').className = 'stateIO led-green-on';
    else document.querySelector('#state_loopRun').className = 'stateIO led-green-off';

    if (Jdata.io.scriptRun) document.querySelector('#state_scriptRun').className = 'stateIO led-orange-on';
    else document.querySelector('#state_scriptRun').className = 'stateIO led-orange-off';

    if (Jdata.io.error) document.querySelector('#state_error_io').className = 'stateIO led-red-on';
    else document.querySelector('#state_error_io').className = 'stateIO led-red-off';

    if (Jdata.io.cil1) document.querySelector('#state_cil1').className = 'stateIO led-orange-on';
    else document.querySelector('#state_cil1').className = 'stateIO led-orange-off';

    if (Jdata.io.cil2) document.querySelector('#state_cil2').className = 'stateIO led-orange-on';
    else document.querySelector('#state_cil2').className = 'stateIO led-orange-off';

    if (Jdata.io.cil3) document.querySelector('#state_cil3').className = 'stateIO led-orange-on';
    else document.querySelector('#state_cil3').className = 'stateIO led-orange-off';

    if (Jdata.io.motor) document.querySelector('#state_motor').className = 'stateIO led-orange-on';
    else document.querySelector('#state_motor').className = 'stateIO led-orange-off';

    if (Jdata.io.MCP1) document.querySelector('#state_MCP1').className = 'stateIO led-orange-on';
    else document.querySelector('#state_MCP1').className = 'stateIO led-orange-off';

    // outputs
    if (Jdata.io.deksel) document.querySelector('#state_deksel').className = 'stateIO led-orange-on';
    else document.querySelector('#state_deksel').className = 'stateIO led-orange-off';

    if (Jdata.io.muntje) document.querySelector('#state_muntje').className = 'stateIO led-orange-on';
    else document.querySelector('#state_muntje').className = 'stateIO led-orange-off';

    if (Jdata.io.Kleur1) document.querySelector('#state_Kleur1').className = 'stateIO led-orange-on';
    else document.querySelector('#state_Kleur1').className = 'stateIO led-orange-off';

    if (Jdata.io.Kleur2) document.querySelector('#state_Kleur2').className = 'stateIO led-orange-on';
    else document.querySelector('#state_Kleur2').className = 'stateIO led-orange-off';

    if (Jdata.io.check) document.querySelector('#state_check').className = 'stateIO led-orange-on';
    else document.querySelector('#state_check').className = 'stateIO led-orange-off';

    if (Jdata.io.MCP2) document.querySelector('#state_MCP2').className = 'stateIO led-orange-on';
    else document.querySelector('#state_MCP2').className = 'stateIO led-orange-off';
    
}