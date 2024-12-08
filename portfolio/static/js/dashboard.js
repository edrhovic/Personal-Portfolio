document.addEventListener("DOMContentLoaded", () => {
    const typingEffect = (element, words, speed = 150) => {
        let i = 0, j = 0;
        let isDeleting = false;

        const type = () => {
            if (j < words.length) {
                const currentWord = isDeleting
                    ? words[j].substring(0, i--)
                    : words[j].substring(0, i++);
                
                element.textContent = currentWord;

                if (!isDeleting && i === words[j].length) {
                    isDeleting = true;
                    setTimeout(type, 1000);
                } else if (isDeleting && i === 0) {
                    isDeleting = false;
                    j = (j + 1) % words.length;
                    setTimeout(type, 500);
                } else {
                    setTimeout(type, speed);
                }
            }
        };

        type();
    };

    const professionText = document.querySelector(".profession span");

    if (professionText) {
        typingEffect(professionText, ["Developer ", "Web Designer "], 75);
    }

    const elementsToAnimate = document.querySelectorAll(".hidden");

    const revealOnScroll = () => {
        elementsToAnimate.forEach((el) => {
            const rect = el.getBoundingClientRect();
            if (rect.top < window.innerHeight - 100) {
                el.classList.add("visible");
                el.classList.remove("hidden");
            }
        });
    };

    window.addEventListener("scroll", revealOnScroll);
    revealOnScroll();
});
