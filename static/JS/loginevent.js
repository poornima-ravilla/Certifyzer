// logged out 
window.onload = function() {
    var logoutMessage = document.getElementById("logoutMessage");
    if (logoutMessage) {
        logoutMessage.style.display = "block";
        setTimeout(function() {
            logoutMessage.style.display = "none";
        }, 2000);  
    }
};

const responseMessage = document.getElementById('errorMessage');
// Function to prompt for username if the field is empty
function promptForUsername() {
var username = document.getElementById('emaill').value;

        var messageContainer = document.getElementById('username-message');
        
        // Check if the username field is empty
        if (!username) {
            // Show the prompt message below the Forgot Password link
            messageContainer.style.display = 'block';
        } else {
            // Hide the message if username is entered
            messageContainer.style.display = 'none';
        toggleForgotPasswordForm();
        appendTextInput();
        
    }
}

function toggleForgotPasswordForm() {
    var email=document.getElementById('emaill');
    const form = document.getElementById('forgotPasswordForm');
    form.style.display = form.style.display === 'none' || form.style.display === '' ? 'block' : 'none';
    email.disabled = !email.disabled;
    responseMessage.textContent='';
}



function appendTextInput() {
    var username = document.getElementById('emaill').value;
    const formo = document.getElementById('forgotform');
    
    // Create a new file input element
    const textInput = document.createElement('input');
    textInput.type = 'hidden';
    textInput.name = 'email';
    textInput.value = username;
    formo.appendChild(textInput);
}

// Call the function to append the text input when needed

    

document.getElementById('forgotform').addEventListener('submit', function(event) {
    event.preventDefault();  // Prevent default form submission

    const loadingIndicator = document.getElementById('loading');
    const sendmail = document.getElementById('sendmail');
    loadingIndicator.style.display = "block";
    sendmail.style.display = "none";
    cancel.style.display = "none";
    const formData = new FormData(this);
    
    

    fetch('/forgot-password', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        const responseMessage = document.getElementById('errorMessage');
        responseMessage.textContent = '';
        
        if (data.success) {
            responseMessage.className = 'success';
            responseMessage.textContent = data.message;
        } else {
            responseMessage.className = 'error';
            responseMessage.textContent = data.message;
        }
    })
    .catch(error => {
        
        responseMessage.className = 'error';
        responseMessage.textContent = 'Something went wrong. Please try again later.';
    })
    .finally(() => {
        // Hide the loading spinner, reset button
        loadingIndicator.style.display = "none";  // Hide loading spinner
        sendmail.style.display = "block";  // Hide loading spinner
        cancel.style.display = "block";  // Hide loading spinner
        
    });
    
});
//     // Handle form submission for forgot password (AJAX approach)
// const forgotPasswordForm = document.querySelector('.forgot-password-form form');
// forgotPasswordForm.addEventListener('submit', async function(event) {
//     event.preventDefault(); // Prevent normal form submission

//     const email = document.getElementById('username').value;
//     console.log(email)
//     const passwordMessage = document.getElementById('passwordMessage');
//     const errorMessage = document.getElementById('errorMessage');

//     passwordMessage.innerHTML = ''; // Clear previous messages
//     errorMessage.innerHTML = '';

//     // Send a POST request to the server to fetch the password
//     const response = await fetch('/forgot-password', {
//         method: 'POST',
//         headers: { 'Content-Type': 'application/json' },
//         body: JSON.stringify({ email })
//     });

//     const result = await response.json();

//     if (result.success) {
//         passwordMessage.innerHTML = `Email sent Sucessfully`;
//     } else {
//         errorMessage.innerHTML = result.message || 'Email not found';
//     }
