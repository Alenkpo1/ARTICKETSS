//Configura el manejo de clics para mostrar u ocultar respuestas de preguntas frecuentes al cargar el DOM.
document.addEventListener("DOMContentLoaded", () => {
    const faqItems = document.querySelectorAll(".faq-item");

    faqItems.forEach(item => {
        const question = item.querySelector(".faq-question");
        const answer = item.querySelector(".faq-answer");

        question.addEventListener("click", () => {
            const isVisible = answer.style.display === "block";
            answer.style.display = isVisible ? "none" : "block";
        });
    });
});