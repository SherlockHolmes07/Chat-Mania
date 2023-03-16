document.addEventListener('DOMContentLoaded', () => {
    // get the join button
    document.querySelectorAll('#join-btn').forEach(button => {
        button.onclick = () => { // when the button is clicked
            const roomId = button.value; // get the room id from the button
            const csrftoken = getCookie('csrftoken'); // get the csrf token from the cookie
            // send a POST request to the server
            fetch('/joinRoom', {
                method: 'POST',
                body: JSON.stringify({
                    room: roomId,
                }),
                headers: { "X-CSRFToken": csrftoken },
            })
            .then((response) => {
                console.log(response);
                if (response.status == 200) {
                    //disable the button
                    button.disabled = true;
                    button.innerHTML = "Requested";
                    // add to the buttons class
                    button.classList.add("disabled");

                }
             })
             .catch((error) => console.log(error));
        }
    })

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