var nameArray = [];
var emailArray = [];
var passwordArray = [];
var phone_numberArray = [];
var password = [];

//for login

function login() {
    var email = document.getElementById("email").value;
    var password = document.getElementById("password").value;

    if (!email || !password) {
        alert("Please fill in all fields");
        return false;
    }

    $.ajax({
        method: 'POST',
        url: 'http://127.0.0.1:5000/login',
        contentType: 'application/json;charset=UTF-8',
        data: JSON.stringify({
            'email': email,
            'password': password
        }),
        dataType: "json",
        success: function (data) {
            if (data.status === 1) {
                alert("Account login successfully");
                // Uncomment and modify the following line to redirect after a successful login
                // window.location.href = "http://127.0.0.1:5000/first";
            } else {
                alert("Invalid credentials. Please try again.");
            }
        },
        statusCode: {
            400: function () {
                $('#msg').html('<span style="color: red;">Bad request - invalid credentials</span>');
            }
        },
        error: function (err) {
            console.log(err);
            alert("An error occurred. Please try again.");
        }
    });

    return false; // Prevent the default form submission
}
   