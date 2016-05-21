$(function() {

    function capitalize(string) {
        return string.charAt(0).toUpperCase() + string.slice(1);
    }

    $('#search input').on('input', function(evt) {
        var term = $(this).val(),
            url = '/glossary/search/' + term,
            li_str = '';
        $.get(url, {}, function(data) {
            $.each(data.results, function(idx, obj) {
                var type_ = capitalize(obj.type_),
                    dangling = '';
                if (!obj.has_entity) {
                    dangling = ' [Dangling]';
                }
                li_str += '' +
                    '<li class="ellipsis">' +
                    '   <span>' + type_ + dangling + ': </span>' +
                    '   <a href="/glossary/gloss/' + obj.idx + '">' + obj.text_ + '</a>' +
                    '</li>';
            });
            $('.page').html('<ul id="gloss-search-results" class="list-unstyled">' + li_str + '</ul>');
        });
    });
});
