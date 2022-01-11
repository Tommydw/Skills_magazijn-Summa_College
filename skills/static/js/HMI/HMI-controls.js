function updateDisplay(){
    // document.getElementById('data').innerHTML = JSON.stringify(Jdata, null, 2); // print JSON in html
    if (Jdata.state.order.kleur == "rood") document.getElementById('statusSystem').src = statusMagazijn[1].src;
    else if (Jdata.state.order.kleur == "zwart") document.getElementById('statusSystem').src = statusMagazijn[2].src;
    else if (Jdata.state.order.kleur == "zilver") document.getElementById('statusSystem').src = statusMagazijn[3].src;
}
function updateBlokje(){
    if (document.getElementById('Rood').checked) document.getElementById('hetBlokje').src = blokje[0].src;
    else if (document.getElementById('Zwart').checked) document.getElementById('hetBlokje').src = blokje[1].src;
    else if (document.getElementById('Zilver').checked) document.getElementById('hetBlokje').src = blokje[2].src;
    if (document.getElementById('Deksel').checked) document.getElementById('deDeksel').src = blokje[3].src;
    else document.getElementById('deDeksel').src = blokje[5].src;
    if (document.getElementById('Muntje').checked) document.getElementById('hetMuntje').src = blokje[4].src;
    else document.getElementById('hetMuntje').src = blokje[5].src;
}

function sendOrder(){
    if (buttonEnable && !Jdata.state.error){
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
    }else if (Jdata.state.error){
        console.error('Server staat in error modus!');
        alert('Error modus is actief!');
    }
    else console.log('Wachten op vorige bevestiging');
}
