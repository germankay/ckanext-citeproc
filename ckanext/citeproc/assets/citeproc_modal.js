this.ckan.module('citeproc-modal', function($){
  return {
    /* options object can be extended using data-module-* attributes */
    options : {
      object_id: null,
      object_type: null,
    },
    initialize: function (){
      const objectID = this.options.object_id;
      const objectType = this.options.object_type;

      let citeButton = $(this.el).find('.citeproc-wrapper');
      let citeModal = $('#citeproc-modal');

    }
  };
});
