document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('Send').onclick = () => {
        const message = document.getElementById('text-message').value;
        console.log(message);
        const roomId = document.getElementById('room_id').value;
        console.log(roomId);
        const username = document.getElementById('user_name').value;
        console.log(username);
        // clear the input field
        document.getElementById('text-message').value = '';
        
        const csrftoken = getCookie('csrftoken'); // get the csrf token from the cookie
        // send a POST request to the server
        fetch('/sendMessage', {
            method: 'POST',
            body: JSON.stringify({
                roomId: roomId,
                message: message,
            }),
            headers: { "X-CSRFToken": csrftoken },
        })
        .then((response) => {
            console.log(response);
         })
         .catch((error) => console.log(error));

    }
})

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '='))
            {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}