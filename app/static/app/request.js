document.addEventListener('DOMContentLoaded', () => {
    // get the join button
    document.querySelectorAll('#AcceptRequest').forEach(button => {
        button.onclick = () => { // when the button is clicked
            const requestId = button.value; // get the request id from the button
            const csrftoken = getCookie('csrftoken'); // get the csrf token from the cookie
         
            // send a POST request to the server
            fetch('/AcceptRequest', {
                method: 'POST',
                body: JSON.stringify({
                    requestId: requestId
                }),
                headers: { "X-CSRFToken": csrftoken },
            })
            .then((response) => {
                console.log(response);
                if (response.status == 200) {
                    // hide the elemet by the roomID
                    document.getElementById(`request${requestId}`).style.display = "none";
                }
             })
             .catch((error) => console.log(error));
        }
    })

    document.querySelectorAll('#RejectRequest').forEach(button => {
        button.onclick = () => { // when the button is clicked
            const requestId = button.value; // get the request id from the button
            const csrftoken = getCookie('csrftoken'); // get the csrf token from the cookie

             // send a POST request to the server
             fetch('/RejectRequest', {
                method: 'POST',
                body: JSON.stringify({
                    requestId: requestId
                }),
                headers: { "X-CSRFToken": csrftoken },
            })
            .then((response) => {
                console.log(response);
                if (response.status == 200) {
                    // hide the elemet by the roomID
                    document.getElementById(`request${requestId}`).style.display = "none";
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