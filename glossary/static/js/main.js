$(function() {

    glossary();
    search();
    add_entity_select();

    function glossary() {
        $('#nav #controls button#archive-action').click(function() {
            var gloss_ids = get_checked_gloss_ids();
            $.post('/glossary/archive', { gloss_ids: gloss_ids }, function(data) {
                if (data.status == 'success') {
                    window.location.reload();
                } else {
                    alert('Unknown error.');
                }
            });
        });

        $('#nav #controls button#label-action').click(function() {
            var gloss_ids = get_checked_gloss_ids(),
                label_id = $('#nav #controls select#label').val();
            $.post('/glossary/label', { gloss_ids: gloss_ids, label_id: label_id }, function(data) {
                if (data.status == 'success') {
                    window.location.reload();
                } else {
                    alert('Unknown error.');
                }
            });
        });
    }

    function add_entity_select() {
        $('#entity-add-menu-page select').change(function(evt) {
            var type_ = $(evt.target).val().toLowerCase();
            window.location.pathname = '/glossary/entity/' + type_ + '/add';
        });
    }

    function search() {
        $('#search button').click(function(evt) {
            evt.preventDefault();
            var term = $(this).parent().find('input').val();
            window.location.replace(window.location.href + term);
        });
    }

    function render_search_results(data) {
        var li_str = '';
        $.each(data.results, function(idx, obj) {
            var path = '';
            if (obj.type_ != 'gloss') {
                path = '/glossary/entity/' + obj.type_;
            } else {
                path = '/glossary/gloss';
            }
            li_str += '' +
                '<li class="ellipsis">' +
                '   <span>' + capitalize(obj.type_) + ': </span>' +
                '   <a href="' + path + '/' + obj.idx + '">' + obj.text_ + '</a>' +
                '</li>';
        });
        $('.page').html('<ul id="glossary" class="list-unstyled">' + li_str + '</ul>');
    }

    function capitalize(string) {
        return string.charAt(0).toUpperCase() + string.slice(1);
    }

    function remove_menu_highlighting() {
        $('#menu li span').removeClass('active');
    }

    function get_checked_gloss_ids() {
        var gloss_ids = [];
        $('#glossary input:checked').each(function() {
            gloss_ids.push($(this).attr('name'));
        });
        return gloss_ids;
    }
});
