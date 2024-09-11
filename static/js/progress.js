function updateProgressBar() {
    fetch('/progress')
        .then(response => response.json())
        .then(data => {
            const progressBar = document.getElementById('progress-bar');
            if (progressBar) {
                progressBar.style.width = `${data.progress}%`;
                progressBar.setAttribute('aria-valuenow', data.progress);
                progressBar.innerText = `${data.progress}%`;
            }
        })
        .catch(error => console.error('Error fetching progress:', error));
}

// Call the function to update progress bar periodically
setInterval(updateProgressBar, 1000);
