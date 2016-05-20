$(function() {
    $('#search input').on('input', function(evt) {
        var term = $(this).val(),
            url = '/glossary/search/' + term,
            li_str = '';
        $.get(url, {}, function(data) {
            $.each(data.results, function(idx, text) {
                li_str += '<li class="ellipsis"><a href="/glossary/gloss/' + idx + '">' + text + '</a></li>';
            });
            $('.page').html('<ul class="list-unstyled">' + li_str + '</ul>');
        });
    });
});
