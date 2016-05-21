$(function() {

    search();
    add_entity_select();

    function add_entity_select() {
        $('#entity-add-menu-page select').change(function(evt) {
            var type_ = $(evt.target).val().toLowerCase();
            window.location.pathname = '/glossary/entity/' + type_ + '/add';
        });
    }

    function search() {
        $('#search input').on('input', function(evt) {
            var term = $(this).val(),
                url = '/glossary/search/' + term,
                li_str = '';
            remove_menu_highlighting();
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
    }

    function capitalize(string) {
        return string.charAt(0).toUpperCase() + string.slice(1);
    }

    function remove_menu_highlighting() {
        $('#menu li span').removeClass('highlight');
    }
});
