# EmailLibrary.py
import smtplib
import imaplib
import email
from email.header import decode_header
import re
from email.message import EmailMessage

def send_email_alert(subject, body, to):
    msg = EmailMessage()
    msg.set_content(body)
    msg['subject'] = subject
    msg['to'] = to

    user = "nong.nukhun@gmail.com"
    password = "xetl hdth asrc judh"

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(user, password)
    server.send_message(msg)
    server.quit()

def find_emails_in_text(text):
    user = "nong.nukhun@gmail.com"
    password = "xetl hdth asrc judh"

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(user, password)
    server.select('inbox')

    data = mail.search('696965', 'ALL')
    print(data)

    # email_pattern = r'[0-9]{6}'
    # emails = re.findall(email_pattern, text)
    # print(emails)
    # return emails

def read_emails(search_text):
    decoded_payload="Not Found"
    user = "nong.nukhun@gmail.com"
    password = "xetl hdth asrc judh"

    # Connect to the server
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    
    # Login to your account
    mail.login(user, password)
    mail.enable
    mail.utf8_enabled
    # Select the mailbox you want to use
    mail.select("inbox")
    # ค้นหาอีเมลที่มีคำว่า "(OTP)" และเลขอ้างอิง DPAM
    #search_text = "KOBCD"
    search_criteria = f'(TEXT "{search_text}")'.encode('UTF-8')
    print(search_criteria)
    status, data = mail.search("UTF-8", search_criteria)

    # Search for all emails
    #status, data = mail.search('UTF-8', 'ALL')
    
    if status == 'OK':

        email_ids = data[0].split()
        print("Found emails:", email_ids)
        
        for email_id in email_ids:
            # Fetch the email headers and body for each email
            status, message_data = mail.fetch(email_id, '(RFC822)')
            
            if status == 'OK':
                # Get the email content
                raw_email = message_data[0][1]
                
                # Parse the email message
                email_message = email.message_from_bytes(raw_email)
                
                # แปลงหัวข้อให้เป็น UTF-8 ถ้ามีอักขระพิเศษ
                subject = email_message['subject']
                decoded_subject, charset = decode_header(subject)[0]
                if charset:
                    decoded_subject = decoded_subject.decode(charset)

                # Print out the email details
                print(f"Subject: {decoded_subject}")
                print(f"From: {email_message['from']}")
                print(f"To: {email_message['to']}")
                print(f"Date: {email_message['date']}")
                
                # If the email message is multipart
                if email_message.is_multipart():
                    for part in email_message.walk():
                        # If part is text/plain or text/html
                        if part.get_content_type() == "text/plain" or part.get_content_type() == "text/html":
                            # Decode the header if necessary
                            content_type = part.get_content_type()
                            charset = part.get_content_charset()
                            if charset:
                                decoded_payload = part.get_payload(decode=True).decode(charset)
                            else:
                                decoded_payload = part.get_payload(decode=True)
                            
                            print(f"Content:\n{decoded_payload}")
                else:
                    # If the email message isn't multipart
                    content_type = email_message.get_content_type()
                    charset = email_message.get_content_charset()
                    if charset:
                        decoded_payload = email_message.get_payload(decode=True).decode(charset)
                    else:
                        decoded_payload = email_message.get_payload(decode=True)
                    
                    print(f"Content:\n{decoded_payload}")
                    
            else:
                print("Error fetching email:", status)
    else:
        print("Error searching emails:", status)
    
    
    
    # Logout and close the connection
    mail.logout()
    return decoded_payload

if __name__ == '__main__':
    #send_email_alert("Hey","Hello world","nong.nukhun@gmail.com")
    #find_emails_in_text("รหัสผ่านแบบใช้ครั้งเดียว (OTP) ของท่านคือ 696965 เลขที่อ้างอิงDPAM")
    read_emails("KOBCD")