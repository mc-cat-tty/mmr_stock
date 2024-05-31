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

function createCard(request) {
  const card = document.createElement('div');
  card.className = 'shadow-sm card d-flex mb-3 p-1 ps-2 pe-2 text-bg-light align-middle';

  card.innerHTML = `
    <div class="row ms-1 text-muted font-monospace">
      ${request.profile_name}
      ${request.date}
      
      <p class="card-text ms-auto fw-bold col-sm-2 m-0 justify-content-center d-flex">
      ${request.quantity} PCS
      </p>
    </div>

    <div class="row">
      <div class="card-image col-sm-2 mb-1">
        <img
          class="card-img-left align-middle"
          src="${request.component_pic}"
          title="${request.component_name}"
          width="64px"
          height="64px"
        >
      </div>
      <p class="card-text col-sm-10 ps-2 pe-2 m-0">
        ${request.component_name.slice(0, 150) + (request.component_name.length > 150 ? "..." : "")}
        <br>
        ${request.component_code}
      </p>
    </div>

    <div class="ms-auto">
      <button type="button" class="btn btn-danger btn-sm" onclick="onClickRequest(this, ${request.id}, false)">Reject</button>
      <button type="button" class="btn btn-success btn-sm" onclick="onClickRequest(this, ${request.id}, true)">Approve</button>
    </div>
  `;

  return card;
}


function addRequest(request) {
  request = JSON.parse(request);
  let container = $("#request-container");
  container.prepend(createCard(request));
}