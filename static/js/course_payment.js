function deleteUser(id) {
    if(confirm('Are you sure ?')) {
        fetch('/course/1/payments', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
              'X-CSRFToken': document.querySelector('[name="csrf-token"]').getAttribute('content')
          },
          body: JSON.stringify({id})
        })
        .then(response => response.json())
        .then(data => {
          console.log(data);
          window.location.reload();
        })
        .catch(error => {
          console.error('Error:', error);
        });
    }
}

function updateUser(id) {
    fetch('/course/1/payments', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': document.querySelector('[name="csrf-token"]').getAttribute('content')
      },
      body: JSON.stringify({id})
    })
    .then(response => response.json())
    .then(data => {
      console.log(data);
      window.location.reload();
    })
    .catch(error => {
      console.error('Error:', error);
    });
}
