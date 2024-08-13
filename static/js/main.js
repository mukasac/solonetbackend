// Global variables
let isLoggedIn = false;
let currentUser = null;
let selectedPlan = '';
let selectedPrice = 0;

// Get modal elements
const loginModal = document.getElementById('loginModal');
const signupModal = document.getElementById('signupModal');
const profileModal = document.getElementById('profileModal');
const addPaymentModal = document.getElementById('addPaymentModal');
const planConfirmModal = document.getElementById('planConfirmModal');

// Event listener for plan selection
document.querySelectorAll('.select-plan').forEach(button => {
    button.addEventListener('click', function(e) {
        e.preventDefault();
        selectedPlan = this.getAttribute('data-plan');
        selectedPrice = this.getAttribute('data-price');
        handlePlanSelection();
    });
});

function handlePlanSelection() {
    if (isLoggedIn) {
        showProfileModal();
    } else {
        showLoginModal();
    }
}

function showLoginModal() {
    loginModal.style.display = 'block';
}

function showProfileModal() {
    updateProfileInfo();
    profileModal.style.display = 'block';
}

function updateProfileInfo() {
    document.getElementById('profileName').textContent = currentUser.name;
    document.getElementById('profileEmail').textContent = currentUser.email;
    document.getElementById('profilePlan').textContent = selectedPlan;
    // Update payment methods display
    updatePaymentMethods();
}

function updatePaymentMethods() {
    const paymentMethodsContainer = document.getElementById('paymentMethods');
    paymentMethodsContainer.innerHTML = ''; // Clear existing methods
    if (currentUser.paymentMethods && currentUser.paymentMethods.length > 0) {
        currentUser.paymentMethods.forEach(method => {
            const methodElement = document.createElement('div');
            methodElement.textContent = `Card ending in ${method.last4}`;
            paymentMethodsContainer.appendChild(methodElement);
        });
    } else {
        paymentMethodsContainer.innerHTML = '<p>No payment methods added yet.</p>';
    }
}

// Handle login form submission
document.getElementById('loginForm').onsubmit = function(e) {
    e.preventDefault();
    const email = document.getElementById('loginEmail').value;
    const password = document.getElementById('loginPassword').value;
    // Simulate successful login
    isLoggedIn = true;
    currentUser = { name: 'John Doe', email: email, paymentMethods: [] };
    loginModal.style.display = 'none';
    showProfileModal();
}

// Handle signup form submission
document.getElementById('signupForm').onsubmit = function(e) {
    e.preventDefault();
    const name = document.getElementById('signupName').value;
    const email = document.getElementById('signupEmail').value;
    const password = document.getElementById('signupPassword').value;
    // Simulate successful signup
    isLoggedIn = true;
    currentUser = { name: name, email: email, paymentMethods: [] };
    signupModal.style.display = 'none';
    showProfileModal();
}

// Handle add payment method button
document.getElementById('addPaymentMethod').onclick = function() {
    profileModal.style.display = 'none';
    addPaymentModal.style.display = 'block';
}

// Handle add payment form submission
document.getElementById('addPaymentForm').onsubmit = function(e) {
    e.preventDefault();
    const cardNumber = document.getElementById('cardNumber').value;
    const last4 = cardNumber.slice(-4);
    currentUser.paymentMethods.push({ last4: last4 });
    addPaymentModal.style.display = 'none';
    showPlanConfirmModal();
}

function showPlanConfirmModal() {
    document.getElementById('selectedPlan').textContent = selectedPlan;
    document.getElementById('selectedPrice').textContent = selectedPrice;
    planConfirmModal.style.display = 'block';
}

// Handle plan confirmation
document.getElementById('confirmPlan').onclick = function() {
    // Here you would typically process the payment
    alert(`Payment processed for ${selectedPlan} plan. Amount: $${selectedPrice}`);
    currentUser.plan = selectedPlan;
    planConfirmModal.style.display = 'none';
    showProfileModal();
}

// Close modals when clicking outside
window.onclick = function(event) {
    if (event.target.classList.contains('modal')) {
        event.target.style.display = 'none';
    }
}

// Close buttons for modals
document.querySelectorAll('.close').forEach(closeBtn => {
    closeBtn.onclick = function() {
        this.closest('.modal').style.display = 'none';
    }
});