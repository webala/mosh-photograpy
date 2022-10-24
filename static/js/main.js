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
const csrftoken = getCookie('csrftoken');


//This function sends data to the backend
const postData = async (data, endpoint) => {
    const res = await fetch(endpoint, {
        method: 'POST',
            // credentials: "same-origin",
            headers: {
                'Content-Type': 'application/json',
                // "Accept": "application/json",
                'X-CSRFToken': csrftoken,

            },
            body: JSON.stringify(data)
    })
    const jsonResponse = await res.json()
    return jsonResponse
}

//Navigatio toggle functionality
const nav = document.querySelector('.nav-items')
const navBtn = document.querySelector('.nav-btn')

navBtn.addEventListener('click', () => {
    nav.classList.toggle('active')
})