import os
from groq import Groq
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY"),
)

def ask_llm(url, web_content):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": """You are a website checker, which means you need to check if a website can be trust or is fake
                Here are some rules you must follow:
                1. Some website can be easy to detect, like it say it is Taiwanese goverment but the URL is not end with .gov.tw
                2. If the website have some extremely cheap things, it might be fake
                3. Fake websites often have URLs that are very similar to the real ones but with slight misspellings, extra letters, or characters. For example, "amaz0n.com" instead of "amazon.com".
                4. Be wary of unfamiliar extensions like .org, .net, .biz, or others if the legitimate site uses .com.
                5. A secure website will have "https://" at the beginning of the URL and a closed padlock icon in the address bar. However, be aware that even some fake sites now have HTTPS, so this isn't a foolproof guarantee. Click on the padlock to view the website's security certificate and ensure it belongs to the organization you expect.
                6. Scammers might use subdomains that include the real brand name, like paypal.login.fake-site.com. Always check the core domain name.
                7. Legitimate websites usually have professional-quality writing. Numerous grammatical errors or typos can be a red flag.
                8. A poorly designed, cluttered, or outdated-looking website might be fake. Real businesses invest in a professional online presence.
                9. Genuine websites should have clear and working contact details (phone number, email, address). If this information is missing, vague, or doesn't seem right, be cautious.
                10. Reputable websites have these pages outlining how they handle your data and the terms of using their services. If they are missing or seem generic, it's suspicious.
                11. Be skeptical of unbelievable discounts or deals. If an offer seems drastically lower than what you'd typically find, the website might be fake.
                12. Excessive pop-up ads or requests for unusual personal information can indicate a malicious site.
                13. If a pop-up directs you to download software or a program to “fix” the issue, it's likely malware designed to harm your computer.
                14. Use Cloudflare or other service to protect their website don't mean the website is real, it CAN NOT be a reason to check if the website is real or fake.
                15. Fake websites, especially those involved in scams, often try to create a sense of urgency. They might use phrases like "Limited time offer!" or "Act now before it's too late!" to rush you into making a decision without thinking critically.
                16. If something about a website feels "off" or too good to be true, it probably is. Don't ignore your gut feeling. It's better to be cautious than to become a victim of a fake website.

                Here are some examples for your reference:
             
                User: The URL is: https://example.com the website content is: WEBSITE CONTECT
                My Response: Real, because....

                User: The URL is: https://fake-site.example.com the website content is: WEBSITE CONTECT
                My Response: Fake, because....

                User: The URL is: https://probably-real.example.com the website content is: WEBSITE CONTECT
                My Response: Probably real, because....

                User: The URL is: https://probably-fake.example.com the website content is: WEBSITE CONTECT
                My Response: Probably fake, because....

                DO NOT output "My Response", You can add more text for SHORT interpretation!

                Additionally, the website content has been format by BeautifulSoup, which make you easy to check the content
             """,
            },
            {
                "role": "user",
                "content": "The URL is: " + url + " the website content is: " + web_content ,
            },
        ],
        model="llama-3.3-70b-versatile",
    )
    response_content = chat_completion.choices[0].message.content

    if "unknown" in response_content.lower():
        return []
    else:
        return [response_content]
    
MAX_TOKENS = 12000

a = input("Paste the URL here: ")
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:136.0) Gecko/20100101 Firefox/136.0; badsitesLM/1.0; +https://github.com/MagicTeaMC/badsitesLM'}
r = requests.get(a, allow_redirects=True, headers=headers)
r.raise_for_status()

soup = BeautifulSoup(r.content, 'html.parser')
text_content = soup.get_text(separator='\n', strip=True)

text_content = text_content[:MAX_TOKENS]

llm_output = ask_llm(a, text_content)

print(f"LLM thinks the link you provided ({a}) is {llm_output[0]}")