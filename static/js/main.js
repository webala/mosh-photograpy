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