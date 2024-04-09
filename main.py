from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

'''
find_reflections(html: str, unique_val: str) -> list[str]

A method to locate all reflection points of a parameter.
'''
def find_reflections(html: str, unique_val: str) -> list[str]:
    reflections = []
    # Iterate throguh each line of the HTML
    for line in html.splitlines():
            # If the line contains the unique value, then add it to the list
            if line.find(unique_val) != -1:
                reflections.append(line.strip())
                
    return reflections

'''
determine_escape_chars(html_tag: str, unique_val: str) -> str

Determine what is to the right of the reflection point which we will use to 
terminate the element in which the reflection occurs.
'''
def determine_escape_chars(html_tag: str, unique_val: str) -> str:
    return html_tag.split(unique_val, 2)[1]

def determine_absorb_chars(html_tag: str, unique_val: str) -> str:
    return html_tag.split(unique_val, 2)[0]

def create_injection(html_tag: str, unique_val: str, payload: str) -> str:
    return f"{determine_escape_chars(html_tag, unique_val)}{payload}{determine_absorb_chars(html_tag, unique_val)}"

'''
main()

The main method
'''
def main():
    #Testing url: https://public-firing-range.appspot.com/reflected/parameter/attribute_quoted?q=a

    url = "https://public-firing-range.appspot.com/reflected/parameter/attribute_quoted?q=a"
    parameter_name = "q"
    parameter_value = "a"

    unique_value = "AWrfWEsw"

    unique_url = url.replace(f"{parameter_name}={parameter_value}", f"{parameter_name}={unique_value}")

    with sync_playwright() as p:
        browser = p.webkit.launch()
        page = browser.new_page()
        page.goto(unique_url) # Make request to specified page
        
        html = BeautifulSoup(page.content(), features="html.parser").prettify() # Get nicely formatted HTML
        with open("untracked/page.html", "w") as file:
            file.write(html)
        
        reflections = find_reflections(html, unique_value) # Get list of reflection points
        print(reflections)
        
        for reflection in reflections:
            inj = create_injection(reflection, unique_value, "<script>alert()</script>")
            print(inj)
            
        browser.close()

main()
    