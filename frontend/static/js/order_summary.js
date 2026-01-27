const BASE_URL = "http://127.0.0.1:5000";

fetch(`${BASE_URL}/cart/details`)
    .then(res => res.json())
    .then(data => {
        const table = document.getElementById("orderTable");
        table.innerHTML = "";

        if (!data.items || data.items.length === 0) {
            table.innerHTML = `
        <tr>
          <td colspan="4" class="text-center">Cart is empty</td>
        </tr>
      `;
            document.getElementById("totalAmount").innerText = "$0";
            return;
        }

        data.items.forEach(item => {
            table.innerHTML += `
        <tr>
          <td>${item.name}</td>
          <td>${item.quantity}</td>
          <td>$${item.price}</td>
          <td>$${item.total}</td>
        </tr>
      `;
        });

        document.getElementById("totalAmount").innerText = `$${data.total}`;
    })
    .catch(err => {
        console.error("Error loading order summary:", err);
    });

function confirmOrder() {
    fetch(`${BASE_URL}/orders/confirm`, {
        method: "POST"
    })
        .then(res => res.json())
        .then(() => {
            window.location.href = "/dashboard";
        })
        .catch(err => console.error("Order failed:", err));
}

function goBack() {
    window.history.back();
}

