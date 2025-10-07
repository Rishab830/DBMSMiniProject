function togglePassword(passwordId) {
    const passwordInput = document.getElementById(passwordId);
    const toggleButton = document.getElementById("toggle-"+passwordId);

    if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
        toggleButton.textContent = '🙈';
    } else {
        passwordInput.type = 'password';
        toggleButton.textContent = '👁️';
    }
}

document.addEventListener('DOMContentLoaded', function () {
    const currentDateElement = document.getElementById('currentDate');
    if (currentDateElement) {
        const today = new Date();
        const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
        currentDateElement.textContent = today.toLocaleDateString('en-US', options);
    }

    const addMedForm = document.getElementById('addMedForm');
    if (addMedForm) {
        addMedForm.addEventListener('submit', function (e) {
            e.preventDefault();

            const medName = document.getElementById('medName').value;
            const medDosage = document.getElementById('medDosage').value;
            const medFrequency = document.getElementById('medFrequency').value;
            const medTime = document.getElementById('medTime').value;
            const medDuration = document.getElementById('medDuration').value;

            const medicationsList = document.getElementById('medicationsList');

            const newMedCard = document.createElement('div');
            newMedCard.className = 'med-card';
            newMedCard.innerHTML = `
                <div class="med-header">
                    <h3>${medName}</h3>
                    <span class="med-dosage">${medDosage}</span>
                </div>
                <div class="med-details">
                    <p><strong>Frequency:</strong> ${medFrequency}</p>
                    <p><strong>Time:</strong> ${medTime}</p>
                    <p><strong>Duration:</strong> ${medDuration}</p>
                </div>
            `;

            medicationsList.appendChild(newMedCard);

            closeAddMedModal();
            addMedForm.reset();
        });
    }

    loadProfileData();
});

function showAddMedModal() {
    const modal = document.getElementById('addMedModal');
    if (modal) {
        modal.style.display = 'block';
    }
}

function closeAddMedModal() {
    const modal = document.getElementById('addMedModal');
    if (modal) {
        modal.style.display = 'none';
    }
}

window.onclick = function (event) {
    const modal = document.getElementById('addMedModal');
    if (event.target === modal) {
        closeAddMedModal();
    }
}

function editUser(userId) {
    alert('Edit functionality for user ' + userId + ' would be implemented here.');
}

function deleteUser(userId) {
    if (confirm('Are you sure you want to delete user ' + userId + '?')) {
        const row = event.target.closest('tr');
        if (row) {
            row.style.transition = 'opacity 0.3s';
            row.style.opacity = '0';
            setTimeout(() => {
                row.remove();
            }, 300);
        }
    }
}
