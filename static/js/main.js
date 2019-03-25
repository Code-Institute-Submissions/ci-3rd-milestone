testTemplate = require('../../templates/handlebars/test.hbs');


// ----------------------------------------------------------------------------- SIGN UP
const signupUser = (btn) => {
    // Get form data
    const form = btn.parentNode.parentNode.parentNode;

    const formParams = {
        firstname: form.querySelector('[name=firstname]').value,
        lastname: form.querySelector('[name=lastname]').value,
        email: form.querySelector('[name=email]').value,
        password: form.querySelector('[name=password]').value,
        repeatpassword: form.querySelector('[name=repeat_password]').value
    };

    // Check email
    if (formParams.email === '') {
        M.toast({ html: 'Please provide an email', classes: 'red darken-1' });
        var email = $('[name=email]')[0];
        $(email).addClass('invalid');
        return;
    }

    // Check password
    if (formParams.password === '') {
        M.toast({ html: 'Please provide a password', classes: 'red darken-1' });
        var password = $('[name=password]')[0];
        $(password).addClass('invalid');
        return;
    }

    // Check password equal
    if (formParams.password !== formParams.repeatpassword) {
        M.toast({ html: 'Passwords are not equal', classes: 'red darken-1' });
        var password = $('[name=password]')[0];
        var repeatpassword = $('[name=repeat_password]')[0];
        $(password).addClass('invalid');
        $(repeatpassword).addClass('invalid');
        return;
    }


    // Modify DOM with loading text
    $(btn).toggleClass('disabled');
    $('.signup-loading').css('visibility', 'visible');

    // Send POST method to backend server
    fetch('/signup', {
        method: 'POST',
        body: $.param(formParams),
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
    }).then(res => {
        // Convert response to JSON
        return res.json();
    }).then(data => {
        if (data.status == 'ok') {
            // Provicde message to user
            M.toast({ html: 'Success!', classes: 'light-green darken-1' });

            // Remove loading text
            $('.signup-loading').css('visibility', 'hidden');

            // Redirect
            setTimeout(() => window.location.replace('/dashboard'), 1000);
        } else if (data.status == 'failed') {
            // Provicde message to user
            M.toast({ html: 'Email address already in use', classes: 'red darken-1' });

            // Set email form input to red
            var email = $('[name=email]')[0];
            $(email).addClass('invalid');

            // Reset button and loading text
            $(btn).toggleClass('disabled');

            // Remove loading text
            $('.login-loading').css('visibility', 'hidden');
        }


    }).catch(err => {
        console.log(err)
    })

}

// ----------------------------------------------------------------------------- LOGIN
const logInUser = (btn) => {
    // Get form data
    const form = btn.parentNode.parentNode.parentNode;

    const formParams = {
        email: form.querySelector('[name=email]').value,
        password: form.querySelector('[name=password]').value
    };

    // Check email
    if (formParams.email === '') {
        M.toast({ html: 'Please provide an email', classes: 'red darken-1' });
        var email = $('[name=email]')[0];
        $(email).addClass('invalid');
        return;
    }

    // Check password
    if (formParams.password === '') {
        M.toast({ html: 'Please provide a password', classes: 'red darken-1' });
        var password = $('[name=password]')[0];
        $(password).addClass('invalid');
        return;
    }


    // Modify DOM with loading text
    $(btn).toggleClass('disabled');
    $('.login-loading').css('visibility', 'visible');

    // Send POST method to backend server
    fetch('/login', {
        method: 'POST',
        redirect: 'follow',
        body: $.param(formParams),
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
    }).then(res => {
        // Check for redirect
        if (res.redirected) {
            return window.location.replace('/dashboard');
        }

        // Convert response to JSON
        return res.json();
    }).then(data => {
        if (data.status == 'failed') {
            // Provicde message to user
            M.toast({ html: data.message, classes: 'red darken-1' });

            // Remove loading text
            $('.login-loading').css('visibility', 'hidden');

            // Reset button and loading text
            $(btn).toggleClass('disabled');
        }


    }).catch(err => {
        console.log(err)
    })

}


function myTest() {
    const data = [
        {
            name: 'hoi'
        },
        {
            name: 'doei'
        }
    ]


    console.log(testTemplate(data));
}


// ----------------------------------------------------------------------------- EXPORTS
module.exports = {
    signupUser: signupUser,
    logInUser: logInUser,
    myTest: myTest
}