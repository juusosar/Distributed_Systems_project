let ships = [];

function handleCellClickSetup(row, col) {
    let cell = document.getElementById('cell-' + row + '-' + col);
    let orientation = document.querySelector('input[name="orientation"]:checked')
    let length
    let temp
    let message = document.getElementById("invalid")

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
            ships.push([(row), col])
            for (let i = 1; i < length; i++) {
                temp = document.getElementById('cell-' + (row+i) + '-' + col)
                temp.style.backgroundColor = 'grey'
                ships.push([(row+i), col])
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
            ships.push([(row), col])
            for (let i = 1; i < length; i++) {
                temp = document.getElementById('cell-' + row + '-' + (col+i))
                temp.style.backgroundColor = 'grey'
                ships.push([row, (col+i)])
            }
            break
    }

    let data = {'col': col,
            'row': row,
            'orientation': orientation['id'],
            'length': length,
            'ship_indexes': ships
    }

    sendClickRequest(data);
}

async function handleShoot(row, col) {
    let cell = document.getElementById('op-cell-' + row + '-' + col);
    let data = {'col': col,
            'row': row
    }
    console.log(await sendShootRequest(data, cell))
}

function sendClickRequest(data) {
    // Send Click event to Flask server
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
                    "<h3 id='shiptext'>All ships placed!<br>Press 'Find Game' to start looking for an opponent.</h3>"
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

function sendShootRequest(data, cell) {
    fetch('/shoot', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    }).then(response => {
        if (response.ok) {
            return response.json()
        } else {
            console.log(response)
        }
    }).then(shoot_action => {
        let shoot_data = shoot_action
        console.log(shoot_data);
        for (let i = 0; i < shoot_data['hits'].length; i++) {
            console.log(shoot_data['hits'])
            if (shoot_data['row'] === shoot_data['hits'][i][0] && shoot_data['col'] === shoot_data['hits'][i][1]) {
                cell.style.backgroundColor = 'red'
            } else {
                cell.style.backgroundColor = 'grey'
            }
        }
        document.getElementById('turn').textContent = "It's the opponents turn!"
        return fetch('/turn');
    }).catch(error => {
        console.error('Error:', error);
    });
}
