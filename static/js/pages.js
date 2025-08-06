console.log("PAGES")
activateButton();
var userId = sessionStorage.getItem('userId');
if (userId) {
  showUserPhoto();
}
else {
  showLoginBnt();
}

var input = document.getElementById('password');
var button = document.getElementById("loginBtn");

if (input) {
  input.addEventListener("keypress", function(event) {
    if (event.key === "Enter") {
      event.preventDefault();
      // Programmatically click the button
      button.click();
    }
  });
}

if (sessionStorage.getItem('userId')) {
  var url = "/enforce_active_user/"
  let data = {
    userId: sessionStorage.getItem('userId'),
    isExecutiveMember: sessionStorage.getItem('isExecutiveMember')
  }
  let fetchData = {
    method: 'POST',
    body: JSON.stringify(data),
    headers: new Headers({
      'Content-Type': 'application/json; charset=UTF-8'
    })
  }

  fetch(url, fetchData)
  .then(res => res.json())
  .then(out => {
    console.log("out: ", out);
  })
  .catch(err => console.log(err));
}
