document.addEventListener("DOMContentLoaded", function() {

    let selectedId = null;
    let tableId = null;

    // Show modal and store selected ID
    document.querySelectorAll(".delete-table-entry").forEach(button => {
        button.addEventListener("click", function (event) {
            event.preventDefault();
            selectedId = this.getAttribute("data-id");
            tableId = this.getAttribute("table-id");
            document.getElementById("delete-modal").classList.add("show");
        });
    });

    // Handle cancel button
    document.querySelector(".cancel-btn").addEventListener("click", function () {
        document.getElementById("delete-modal").classList.remove("show");
        selectedId = null;
        tableId = null;
    });


    // Handle delete confirmation
    document.querySelector(".confirm-delete-btn").addEventListener("click", function () {
        if (selectedId && tableId) {
            fetch(`/${tableId}/delete/${selectedId}`, { 
                method: "DELETE",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCSRFToken()
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert("Deleted successfully!");
                    location.reload(); // Refresh to update the table
                } else {
                    alert(data.error);
                }
                document.getElementById("delete-modal").style.display = "none";
            })
            .catch(error => console.error("Error:", error));
        }
    });

});

//    // existing login code
//    const loginButton = document.querySelector("button");
//    if (loginButton) {
//        loginButton.addEventListener("click", function() {
//            window.location.href = "home.html";
//        });
//    }

// Function to get CSRF token from cookies
function getCSRFToken() {
    let cookieValue = null;
    let cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
        let cookie = cookies[i].trim();
        if (cookie.startsWith("csrftoken=")) {
            cookieValue = cookie.substring("csrftoken=".length, cookie.length);
            break;
        }
    }
    return cookieValue;
}
