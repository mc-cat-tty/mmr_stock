const headers = { 'X-CSRFToken': 'STUB' };
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
  request = JSON.parse(request);
  const card = `
  <div class="request-card shadow-sm card d-flex mb-3 p-1 ps-2 pe-2 text-bg-light align-middle STUB">
  <div class="row ms-1 text-muted font-monospace">
    STUB
    STUB
    STUB
    <p class="card-text ms-auto fw-bold col-sm-2 m-0 justify-content-center d-flex">
      <br> STUB PCS
    </p>
  </div>

  <div class="row">
    <div class="card-image col-sm-2">
      <img
        class="card-img-left align-middle"
        src="STUB"
        title="STUB"
        width="64px"
        height="64px"
      >
    </div>
    <p class="card-text col-sm-10 ps-2 pe-2 mb-1 m-0">
      STUB STUB
      <br>
      STUB
    </p>
  </div>
  STUB
  <div class="ms-auto">
    <button type="button" class="btn btn-danger btn-sm" onclick="onClickRequest(this, STUB, false)">Reject</button>
    <button type="button" class="btn btn-success btn-sm pb-1" onclick="onClickRequest(this, STUB, true)">Approve</button>
  </div>
  STUB
  </div>`;
  
  $("#request-container").append(card);
}