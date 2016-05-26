$(function() {

    setup_search();
    var page = get_page();
    if (get_page() == 'glossary') {
        index_page();
    } else if (get_page() == 'gloss') {
        gloss_page();
    } else if (get_page() == 'create') {
         add_entity_select();
    }

    function index_page() {
        $('#nav #controls button#archive-action').click(function() {
            var gloss_ids = get_checked_gloss_ids();
            $.post('/glossary/gloss/archive', { gloss_ids: gloss_ids }, function(data) {
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
            $.post('/glossary/label/add', { gloss_ids: gloss_ids, label_id: label_id }, function(data) {
                if (data.status == 'success') {
                    window.location.reload();
                } else {
                    alert('Unknown error.');
                }
            });
        });
    }

    function gloss_page() {
        $('#nav #controls button#label-action').click(function() {
            var gloss_id = get_gloss_id(),
                label_id = $('#nav #controls select#label').val();
            $.post('/glossary/label/add', { gloss_id: gloss_id, label_id: label_id }, function(data) {
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
            window.location.pathname = '/glossary/entity/create/' + type_;
        });
    }

    function setup_search() {
        $('#search button').click(function(evt) {
            evt.preventDefault();
            var term = $(this).parent().find('input').val(),
                // We don't just use window.location.href in case the user searches
                // while already on a search results page.
                url = window.location.origin + '/glossary?q=' + term;
            window.location.replace(url);
        });
    }

    function get_checked_gloss_ids() {
        var gloss_ids = [];
        $('#glossary input:checked').each(function() {
            gloss_ids.push($(this).attr('name'));
        });
        return gloss_ids;
    }

    function get_page() {
        var path = window.location.pathname.split('/'),
            parts = [],
            i;
        for (i = 0; i < path.length; i++) {
            if (path[i] === '')
                continue;
            parts.push(path[i]);
        }
        if (parts.length === 1) {
            return parts[0];
        } else if (parts.length > 1) {
            return parts[parts.length-1];
        }
    }

    function get_gloss_id() {
        var parts = window.location.href.split('/');
        return parts[parts.length-1];
    }
});
