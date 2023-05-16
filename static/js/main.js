// Get queryString parameters
const queryString = window.location.search;
const urlParams = new URLSearchParams(queryString);

// If user is editing a comment, scroll to the comments section
if (urlParams.get('edit_comment_id')) {
    document.getElementById('comments-container').scrollIntoView();
}

// If user clicks on the comments link, scroll to the comments section
const commentsLink = document.getElementById('comments-link');
if (commentsLink) {
    commentsLink.addEventListener('click', () => {
        document.getElementById('comments-container').scrollIntoView();
    });
}


// Hide messages after specified time (3 seconds)
setTimeout(function() {
    const messages = document.getElementById("msg");
    const alert = new bootstrap.Alert(messages);
    alert.close();
}, 3000);