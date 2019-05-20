const dashboardRecipeTemplate = require('../../templates/handlebars/dashboard-recipes.hbs');
const dashboardUserTemplate = require('../../templates/handlebars/dashboard-personal.hbs');
const favoritesTemplate = require('../../templates/handlebars/dashboard-favorites.hbs');

// ----------------------------------------------------------------------------- LOGIN
exports.logInUser = btn => {
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

// ----------------------------------------------------------------------------- SIGN UP
exports.signupUser = btn => {
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

// ----------------------------------------------------------------------------- UPDATE USER DATA
exports.updateUserData = () => {
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
  fetch(window.location.origin + '/user/', {
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

// ----------------------------------------------------------------------------- GET USER FAVORITES
exports.getUserFavorites = () => {
  // Get all recipe data from user
  fetch(window.location.origin + '/user/favorites', {
    method: 'GET',
    redirect: 'follow'
  }).then(res => {
    // Get json object
    return res.json()
  }).then(resObj => {

    // Map description
    resObj.favorites.map(favorite => {
      if (favorite.description.length > 100) {
        favorite.description = favorite.description.slice(0, 100) + '...';
      }
      return favorite;
    });

    // Get html template
    const htmlString = favoritesTemplate(resObj);

    // Edit html DOM
    $('#favorites-loader').remove();
    $('#favorites-container').append(htmlString);
  })

}

// ----------------------------------------------------------------------------- GET USER DATA
exports.getUserData = () => {
  // Get all recipe data from user
  fetch(window.location.origin + '/user', {
    method: 'GET',
    redirect: 'follow'
  }).then(res => {
    // Get json object
    return res.json()
  }).then(resObj => {
    // Set userdata in object
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

// ----------------------------------------------------------------------------- GET USER RECIPES
exports.getUserRecipes = page => {
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


