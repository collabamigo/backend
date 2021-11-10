## Fields supported
* Text (text)
* Number (number)
* Single CQ (scq)
* Multiple CQ (mcq)
* Email (email)
* File (file)
* Boolean (bool) (not offered)
* Date (date)
* DateTime (datetime)

## Sample Form creation Request

```
{
    1: { 
        type: "text" ,
        name: "What is your name?" ,
    },
    2: { 
        type: "mcq" ,
        name: "Choose a fruit",
        choice: {1:"apple"; 2:"orange"; 3:"fruit"},
    },
    3: {
        type: "integer",
        name: "Enter the marks",
    },
    4: {
        type:"email",
        name: "Whats your email",
    },
    5: {
        type:"file",
        name: "Upload an image",
    },    
}
```
## Sample Form Response

```
{
    1: {
        type:"text"
        qid:1
        response: "Shikhar"
    },
    2: {
        type:"choice"
        qid:2
        response: "Apple"
    },
    3: {
        type:"integer"
        qid:3
        response: 97
    },
}
```
