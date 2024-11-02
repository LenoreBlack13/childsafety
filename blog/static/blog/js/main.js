(function () {
    "use strict";

    // Reviews text on carousel
    function toggleText(reviewId) {
        const textElement = document.getElementById(reviewId);
        if (textElement) { // Проверяем наличие элемента
            const moreText = textElement.querySelector('.more-text');
            const readMoreSpan = textElement.nextElementSibling;

            if (moreText) { // Проверяем наличие .more-text
                // Проверяем, виден ли дополнительный текст
                if (moreText.style.display === 'none' || moreText.style.display === '') {
                    moreText.style.display = 'inline';
                    readMoreSpan.textContent = 'Скрыть';
                } else {
                    moreText.style.display = 'none';
                    readMoreSpan.textContent = '...Читать далее';
                }
            }
        }
    }

    // Current year
    const currentYearElement = document.getElementById('current-year');
    if (currentYearElement) {
        currentYearElement.textContent = new Date().getFullYear();
    }

    // Category dropdown
    function toggleDropdown() {
        const dropdownContent = document.getElementById("dropdown-content");
        if (dropdownContent) { // Проверяем существование элемента
            dropdownContent.style.display = dropdownContent.style.display === "block" ? "none" : "block";
        }
    }

    // Закрытие выпадающего списка при щелчке вне
    window.onclick = function (event) {
        if (!event.target.matches('.dropbtn')) {
            const dropdowns = document.getElementsByClassName("dropdown-content");
            for (let i = 0; i < dropdowns.length; i++) {
                const openDropdown = dropdowns[i];
                if (openDropdown.style.display === "block") {
                    openDropdown.style.display = "none";
                }
            }
        }
    }

    // Комментарии
    window.toggleReplyForm = function(commentId) {
        const form = document.getElementById(`reply-form-${commentId}`);
        if (form) { // Проверяем существование формы
            form.style.display = form.style.display === 'none' ? 'block' : 'none';
        }
    };

    // Обработчики событий при загрузке документа
    document.addEventListener('DOMContentLoaded', function () {
        const prevButton = document.getElementById('prevButton');
        const nextButton = document.getElementById('nextButton');
        const carousel = document.querySelector('#question-slider');

        if (carousel) { // Проверяем существование карусели
            // Функция для управления видимостью кнопок "Предыдущий" и "Следующий"
            function toggleButtons() {
                const items = [...carousel.querySelectorAll('.carousel-item')];
                const activeIndex = items.findIndex(item => item.classList.contains('active'));

                if (prevButton) {
                    prevButton.style.display = activeIndex === 0 ? 'none' : 'inline-block';
                }

                if (nextButton) {
                    if (activeIndex === items.length - 1) {
                        nextButton.style.display = 'none';
                        nextButton.disabled = true;
                    } else {
                        nextButton.style.display = 'inline-block';
                        nextButton.disabled = false;
                    }
                }
            }

            // Изначально скрываем кнопки на первом слайде
            toggleButtons();

            // Обработчик события для обновления видимости кнопок при переключении слайдов
            carousel.addEventListener('slid.bs.carousel', toggleButtons);
        }

        // Получаем все radio-кнопки и назначаем им обработчик
        const quizForm = document.getElementById('quiz-form');
        if (quizForm) { // Проверяем существование формы с вопросами
            const radioButtons = quizForm.querySelectorAll('input[type="radio"]');

            radioButtons.forEach(radio => {
                radio.addEventListener('change', function () {
                    // Переключаем на следующий слайд
                    if (nextButton) {
                        nextButton.click();
                    }
                });
            });
        }
    });

    // Поиск по блогу
    $(document).ready(function () {
        $('#search-form').on('submit', function (event) {
            event.preventDefault();
            var query = $('#search-input').val();

            $.ajax({
                url: "/search/",
                data: {
                    'query': query
                },
                dataType: 'json',
                success: function (data) {
                    $('.post-list').empty(); // очищаем текущие посты
                    $.each(data.posts, function (index, post) {
                        $('.post-list').append(`
                            <article class="media content-section">
                                <img class="rounded-circle article-img" src="${post.author_profile}">
                                <div class="media-body">
                                    <div class="article-metadata">
                                        <a class="mr-2" href="/user-posts/${post.author}">${post.author}</a>
                                        <small class="text-muted">${post.date_posted}</small>
                                    </div>
                                    <h2><a class="article-title" href="/post/${post.id}">${post.title}</a></h2>
                                    <p class="article-content">${post.content}</p>
                                </div>
                            </article>
                        `);
                    });
                },
                error: function (xhr, status, error) {
                    console.log('Ошибка поиска: ', error);
                }
            });
        });
    });
})();
