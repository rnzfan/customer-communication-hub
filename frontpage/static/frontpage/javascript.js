// Active Task
let active_task;

// Add events for each forms
const assign_form_nodes = document.querySelectorAll(".task_details>.assign_form");
assign_form_nodes.forEach((node) => {
    node.addEventListener("submit", (event) => {
        event.preventDefault();
        assignMember(event);
    })
});

const unassign_form_nodes = document.querySelectorAll(".task_details>.unassign_form");
unassign_form_nodes.forEach((node) => {
    node.addEventListener("submit", (event) => {
        event.preventDefault();
        unassignMember(event);
    })
});

async function unassignMember(event) {
    const page_number = event.srcElement[0].getAttribute("data-page")
    const response = await fetch("/unassign", {
        method: "POST",
        body: JSON.stringify({
          task_id: event.srcElement[0].value,
        }),
        headers: {'X-CSRFToken': csrftoken},
        mode: 'same-origin' // Do not send CSRF token to another domain.
    })
    const data = await response.json();

    // Reloading the page to reflect the change
    location = location.href + `?page=${page_number}`
}

async function assignMember(event) {
    const page_number = event.srcElement[1].getAttribute("data-page")
    const response = await fetch("/assign", {
        method: "POST",
        body: JSON.stringify({
          task_id: event.srcElement[1].value,
          member_id: event.srcElement[0].value
        }),
        headers: {'X-CSRFToken': csrftoken},
        mode: 'same-origin' // Do not send CSRF token to another domain.
    })
    const data = await response.json();

    // Reloading the page to reflect the change
    location = location.href + `?page=${page_number}`
}

function showTaskDetails(task_id) {
    if (active_task) {   
        document.querySelector(`#task_list_${active_task}`).style.border = "1px solid lightseagreen";
        document.querySelector(`#task_${active_task}`).style.display = "none";
        document.querySelector(`#draft_${active_task}`).style.display = "none";

    }
    document.querySelector(`#task_list_${task_id}`).style.border = "1px solid darkslateblue";
    document.querySelector(`#task_${task_id}`).style.display = "block";
    document.querySelector(`#draft_${task_id}`).style.display = "block";
    active_task = task_id;
    history.replaceState({"task_id": task_id}, "", `/task/${task_id}`); // Updated URL but not reloading the page
}

// Copy from Django Documentation:
// https://docs.djangoproject.com/en/4.0/ref/csrf/
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

