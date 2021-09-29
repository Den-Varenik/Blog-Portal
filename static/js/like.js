document.addEventListener('DOMContentLoaded', function(){
    const listLikeButtons = document.getElementsByName('postLike');
    const csrftoken = getCookie('csrftoken');

    listLikeButtons.forEach(elem => addEventListenerToLikeButton(elem, csrftoken));
});

function addEventListenerToLikeButton(likeButton, csrftoken) {
    likeButton.addEventListener('click', function () {
        $.ajax({
            url: window.location.origin+likeButton.value,
            type: "POST",
            headers: {
                "X-CSRFToken": csrftoken,
            },
            success: function (response) {
                console.log(response);
            },
            error: function (response) {
                console.log(response.responseJSON.errors);
            }
        });
    });
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}