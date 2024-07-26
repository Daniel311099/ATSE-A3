URL_ = 'http://127.0.0.1:5000';

document.getElementById('loginForm').addEventListener('submit', function (e) {
    e.preventDefault();

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    fetch (URL_+'/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({username, password}),
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        if (data.status === 'success') {
            alert('Login successful!');
            localStorage.setItem('user_id', data.user_id);  // Save user_id in localStorage
            document.getElementById('login').style.display = 'none';
            document.getElementById('booking').style.display = 'block';
            loadSeatMap();
        } else {
            alert('Login failed!');
        }
    });
});

function loadSeatMap() {
    const seatMap = document.getElementById('seatMap');
    seatMap.innerHTML = '';
    for (let i = 0; i < 30; i++) {
        const seat = document.createElement('div');
        seat.classList.add('seat');
        seat.dataset.index = i;
        seat.addEventListener('click', selectSeat);
        seatMap.appendChild(seat);
    }
    // fetch available seats
    const flight_id = 1;
    const passenger_ids = [1, 2, 3];
    const url = new URL(URL_+`/seats/${flight_id}`);
    passenger_ids.forEach(id => url.searchParams.append('passenger_ids', id));
    fetch(url).then(response => response.json())
    .then(data => {
        console.log(data);
        data.forEach(seat => {
            const seatElement = document.querySelector(`.seat[data-index="${seat.index}"]`);
            seatElement.classList.add('locked');
        });
    });
}

function selectSeat(event) {
    const seat = event.target;
    if (seat.classList.contains('locked')) {
        return;
    }
    seat.classList.toggle('selected');
}

document.getElementById('confirmBooking').addEventListener('click', function () {
    const selectedSeats = document.querySelectorAll('.seat.selected');
    selectedSeats.forEach(seat => {
        seat.classList.remove('selected');
        seat.classList.add('locked');
    });
    // post selected seats to server
    alert('Seats booked successfully!');
});
