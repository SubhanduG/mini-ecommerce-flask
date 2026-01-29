const BASE_URL = "http://127.0.0.1:5000";

document.addEventListener("DOMContentLoaded", () => {
    loadCartSummary();

    const confirmBtn = document.getElementById("confirmOrderBtn");
    if (confirmBtn) confirmBtn.addEventListener("click", confirmOrder);

    const backBtn = document.getElementById("goBackBtn");
    if (backBtn) backBtn.addEventListener("click", goBack);
});

async function loadCartSummary() {
    try {
        const res = await fetch(`${BASE_URL}/cart/details`, {
            credentials: "include",
            cache: "no-store"
        });
        const data = await res.json();

        const table = document.getElementById("orderTable");
        const totalElem = document.getElementById("totalAmount");

        table.innerHTML = "";

        if (!data.items || data.items.length === 0) {
            table.innerHTML = `<tr><td colspan="4" class="text-center">Cart is empty</td></tr>`;
            if (totalElem) totalElem.innerText = "$0";
            return;
        }

        data.items.forEach(item => {
            table.innerHTML += `
                <tr>
                    <td>${item.name}</td>
                    <td class="text-center">${item.quantity}</td>
                    <td>$${item.price}</td>
                    <td>$${item.total}</td>
                </tr>
            `;
        });

        if (totalElem) totalElem.innerText = `$${data.total}`;

    } catch (err) {
        console.error("Error loading order summary:", err);
        alert("Failed to load your cart. Please try again later.");
    }
}

async function confirmOrder() {
    try {
        const res = await fetch(`${BASE_URL}/orders/confirm`, {
            method: "POST",
            credentials: "include"
        });
        const data = await res.json();
        alert(data.message);

        if (res.ok) {
            window.location.href = "/";
        } else {
            await loadCartSummary();
        }

    } catch (err) {
        console.error("Error confirming order:", err);
        alert("Something went wrong while placing the order.");
    }
}

function goBack() {
    window.history.back();
}
