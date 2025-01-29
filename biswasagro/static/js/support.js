document.addEventListener("DOMContentLoaded", function () {
    const forms = document.querySelectorAll(".form-container");
    const buttons = document.querySelectorAll(".sidebar button");

    buttons.forEach(button => {
        button.addEventListener("click", function () {
            const formToShow = document.getElementById(this.getAttribute("data-form"));

            forms.forEach(form => form.classList.add("hidden"));
            formToShow.classList.remove("hidden");
        });
    });
});
