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
var state = State.VIEW;
var currentId;
const textualFields = [ {% for field in modal_textual_fields %} "{{ field.name }}",  {% endfor %} ];
const numericFields = [ {% for field in modal_numeric_fields %} "{{ field.name }}",  {% endfor %} ];
const booleanFields = [ {% for field in modal_boolean_fields %} "{{ field.name }}",  {% endfor %} ];
const fields = textualFields.concat(numericFields);
const headers = { 'X-CSRFToken': '{{ csrf_token }}' };

function onClickComponentCard(caller, id) {
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

  $('#getComponentsValue').val('');
  currentId = id;
}

function onClickAdd(caller) {
  toEditMode();
}

function onClickEdit(caller) {
  toEditMode();
}

function onClickSave(caller) {
  switch (state) {
    case State.EDIT:
      $.ajax({
        url: `/components/${currentId}/`,
        type: 'PUT',
        headers: headers,
        data: { pk: currentId, ...getModalData() },
        success: () => removeBanner(),
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

function onClickCancel(caller) {
  switch (state) {
    case State.EDIT:
      toViewMode();
      break;
    case State.VIEW:
      modal.modal('hide');
      break;
  }
}

function onClickDel(caller) {
  $.ajax({
    url: `/components/${currentId}/`,
    type: 'DELETE',
    headers: headers,
    success: () => {
      modal.modal('hide');
      $(`.component-${currentId}`).remove();
    },
    error: (response) => addBanner("Failed delete")
  });
}

function onClickStar(caller, event, id) {
  event.stopPropagation();

  const data = { component_pk: id };

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

function onClickGet(caller) {
  if (!$('#getComponentsValue').val()) return;

  $.ajax({
    url: `components/${currentId}/`,
    type: "PATCH",
    headers: headers,
    data: { quantity: $('#getComponentsValue').val() },
    success: (response) => {
      if (response.action === 'get') {
        addBanner(`You just got ${response.quantity} components. Congratulations!`, 'success');
      }
      else {
        addBanner(`You just requested ${response.quantity} components. Wait for approval!`, 'warning');
      }
      $('#quantityValue').val($('#quantityValue').val() - $('#getComponentsValue').val());
    },
    error: () => addBanner("Failed to get requested quantity")
  })
}

function toEditMode() {
  state = State.EDIT;

  fields.forEach(
    field => modal
      .find(`#${field}Value`)
      .attr('class', 'form-control')
      .attr('readonly', false)
  );

  booleanFields.forEach(
    field => modal
    .find(`#${field}Value`)
    .attr('disabled', false)
  );

  ['delBtn', 'editBtn'].forEach(id => modal.find(`#${id}`).hide());
  modal.find('#saveBtn').show()
}

function toViewMode() {
  fields.forEach(
    field => modal
      .find(`#${field}Value`)
      .attr('class', 'form-control-plaintext')
      .attr('readonly', true)
  );

  booleanFields.forEach(
    field => modal
    .find(`#${field}Value`)
    .attr('disabled', true)
  );

  ['delBtn', 'editBtn'].forEach(id => modal.find(`#${id}`).show());
  modal.find('#saveBtn').hide()

  state = State.VIEW;
}

function addBanner(message, status = 'fail') {
  if (!modal.find("#failedOperation").length) modal.find("#body").append(alertHtml);
  modal.find("#failedOperation").html(message);
  switch (status) {
    case 'fail':
      modal.find("#banner").attr('class', 'alert alert-danger d-flex align-items-center mt-4')
      break;
    case 'success':
      modal.find("#banner").attr('class', 'alert alert-success d-flex align-items-center mt-4')
      break;
    case 'warning':
      modal.find("#banner").attr('class', 'alert alert-warning d-flex align-items-center mt-4')
      break;
  }
}

function removeBanner() {
  modal.find("#banner").remove()
}

function dynPopulate(json_response) {
  Object.entries(json_response).forEach(
    ([field, value]) => modal.find(`#${field}Value`).val(value)
  );

  Object.entries(json_response).filter(
    ([field,]) => booleanFields.includes(field)
  ).forEach(
    ([field, value]) => modal.find(`#${field}Value`).attr('checked', value)
  )

  Object.entries(json_response)
    .filter(([, value]) => typeof (value) != 'number' && !value)
    .forEach(
      ([field]) => modal.find(`#${field}Value`).val('-')
    )

  modal.find('#title').html(json_response.code);
  modal.find('#picture').attr('src', json_response.picture);
  modal.find('#lock').css('visibility', json_response.protection ? 'visible' : 'hidden');
  if (json_response.protection) modal.find('#getBtn').html("Request").attr('class', 'btn btn-warning col-md-2')
  else modal.find('#getBtn').html("Get").attr('class', 'btn btn-primary col-md-1')

  modal.find("#banner").remove();
  fieldsContainer.show();
  toViewMode();
}

function getModalData() {
  return Object.fromEntries(
    fields
      .map(field => [field, $(`#${field}Value`).val()])
      .filter(([, val]) => !!val && val != '-')
  );
}