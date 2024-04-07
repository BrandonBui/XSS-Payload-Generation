# XSS-Payload-Generation

## Project Goal/Ideas
The goal of this project is to explore various ways we can automate the generation of XSS payloads. Some ideas I've been brainstorming include:
1) Analyzing the surrounding HTML similar to how an attacker would by understanding what characters are needed to escape out of the leading HTML and absorb any remaining HTML. (Initial iteration will be similar to this)
2) Maintain a collection of XSS payloads and how they were useed to perform a "similarity" search to find payloads that may work given a certain context.
3) Create an ML model trained on XSS payloads for various contexts: Take in the HTML/JavaScript element where the user input is reflected --> Produce an XSS payload that would work.

Ideas 1 and 2 could reasonably be implemented, idea 3 would be more complicated. It's also not nearly as practical but could be pretty cool.

## Intelligent Payload Generation
There is no standard way for parameters to be reflected back onto the HTML. The reflection could appear in various different HTML elements, different attributes within elements, or even as text on the page itself. Somehow automating the process of analyzing the surrounding HTML to then craft a payload that both follows the rules of the input and the rules of HTML to create a valid injection will be a vital step in this project.  

  
__*Very* High Level Overview of Process__
1) Determine if payload is reflected
2) Determine what HTML is to the left of the reflection point and escape out of that HTML
3) Insert injection
4) Determine what HTML is to the right of the reflection point and absorb that remaining HTML

## Development Updates ##
### 4/6/2024 ###
The initial iteration of this tool will be focused on injecting payloads within an HTML element tag. The tool will attempt to determine the characters needed to escape and absorb the surrouning HTML and insert the injection. For example:

```html
<input id="commment-input" value="REFLECTED USER INPUT"/>
```

In this instance, the user's input gets reflected inside of the input tag. There are two options for injecting an XSS payload (I've tried adding the pipe character ( | ) to make it easier to delineate what the injection is):  
1) Breaking out of the value attribute's value and injecting the code within the input element tag:  
```html
<input id="comment-input" value=" | xss" onload=alert() class=" | "/>
```
In this case, the payload is ```xss" onload=alert() class="```. The ```xss"``` portion ends the ```value``` attribute in the original HTML, allowing an attacker to insert their own HTML. In this case, we insert ```onload=alert()``` which executes the JavaScript alert() function when the element loads in the browser.  Finally, we need to absorb the original " (double quote) that ends the ```value``` attribute.  In this case, we use ```class="``` to create a new attribute and absorb the remaining ".

2) Breaking out of the entire HTML element and injecting entirely new HTML:
```html
<input id="comment-input" value=" | xss"/> <script>alert()</script> <input class=" | "/>
```
In this case, the payload is ```xss"/> <script>alert()</script> <input class="```.  The ```xss"/>``` ends the entire ```input``` element, allowing an attacker to insert their own HTML.  In this case, we insert ```<script>alert()</script>```. Realistically, any JavaScript could be inserted between the script tags. Finally, we need to absorb the remaining quote and closing angle bracket. In this case, we use ```<input class=``` to absorb the remaining "/>.
