// ----------------------------------------------------------------------------- ADD/REMOVE FAVORITE RECIPE
exports.toggleFavorite = (recipeId, element) => {
  // Check which class is active
  let isFav = false;
  if ($('.favorite-active')[0]) isFav = true;

  if (!isFav) {
    fetch(window.location.origin + '/favorite/' + recipeId, {
      method: 'POST'
    }).then(res => {
      // Get json object
      return res.json()
    }).then(resObj => {
      // Render template
      console.log(resObj)
      if (resObj.status === 'success') {
        $(element).toggleClass('favorite-active');
      }
      else if (resObj.status === 'failed') {
        return M.toast({ html: 'Oops... Something went wrong', classes: 'red darken-1' });
      }
    });
  }
  else {
    fetch(window.location.origin + '/favorite/' + recipeId, {
      method: 'DELETE'
    }).then(res => {
      // Get json object
      return res.json()
    }).then(resObj => {
      if (resObj.status === 'success') {
        $(element).toggleClass('favorite-active');
      }
      else if (resObj.status === 'failed') {
        return M.toast({ html: 'Oops... Something went wrong', classes: 'red darken-1' });
      }
    });
  }
}

// ----------------------------------------------------------------------------- UPDATE RATING RECIPE
exports.updateRating = radioButton => {
  // Get required parameters
  const urlIdIndex = window.location.pathname.lastIndexOf('/');
  const recipeId = window.location.pathname.substring(urlIdIndex + 1);
  const rating = $(radioButton)[0].value;

  if (!rating) {
    console.log('Rating is undefined, something went wrong');
    return M.toast({ html: 'Rating could not be updated...', classes: 'red darken-1' });
  }

  fetch(window.location.origin + '/rating/', {
    method: 'PATCH',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      rating: rating,
      recipe_id: recipeId
    })
  }).then(res => {
    // Get json object
    return res.json()
  }).then(resObj => {
    if (resObj.status === 'success') {
      M.toast({ html: resObj.message, classes: 'light-green darken-1' });
    }
    else if (resObj.status === 'failed') {
      return M.toast({ html: resObj.message, classes: 'red darken-1' });
    }
  });

}