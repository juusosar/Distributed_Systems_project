function handleCellClick(row, col) {
    let cell = document.getElementById('cell-' + row + '-' + col);

    if (cell.style.backgroundColor === 'grey')
        cell.style.backgroundColor = 'lightgrey'
    else cell.style.backgroundColor = 'grey'

//  let player = document.cookie
    let orientation = document.querySelector('input[name="orientation"]:checked')

    let temp;
    switch(orientation['id']) {
        case 'v':
            for (let i = 1; i < 4; i++) {
                temp = document.getElementById('cell-' + (row+i) + '-' + col)
                temp.style.backgroundColor = 'grey'
            }
            break
        case 'h':
            for (let i = 1; i < 4; i++) {
                temp = document.getElementById('cell-' + row + '-' + (col+i))
                temp.style.backgroundColor = 'grey'
            }
            break
    }

    // Send AJAX request to Flask server
    fetch('/cell_click', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({row: row,
                                    col: col,
                                    orientation: orientation['id']})
    }).then(response => {
        if (response.ok) {
            //console.log(response)
        } else {
            // Handle error response
        }
    }).catch(error => {
        console.error('Error:', error);
    });
}
