function updateDisplay(){
    // document.getElementById('data').innerHTML = JSON.stringify(Jdata, null, 2); // print JSON in html
    if (Jdata.state.order.kleur == "rood"){
        document.getElementById('statusSystem').src = statusMagazijn[1].src;
        document.getElementById('blokie').src = blokje[0].src;
        document.getElementById('blokie').style.animation = 'blokje1 2s ease-out infinite';
        document.getElementById('orderInfo').textContent = 'Kleur: rood';
    }
    else if (Jdata.state.order.kleur == "zwart"){
        document.getElementById('statusSystem').src = statusMagazijn[2].src;
        document.getElementById('blokie').src = blokje[1].src;
        document.getElementById('blokie').style.animation = 'blokje2 2.5s ease-out infinite';
        document.getElementById('orderInfo').textContent = 'Kleur: zwart';
    }
    else if (Jdata.state.order.kleur == "zilver"){
        document.getElementById('statusSystem').src = statusMagazijn[3].src;
        document.getElementById('blokie').src = blokje[2].src;
        document.getElementById('blokie').style.animation = 'blokje3 3s ease-out infinite';
        document.getElementById('orderInfo').textContent = 'Kleur: zilver';
    }
    if (Jdata.state.order.muntje) document.getElementById('orderInfo').textContent = document.getElementById('orderInfo').textContent + ", met muntje";
    if (Jdata.state.order.deksel) document.getElementById('orderInfo').textContent = document.getElementById('orderInfo').textContent + ", met deksel";

    if (Jdata.io.mag1)
    {
        document.getElementById('magEen').style.display = 'block';
        document.getElementById('magEenText').style.display = 'block';
    }
    else
    {
        document.getElementById('magEen').style.display = 'none';
        document.getElementById('magEenText').style.display = 'none';
    }

    if (Jdata.io.mag2)
    {
        document.getElementById('magTwee').style.display = 'block';
        document.getElementById('magTweeText').style.display = 'block';
    }
    else
    {
        document.getElementById('magTwee').style.display = 'none';
        document.getElementById('magTweeText').style.display = 'none';
    }

    if (Jdata.io.mag3)
    {
        document.getElementById('magDrie').style.display = 'block';
        document.getElementById('magDrieText').style.display = 'block';
    }
    else
    {
        document.getElementById('magDrie').style.display = 'none';
        document.getElementById('magDrieText').style.display = 'none';
    }

    if (Jdata.state.stock.mag1 == 0){
        document.getElementById('Rood').disabled = true;
        if (document.getElementById('Rood').checked) document.getElementById('Rood').checked = false;
        document.getElementById('roodBox').style.display = 'none';
    } 
    else 
    {
        document.getElementById('roodBox').style.display = 'block';
        document.getElementById('Rood').disabled = false;
    }

    if (Jdata.state.stock.mag2 == 0){
        document.getElementById('Zwart').disabled = true;
        document.getElementById('zwartBox').style.display = 'none';
        if (document.getElementById('Zwart').checked) document.getElementById('Zwart').checked = false;
    } 
    else 
    {
        document.getElementById('zwartBox').style.display = 'block';
        document.getElementById('Zwart').disabled = false;
    }

    if (Jdata.state.stock.mag3 == 0){
        document.getElementById('Zilver').disabled = true;
        document.getElementById('zilverBox').style.display = 'none';
        if (document.getElementById('Zilver').checked) document.getElementById('Zilver').checked = false;
    } 
    else 
    {
        document.getElementById('zilverBox').style.display = 'block';
        document.getElementById('Zilver').disabled = false;
    }

}
function updateBlokje(){
    if (document.getElementById('Rood').checked) document.getElementById('hetBlokje').src = blokje[0].src;
    else if (document.getElementById('Zwart').checked) document.getElementById('hetBlokje').src = blokje[1].src;
    else if (document.getElementById('Zilver').checked) document.getElementById('hetBlokje').src = blokje[2].src;
    if (document.getElementById('Deksel').checked) document.getElementById('deDeksel').src = blokje[3].src;
    else if(document.getElementById('deDeksel').src != blokje[5].src) document.getElementById('deDeksel').src = blokje[5].src;
    if (document.getElementById('Muntje').checked) document.getElementById('hetMuntje').src = blokje[4].src;
    else if (document.getElementById('hetMuntje').src != blokje[5].src) document.getElementById('hetMuntje').src = blokje[5].src;
}

function warning(text){
    console.warn(text);
    alert(text);
}

function sendOrder(){
    var rood = document.getElementById('Rood').checked;
    var zwart = document.getElementById('Zwart').checked;
    var zilver = document.getElementById('Zilver').checked;
    var deksel = document.getElementById('Deksel').checked;
    var munt = document.getElementById('Muntje').checked;
    var order = {'kleur': String(),
                'deksel': Boolean(),
                'muntje': Boolean()};
    if (buttonEnable && 
        !Jdata.state.error && 
        !(Jdata.state.stock.mag1 == 0 && Jdata.state.stock.mag2 == 0 && Jdata.state.stock.mag3 == 0) &&
        (rood || zwart || zilver) &&
        !(!Jdata.state.master && !Jdata.io.PLCactief)
        )
    {
        buttonEnable = false;
    
        if (rood) order.kleur = 'rood';
        else if (zwart) order.kleur = 'zwart';
        else if (zilver) order.kleur = 'zilver';
        else alert('Fout bij het verzenden van de order. Vernieuw de pagina A.U.B.');
        order.deksel = deksel;
        order.muntje = munt;
        console.log(order)
        socket.emit('order', order);
    }
    else
    {
        if (Jdata.state.error){
            console.error('Server staat in error modus!');
            alert('Error modus is actief!');
        }
        else if(Jdata.state.stock.mag1 == 0 && Jdata.state.stock.mag2 == 0 && Jdata.state.stock.mag3 == 0)
            warning('Geen vooraad meer in het magazijnen');
        else if (!(rood || zwart || zilver)) 
            warning('Geen kleur geselecteerd!')
        else if (!Jdata.state.master && !Jdata.io.PLCactief)
            warning('PLC is nog niet klaar, wachten op PLCactief signaal');
        else 
            warning('Wachten op vorige bevestiging');
    }
        
}
