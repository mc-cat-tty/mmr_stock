const headers = { 'X-CSRFToken': '{{ csrf_token }}' };
const requst_card_classes = "shadow-sm card d-flex mb-3 p-1 ps-2 pe-2 text-bg-light align-middle"
const user_id = window.location.pathname.split("/").filter(x => !!x).pop()
var updates_ws = new WebSocket(`ws://localhost:8080/dash/updates/${user_id}`);

updates_ws.onmessage = msg => addRequest(msg.data);

function onClickRequest(caller, id, approved=false) {
  $.ajax({
    url: `/requests/${id}/`,
    type: "PUT",
    headers: headers,
    data: {'approved': approved},
    success: response => {
      $(caller)
        .parent().parent()
        .attr(
          "class",
          requst_card_classes
          + (response.approved ? ' bg-success-subtle' : ' bg-danger-subtle')
        );
      $(caller).parent().hide()
    }
  });
}

function addRequest(request) {
  request = Object.fromEntries(request)
  console.log(request)
  console.log(request.component_name)
}