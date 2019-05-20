const Croppie = require('croppie');

// ----------------------------------------------------------------------------- CROPPIE LISTENERS
let croppieObject;

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

