def send_ssl_email(sender,password,receivers:list,subject,plain_message='',html_message=''):
    import smtplib, ssl
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    
    #sender = "svc-etl@datayes.com" 
    #password = 'Aa111111'
    
    receivers = ','.join(receivers)
    
    
    host = "smtp.mxhichina.com"
    port = 465  # For SSL
    context = ssl.create_default_context()

    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = sender
    message["To"] = receivers
    
    if html_message:
        html_message_part = MIMEText(html_message, "html")
        message.attach(html_message_part)
    if plain_message:
        plain_message_part = MIMEText(plain_message, "plain")
        message.attach(plain_message_part)
        


   

    with smtplib.SMTP_SSL(host=host, port=port, context=context) as server:
        server.login(user=sender, password=password)
        server.sendmail(sender, receivers, msg=message.as_string())
