$(function() {

    setup_search();
    setup_nav_controls();
    watch_for_edits();
    setup_tooltips();
    setup_add_image_button();
    toggle_label_visibility();

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
            '<li>' + escape_html(imgTag) + '</li>'
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

    function watch_for_edits() {
        var $text = $('textarea#edit-field'),
            $preview = $('#edit-preview');

        refresh_edit_preview();

        $text.change(refresh_edit_preview);
        $text.keyup(debounce(refresh_edit_preview, 1000));

        function refresh_edit_preview() {
            var text = $('textarea').val();
            $.ajax({
                url: 'gloss/preview',
                type: 'POST',
                data: {
                    text: $text.val()
                },
                success: function(data) {
                    $preview.html(data);
                    MathJax.Hub.Queue(['Typeset', MathJax.Hub]);
                }
            });
        }
    }

    function escape_html(string) {
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

    function toggle_label_visibility() {
        var $button = $('#btn-show-labels button'),
            $list = $('#menu-label-list'),
            isHidden = true;
        $button.click(function() {
            isHidden = !isHidden;
            if (isHidden) {
                $list.addClass('hidden');
                $button.text('Show Labels');
            } else {
                $list.removeClass('hidden');
                $button.text('Hide Labels');
            }
        });
    }

    /* Credit: https://davidwalsh.name/javascript-debounce-function.
     */
    function debounce(func, wait, immediate) {
        var timeout;
        return function() {
            var context = this, args = arguments;
            var later = function() {
                timeout = null;
                if (!immediate) func.apply(context, args);
            };
            var callNow = immediate && !timeout;
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
            if (callNow) func.apply(context, args);
        };
    };
});
