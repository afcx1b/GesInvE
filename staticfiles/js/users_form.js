document.addEventListener("DOMContentLoaded", function () {
    function validateField(input, field) {
        let value = input.value.trim();
        let feedback = input.nextElementSibling;

        if (!value) {
            feedback.textContent = "";
            return;
        }

        fetch(`/users/validate_field/?field=${field}&value=${value}`)
            .then(response => response.json())
            .then(data => {
                if (!data.valid) {
                    feedback.textContent = data.message;
                    input.classList.add("is-invalid");
                } else {
                    feedback.textContent = "";
                    input.classList.remove("is-invalid");
                }
            });
    }

    document.getElementById("id_email").addEventListener("input", function () {
        validateField(this, "email");
    });

    document.getElementById("id_dni").addEventListener("input", function () {
        validateField(this, "dni");
    });

    document.getElementById("id_password").addEventListener("input", function () {
        validateField(this, "password");
    });

    document.getElementById("id_confirm_password").addEventListener("input", function () {
        let password = document.getElementById("id_password").value;
        let confirmPassword = this.value.trim();
        let feedback = this.nextElementSibling;

        if (confirmPassword && confirmPassword !== password) {
            feedback.textContent = "Las contraseñas no coinciden.";
            this.classList.add("is-invalid");
        } else {
            feedback.textContent = "";
            this.classList.remove("is-invalid");
        }
    });
});
