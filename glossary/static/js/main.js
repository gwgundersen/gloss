$(function() {

    setup_search();
    setup_nav_controls();
    //setup_datatables();
    setup_tooltips();
    setup_add_image_button();

    function setup_add_image_button() {
        $('#add-image-btn').click(function(evt) {
            evt.preventDefault();
            $('#image-upload-btn').trigger('click');
            $(':file').change(function(evt) {
                var file = this.files[0],
                    name = file.name,
                    formData;
                formData = new FormData();
                formData.append('file', $('#image-uploader input[type="file"]')[0].files[0]);
                $.ajax({
                    url: '/image/upload',
                    type: 'POST',
                    data: formData,
                    cache: false,
                    processData: false,
                    contentType: false,
                    success: function(data) {
                        console.log('Success:');
                        add_uploaded_image_tag(data);
                    },
                    error: function(data) {
                        console.log('Error:');
                        console.log(data);
                    }
                }, 'json');
            });
        });
    }

    function add_uploaded_image_tag(imgTag) {
        $('#uploaded-image-names').append(
            '<li>' + escapeHtml(imgTag) + '</li>'
        );
    }

    function setup_nav_controls() {
        $('#nav #controls button#archive-action').click(function() {
            var gloss_ids = get_checked_gloss_ids();
            $.post('gloss/archive', { gloss_ids: gloss_ids }, function(data) {
                if (data.status == 'success') {
                    window.location.reload();
                } else {
                    alert('Unknown error.');
                }
            });
        });
        $('#nav #controls button#archive-action').click(function() {
            var gloss_ids = get_checked_gloss_ids();
            $.post('gloss/archive', { gloss_ids: gloss_ids }, function(data) {
                if (data.status == 'success') {
                    window.location.reload();
                } else {
                    alert('Unknown error.');
                }
            });
        });
        $('#nav #controls button#label-action').click(function() {
            var gloss_ids = get_checked_gloss_ids(),
                label_id = $('#nav #controls select#label').val(),
                payload = { gloss_ids: gloss_ids, label_id: label_id, is_js: true };
            $.post('label/add', payload, function(data) {
                if (data.status == 'success') {
                    window.location.reload();
                } else {
                    alert('Unknown error.');
                }
            });
        });
    }

    function setup_search() {
        $('#search button').click(function(evt) {
            evt.preventDefault();
            var term = $(this).parent().find('input').val(),
                // We don't just use window.location.href in case the user searches
                // while already on a search results page.
                url = window.location.origin + '?q=' + term;
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

    function setup_datatables() {
        $('.dtable').DataTable();
    }

    function setup_tooltips() {
        var $elem;

        function mouseIn() {
            var value = $(this).attr('data-tooltip'),
                pos = $(this).position();
            $elem = $('' +
                '<div class="tooltip" ' +
                '     style="top: ' + pos.top + ' left: ' + pos.left + '"' +
                '>' + value + '</div>'
            );
            $(this).append($elem);
        }

        function mouseOut() {
            $elem.remove();
        }

        $('*[data-tooltip]').hover(mouseIn, mouseOut);
    }

    function escapeHtml(string) {
        var entityMap = {
            "&": "&amp;",
            "<": "&lt;",
            ">": "&gt;",
            '"': '&quot;',
            "'": '&#39;',
            "/": '&#x2F;'
        };
        return String(string).replace(/[&<>"'\/]/g, function (s) {
            return entityMap[s];
        });
    }
});
