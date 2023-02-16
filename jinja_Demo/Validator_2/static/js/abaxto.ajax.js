AjaxService = (function () {
    function postData(url, data) {
        $.ajax({
            type: "POST",
            url: url,
            data: data,
            success: function (response) {
                $(document).trigger('ajaxSuccess', [{
                    source: url,
                    response: response
                }]);
            },
            error: function (response) {
                $(document).trigger('ajaxError', [{
                    source: url,
                    response: response
                }]);
            }
        });
    }

    // export setup method
    return {
        Post: postData
    };

})();