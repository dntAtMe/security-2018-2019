const LocalStrategy = require('passport-local').Strategy;

const mysql = require('mysql');
const bcrypt = require('bcrypt');
const dbconfig = require('./database');
const connection = mysql.createConnection(dbconfig.connection);

connection.query('USE ' + dbconfig.database);

module.exports = function(passport) {
    
    passport.serializeUser(function(user, done) {
        done(null, user.id);
    });

    passport.deserializeUser(function(id, done) {
        connection.query("SELECT * FROM user WHERE id = ? ", [id], function(err, rows) {
            done(err, rows[0]);
        });
    });

    passport.use(
        'local-signup',
        new LocalStrategy({
            usernameField: 'username',
            passwordField: 'password',
            passReqToCallback: true
        },
        function(req, username, password, done) {
            connection.query("SELECT * FROM user WHERE username = ?",[username], function(err, rows) {
                if (err)
                    return done(err);
                if (rows.length) {
                    return done(null, false, req.flash('signupMessage', 'That username is already taken.'));
                } else {
                    // if there is no user with that username
                    // create the user
                    let newUserMysql = {
                        username: username,
                        password: bcrypt.hashSync(password, 10),  // use the generateHash function in our user model
                    }; 

                    let insertQuery = "INSERT INTO user ( username, password  ) values (?, ?)";

                    connection.query(insertQuery,[newUserMysql.username, newUserMysql.password],function(err, rows) {
                        console.log("err: ", err, rows);
                        if (err)
                            return done(null, false, req.flash('signupMessage', 'undefined'));
                        newUserMysql.id = rows.insertId;

                        return done(null, newUserMysql);
                    });
                }
            });
        })
    );
}