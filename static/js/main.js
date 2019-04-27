// RENDER TEMPLATES
const testTemplate = require('../../templates/handlebars/test.hbs');
const dashboardRecipeTemplate = require('../../templates/handlebars/dashboard-recipes.hbs');
const dashboardUserTemplate = require('../../templates/handlebars/dashboard-personal.hbs');
const drinksRecipePage = require('../../templates/handlebars/drinks-recipe-page.hbs');


// JAVASCRIPT MODULES
const Croppie = require('croppie');


// ----------------------------------------------------------------------------- CROPPIE LISTENERS
let croppieObject;
$('.croppie-file-input').on('change', event => {
    if ($('.croppie-file-input')[0].files[0]) {
        console.log('Image found in input field');

        const fileupload = $('.croppie-file-input')[0].files[0];
        const reader = new FileReader();

        // Read data in reader object
        reader.readAsDataURL(fileupload);

        // Function: start croppie object and bind image to div
        reader.onloadend = function () {
            if (!croppieObject) {
                croppieObject = $('#croppie').croppie({
                    viewport: {
                        width: 180,
                        height: 240
                    },
                    boundary: { width: 300, height: 300 },
                });
            }
            croppieObject.croppie('bind', {
                url: this.result
            });
        }
    } else {
        console.log('No file found in input field');
    }
});

$('.croppie-file-input-modal').on('change', event => {
    if ($('.croppie-file-input-modal')[0].files[0]) {
        console.log('Image found in input field');

        const fileupload = $('.croppie-file-input-modal')[0].files[0];
        const reader = new FileReader();

        // Read data in reader object
        reader.readAsDataURL(fileupload);

        // Function: start croppie object and bind image to div
        reader.onloadend = function () {
            if (!croppieObject) {
                croppieObject = $('#croppie').croppie({
                    viewport: {
                        width: 250,
                        height: 250
                    },
                    boundary: { width: 300, height: 300 },
                });
            }
            croppieObject.croppie('bind', {
                url: this.result
            });
        }
    } else {
        console.log('No file found in input field');
    }
});

$('#crop-profile-picture').on('click', function () {
    if (croppieObject) {
        console.log('Cropping image');
        croppieObject.croppie('result', {
            type: 'base64',
            format: 'jpg',
            size: { width: 300, height: 300 }
        }).then(resp => {
            $('.profile-img').attr('src', resp);

            // Send response to sercer
            fetch('/user/image', {
                method: 'POST',
                body: JSON.stringify({
                    image_base64: resp.split(',')[1],
                    old_image_path: TE.userData.image_path
                }),
                headers: {
                    'Content-Type': 'application/json'
                }
            }).then(res => {
                console.log(res)
                return res.json();
            }).then(resObj => {
                console.log(resObj);
                if (resObj.status == 'ok') {
                    TE.userData.image_path = resObj.new_image_path;
                    M.toast({ html: 'Successfully updated!', classes: 'light-green darken-1' });
                } else if (resObj.status == 'failed') {
                    M.toast({ html: 'Something went wrong', classes: 'red darken-1' });
                }
            })
        })
    } else {
        console.log('No croppie object found');
    }
})

// ----------------------------------------------------------------------------- SIGN UP
const signupUser = btn => {
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
const logInUser = btn => {
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
            return window.location.replace(res.url);
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

// ----------------------------------------------------------------------------- ADD RECIPE
const addRecipe = btn => {
    const form = btn.parentNode.parentNode.parentNode;

    // Get values from input fields
    const formParams = {
        title: form.querySelector('[name=title]').value,
        description: form.querySelector('[name=description]').value,
        recipe: form.querySelector('[name=recipe]').value,
        image_name: "",
        image_base64: ""
    };

    // Construct ingredients
    let ingredientsList = "";
    $('.recipe-line').each((index, element) => {
        // Value from ingredient input
        let ingredient = $(element).find('input')[0].value;
        ingredientsList += '<ingredient>' + ingredient + '</ingredient>';
    });
    formParams.ingredients = ingredientsList;
    console.log(formParams);

    // Check if file was uploaded
    if ($('.croppie-file-input')[0].files[0]) {
        console.log($('.croppie-file-input')[0].files[0])
        formParams.image_name = $('.croppie-file-input')[0].files[0].name;
    } else {
        return M.toast({ html: 'Please upload a photo', classes: 'red darken-1' });
    }

    // Check if values are not empty
    if (formParams.title == "" || formParams.description == "" || formParams.recipe == "" || formParams.ingredients == "") {
        return M.toast({ html: 'Please fill in all input fields', classes: 'red darken-1' });
    }

    // Check if croppie object exists
    if (croppieObject) {
        croppieObject.croppie('result', {
            type: 'base64',
            format: 'jpg',
            size: { width: 300, height: 400 }
        }).then(resp => {

            // Add base64 image data
            formParams.image_base64 = resp.split(',')[1];

            // Open load bar
            $('body').append(`<div class="loader-container">
                                    <div class="loader"></div>
                                </div>`);

            // Send response to sercer
            fetch(window.location.origin + '/recipe', {
                method: 'POST',
                body: JSON.stringify(formParams),
                headers: {
                    'Content-Type': 'application/json'
                }
            }).then(res => {
                console.log(res)
                if (res.redirected) {
                    return window.location.replace(res.url);
                }
            })
        })
    } else {
        return M.toast({ html: 'Please upload a photo', classes: 'red darken-1' });
    }
}



// ----------------------------------------------------------------------------- GET USER RECIPES
const getUserRecipes = page => {
    let initialize;
    if (!page) {
        page = 1;
        initialize = true;
    }

    // Add loading container
    if (!initialize) {
        // Remove active class pagination
        $('.recipe-pagination').find('li').removeClass('active deep-orange darken-1')

        // Add classes to new pagination 
        const newPageIcon = $('.recipe-pagination').find('li')[page];
        $(newPageIcon).addClass('active deep-orange darken-1');

        // Add loader screen
        $('.recipe-card-container')
            .append(`<div class="card-container-loader">
                    <div class="loader"></div>
                </div>`)
    }

    TE.activeUserRecipePage = page;

    // Get all recipe data from user
    fetch(window.location.origin + '/recipe/user?page=' + page, {
        method: 'GET',
        redirect: 'follow'
    }).then(res => {
        // Get json object
        return res.json()
    }).then(resObj => {
        // Render template
        const htmlString = dashboardRecipeTemplate(resObj);

        // Remove elements
        if (initialize) {
            // Edit html DOM
            $('#recipe-loader').remove();
        } else {
            $('.recipe-pagination').remove();
            $('.recipe-card-container').remove();
        }

        // Add new html
        $('#recipe-container').append(htmlString);
    })
}


// ----------------------------------------------------------------------------- GET USER DATA
const getUserData = () => {
    // Get all recipe data from user
    fetch(window.location.origin + '/user', {
        method: 'GET',
        redirect: 'follow'
    }).then(res => {
        // Get json object
        return res.json()
    }).then(resObj => {
        // Render template
        TE.userData = resObj;

        // Set form fields
        $('#modal-details-update').find('[name=firstname]').attr('value', resObj.firstname);
        $('#modal-details-update').find('[name=lastname]').attr('value', resObj.lastname);
        $('#modal-details-update').find('[name=email]').attr('value', resObj.email);
        M.updateTextFields();

        // Get html template
        const htmlString = dashboardUserTemplate(resObj);

        // Edit html DOM
        $('#user-loader').remove();
        $('#user-container').append(htmlString);
    })

}

// ----------------------------------------------------------------------------- UPDATE USER DATA
const updateUserData = () => {
    const formParams = {
        firstname: $('#modal-details-update').find('[name=firstname]')[0].value,
        lastname: $('#modal-details-update').find('[name=lastname]')[0].value,
        email: $('#modal-details-update').find('[name=email]')[0].value
    }

    // Update user data in browers
    TE.userData.firstname = formParams.firstname;
    TE.userData.lastname = formParams.lastname;
    TE.userData.email = formParams.email;

    const htmlString = dashboardUserTemplate(TE.userData);

    // Edit html DOM
    $('#user-container').children().last().remove()
    $('#user-container').append(htmlString);

    // Get all recipe data from user
    fetch(window.location.origin + '/user', {
        method: 'POST',
        body: JSON.stringify(formParams),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => {
        // Get json object
        return res.json()
    }).then(resObj => {

        // Render template
        console.log(resObj)
    })

}

// ----------------------------------------------------------------------------- DELETE USER RECIPES
const deleteRecipe = recipeId => {
    var anwser = confirm('Are you sure you want to delete this recipe?');

    if (anwser) {
        // Get all recipe data from user
        fetch(window.location.origin + '/recipe/' + recipeId, {
            method: 'DELETE'
        }).then(res => {
            // Get json object
            return res.json()
        }).then(resObj => {
            // Render template
            console.log(resObj)
            if (resObj.status == 'ok') {
                getUserRecipes(TE.activeUserRecipePage);
            }
        })
    }
}

// ----------------------------------------------------------------------------- GET RECIPES 
const getRecipes = page => {
    let initialize;
    if (!page) {
        page = 1;
        initialize = true;
    }

    // Add loading container
    if (!initialize) {
        // Remove active class pagination
        $('.recipe-pagination').find('li').removeClass('active deep-orange darken-1')

        // Add classes to new pagination 
        const newPageIcon = $('.recipe-pagination').find('li')[page];
        $(newPageIcon).addClass('active deep-orange darken-1');

        // Add loader screen
        $('.recipes-page-wrapper')
            .append(`<div class="card-container-loader">
                    <div class="loader"></div>
                </div>`)
    }

    // Get all recipe data from user
    fetch(window.location.origin + '/drinks/recipes?page=' + page, {
        method: 'GET'
    }).then(res => {
        // Get json object
        return res.json()
    }).then(resObj => {
        console.log(resObj);
        let recipes = resObj.recipes;

        //Check if equal amount of items
        let uneven = true;
        if (Math.floor(recipes.length / 2) == recipes.length / 2) {
            uneven = false;
        }

        resObj.uneven = uneven;
        // Render template
        const htmlString = drinksRecipePage(resObj);

        if (!initialize) {
            $('.recipe-pagination').remove();
            $('.recipes-page-wrapper').remove();
        }

        $('.recipes-page-container').append(htmlString);

    })

}

// ----------------------------------------------------------------------------- ADD RECIPE LINE
const addRecipeLine = element => {
    // Get main recipe line element
    const recipeLine = element.parentNode.parentNode;

    // Insert new line
    const htmlLine = `
    <div class="row recipe-line" style="margin-bottom: 0">
        <div class="input-field col s10">
        <input id="last_name" type="text" class="validate" placeholder="Extra ingredient">
        </div>
        <div class="col s2"><i class="small material-icons deep-orange-text text-darken-1 right-align"
            onclick="TE.addRecipeLine(this)">add_circle_outline</i>
        </div>
    </div>`;
    $(recipeLine).after(htmlLine);

    // Modify current element
    element.innerText = 'remove_circle_outline';
    $(element).removeClass('deep-orange-text text-darken-1');
    $(element).addClass('grey-text');
    $(element).attr("onclick", "TE.removeRecipeLine(this)");
}

// ----------------------------------------------------------------------------- REMOVE RECIPE LINE
const removeRecipeLine = element => {
    // Get main recipe line element
    const recipeLine = element.parentNode.parentNode;

    $(recipeLine).remove();
}


// ----------------------------------------------------------------------------- EXPORTS
module.exports = {
    signupUser: signupUser,
    logInUser: logInUser,
    addRecipe: addRecipe,
    getUserRecipes: getUserRecipes,
    getUserData: getUserData,
    updateUserData: updateUserData,
    deleteRecipe: deleteRecipe,
    getRecipes: getRecipes,
    addRecipeLine: addRecipeLine,
    removeRecipeLine: removeRecipeLine
}

// https://codepen.io/asrulnurrahim/pen/WOyzxy