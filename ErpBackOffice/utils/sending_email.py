from django.core.mail import send_mail


class sending_email(object):

    sujet = ""
    message = ""
    from_email = ""
    recipient_list = []
    title = ""
    subtitle = ""
    body = ""
    html_message = ""
    fail_silently = False

    @staticmethod
    def send_mail_test(sujet, message, recipient_list, fail_silently, title, subtitle, body):
        '''sujet = "Test envoie mail"
        message = "Test envoie mail avec style"        
        recipient_list = ["fabermandeke@gmail.com"]'''

        from_email = 'noreply.nsandax@gmail.com'

        html_message =  '<!doctype html><html><head><meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no"><meta charset="utf-8">'
        html_message = html_message + '<style type="text/css">'
        html_message = html_message + '* { margin: 0; padding: 0; font-size: 100%; font-family: "Avenir Next", "Helvetica Neue", "Helvetica", Helvetica, Arial, sans-serif; line-height: 1.65; }img { max-width: 100%; margin: 0 auto; display: block; }body, .body-wrap { width: 100% !important; height: 100%; background: #f8f8f8; }a { color: #71bc37; text-decoration: none; }a:hover { text-decoration: underline; }.text-center { text-align: center; }.text-right { text-align: right; }.text-left { text-align: left; }.button { display: inline-block; color: white; background: #d2023b; border: solid #d2023b; border-width: 10px 20px 8px; font-weight: bold; border-radius: 4px; }'
        html_message = html_message + '.button:hover { text-decoration: none; }h1, h2, h3, h4, h5, h6 { margin-bottom: 20px; line-height: 1.25; }h1 { font-size: 16px; }h2 { font-size: 28px; }h3 { font-size: 24px; }h4 { font-size: 20px; }h5 { font-size: 16px; }p, ul, ol { font-size: 16px; font-weight: normal; margin-bottom: 20px; }.container { display: block !important; clear: both !important; margin: 0 auto !important; max-width: 580px !important; }.container table { width: 100% !important; border-collapse: collapse; }.container .masthead { padding: 25px 0; background: #d2023b; color: white; }.container .mastheadimg { width: 200px; padding: 10px 0; background:transparent;border-bottom:5px #00172d solid; }.container .masthead h1 { margin: 0 auto !important; max-width: 90%; text-transform: uppercase; }.container .content { background: white; padding: 30px 35px; }.container .content.footer { background: none; }.container .content.footer p { margin-bottom: 0; color: #888; text-align: center; font-size: 14px; }.container .content.footer a { color: #888; text-decoration: none; font-weight: bold; }.container .content.footer a:hover { text-decoration: underline; }.logo { width: 200px; }'
        html_message = html_message + '</style>'
        html_message = html_message + '</head><body>'
        html_message = html_message + '<table class="body-wrap">'
        html_message = html_message + '<tr><td class="container"><table>'
        html_message = html_message + '<tr><td align="center" class="mastheadimg"><img class="logo" src="http://www.influxapp.media/assets/images/logo_arpce_large.png"/></td></tr>'
        html_message = html_message + '<tr><td align="center" class="masthead"><h1>'+ title +'</h1></td></tr>'
        html_message = html_message + '<tr><td class="content"><img width=220 height=220 src="http://www.influxapp.media/assets/images/danger.png"/>'
        html_message = html_message + '<h4 style="margin-top:10px">' + subtitle + '</h4><p>'+ body +'</p></td></tr>'
        html_message = html_message + '</table></td></tr>'
        html_message = html_message + '<tr><td class="container"><table><tr><td class="content footer" align="center"><p>Nsandax ERP</p><p><a href="mailto:">admin@arpce.cd</a> </p></td></tr></table></td></tr>'
        html_message = html_message + '</table></body></html>'

        send_mail(sujet, message, from_email, recipient_list, fail_silently = False, html_message = html_message)