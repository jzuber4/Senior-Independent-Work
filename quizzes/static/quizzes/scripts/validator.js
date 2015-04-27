(function ( $ ) {

    $.fn.validator = function(options) {

        var opts = $.extend({}, $.fn.validator.defaults, options);
        
        return this.each(function() {
            var element = $(this),
                form = this.form;

            var alertId = element.attr("id")+opts.alertId;
            var alertDiv = opts.alertDiv.clone().text(opts.alertText).attr("id", alertId);

            $(form).submit(function(e) {
                canSubmit = opts.isValid(element);
                if (!canSubmit) {
                    e.preventDefault();
                    if (!$("#"+alertId).length) {
                        $(form).after(alertDiv);
                    }   
                }
            });

            element.on(opts.on, function() {
                canSubmit = opts.isValid(element);
                if (canSubmit) {
                    $("#"+alertId).remove();
                    element.closest(".form-group").removeClass("has-error");
                } else {
                    element.closest(".form-group").addClass("has-error");
                }
            });
            element.closest(".form-group").addClass("has-error");
        });
    };

    $.fn.validator.defaults = {
            isValid: function(element) { return $.trim(element.val()).length > 0;}, // non whitespace
            alertDiv: $("<div class='alert alert-danger' role='alert'></div>"), 
            alertText: "Input invalid", 
            alertId: "-validatorAlert",
            on: "input"
    };

}( jQuery ));
