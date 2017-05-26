tinymce.init({
  selector: 'textarea',
  height: 500,
  menubar: false,
  plugins: [
    'autosave',
    'advlist autolink lists link charmap print preview anchor',
    'searchreplace visualblocks code fullscreen',
    'insertdatetime table contextmenu paste code'
  ],
  autosave_restore_when_empty: true,
  toolbar: 'undo redo | insert | styleselect | bold italic | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | link image',
  content_css: '//www.tinymce.com/css/codepen.min.css'
});
