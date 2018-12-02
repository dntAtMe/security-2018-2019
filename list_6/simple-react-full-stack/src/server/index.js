const express = require('express');
const os = require('os');
const morgan = require('morgan');
const passport = require('passport');
const session = require('express-session');
const flash = require('connect-flash');
const cookieParser = require('cookie-parser');
const bodyParser = require('body-parser');

const app = express();


require('./config/passport')(passport);

app.use(morgan('dev'));
app.use(express.static('dist'));
app.use(cookieParser());
app.use(bodyParser.urlencoded({
	extended: true
}));
app.use(bodyParser.json());

// required for passport
app.use(session({
	secret: 'vidyapathaisalwaysrunning',
	resave: true,
	saveUninitialized: true
} )); // session secret

app.use(passport.initialize());
app.use(passport.session()); // persistent login sessions
app.use(flash());

require('./routes.js')(app, passport);

app.listen(8080, () => console.log('Listening on port 8080!'));
