const express = require('express');
const session = require('express-session'); // for session ids
const app = express();
const bodyParser = require('body-parser');
const path = require('path');
const fs = require('fs').promises;

// middleware
app.use(express.json());  // Middleware to parse JSON requests
app.use(session({ // Setup express-session middleware
    secret: 'clearsignal_proto2024',    // Use a random string for production
    resave: false,
    saveUninitialized: true,
    cookie: { secure: false }  // For development. Set to true if using HTTPS in production
}));
app.use(bodyParser.urlencoded({ extended: true }));
app.use(express.static(path.join(__dirname, `public`)));


async function update_user_json(username, password) {
    const data = await fs.readFile('users.json', 'utf8')

     // Parse the JSON data
     const users = JSON.parse(data);

     // Check if the username exists
     const userExists = users.some(user => user.username === username);

     // If the user exists & true, return Y to go straight to dashboard else, go to preference page
     if (userExists && users['username'] == password) {
         return "Y";
     } else if (userExists) {
        // return W to know user taken
        return "W";
     } else {
        return "N"
     }
}


async function return_user_graph(pref_list) {
    const raw_data = await fs.readFile('monthly_overview/demo.json', 'utf8')
    const data = JSON.parse(raw_data);
    
    let weighted_list = [];

    // for demo, [0, 59] for 60 elements
    for (let i = 0; i < data.length; i++) {

        let line1 = 0
        let line2 = 0
        let line3 = 0
        let line4 = 0
        let line5 = 0
        
        for (let j = 0; j < pref_list.length; j++) {
            let category = pref_list[j].toLowerCase();
            if (j == 0) {
                line1 = data[i][category]*0.04
            } else if (j == 1) {
                line2 = data[i][category]*0.02
            } else if (j == 2) {
                line3 = data[i][category]*0.01
            } else if (j == 3) {
                line4 = data[i][category]*0.0075
            } else if (j == 4) {
                line5 = data[i][category]*0.005
            }
        }

        weighted_list.push(line1+line2+line3+line4+line5)
    }

    return weighted_list
}

// return_user_graph([
//     "entertainment",
//     "tech",
//     "business",
//     "science",
//     "politics"
//   ])

app.get('/', (req, res) => {
    console.log("Session ID:", req.sessionID);

    res.sendFile(path.join(__dirname, `public`, 'sign_in.html'));
});

app.post('/sign-in', async (req, res) => {
    try {
        let data = req.body

        let check = await update_user_json(data['username'], data['password'])
        if (check == "Y") {
            req.session.username = data['username']
            req.session.password = data['password']

            res.send({"res": "dashboard"}) // redirects to GET /pref-page in the html file
        } else if (check == "W") {
            res.send({"res": "wrong"})
        } else {
            req.session.username = data['username']
            req.session.password = data['password']

            res.send({"res": "pref-page"})
        }

    } catch(err) {
        console.log(err)
    }
})

app.get('/pref-page', async (req, res) => {
    try {
        res.sendFile(path.join(__dirname, `public`, 'prefs.html'));
    } catch(err) {
        console.log(err)
    }
})

app.post('/update-prefs', async (req, res) => {
    try {
        let preferences = req.body['prefs']
        req.session.prefs = preferences
        console.log(req.sessionID, req.session)
        let username = req.session.username
        let password = req.session.password

        
        let check = await update_user_json(username, password)
        console.log(check, username, password)
        const f = await fs.readFile('users.json', 'utf8')
        // Parse the JSON data
        let users = JSON.parse(f);

        if (check == "N") {
            // User doesn’t exist, create a new user object
            const newUser = { username, password, preferences};

            // Append new user to the users array
            users.push(newUser);

            // Write the updated users back to the file
            await fs.writeFile('users.json', JSON.stringify(users, null, 2), 'utf8');
        } else if (check == "Y") {
            let foundUser = false;
            users = users.map(user => {
                if (user.username === username) {
                    foundUser = true
                    return { ...user, password, preferences: preferences}
                }
                return users;
            })
            console.log(users)

            if (foundUser) {
                await fs.writeFile('users.json', JSON.stringify(users, null, 2), 'utf8');
                console.log(`preferences updated for user ${username}.`);
            } else {
                console.log(`User ${username} not found.`);
            }
        }
        res.send({"res": "Y"})
    } catch(err) {
        console.log(err)
    }
})

app.get('/dashboard', async (req, res) => {
    try {
        console.log("id:", req.sessionID)
        res.sendFile(path.join(__dirname, `public`, 'dashboard.html'));
    } catch(err) {
        console.log(err)
    }
})

app.get('/load', async (req, res) => {
    try {
        payload = await return_user_graph(req.session.prefs)
        console.log("f", payload)
        res.send({"data": payload})
    } catch(e) {
        console.log(e)
    }
})

app.listen('3010', () => {
    console.log(`Server is running on http://localhost:3010`);
});
