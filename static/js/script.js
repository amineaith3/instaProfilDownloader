document.addEventListener('DOMContentLoaded', function() {
    const faqItems = document.querySelectorAll('.faq-item');

    faqItems.forEach(item => {
        item.addEventListener('click', function() {
            const answer = this.querySelector('.faq-answer');
            const isVisible = answer.style.display === 'block';
            answer.style.display = isVisible ? 'none' : 'block';
        });
    });
});

function clearImageSection() {
    const imageSection = document.getElementById('image-section');
    imageSection.style.display = 'none'; // Hide the entire image section
}