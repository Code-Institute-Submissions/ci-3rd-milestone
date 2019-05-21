const drinksRecipePage = require('../../templates/handlebars/drinks-recipe-page.hbs');
const user = require('./user');

// ----------------------------------------------------------------------------- CROPPIE LISTENER
let croppieObject;
$('.croppie-file-input').on('change', event => {
  if ($('.croppie-file-input')[0].files[0]) {
    console.log('Image found in input field');
    $('.upload-img').attr('src', '/static/images/placeholder.png')

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



// ----------------------------------------------------------------------------- ADD RECIPE
exports.addRecipe = btn => {
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
    if (ingredient != '') {
      ingredientsList += '<in>' + ingredient + '</in>';
    }
  });
  formParams.ingredients = ingredientsList;
  console.log(formParams);

  // Get labels
  const selectElem = $('select');
  const instance = M.FormSelect.getInstance(selectElem);
  const labelIds = instance.getSelectedValues();
  formParams.labels = labelIds;


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

  // Check if at least one label is selected
  if (labelIds.length == 0) {
    return M.toast({ html: 'Please select at least one label!', classes: 'red darken-1' });
  }

  // Check length of title, description and recipe
  if (formParams.title.length > 32 || formParams.description.length > 500 || formParams.recipe.length > 500) {
    return M.toast({ html: 'Too many characters!', classes: 'red darken-1' });
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
      fetch(window.location.origin + '/recipe/', {
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

// ----------------------------------------------------------------------------- UPDATE RECIPE
exports.updateRecipe = btn => {
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
    if (ingredient != '') {
      ingredientsList += '<in>' + ingredient + '</in>';
    }
  });
  formParams.ingredients = ingredientsList;
  console.log(formParams);

  // Get labels
  const selectElem = $('select');
  const instance = M.FormSelect.getInstance(selectElem);
  const labelIds = instance.getSelectedValues();
  formParams.labels = labelIds;

  // Check if file was uploaded
  if ($('.croppie-file-input')[0].files[0]) {
    // console.log($('.croppie-file-input')[0].files[0])
    formParams.image_name = $('.croppie-file-input')[0].files[0].name;
  }

  // Check if values are not empty
  if (formParams.title == "" || formParams.description == "" || formParams.recipe == "") {
    return M.toast({ html: 'Please fill in all input fields', classes: 'red darken-1' });
  }

  // Check if at least one label is selected
  if (labelIds.length == 0) {
    return M.toast({ html: 'Please select at least one label!', classes: 'red darken-1' });
  }

  // Check length of title, description and recipe
  if (formParams.title.length > 32 || formParams.description.length > 500 || formParams.recipe.length > 500) {
    return M.toast({ html: 'Too many characters!', classes: 'red darken-1' });
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

      // Send request
      sendUpdateRequest();
    });
  } else {
    sendUpdateRequest();
  }

  // Send update request to backend server
  function sendUpdateRequest() {
    // Open load bar
    $('body').append(`<div class="loader-container">
          <div class="loader"></div>
      </div>`);

    let urlIdIndex = window.location.pathname.lastIndexOf('/');
    let recipeId = window.location.pathname.substring(urlIdIndex + 1);

    // Send response to sercer
    fetch(window.location.origin + '/recipe/' + recipeId, {
      method: 'PATCH',
      body: JSON.stringify(formParams),
      headers: {
        'Content-Type': 'application/json'
      }
    }).then(res => {
      return res.json()
    }).then(resData => {
      console.log(resData);
      if (resData.status === 'success') {
        window.location = document.referrer;
      }
      else if (resData.status == 'failed') {
        $('.loader-container').remove();
        M.toast({ html: 'Oops... Something went wrong', classes: 'red darken-1' });
      }
    })
  }
}

// ----------------------------------------------------------------------------- DELETE USER RECIPES
exports.deleteRecipe = recipeId => {
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
        if (window.location.pathname == '/dashboard') {
          user.getUserRecipes(TE.activeUserRecipePage);
        }
        else {
          window.location = document.referrer;
        }
      }
    })
  }
}

// ----------------------------------------------------------------------------- GET RECIPES 
exports.getRecipes = page => {
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

  // Get search selections
  $('select').formSelect();
  const ratingSelectElem = $('#rating-selector');
  const ratingInstance = M.FormSelect.getInstance(ratingSelectElem);
  const ratingValue = ratingInstance.getSelectedValues();
  const labelSelectElem = $('#label-selector');
  const labelInstance = M.FormSelect.getInstance(labelSelectElem);
  const labelValues = labelInstance.getSelectedValues().join('+');

  // Query string
  const querystring = '/drinks/recipes?page=' + page + '&rating=' + ratingValue[0] + '&labels=' + labelValues;

  // Get all recipe data from user
  fetch(window.location.origin + querystring, {
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

    // Map description and rating 
    resObj.recipes.map(recipe => {
      // Cut description if necessary
      if (recipe.description.length > 65) {
        recipe.description = recipe.description.slice(0, 65) + '...';
      }
      // Determinae how many stars
      recipe.stars = {
        zero: false,
        one: false,
        two: false,
        three: false,
        four: false,
        five: false
      }
      const eps = 0.2;
      if (recipe.avg_rating >= 5 - eps) recipe.stars.five = true;
      else if (recipe.avg_rating >= 4 - eps) recipe.stars.four = true;
      else if (recipe.avg_rating >= 3 - eps) recipe.stars.three = true;
      else if (recipe.avg_rating >= 2 - eps) recipe.stars.two = true;
      else if (recipe.avg_rating >= 1 - eps) recipe.stars.one = true;
      else recipe.stars.zero = true;

      return recipe;
    });

    console.log(resObj)
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
exports.addRecipeLine = element => {
  // Get main recipe line element
  const recipeLine = element.parentNode.parentNode;

  // Insert new line
  const htmlLine = `
  <div class="row recipe-line" style="margin-bottom: 0">
      <div class="input-field col recipe-line-description">
      <input id="last_name" type="text" class="validate" placeholder="Extra ingredient">
      </div>
      <div class=""><i class="recipe-line-icon small material-icons deep-orange-text text-darken-1 right-align"
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
exports.removeRecipeLine = element => {
  // Get main recipe line element
  const recipeLine = element.parentNode.parentNode;

  $(recipeLine).remove();
}