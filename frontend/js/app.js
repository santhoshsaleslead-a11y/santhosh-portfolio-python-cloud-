const API = "http://localhost:8000";

// Load Services
async function loadServices() {
    const res = await fetch(API + "/services");
    const data = await res.json();

    const list = document.getElementById("serviceList");
    if (list) {
        list.innerHTML = "";
        data.forEach(s => {
            list.innerHTML += `<li>${s.name} - $${s.price}</li>`;
        });
    }
}
loadServices();

// Admin Login
async function adminLogin() {
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    const res = await fetch(API + "/admin/login", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({email, password})
    });

    const data = await res.json();
    localStorage.setItem("token", data.token);
    window.location.href = "admin.html";
}

// Payment
async function makePayment() {
    const email = document.getElementById("email").value;
    const service = document.getElementById("service").value;
    const amount = document.getElementById("amount").value;
    const method = document.getElementById("method").value;

    await fetch(API + "/payment", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({email, service, amount, method})
    });

    alert("Payment Successful");
}
