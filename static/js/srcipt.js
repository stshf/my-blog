document.addEventListener('DOMContentLoaded', function() {
    // Toggle機能の設定
    const menuToggle = document.querySelector('.menu-toggle');
    const menu = document.getElementById('menu');

    menuToggle.addEventListener('click', function() {
        menu.classList.toggle('show');
    });

    window.addEventListener('resize', function() {
        if (window.innerwidth > 768) {
            menu.classList.remove('show')
        }
    });

    // コメント機能の設定
    const commentForms = document.querySelectorAll('.comment-form');
    commentForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            const name = this.querySelector('.commenter-name').value;
            const text = this.querySelector('.comment-text').value;

            if (name && text) {
                addComment(this, name, text);
                this.reset();
            }
        });
    });

    //検索機能の実装
    const searchForm = document.getElementById('search-form');
    const searchInput = document.getElementById('search-input');
    const resetButton = document.getElementById('reset-search');
    const blogPosts = document.querySelectorAll('#blog-posts article');


    function performSearch() {
        const searchTerm = searchInput.value.toLowerCase();

        blogPosts.forEach(post => {
            const title = post.querySelector('h3').textContent.toLowerCase();
            const content = post.querySelector('p:not(.date)').textContent.toLowerCase();

            if (title.includes(searchTerm) || content.includes(searchTerm)) {
                post.style.display = 'block';
            } else {
                post.style.display = 'none';
            }
        });
    }
searchForm.addEventListener('submit', function(e) {
    e.preventDefault();       
    performSearch();
});

// 検索入力欄の内容が変更されるたびに検索を実行
searchInput.addEventListener('input', performSearch);

// リセットボタンのイベントリスナー
resetButton.addEventListener('click', function() {
    searchInput.value = '';
    performSearch();
});

// comment
function addComment(form, name, text) {
    const commentsList = form.closest('.comments-section').querySelector('.comments-list');
    const li = document.createElement('li');
    li.innerHTML = `
        <strong>${name}</storng> - ${new Date().toLocaleString()}
        <p>${text}</p>
        `;
    commentsList.appendChild(li);
}
});