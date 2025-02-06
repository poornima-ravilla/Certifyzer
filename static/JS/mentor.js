function goBack() {
    document.getElementById('searchStudentForm').reset();
    const resultsDiv = document.getElementById('results');
    resultsDiv.style.display = 'none';
    document.querySelector('.wrapper').classList.remove('slide-left');
}
async function handleFormSubmit(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const response = await fetch('/search', {
        method: 'POST',
        body: formData
    });
    const resultsDiv = document.getElementById('results');
    const result = await response.json();
    if (response.ok) {
        resultsDiv.textContent = "STUDENT FOUND\n\n" + result.message;
        resultsDiv.className = 'results success';
    } else {
        resultsDiv.textContent = result.error || result.message;
        resultsDiv.className = 'results error'; 
    }
    document.querySelector('.wrapper').classList.add('slide-left');
}

function logout() {
// Send a request to the /logout route in the backend to clear the session
fetch('/logout', {
method: 'GET', // You can use POST or GET based on your backend setup
headers: {
    'Content-Type': 'application/json',
},
})
.then(response => response.json())  // Parse the JSON response
.then(data => {
// Check if the logout was successful
if (data.message === 'Logged out successfully') {
    // You can display a success message or alert
    alert(data.message);

    // Redirect the user to the login page or homepage
    window.location.href = '/loginevent'; // or you can use '/' for the homepage
} else {
    // Handle any error messages from the backend
    alert('Logout failed. Please try again.');
}
})
.catch(error => {
// Catch any errors that occur during the fetch request
console.error('Error during logout:', error);
});
}