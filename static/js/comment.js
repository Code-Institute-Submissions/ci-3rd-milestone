// ----------------------------------------------------------------------------- DELETE RECIPE COMMENT
exports.postComment = element => {
  const form = element.parentNode;
  const message = $(form).find('textarea')[0].value;

  if (message === '') {
    return;
  }
  else if (message.length > 500) {
    return M.toast({ html: 'Message is too long, maximum character of 500 allowed!', classes: 'red darken-1' });
  }

  $(form).submit();
}


// ----------------------------------------------------------------------------- DELETE RECIPE COMMENT
exports.deleteComment = commentId => {

  fetch(window.location.origin + '/comment/' + commentId, {
    method: 'DELETE'
  }).then(res => {
    // Get json object
    return res.json()
  }).then(resObj => {
    // Render template
    console.log(resObj)
    if (resObj.status === 'success') {
      document.location.reload(true)
    }
    else if (resObj.status === 'failed') {
      return M.toast({ html: 'Oops... Something went wrong', classes: 'red darken-1' });
    }
  });
}