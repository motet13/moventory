const scanIN = document.querySelector('#qr-input');
const scanOUT = document.querySelector('#qr-output');

scanIN.addEventListener('keyup', (e) => {
    e.preventDefault();

    let list = document.createElement('li');
    let span = document.createElement('span');
    let spanValue = document.createTextNode('highlight_off');

    res.forEach((prod) => {
        prodName = prod.product_name
        prodId = prod.id.toString()
        encodeScanINValue = prodName.slice(0,3).toUpperCase()

        if (prodId.length == 1) {encodedINValue = `${encodeScanINValue}00${prodId}`;} 
        else if (prodId.length == 2) {encodedINValue = `${encodeScanINValue}0${prodId}`;}
        else {encodedINValue = `${encodeScanINValue}${prodId}`;}

        if (encodedINValue === scanIN.value.toUpperCase() && scanIN.value.length == 6) {
            let outProdName = document.createTextNode(`${prodName}
                (current: ${prod.quantity},
                type: ${prod.product_type},
                prize: ${prod.price})
                `);
            
            span.classList.add('material-icons');

            // Style list
            list.classList.add('scanOUTStyle');
    
            list.appendChild(outProdName);
            span.appendChild(spanValue);
            list.appendChild(span);
            scanOUT.appendChild(list);
            scanIN.select();
            
        }
    });
            // remove scanINValue
        // scanIN.value = '';
});


// Delete product
scanOUT.addEventListener('click', e => {
    if (e.target.textContent === 'highlight_off') {
        e.target.parentElement.remove();
    }
});
