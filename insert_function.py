with open('email-subscription-handler/lambda_function.py', 'r', encoding='utf-8') as f:
    content = f.read()

with open('email-subscription-handler/pdf_email_function.txt', 'r', encoding='utf-8') as f:
    new_func = f.read()

insert_pos = content.find('def list_book_subscribers():')
new_content = content[:insert_pos] + new_func + content[insert_pos:]

with open('email-subscription-handler/lambda_function.py', 'w', encoding='utf-8') as f:
    f.write(new_content)

print('PDF email function inserted successfully')
