// Please see documentation at https://docs.microsoft.com/aspnet/core/client-side/bundling-and-minification
// for details on configuring this project to bundle and minify static web assets.

//
// Session updater
//
SessionUpdater = (function () {
    var keepSessionAliveUrl = null;
    var timeout = 10 * 1000 * 60; // 10 minutes

    function setupSessionUpdater(actionUrl) {
        // store local value
        keepSessionAliveUrl = actionUrl;

        // start timeout - it'll run after n minutes
        checkToKeepSessionAlive();
    }

    // fires every n minutes - if there's been movement ping server and restart timer
    function checkToKeepSessionAlive() {
        setTimeout(function () { keepSessionAlive(); }, timeout);
    }

    function keepSessionAlive() {
        // if we've had any movement since last run, ping the server

        $.ajax({
            type: "POST",
            url: keepSessionAliveUrl,
            success: function (data) {

                // restart timeout to check again in n minutes
                checkToKeepSessionAlive();
            },
            error: function (data) {
                //console.log("Error posting to " & keepSessionAliveUrl);
            }
        });
    }

    // export setup method
    return {
        Setup: setupSessionUpdater
    };

})();