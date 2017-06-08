tinymce.init({
  selector: 'textarea',
  height: 500,
  menubar: false,
  branding: false,
  plugins: [
    'autosave',
    'advlist autolink lists link charmap print preview anchor',
    'searchreplace visualblocks code fullscreen',
    'insertdatetime table contextmenu paste code',
    'template',
  ],
  templates: [
    {title: 'Gym Membership Cancellation', description: 'Use this template to cancel a gym membership.', url: 'static/main/js/tinymce/templates/gym-membership.html'},
    {title: 'Creditor Debt Validation Request', description: 'Use this template to request that a creditor provide proof of your debt.', url: 'static/main/js/tinymce/templates/debt-validation.html'}
  ],
  autosave_restore_when_empty: true,
  toolbar: 'template | undo redo | bold italic | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent',
});
