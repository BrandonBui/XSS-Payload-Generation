# XSS-Payload-Generation
## Intelligent Payload Generation
There is no standard way for parameters to be reflected back onto the HTML. The reflection could appear in various different HTML elements, different attributes within elements, or even as text on the page itself. Somehow automating the process of analyzing the surrounding HTML to then craft a payload that both follows the rules of the input and the rules of HTML to create a valid injection will be a vital step in this project.  

  
__*Very* High Level Overview of Process__
1) Determine if payload is reflected
2) Determine what HTML is to the left of the reflection point and escape out of that HTML
3) Insert injection
4) Determine what HTML is to the right of the reflection point and absorb that remaining HTML
