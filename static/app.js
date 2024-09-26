let articles = [];
let previousArticleCount = 0;

// Only display two articles at a time (one per column)
const template = document.getElementById('article-template');

function fetchArticles() {
    fetch('/api/rss')
        .then(response => response.json())
        .then(data => {
            articles = data;

            // Start displaying articles after fetching
            displayArticles();

        })
        .catch(error => console.error('Error fetching articles:', error));
}

function displayArticles() {
    const slick = $('#articles');

    // Build out the articles, and add them to the articles div
    const fetchTime = new Date().toLocaleString();
    for (let i = 0; i < articles.length; i++) {
        const article = articles[i];
        const articleDiv = buildArticleDiv(article, fetchTime);
        slick.slick('slickAdd', articleDiv);
    }

    if (previousArticleCount > 0) {
        for (let i = 0; i < previousArticleCount; i++) {
            slick.slick('slickRemove', 0);
        }
    }

    previousArticleCount = articles.length;

}

function buildArticleDiv(article) {
    const articleClone = document.importNode(template.content, true);
    const articleTitle = articleClone.querySelector('.article-title');
    const articleDate = articleClone.querySelector('.article-date');
    const articleImage = articleClone.querySelector('.article-image');
    const articleDescription = articleClone.querySelector('.article-description');
    const articleBody = articleClone.querySelector('.article-body');
    const articleLink = articleClone.querySelector('.article-link');
    const channelName = articleClone.querySelector('.channel-name')
    const channelLogo = articleClone.querySelector('.channel-logo')

    articleTitle.innerHTML = article.article_title;
    articleDate.textContent = article.article_pubDate;
    articleImage.src = article.article_images;
    articleDescription.innerHTML = article.article_description;
    articleBody.innerHTML = article.article_body;
    articleLink.href = article.article_link;
    articleLink.textContent = article.title;
    channelName.textContent = article.channel_title;
    channelLogo.src = article.channel_image;

    return articleClone;
}

$(document).ready(function () {
    fetchArticles();

// Create a carousel of articles
    $('#articles').slick({
        slidesToShow: 2,
        slidesToScroll: 1,
        autoplay: true,
        autoplaySpeed: 30000,
        pauseOnHover: false,
        pauseOnDotsHover: false
    });

    $('#articles').on('afterChange', function (event, slick, currentSlide) {
        if (currentSlide === slick.slideCount - 2) {
            fetchArticles();
        }
    });
});