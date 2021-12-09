function updateDisplay(Jdata){
    document.getElementById('data').innerHTML = JSON.stringify(Jdata, null, 2); // print JSON in html
}

function sendOrder(){
    if (buttonEnable){
        buttonEnable = false;
        var rood = document.getElementById('Rood').checked;
        var zwart = document.getElementById('Zwart').checked;
        var zilver = document.getElementById('Zilver').checked;
        var deksel = document.getElementById('Deksel').checked;
        var munt = document.getElementById('Muntje').checked;
        var order = {'kleur': String(),
                    'deksel': Boolean(),
                    'muntje': Boolean()};
    
        if (rood) order.kleur = 'rood';
        else if (zwart) order.kleur = 'zwart';
        else if (zilver) order.kleur = 'zilver';
        else alert('Fout bij het verzenden van de order. Vernieuw de pagina A.U.B.');
        order.deksel = deksel;
        order.muntje = munt;
        console.log(order)
        socket.emit('order', order);
    }else console.log('Wachten op vorige bevestiging');
}

var motor = false;
function toggel(){
    if (motor){
        motor = false;
    }else{
        motor= true;
    }
    console.log(motor);
    socket.emit('motor', motor);
}
var cil1 = false;
function cilinder1(){
    if (cil1){
        cil1 = false;
    }else{
        cil1= true;
    }
    // console.log(cil1);
    socket.emit('cil1', cil1);
}
var cil2 = false;
function cilinder2(){
    if (cil2){
        cil2 = false;
    }else{
        cil2= true;
    }
    // console.log(cil2);
    socket.emit('cil2', cil2);
}
var cil3 = false;
function cilinder3(){
    if (cil3){
        cil3 = false;
    }else{
        cil3= true;
    }
    // console.log(cil3);
    socket.emit('cil3', cil3);
}