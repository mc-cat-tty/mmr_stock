const modal = $('#componentModal');
const fieldsContainer = modal.find("#fieldsContainer");
const State = Object.freeze({
  VIEW: 'view',
  EDIT: 'edit'
});
const alertHtml =
  '<div class="alert alert-danger d-flex align-items-center mt-4" role="alert" id="banner">'
  + '<i class="bi bi-exclamation-circle me-2" width="24" height="24" role="img"></i>'
  + '<div id="failedOperation"> Failed update </div>'
  + '</div>';
var fields;
var state = State.VIEW;
var currentId;
const headers = {'X-CSRFToken': '{{ csrf_token }}'};

function toEditMode () {
  state = State.EDIT;

  fields.forEach(
    field => modal
      .find(`#${field}Value`)
      .attr('class', 'form-control')
      .attr('readonly', false)
  );

  ['delBtn', 'editBtn'].forEach(id => modal.find(`#${id}`).hide());
  modal.find('#saveBtn')
    .attr('class', 'btn btn-info')
    .html('Save changes')
}

function toViewMode () {
  fields.forEach(
    field => modal
      .find(`#${field}Value`)
      .attr('class', 'form-control-plaintext')
      .attr('readonly', true)
  );

  ['delBtn', 'editBtn'].forEach(id => modal.find(`#${id}`).show());
  modal.find('#saveBtn')
    .attr('class', 'btn btn-primary')
    .html('Update quantity')

  state = State.VIEW;
}

function addBanner(message) {
  if (!modal.find("#failedOperation").length) modal.find("#body").append(alertHtml)
  modal.find("#failedOperation").html(message)
}

function onClickComponentCard (caller, id) {
  modal.modal('show');

  $.ajax({
    url: `/components/${id}`,
    type: 'GET',
    success: dynPopulate,
    error: () => {
      addBanner("Server not available");
      fieldsContainer.hide();
    }
  });

  currentId = id;
}

function dynPopulate (json_response) {
  fields = Object.keys(json_response);

  Object.entries(json_response).forEach(
    ([field, value]) => modal.find(`#${field}Value`).val(value)
  );

  Object.entries(json_response)
    .filter(([field, value]) => !value)
    .forEach(
      ([field, value]) => modal.find(`#${field}Value`).val('-')
    )
  
  modal.find('#title').html(json_response.code);
  modal.find('#picture').attr('src', json_response.picture);
  modal.find('#lock').css('visibility', json_response.protection ? 'visible' : 'hidden');
  
  modal.find("#banner").remove();
  fieldsContainer.show();
  toViewMode();
}

function onClickEdit (caller) {
  toEditMode();
}

function getModalData() {
  return Object.fromEntries(
    fields
      .map(field => [field, $(`#${field}Value`).val()])
      .filter(([field, val]) => !!val)
  );
}

function onClickSave (caller) {
  switch (state) {
    case State.EDIT:
      $.ajax({
        url: `/components/${currentId}/`,
        type: 'PUT',
        headers: headers,
        data: {pk: currentId, ...getModalData()},
        error: (response) => addBanner(response.responseText)
      });
      toViewMode();
      break;

    case State.VIEW:
      modal.modal('hide');
      break;
  }
  toViewMode();
}

function onClickCancel (caller) {
  switch (state) {
    case State.EDIT:
      toViewMode();
      break;
    case State.VIEW:
      toViewMode();
      modal.modal('hide');
      break;
  }
}

function onClickDel (caller) {

}

function onClickStar(caller, event, id) {
  event.stopPropagation();

  const data = {component_pk: id};
  
  $.ajax({
    url: 'analytics/favorites/',
    type: 'POST',
    headers: headers,
    data: data,
    success: (response) => {
      if (response.status) {
        $(`.starred-badge-component-${id}`).show();
        $(`.unstarred-badge-component-${id}`).hide();
      }
      else {
        $(`.starred-badge-component-${id}`).hide();
        $(`.unstarred-badge-component-${id}`).show();
      }
    }
  });

}
