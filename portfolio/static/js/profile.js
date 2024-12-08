document.addEventListener("DOMContentLoaded", function () {
    const profileHeader = document.querySelector('.profile-header');
    const profileImage = document.querySelector('.profile-header img');
    const profileDetails = document.querySelector('.profile-details');
    const editBtn = document.querySelector('.edit-btn');
    const deleteBtn = document.querySelector('.delete-btn');
    const deleteModal = document.querySelector('.delete-modal .modal-content');

    // Adding a check to ensure elements exist before applying animations
    if (profileHeader && profileImage && profileDetails && editBtn && deleteBtn && deleteModal) {
        setTimeout(() => {
            profileHeader.style.animation = "slideIn 1s forwards, fadeIn 1s forwards";
            profileImage.style.animation = "slideIn 1s forwards 0.4s, fadeIn 1s forwards 0.4s";
            profileDetails.style.animation = "slideIn 1s forwards 0.5s, fadeIn 1s forwards 0.5s";
            editBtn.style.animation = "slideIn 1s forwards 0.8s, fadeIn 1s forwards 0.8s";
            deleteBtn.style.animation = "slideIn 1s forwards 0.9s, fadeIn 1s forwards 0.9s";
            deleteModal.style.animation = "slideIn 1s forwards 1.2s, fadeIn 1s forwards 1.2s";
        }, 500);
    }
});

// Trim inputs when form is submitted
document.querySelector('form').addEventListener('submit', function(event) {
    const inputs = this.querySelectorAll('input');
    inputs.forEach(function(input) {
        input.value = input.value.trim();
    });
});

// Trim input on blur event
document.querySelectorAll('input').forEach(function(input) {
    input.addEventListener('blur', function() {
        input.value = input.value.trim();
    });
});
