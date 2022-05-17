# Yun Board Game Next
 Peking University Database (Honor Track) Spring'2022 Midterm Practice,
 and next generation of Yun Board Game

# Database Design

- user table
    - uid
    - name
    - password
    - avatarUrl
- boardGame table
    - bgid
    - name
    - imgUrl
- extension table
    - exid
    - name
    - bgid
- play table
    - pid
    - time
    - bgid
    - winnerid
    - loserid
    - scoreboard
    - order
- collection table
    - uid
    - bgid
- participate table
    - uid
    - pid