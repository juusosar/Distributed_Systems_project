function handleCellClickSetup(row, col) {
    let cell = document.getElementById('cell-' + row + '-' + col);

    if (cell.style.backgroundColor === 'grey')
        cell.style.backgroundColor = 'lightgrey'
    else cell.style.backgroundColor = 'grey'

//  let player = document.cookie
    let orientation = document.querySelector('input[name="orientation"]:checked')
    let length = parseInt(document.getElementById("shiplength").textContent)
    let temp;
    switch(orientation['id']) {
        case 'v':
            for (let i = 1; i < length; i++) {
                temp = document.getElementById('cell-' + (row+i) + '-' + col)
                temp.style.backgroundColor = 'grey'
            }
            break
        case 'h':
            for (let i = 1; i < length; i++) {
                temp = document.getElementById('cell-' + row + '-' + (col+i))
                temp.style.backgroundColor = 'grey'
            }
            break
    }

    let data = {'col': col,
            'row': row,
            'orientation': orientation['id'],
            'length': length
    }

    sendClickRequest(data);
}

function sendClickRequest(data) {
    // Send AJAX request to Flask server
    fetch('/cell_click', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    }).then(response => {
        if (response.ok) {
           console.log(response.json())
            document.getElementById('shiplength').textContent = (data['length'] - 1).toString()
            if (data['length'] === 1){
                let shiptext = document.getElementById("shiptext")
                shiptext.innerHTML =
                    "<h3 id='shiptext'>All ships placed! Press start game to start looking for an opponent.</h3>"
                document.getElementById("startsetup").removeAttribute("hidden")
            }
        } else {
            // Handle error response
            console.log(response)
        }
    }).catch(error => {
        console.error('Error:', error);
    });
}