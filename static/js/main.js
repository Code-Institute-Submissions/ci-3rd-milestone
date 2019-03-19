

const signupUser = (btn) => {
    const form = btn.parentNode;

    const formParams = {
        firstname: form.querySelector('[name=firstname]').value,
        lastname: form.querySelector('[name=lastname]').value,
        email: form.querySelector('[name=email]').value,
        password: form.querySelector('[name=password]').value
    };

    fetch('/signup', {
        method: 'POST',
        body: $.param(formParams),
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
    }).then(res => {
        return res.json();
    }).then(data => {
        console.log(data);
    }).catch(err => {
        console.log(err)
    })

    console.log(formParams);
}