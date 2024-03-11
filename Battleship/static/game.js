function handleCellClick(row, col) {
    let cell = document.getElementById('cell-' + row + '-' + col);
    // Toggle cell color
//    if (cell.backgroundColor === 'lightgray') {
//        cell.backgroundColor = 'blue'; // Change to desired color
//    } else {
 //       cell.backgroundColor = 'lightgray';
 //   }
    let player = document.cookie

    // Send AJAX request to Flask server
    fetch('/cell_click', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({row: row, col: col, player: player})
    }).then(response => {
        if (response.ok) {
            // Handle successful response
            console.log(response)
        } else {
            // Handle error response
        }
    }).catch(error => {
        console.error('Error:', error);
    });
}
