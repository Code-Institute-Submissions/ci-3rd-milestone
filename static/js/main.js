

const signupUser = (btn) => {
    console.log(btn);
    const form = btn.parentNode.parentNode.parentNode;

    const formParams = {
        firstname: form.querySelector('[name=firstname]').value,
        lastname: form.querySelector('[name=lastname]').value,
        email: form.querySelector('[name=email]').value,
        password: form.querySelector('[name=password]').value
    };

    // MOdify DOM
    $(btn).toggleClass('disabled');
    $('.signup-loading').css('visibility', 'visible');

    fetch('/signup', {
        method: 'POST',
        body: $.param(formParams),
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
    }).then(res => {
        return res.json();
    }).then(data => {
        if (data.status == 'ok') {
            $(btn).toggleClass('disabled');
            $('.signup-loading').css('visibility', 'hidden');
        }
    }).catch(err => {
        console.log(err)
    })

    console.log(formParams);
}