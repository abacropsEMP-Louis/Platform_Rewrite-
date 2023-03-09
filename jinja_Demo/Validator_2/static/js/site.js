// Please see documentation at https://docs.microsoft.com/aspnet/core/client-side/bundling-and-minification
// for details on configuring this project to bundle and minify static web assets.

// Write your JavaScript code.

$(document).ready(function () {
    $('#errorModal').modal();
    $('#infoModal').modal();
});

function addCommas(x) {
    var parts = x.toString().split(".");
    parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    return parts.join(".");
}

function preciseRound(num, decimals) {
    return Math.round(num * Math.pow(10, decimals)) / Math.pow(10, decimals);
}

function showInformationMessage(message) {
    $('#modalInformation').find('span#spanInformationMessage').html(message);
    $('#modalInformation').modal('show')
}

function showErrorMessage(message) {
    
    $('#modalError').find('span#spanErrorMessage').html(message);
    $('#modalError').modal('show')
}

//
// Validation
//
function validateEmail(field) {
    var regexp = /^\w+([-+.']\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$/;
    return regexp.test(field.val());
}

function validatePassword(field) {
    var regexp = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{6,15}$/;
    return regexp.test(field.val());
}

function validateFloat(field) {
    var regexp = /^(-?)(0|([1-9][0-9]*))(\.[0-9]+)?$/;
    return regexp.test(field.val());
}

function validateRegexField(field, pattern) {
    var regexp = pattern;
    return regexp.test(field.val());
}

function validateRequiredField(field) {
    return (field.val().trim().length != 0);
}

function validateRequiredMobile(mobileCountry, mobileNumber) {
    var country = validateRegexField(mobileCountry, /^\d+(\.\d{1,2})?$/);
    var number = validateRegexField(mobileNumber, /^\d+(\.\d{1,2})?$/);

    if (country == true
        && number == true
        && mobileNumber.val().length > 8) {
        return true;
    }

    return false;
}

    
function checkStrength(password) {
    var strength = 0
    if (password.length < 6) {
        $('#strengthMessage').removeClass()
        $('#strengthMessage').addClass('Short')
        return 'Too short'
    }
    if (password.length > 7) strength += 1
    // If password contains both lower and uppercase characters, increase strength value.  
    if (password.match(/([a-z].*[A-Z])|([A-Z].*[a-z])/)) strength += 1
    // If it has numbers and characters, increase strength value.  
    if (password.match(/([a-zA-Z])/) && password.match(/([0-9])/)) strength += 1
    // If it has one special character, increase strength value.  
    if (password.match(/([!,%,&,@,#,$,^,*,?,_,~])/)) strength += 1
    // If it has two special characters, increase strength value.  
    if (password.match(/(.*[!,%,&,@,#,$,^,*,?,_,~].*[!,%,&,@,#,$,^,*,?,_,~])/)) strength += 1
    // Calculated strength value, we can return messages  
    // If value is less than 2  
    if (strength < 2) {
        $('#strengthMessage').removeClass()
        $('#strengthMessage').addClass('Weak')
        return 'Weak'
    } else if (strength == 2) {
        $('#strengthMessage').removeClass()
        $('#strengthMessage').addClass('Good')
        return 'Good'
    } else {
        $('#strengthMessage').removeClass()
        $('#strengthMessage').addClass('Strong')
        return 'Strong'
    }
}  

//
// Loader
//

function showPageLoader(flag) {
    var preloader = $('#mdb-preloader');
    if (flag == true) {
        preloader.show()
    }
    else {
        preloader.hide()
    }
}