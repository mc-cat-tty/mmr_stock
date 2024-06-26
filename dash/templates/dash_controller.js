const headers = { 'X-CSRFToken': '{{ csrf_token }}' };
const requst_card_classes = "shadow-sm card d-flex mb-3 p-1 ps-2 pe-2 text-bg-light align-middle"
const user_id = window.location.pathname.split("/").filter(x => !!x).pop()

var updates_ws = new WebSocket(`ws://${window.location.host}/dash/updates/${user_id}`);
updates_ws.onmessage = msg => onMessage(msg.data);

function onClickRequest(caller, id, approved=false) {
  $.ajax({
    url: `/requests/${id}/`,
    type: "PUT",
    headers: headers,
    data: {'approved': approved}
  });
}

function onMessage(data) {
  data = JSON.parse(data);
  const action = data.action;
  
  switch (action) {
    case 'add':
      let container = $("#request-container");
      container.prepend(createCard(data.content));
      break;
    case 'approve':
      let logcontainer = $("#log-container");
      let logcard = $(`#request-card-${data.id}`).clone();
      logcard.attr('id', '');
      logcard.find(".request-action-buttons").hide();
      logcard.find(".request-state").html('');
      logcontainer.find("#log-container-separator").show()
      logcontainer.prepend(logcard);
      setOutcome(data.id, true);
      break;
    case 'reject':
      setOutcome(data.id, false);
      break;
  }

}

function setOutcome(id, approved=false) {
  $(`#request-card-${id}`).attr(
    'class',
    requst_card_classes +
    (approved ? ' bg-success-subtle' : ' bg-danger-subtle')
  )

  $(`#request-card-${id}`).find(".request-action-buttons").hide()
  $(`#request-card-${id}`).find(".request-state").html(approved ? "Approved" : "Rejected");
}

function createCard(request) {
  const card = document.createElement('div');
  card.className = requst_card_classes;
  card.id = `request-card-${request.id}`;
  const request_state = ({
    true: "Approved",
    false: "Rejected"
  })[request.approved] || "Pending";

  card.innerHTML = `
    <div class="row ms-1 text-muted font-monospace">
      ${request.profile_name}
      ${request.date}

      <p class="card-text ms-auto col-sm-2 m-0 justify-content-center d-flex request-state">
        ${request_state}
      </p>
      
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

    <div class="ms-auto request-action-buttons">
      <button type="button" class="btn btn-danger btn-sm" onclick="onClickRequest(this, ${request.id}, false)">Reject</button>
      <button type="button" class="btn btn-success btn-sm" onclick="onClickRequest(this, ${request.id}, true)">Approve</button>
    </div>
  `;

  return card;
}