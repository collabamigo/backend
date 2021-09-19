## Fields supported
* Text (text)
* Number (number)
* Single CQ (scq)
* Multiple CQ (mcq)
* Email (email)
* File (file)
* Boolean (bool)
* Date (date)
* DateTime (datetime)

## Sample Form creation Request

```
[
    { 
        id: 1 
        type: "text" 
        label: "What is your name?" 
    },
    { 
        id: 2
        type: "mcq" 
        label: Choose a fruit
        ...
    }
]