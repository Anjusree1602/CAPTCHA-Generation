$(document).ready(function() {
    function updateCaptchaText(newText) {
        $('#captcha-text').text(newText);
    }

    $('#captcha-form').submit(function(e) {
        e.preventDefault();

        var captchaInput = $('#captcha-form input[name="captcha_input"]').val();
        
        $.ajax({
            url: '/verify',
            type: 'POST',
            data: {captcha_input: captchaInput},
            success: function(response) {
                $('#message').text(response.message).toggleClass('success', response.status === 'success').toggleClass('error', response.status !== 'success');
                $('#captcha-form input[name="captcha_input"]').val('');

                if (response.status === 'success') {
                    updateCaptchaText(response.new_captcha_text);
                }
            },
            error: function(xhr, status, error) {
                console.log(error);
            }
        });
    });

    $('#regenerate-button').click(function() {
        $.ajax({
            url: '/regenerate',
            type: 'GET',
            success: function(response) {
                updateCaptchaText(response.new_captcha_text);
            },
            error: function(xhr, status, error) {
                console.log(error);
            }
        });
    });

    // Initial captcha generation on page load
    $('#regenerate-button').trigger('click');
});
