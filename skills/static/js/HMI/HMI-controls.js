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