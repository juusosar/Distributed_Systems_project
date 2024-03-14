let ships = [];

function handleCellClickSetup(row, col) {
    let cell = document.getElementById('cell-' + row + '-' + col);
    let orientation = document.querySelector('input[name="orientation"]:checked')
    let length
    let temp
    let message = document.getElementById("invalid")
    let userid = document.cookie.split('=')[1]

    if (parseInt(document.getElementById("shiplength").textContent) === null) return
    else length = parseInt(document.getElementById("shiplength").textContent)

    if (cell.style.backgroundColor === 'grey') {
        message.removeAttribute("hidden")
        return
    }
    else cell.style.backgroundColor = 'grey'

    switch(orientation['id']) {
        
        case 'v':
            console.log(row, length)
            if (row + length > 10){
                message.removeAttribute("hidden")
                cell.style.backgroundColor = "lightgrey"
                return
            }
            for (let i = 0; i < length; i++) {
                for (let j = 0; j < ships.length; j++) { 
                    if (ships[j][0] === (row + i) && ships[j][1] === (col)) {
                        message.removeAttribute("hidden")
                        cell.style.backgroundColor = "lightgrey"
                        return
                    }
                }
            }
            message.setAttribute("hidden", "")
            ships.push([(row), col, userid])
            for (let i = 1; i < length; i++) {
                temp = document.getElementById('cell-' + (row+i) + '-' + col)
                temp.style.backgroundColor = 'grey'
                ships.push([(row+i), col, userid])
            }
            break
        case 'h':
            console.log(col, length)
            if (col + length > 10){
                message.removeAttribute("hidden")
                cell.style.backgroundColor = "lightgrey"
                return
            }
            for (let i = 0; i < length; i++) {
                for (let j = 0; j < ships.length; j++) {
                    if (ships[j][0] === (row) && ships[j][1] === (col + i)) {
                        message.removeAttribute("hidden")
                        cell.style.backgroundColor = "lightgrey"
                        return
                    }
                }
            }
            message.setAttribute("hidden", "")
            ships.push([(row), col, userid])
            for (let i = 1; i < length; i++) {
                temp = document.getElementById('cell-' + row + '-' + (col+i))
                temp.style.backgroundColor = 'grey'
                ships.push([row, (col+i), userid])
            }
            break
    }
    console.log(ships)

    let data = {'col': col,
            'row': row,
            'orientation': orientation['id'],
            'length': length,
            'ship_indexes': ships
    }

    sendClickRequest(data);
}

function handleShoot(row, col) {
    let cell = document.getElementById('cell-' + row + '-' + col);

    let data = {'col': col,
            'row': row
    }
    sendShootRequest(data);
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
                    "<h3 id='shiptext'>All ships placed!\n Press 'Find Game' to start looking for an opponent.</h3>"
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


function sendShootRequest(data) {
    // Send AJAX request to Flask server
    fetch('/shoot', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    }).then(response => {
        if (response.ok) {
            console.log(response.json())
        } else {
            // Handle error response
            console.log(response)
        }
    }).catch(error => {
        console.error('Error:', error);
    });
}